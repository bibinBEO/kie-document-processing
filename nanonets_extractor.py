import torch
from transformers import AutoProcessor, AutoTokenizer
from qwen_vl_utils import process_vision_info
from PIL import Image
import asyncio
import json
import re
from typing import Dict, Any, List
from customs_schema import CustomsDeclarationSchema, CustomsFieldMapper

class NanoNetsExtractor:
    def __init__(self):
        self.model = None
        self.processor = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.field_mapper = CustomsFieldMapper()
    
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
        """Extract and map customs declaration fields"""
        customs_fields = {
            # Message header
            "nachrichtensender": {
                "eoriNiederlassungsnummer": None
            },
            "nachrichtenempfanger": {
                "dienststellennummer": None
            },
            
            # Header information
            "kopf": {
                "lrn": None,
                "artderAnmeldung": None,
                "artderAusfuhranmeldung": None,
                "beteiligtenKonstellation": None,
                "zeitpunktderAnmeldung": None,
                "massgeblichesDatum": None,
                "kopfDatumdesAusgangs": None,
                "zeitpunktDerGestellung": None,
                "zeitpunktdesEndesderLadetatigkeit": None,
                "sicherheit": None,
                "besondereUmstande": None,
                "inRechnunggestellterGesamtbetrag": None,
                "rechnungswahrung": None,
            },
            
            # Authorization
            "bewilligung": {
                "sequenznummer": None,
                "art": None,
                "referenznummer": None
            },
            
            # Customs offices
            "gestellungszollstelle": {
                "gestellungszollstelle": None
            },
            "ausfuhrzollstelle": {
                "ausfuhrzollstelleDienststellennummer": None
            },
            
            # Parties
            "anmelder": {
                "tin": None,
                "niederlassungsNummer": None,
                "name": None,
                "adresse": {
                    "strasse": None,
                    "plz": None,
                    "ort": None,
                    "land": None
                },
                "ansprechpartner": {
                    "ansprechName": None,
                    "phone": None,
                    "ansprechEmail": None
                }
            },
            
            # Goods positions
            "position": [],
            
            # Additional data
            "additional_extracted_data": {}
        }
        
        # Map extracted data to customs fields
        for key, value in extracted_data.items():
            key_lower = key.lower()
            
            # Map LRN
            if 'lrn' in key_lower or 'referenznummer' in key_lower:
                customs_fields["kopf"]["lrn"] = value
            
            # Map dates
            elif 'datum' in key_lower:
                if 'anmeldung' in key_lower:
                    customs_fields["kopf"]["zeitpunktderAnmeldung"] = value
                elif 'ausgang' in key_lower:
                    customs_fields["kopf"]["kopfDatumdesAusgangs"] = value
                else:
                    customs_fields["kopf"]["massgeblichesDatum"] = value
            
            # Map companies
            elif 'anmelder' in key_lower or 'declarant' in key_lower:
                if isinstance(value, dict):
                    customs_fields["anmelder"].update(value)
                else:
                    customs_fields["anmelder"]["name"] = value
            
            # Map addresses
            elif 'adresse' in key_lower or 'address' in key_lower:
                if isinstance(value, dict):
                    customs_fields["anmelder"]["adresse"].update(value)
            
            # Map positions/line items
            elif 'position' in key_lower or 'line_items' in key_lower:
                if isinstance(value, list):
                    customs_fields["position"] = value
                else:
                    customs_fields["position"].append({"beschreibung": value})
            
            # Store additional data
            else:
                customs_fields["additional_extracted_data"][key] = value
        
        return customs_fields
    
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
