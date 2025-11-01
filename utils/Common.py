from fastapi import UploadFile,File
from pdf2image import convert_from_bytes
import io
import base64
from pathlib import Path
import uuid

async def process_file(file: UploadFile):
    """Process both images and PDFs"""
    file_data = await file.read()
    
    if file.content_type == "application/pdf":
        # Convert PDF to images
        images = convert_from_bytes(file_data, dpi=200)
        processed_images = []
        
        for img in images:
            # Convert PIL image to base64
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=95)
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            processed_images.append(img_base64)
        
        return processed_images
    else:
        # Handle regular images
        img_base64 = base64.b64encode(file_data).decode('utf-8')
        return [img_base64]
        
async def save_images(files:UploadFile=File(...)):

    UPLOAD_DIR=Path("uploads/reports")
    UPLOAD_DIR.mkdir(parents=True,exist_ok=True)
    file_paths=[]
    for file in files:
        file_path=UPLOAD_DIR / f"{uuid.uuid4()}_{file.filename}"
        with file_path.open("wb") as f:
            f.write(await file.read())
        file_paths.append(str(file_path))


    return file_paths

