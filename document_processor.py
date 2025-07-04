import os
from typing import List
from PIL import Image
import asyncio
import aiofiles
from pdf2image import convert_from_path
from docx import Document
import tempfile

class DocumentProcessor:
    def __init__(self):
        self.supported_formats = {'.pdf', '.png', '.jpg', '.jpeg', '.docx', '.txt'}
    
    async def process_file(self, file_path: str) -> List[Image.Image]:
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return await self._process_pdf(file_path)
        elif file_extension in {'.png', '.jpg', '.jpeg'}:
            return await self._process_image(file_path)
        elif file_extension == '.docx':
            return await self._process_docx(file_path)
        elif file_extension == '.txt':
            return await self._process_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    async def _process_pdf(self, file_path: str) -> List[Image.Image]:
        def convert_pdf():
            return convert_from_path(file_path, dpi=300)
        
        loop = asyncio.get_event_loop()
        images = await loop.run_in_executor(None, convert_pdf)
        return images
    
    async def _process_image(self, file_path: str) -> List[Image.Image]:
        def load_image():
            image = Image.open(file_path)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            return image
        
        loop = asyncio.get_event_loop()
        image = await loop.run_in_executor(None, load_image)
        return [image]
    
    async def _process_docx(self, file_path: str) -> List[Image.Image]:
        def extract_text():
            doc = Document(file_path)
            text = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text.append(paragraph.text)
            return '\n'.join(text)
        
        loop = asyncio.get_event_loop()
        text = await loop.run_in_executor(None, extract_text)
        
        text_image = await self._text_to_image(text)
        return [text_image]
    
    async def _process_txt(self, file_path: str) -> List[Image.Image]:
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            text = await f.read()
        
        text_image = await self._text_to_image(text)
        return [text_image]
    
    async def _text_to_image(self, text: str) -> Image.Image:
        def create_text_image():
            from PIL import ImageDraw, ImageFont
            
            img_width, img_height = 800, 1000
            image = Image.new('RGB', (img_width, img_height), color='white')
            draw = ImageDraw.Draw(image)
            
            try:
                font = ImageFont.truetype("arial.ttf", 14)
            except:
                font = ImageFont.load_default()
            
            lines = text.split('\n')
            y_offset = 20
            line_height = 20
            
            for line in lines:
                if y_offset + line_height < img_height - 20:
                    draw.text((20, y_offset), line, fill='black', font=font)
                    y_offset += line_height
                else:
                    break
            
            return image
        
        loop = asyncio.get_event_loop()
        image = await loop.run_in_executor(None, create_text_image)
        return image