

from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException, status, Request
from sqlalchemy.orm import Session


import models
import schemas
from database import get_db
from services.parser import extract_text_from_pdf
from services.analyzer import get_ai_analysis
from .auth import get_current_user
from limiter import limiter 


router = APIRouter(
    prefix="/api/v1",
    tags=["Analysis"]
)


def user_email_rate_limiter(request: Request) -> str:
    
    user = request.state.user
    return user.email


@router.post("/analyze", response_model=schemas.Analysis)
@limiter.limit("5/minute", key_func=user_email_rate_limiter)
async def analyze_resume(
    request: Request, 
    job_description: str = Form(...),
    resume_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    
    print(f"INFO: Analysis request received from user: {current_user.email}")

    
    if not resume_file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload a PDF."
        )

    resume_text = extract_text_from_pdf(resume_file)
    if resume_text.startswith("Error:"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=resume_text
        )
    print(f"INFO: Successfully parsed resume '{resume_file.filename}' for user {current_user.email}.")

    
    print(f"INFO: Sending data to AI for analysis for user {current_user.email}.")
    analysis_result = get_ai_analysis(resume_text, job_description)

    if "error" in analysis_result:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=analysis_result["error"]
        )
    print(f"INFO: Successfully received analysis from AI for user {current_user.email}.")

    
    db_analysis = models.Analysis(
        job_description=job_description,
        resume_filename=resume_file.filename,
        analysis_result=analysis_result,
        owner_id=current_user.id
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)

    return db_analysis