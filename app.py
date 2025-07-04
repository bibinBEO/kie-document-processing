from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import aiofiles
import os
import uuid
from typing import List, Dict, Any
import asyncio
from datetime import datetime

from document_processor import DocumentProcessor
from nanonets_extractor import NanoNetsExtractor

app = FastAPI(title="KIE Document Processing API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
RESULTS_DIR = "results"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

processor = DocumentProcessor()
extractor = NanoNetsExtractor()

@app.on_event("startup")
async def startup_event():
    await extractor.initialize()

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    async with aiofiles.open("templates/index.html", "r") as f:
        content = await f.read()
    return HTMLResponse(content=content)

@app.post("/upload", response_model=Dict[str, str])
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    allowed_extensions = {'.pdf', '.png', '.jpg', '.jpeg', '.docx', '.txt'}
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not supported. Allowed: {', '.join(allowed_extensions)}"
        )
    
    job_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{job_id}_{file.filename}")
    
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    return {"job_id": job_id, "filename": file.filename, "status": "uploaded"}

@app.post("/extract/{job_id}", response_model=Dict[str, Any])
async def extract_document(job_id: str):
    upload_files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(job_id)]
    
    if not upload_files:
        raise HTTPException(status_code=404, detail="Job ID not found")
    
    file_path = os.path.join(UPLOAD_DIR, upload_files[0])
    
    try:
        processed_images = await processor.process_file(file_path)
        
        results = []
        for image in processed_images:
            extracted_data = await extractor.extract_key_value_pairs(image)
            
            # Enhanced processing with customs field mapping
            customs_data = extractor.extract_customs_fields(extracted_data)
            
            # Combine both formats for flexibility
            combined_result = {
                "raw_extraction": extracted_data,
                "customs_format": customs_data,
                "invoice_format": extractor.extract_invoice_fields(extracted_data)
            }
            
            results.append(combined_result)
        
        result_data = {
            "job_id": job_id,
            "timestamp": datetime.now().isoformat(),
            "extracted_data": results,
            "status": "completed"
        }
        
        result_file = os.path.join(RESULTS_DIR, f"{job_id}_results.json")
        async with aiofiles.open(result_file, 'w') as f:
            import json
            await f.write(json.dumps(result_data, indent=2))
        
        return result_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

@app.get("/results/{job_id}", response_model=Dict[str, Any])
async def get_results(job_id: str):
    result_file = os.path.join(RESULTS_DIR, f"{job_id}_results.json")
    
    if not os.path.exists(result_file):
        raise HTTPException(status_code=404, detail="Results not found")
    
    async with aiofiles.open(result_file, 'r') as f:
        import json
        content = await f.read()
        return json.loads(content)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)