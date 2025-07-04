import torch
from transformers import AutoProcessor, AutoTokenizer
from qwen_vl_utils import process_vision_info
from PIL import Image
import asyncio
import json
import re
from typing import Dict, Any, List

class NanoNetsExtractor:
    def __init__(self):
        self.model = None
        self.processor = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
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
        return """Extract all key-value pairs from this document. Focus on:
- Invoice details (invoice number, date, due date, amount)
- Company information (vendor name, address, contact details)  
- Customer information (bill to, ship to addresses)
- Line items (description, quantity, price, total)
- Payment terms and tax information
- Any other relevant document data

Format the response as a JSON object with clear key-value pairs. Use descriptive keys and ensure all extracted text is accurate. For German text, preserve the original language.

Example format:
{
    "invoice_number": "INV-2024-001",
    "date": "2024-01-15",
    "vendor_name": "ABC Company",
    "total_amount": "1,250.00",
    "currency": "EUR",
    "line_items": [
        {
            "description": "Product A",
            "quantity": "2",
            "unit_price": "500.00",
            "total": "1,000.00"
        }
    ]
}"""
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
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
