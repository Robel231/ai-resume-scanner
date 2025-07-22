# backend/main.py

from datetime import timedelta
from typing import Annotated
import os

from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from slowapi.errors import RateLimitExceeded

# Import our project modules
from limiter import limiter, _rate_limit_exceeded_handler
import models, schemas, security
from database import engine, get_db
from services.parser import extract_text_from_pdf
from services.analyzer import get_ai_analysis

# Create all database tables on startup based on our models
models.Base.metadata.create_all(bind=engine)

# Create the main FastAPI application instance
app = FastAPI(
    title="AI Resume Scanner API",
    description="A secure API to analyze resumes against job descriptions using AI.",
    version="1.0.0"
)

# --- DYNAMIC CORS MIDDLEWARE ---
# This allows our deployed frontend to communicate with the API.
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
origins = [
    "http://localhost",
    "http://localhost:3000",
    frontend_url,
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- RATE LIMITER CONFIGURATION ---
# Add the limiter to the app's state and set up the exception handler.
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# --- ENDPOINTS ---

@app.get("/", tags=["Health Check"])
async def root():
    """A simple health check endpoint to confirm the API is running."""
    return {"status": "ok", "message": "Welcome to the AI Resume Scanner API"}

# --- AUTHENTICATION ENDPOINTS ---

@app.post("/auth/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED, tags=["Authentication"])
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Registers a new user."""
    db_user = security.get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = security.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/auth/token", response_model=schemas.Token, tags=["Authentication"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    db: Session = Depends(get_db)
):
    """Provides a JWT access token for a valid user."""
    user = security.get_user(db, email=form_data.username) # The form's "username" field holds our email
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- SECURED AND RATE-LIMITED ANALYSIS ENDPOINT ---

@app.post("/api/v1/analyze", tags=["Analysis"])
@limiter.limit("5/minute") # Apply the rate limit: 5 requests per minute per user
async def analyze_resume(
    request: Request, # The request object is needed for the rate limiter
    current_user: Annotated[models.User, Depends(security.get_current_user)],
    job_description: str = Form(...),
    resume_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Analyzes a resume against a job description.
    This endpoint is protected and requires authentication.
    """
    # The get_current_user dependency has already run, so we have the user.
    # The limiter decorator has also run. If the user exceeded the limit,
    # an exception would have been thrown already.
    
    if not resume_file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")
    
    resume_text = extract_text_from_pdf(resume_file)
    if resume_text.startswith("Error:"):
        raise HTTPException(status_code=400, detail=resume_text)
    
    analysis_result = get_ai_analysis(resume_text, job_description)
    if "error" in analysis_result:
        raise HTTPException(status_code=500, detail=analysis_result["error"])
    
    # Associate the analysis with the logged-in user
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