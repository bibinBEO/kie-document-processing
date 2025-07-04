import torch
from transformers import AutoProcessor, AutoTokenizer
from qwen_vl_utils import process_vision_info
from PIL import Image
import asyncio
import json
import re
from typing import Dict, Any, List
from customs_schema import CustomsDeclarationSchema, CustomsFieldMapper
from complete_customs_schema import CompleteCustomsSchema, CompleteFieldMapper

class NanoNetsExtractor:
    def __init__(self):
        self.model = None
        self.processor = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.field_mapper = CustomsFieldMapper()
        self.complete_mapper = CompleteFieldMapper()
        self.complete_schema = CompleteCustomsSchema()
    
    async def initialize(self):
        def load_model():
            from transformers import Qwen2VLForConditionalGeneration
            
            model_name = "nanonets/Nanonets-OCR-s"
            
            model = Qwen2VLForConditionalGeneration.from_pretrained(
                model_name,
                device_map="auto",
                torch_dtype="auto",
                ignore_mismatched_sizes=True,
                attn_implementation="flash_attention_2"
            )
            
            processor = AutoProcessor.from_pretrained(model_name)
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            return model, processor, tokenizer
        
        loop = asyncio.get_event_loop()
        self.model, self.processor, self.tokenizer = await loop.run_in_executor(None, load_model)
        print(f"NanoNets model loaded on {self.device}")
    
    async def extract_key_value_pairs(self, image: Image.Image) -> Dict[str, Any]:
        prompt = self._create_extraction_prompt()
        
        def inference():
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": image},
                        {"type": "text", "text": prompt}
                    ]
                }
            ]
            
            text = self.processor.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            
            image_inputs, video_inputs = process_vision_info(messages)
            
            inputs = self.processor(
                text=[text],
                images=image_inputs,
                videos=video_inputs,
                padding=True,
                return_tensors="pt"
            )
            
            inputs = inputs.to(self.device)
            
            with torch.no_grad():
                generated_ids = self.model.generate(
                    **inputs,
                    max_new_tokens=512,
                    do_sample=False,
                    temperature=0.1
                )
            
            generated_ids_trimmed = [
                out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
            ]
            
            response = self.processor.batch_decode(
                generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
            )[0]
            
            return response
        
        loop = asyncio.get_event_loop()
        raw_response = await loop.run_in_executor(None, inference)
        
        return self._parse_response(raw_response)
    
    def _create_extraction_prompt(self) -> str:
        return """Extract all key-value pairs from this German customs export declaration (Ausfuhranmeldung) or related document. Focus on:

PRIORITY FIELDS (German customs export declaration):
- LRN (Local Reference Number / Lokale Referenznummer)
- MRN (Movement Reference Number / Bearbeitungsnummer)
- EORI-Nummer (Economic Operator Registration and Identification)
- Anmeldedatum, Ausgangsdatum, Gültigkeitsdatum
- Anmelder, Ausführer, Empfänger, Versender (Name, Adresse, Kontakt)
- Zollstellen (Gestellungszollstelle, Ausfuhrzollstelle, Ausgangszollstelle)
- Warenbezeichnung, Warennummer, Ursprungsland, Bestimmungsland
- Menge, Gewicht (Rohmasse, Eigenmasse), Wert, Währung
- Verkehrszweig, Kennzeichen, Containernummer
- Verfahren, Bewilligung, Dokumente
- Besondere Umstände, Zusätzliche Angaben

ALSO EXTRACT (if present):
- Invoice details (Rechnung: Nummer, Datum, Betrag)
- Company information (Firmenname, Adresse, Kontaktdaten)
- Line items (Positionen: Beschreibung, Menge, Preis)
- Transport information (Transportmittel, Route)
- Any other relevant document data

INSTRUCTIONS:
1. Preserve German text exactly as written
2. Extract ALL text fields, even if they seem incomplete
3. Include field labels/headers when visible
4. Capture table data with row/column structure
5. Note any handwritten text or stamps
6. Extract dates in original format
7. Include reference numbers, codes, and identifiers

Format as comprehensive JSON with nested structure matching German customs declaration format. Use German field names where applicable.

Example structure:
{
    "document_type": "Ausfuhranmeldung",
    "lrn": "DE123456789",
    "kopf": {
        "anmeldedatum": "2024-01-15",
        "artderAnmeldung": "..."
    },
    "anmelder": {
        "name": "Firma XYZ GmbH",
        "adresse": {
            "strasse": "Musterstraße 123",
            "plz": "12345",
            "ort": "Berlin",
            "land": "DE"
        }
    },
    "position": [
        {
            "warenbezeichnung": "Maschinenbauteile",
            "menge": "100",
            "wert": "50000.00"
        }
    ],
    "additional_extracted_data": {
        "any_other_fields": "..."
    }
}"""
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                parsed_data = json.loads(json_str)
                
                # Enhance with field mapping
                enhanced_data = self._enhance_with_field_mapping(parsed_data, response)
                return enhanced_data
            else:
                return self._fallback_parse(response)
        except json.JSONDecodeError:
            return self._fallback_parse(response)
    
    def _fallback_parse(self, response: str) -> Dict[str, Any]:
        lines = response.strip().split('\n')
        result = {"raw_text": response}
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()
                if value:
                    result[key] = value
        
        return result
    
    def _enhance_with_field_mapping(self, parsed_data: Dict[str, Any], raw_response: str) -> Dict[str, Any]:
        """Enhance parsed data with field mapping and pattern matching"""
        enhanced_data = parsed_data.copy()
        
        # Find potential field matches in raw response
        field_matches = self.field_mapper.find_matching_fields(raw_response)
        
        if field_matches:
            enhanced_data["detected_field_patterns"] = field_matches
        
        # Add metadata
        enhanced_data["extraction_metadata"] = {
            "model_used": "nanonets-ocr-s",
            "extraction_timestamp": "2024-01-15T10:00:00Z",
            "field_mapping_applied": True,
            "total_fields_detected": len(field_matches) if field_matches else 0
        }
        
        return enhanced_data
    
    def extract_customs_fields(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and map ALL customs declaration fields using complete schema"""
        # Start with complete empty schema
        customs_fields = self.complete_schema.get_empty_schema()
        
        # Track all mapped and unmapped fields
        mapping_results = {
            "mapped_fields": {},
            "unmapped_fields": {},
            "field_mapping_confidence": {}
        }
        
        # Process each extracted field
        for extracted_key, extracted_value in extracted_data.items():
            if extracted_key in ["extraction_metadata", "detected_field_patterns"]:
                continue
                
            # Find best matching schema field
            best_match = self.complete_mapper.find_best_field_match(extracted_key)
            
            if best_match:
                # Map to schema structure
                mapped_value = self._map_value_to_schema_path(
                    customs_fields, best_match, extracted_value
                )
                mapping_results["mapped_fields"][extracted_key] = {
                    "schema_field": best_match,
                    "value": extracted_value,
                    "mapped_successfully": mapped_value
                }
                mapping_results["field_mapping_confidence"][extracted_key] = "high"
            else:
                # Store unmapped fields for manual review
                mapping_results["unmapped_fields"][extracted_key] = extracted_value
        
        # Enhanced field mapping with context analysis
        self._perform_contextual_mapping(customs_fields, extracted_data, mapping_results)
        
        # Add mapping metadata
        customs_fields["_mapping_metadata"] = mapping_results
        
        return customs_fields
    
    def _map_value_to_schema_path(self, schema: Dict[str, Any], field_path: str, value: Any) -> bool:
        """Map extracted value to specific schema path"""
        try:
            # Handle specific field mappings
            if field_path == "lrn":
                schema["kopf"]["lrn"] = value
            elif field_path == "eori":
                if "anmelder" in str(value).lower():
                    schema["anmelder"]["tin"] = value
                else:
                    schema["nachrichtensender"]["eoriNiederlassungsnummer"] = value
            elif field_path == "anmelder":
                if isinstance(value, dict):
                    self._merge_nested_dict(schema["anmelder"], value)
                else:
                    schema["anmelder"]["name"] = value
            elif field_path == "ausfuehrer":
                if isinstance(value, dict):
                    self._merge_nested_dict(schema["ausfuhrer"], value)
                else:
                    schema["ausfuhrer"]["name"] = value
            elif field_path == "empfaenger":
                if isinstance(value, dict):
                    self._merge_nested_dict(schema["sendung"]["empfanger"], value)
                else:
                    schema["sendung"]["empfanger"]["name"] = value
            elif field_path == "versender":
                if isinstance(value, dict):
                    self._merge_nested_dict(schema["sendung"]["versender"], value)
                else:
                    schema["sendung"]["versender"]["name"] = value
            elif field_path in ["strasse", "plz", "ort", "land"]:
                # Try to map to most likely address context
                self._map_address_field(schema, field_path, value)
            elif field_path == "warenbezeichnung":
                if not schema["position"]:
                    schema["position"] = [self.complete_schema.get_empty_schema()["position"][0].copy()]
                schema["position"][0]["ware"]["wareWarenbezeichnung"] = value
            elif field_path == "menge":
                if not schema["position"]:
                    schema["position"] = [self.complete_schema.get_empty_schema()["position"][0].copy()]
                schema["position"][0]["ware"]["vermessung"]["mengeinbesondererMabeinheit"] = value
            elif field_path == "containernummer":
                if not schema["sendung"]["transportausrustung"]:
                    schema["sendung"]["transportausrustung"] = [{"sequenznummer": None, "containernummer": None, "anzahlderVerschlusse": None, "verschluss": [], "warenpositionsverweis": []}]
                schema["sendung"]["transportausrustung"][0]["containernummer"] = value
            elif field_path == "bewilligung":
                if isinstance(value, dict):
                    self._merge_nested_dict(schema["bewilligung"], value)
                else:
                    schema["bewilligung"]["referenznummer"] = value
            # Add more specific mappings as needed
            else:
                # Generic mapping for remaining fields
                self._generic_field_mapping(schema, field_path, value)
            
            return True
        except Exception as e:
            print(f"Error mapping {field_path}: {e}")
            return False
    
    def _merge_nested_dict(self, target: Dict, source: Dict):
        """Merge nested dictionary into target"""
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                self._merge_nested_dict(target[key], value)
            else:
                target[key] = value
    
    def _map_address_field(self, schema: Dict[str, Any], field_type: str, value: str):
        """Map address fields to most appropriate context"""
        address_contexts = [
            schema["anmelder"]["adresse"],
            schema["ausfuhrer"]["adresse"],
            schema["sendung"]["versender"]["adresse"],
            schema["sendung"]["empfanger"]["adresse"],
            schema["sendung"]["warenort"]["adresse"]
        ]
        
        # Map to first available context or anmelder as default
        for addr_context in address_contexts:
            if addr_context and not addr_context.get(field_type):
                addr_context[field_type] = value
                return
        
        # Default to anmelder
        schema["anmelder"]["adresse"][field_type] = value
    
    def _generic_field_mapping(self, schema: Dict[str, Any], field_path: str, value: Any):
        """Generic mapping for fields not specifically handled"""
        # Try to place in appropriate section based on field name
        if any(word in field_path for word in ["kopf", "header", "anmeldung"]):
            if field_path in schema["kopf"]:
                schema["kopf"][field_path] = value
        elif any(word in field_path for word in ["position", "ware", "goods"]):
            if not schema["position"]:
                schema["position"] = [self.complete_schema.get_empty_schema()["position"][0].copy()]
            # Try to place in position structure
            self._place_in_position_structure(schema["position"][0], field_path, value)
        elif any(word in field_path for word in ["sendung", "transport", "shipment"]):
            self._place_in_sendung_structure(schema["sendung"], field_path, value)
        else:
            # Create additional_fields section if not exists
            if "_additional_fields" not in schema:
                schema["_additional_fields"] = {}
            schema["_additional_fields"][field_path] = value
    
    def _place_in_position_structure(self, position: Dict[str, Any], field_path: str, value: Any):
        """Place field in appropriate position structure"""
        if any(word in field_path for word in ["ware", "goods", "warenbezeichnung"]):
            if "ware" in position and field_path in position["ware"]:
                position["ware"][field_path] = value
        elif any(word in field_path for word in ["verpackung", "package"]):
            if not position["verpackung"]:
                position["verpackung"] = [{"sequenznummer": None, "artderVerpackung": None, "anzahlderPackstucke": None, "versandzeichen": None, "packstuckverweis": {"packstuckverweisPositionsnummer": None}}]
            if field_path in position["verpackung"][0]:
                position["verpackung"][0][field_path] = value
        else:
            if field_path in position:
                position[field_path] = value
    
    def _place_in_sendung_structure(self, sendung: Dict[str, Any], field_path: str, value: Any):
        """Place field in appropriate sendung structure"""
        if field_path in sendung:
            sendung[field_path] = value
        elif any(word in field_path for word in ["transport", "befoerderung"]):
            # Handle transport-related fields
            if "transportausrustung" in field_path and sendung["transportausrustung"]:
                if field_path in sendung["transportausrustung"][0]:
                    sendung["transportausrustung"][0][field_path] = value
    
    def _perform_contextual_mapping(self, schema: Dict[str, Any], extracted_data: Dict[str, Any], mapping_results: Dict[str, Any]):
        """Perform additional contextual mapping based on document structure"""
        # Analyze patterns in extracted data
        
        # Look for table structures (common in positions)
        table_data = self._extract_table_structures(extracted_data)
        if table_data:
            self._map_table_to_positions(schema, table_data)
        
        # Look for address blocks
        address_blocks = self._extract_address_blocks(extracted_data)
        if address_blocks:
            self._map_address_blocks(schema, address_blocks)
        
        # Look for date patterns
        date_fields = self._extract_date_fields(extracted_data)
        if date_fields:
            self._map_date_fields(schema, date_fields)
    
    def _extract_table_structures(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract table-like structures from data"""
        tables = []
        # Implementation depends on how table data is structured in extraction
        # This is a placeholder for table detection logic
        return tables
    
    def _extract_address_blocks(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract address block structures"""
        addresses = []
        # Look for grouped address information
        return addresses
    
    def _extract_date_fields(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Extract date fields from data"""
        dates = {}
        for key, value in data.items():
            if isinstance(value, str) and any(date_indicator in key.lower() for date_indicator in ["datum", "date", "zeit"]):
                dates[key] = value
        return dates
    
    def _map_table_to_positions(self, schema: Dict[str, Any], table_data: List[Dict[str, Any]]):
        """Map table data to position entries"""
        pass
    
    def _map_address_blocks(self, schema: Dict[str, Any], address_blocks: List[Dict[str, Any]]):
        """Map address blocks to appropriate parties"""
        pass
    
    def _map_date_fields(self, schema: Dict[str, Any], date_fields: Dict[str, str]):
        """Map date fields to appropriate schema locations"""
        for field_name, date_value in date_fields.items():
            normalized_field = self.complete_mapper.normalize_field_name(field_name)
            
            if "anmeldung" in normalized_field:
                schema["kopf"]["zeitpunktderAnmeldung"] = date_value
            elif "ausgang" in normalized_field:
                schema["kopf"]["kopfDatumdesAusgangs"] = date_value
            elif "gestellung" in normalized_field:
                schema["kopf"]["zeitpunktDerGestellung"] = date_value
            elif "massgeblich" in normalized_field or "relevant" in normalized_field:
                schema["kopf"]["massgeblichesDatum"] = date_value
            else:
                # Default to massgeblichesDatum if unclear
                if not schema["kopf"]["massgeblichesDatum"]:
                    schema["kopf"]["massgeblichesDatum"] = date_value
    
    def extract_invoice_fields(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        invoice_fields = {
            'invoice_number': None,
            'date': None,
            'due_date': None,
            'vendor_name': None,
            'vendor_address': None,
            'customer_name': None,
            'customer_address': None,
            'total_amount': None,
            'currency': None,
            'tax_amount': None,
            'line_items': [],
            'payment_terms': None
        }
        
        for key, value in extracted_data.items():
            key_lower = key.lower()
            
            if 'invoice' in key_lower and 'number' in key_lower:
                invoice_fields['invoice_number'] = value
            elif 'date' in key_lower and 'due' not in key_lower:
                invoice_fields['date'] = value
            elif 'due' in key_lower and 'date' in key_lower:
                invoice_fields['due_date'] = value
            elif 'vendor' in key_lower or 'seller' in key_lower:
                if 'name' in key_lower:
                    invoice_fields['vendor_name'] = value
                elif 'address' in key_lower:
                    invoice_fields['vendor_address'] = value
            elif 'customer' in key_lower or 'buyer' in key_lower:
                if 'name' in key_lower:
                    invoice_fields['customer_name'] = value
                elif 'address' in key_lower:
                    invoice_fields['customer_address'] = value
            elif 'total' in key_lower and 'amount' in key_lower:
                invoice_fields['total_amount'] = value
            elif 'currency' in key_lower:
                invoice_fields['currency'] = value
            elif 'tax' in key_lower:
                invoice_fields['tax_amount'] = value
            elif 'payment' in key_lower and 'terms' in key_lower:
                invoice_fields['payment_terms'] = value
        
        return invoice_fields
