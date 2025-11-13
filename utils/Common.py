from fastapi import UploadFile,File
from pdf2image import convert_from_bytes
import io
import base64
from pathlib import Path
from datetime import datetime
import uuid
from model.Users import Users
from db.postgres import get_postgres_db

db=next(get_postgres_db())

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

async def save_vet_data(transcript:str,analysis_json:dict,user_id:int,audio:UploadFile=File(...)):
    try:    
        UPLOAD_DIR=Path("uploads/transcripts")
        UPLOAD_DIR.mkdir(parents=True,exist_ok=True)
        
        file_path=UPLOAD_DIR / f"{uuid.uuid4()}_{audio.filename}"
        with file_path.open("wb") as f:
            f.write(await audio.read())
        vet_notes={
            "transcript":transcript,
            "audio":str(file_path),
            "analysis":analysis_json,
            "date":datetime.now().isoformat()
        }
        user=db.query(Users).filter_by(id=user_id).first()

        existing_vet_notes=user.vet_notes if user.vet_notes else []
        existing_vet_notes.append(vet_notes)
        user.vet_notes=existing_vet_notes
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) 
    finally:
        db.close()

    return vet_notes

    
def save_vet_checklist(checklist:dict,user_id:int):
    try:
        user=db.query(Users).filter_by(id=user_id).first()
        existing_vet_checklist=user.vet_checklist if user.vet_checklist else []
        existing_vet_checklist.append(checklist)
        user.vet_checklist=existing_vet_checklist
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) 
    finally:
        db.close()
    return checklist
    

