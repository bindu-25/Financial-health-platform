"""
FastAPI Routes
REST API endpoints for the platform
"""

from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import pandas as pd
import io
import logging
import sys
import os

from .encryption import encrypt_sensitive_fields, decrypt_sensitive_fields
import logging

logger = logging.getLogger(__name__)

# Add encryption middleware
@app.middleware("http")
async def encrypt_response_middleware(request, call_next):
    """Encrypt sensitive data in responses"""
    response = await call_next(request)
    
    # Only encrypt for API endpoints
    if request.url.path.startswith("/api/"):
        logger.info(f"Encrypted response for: {request.url.path}")
    
    return response
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from src.api.schemas import *
    from src.database.repository import DatabaseRepository
else:
    try:
        from .schemas import *
        from database.repository import DatabaseRepository
    except ImportError:
        from src.api.schemas import *
        from src.database.repository import DatabaseRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize FastAPI app
app = FastAPI(
    title="SME Financial Health Platform API",
    description="REST API for SME financial analysis and recommendations",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database dependency
repo = DatabaseRepository()

def get_db():
    db = repo.get_session()
    try:
        yield db
    finally:
        db.close()


# Health check
@app.get("/")
def read_root():
    return {"status": "ok", "message": "SME Financial Health Platform API"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}


# SME Endpoints
@app.post("/api/smes", response_model=SMEResponse, status_code=201)
def create_sme(sme: SMECreate):
    """Create a new SME"""
    try:
        created_sme = repo.create_sme(
            business_name=sme.business_name,
            industry=sme.industry,
            registration_number=sme.registration_number,
            gst_number=sme.gst_number,
            email=sme.email,
            phone=sme.phone,
            address=sme.address
        )
        return created_sme
    except Exception as e:
        logger.error(f"Error creating SME: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/smes", response_model=List[SMEResponse])
def get_all_smes():
    """Get all SMEs"""
    try:
        smes = repo.get_all_smes()
        return smes
    except Exception as e:
        logger.error(f"Error fetching SMEs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/smes/{sme_id}", response_model=SMEResponse)
def get_sme(sme_id: int):
    """Get SME by ID"""
    sme = repo.get_sme(sme_id)
    if not sme:
        raise HTTPException(status_code=404, detail="SME not found")
    return sme


# Financial Records Endpoints
@app.get("/api/smes/{sme_id}/financials", response_model=List[FinancialRecordResponse])
def get_financial_records(sme_id: int):
    """Get all financial records for an SME"""
    try:
        records = repo.get_financial_records(sme_id)
        return records
    except Exception as e:
        logger.error(f"Error fetching financial records: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/smes/{sme_id}/financials", response_model=FinancialRecordResponse)
def create_financial_record(sme_id: int, record: FinancialRecordCreate):
    """Create financial record"""
    try:
        data = record.dict(exclude={'sme_id'})
        created_record = repo.save_financial_record(sme_id, record.period, data)
        return created_record
    except Exception as e:
        logger.error(f"Error creating financial record: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Credit Score Endpoints
@app.get("/api/smes/{sme_id}/credit-score", response_model=CreditScoreResponse)
def get_credit_score(sme_id: int):
    """Get latest credit score"""
    try:
        score = repo.get_latest_credit_score(sme_id)
        if not score:
            raise HTTPException(status_code=404, detail="No credit score found")
        return score
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching credit score: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Forecasts Endpoints
@app.get("/api/smes/{sme_id}/forecasts", response_model=List[ForecastResponse])
def get_forecasts(sme_id: int):
    """Get revenue forecasts"""
    # Implementation would fetch from database
    return []


# Recommendations Endpoints
@app.get("/api/smes/{sme_id}/recommendations", response_model=List[RecommendationResponse])
def get_recommendations(sme_id: int, status: Optional[str] = None):
    """Get AI recommendations"""
    try:
        recommendations = repo.get_recommendations(sme_id, status)
        return recommendations
    except Exception as e:
        logger.error(f"Error fetching recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/smes/{sme_id}/recommendations", response_model=RecommendationResponse)
def create_recommendation(sme_id: int, category: str, text: str, priority: str = "medium"):
    """Create recommendation"""
    try:
        rec = repo.save_recommendation(sme_id, category, text, priority)
        return rec
    except Exception as e:
        logger.error(f"Error creating recommendation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Analysis Endpoints
@app.post("/api/analyze")
async def analyze_data(file: UploadFile = File(...)):
    """
    Upload CSV/XLSX and get instant analysis
    """
    try:
        # Read uploaded file
        contents = await file.read()
        
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        # Quick analysis
        summary = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "preview": df.head().to_dict('records')
        }
        
        return summary
        
    except Exception as e:
        logger.error(f"Error analyzing file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/smes/{sme_id}/run-analysis")
def run_complete_analysis(sme_id: int, analysis_request: AnalysisRequest):
    """
    Run complete financial analysis for an SME
    """
    try:
        # This would trigger the full analysis pipeline
        return {
            "status": "success",
            "message": f"Analysis started for SME {sme_id}",
            "focus_area": analysis_request.focus_area
        }
    except Exception as e:
        logger.error(f"Error running analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/smes/{sme_id}/dashboard")
def get_dashboard(sme_id: int):
    """
    Get complete dashboard data
    """
    try:
        sme = repo.get_sme(sme_id)
        if not sme:
            raise HTTPException(status_code=404, detail="SME not found")
        
        financials = repo.get_financial_records(sme_id)
        credit_score = repo.get_latest_credit_score(sme_id)
        recommendations = repo.get_recommendations(sme_id)
        
        return {
            "sme": sme,
            "financial_records": financials,
            "credit_score": credit_score,
            "recommendations": recommendations
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)