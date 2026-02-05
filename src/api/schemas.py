"""
API Schemas
Pydantic models for request/response validation
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# SME Schemas
class SMEBase(BaseModel):
    business_name: str
    industry: str
    registration_number: Optional[str] = None
    gst_number: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class SMECreate(SMEBase):
    pass


class SMEResponse(SMEBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Financial Record Schemas
class FinancialRecordBase(BaseModel):
    period: str
    total_revenue: float
    total_cogs: float
    gross_profit: float
    operating_expenses: float
    ebitda: float
    net_profit: float
    gross_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    net_profit_margin: Optional[float] = None


class FinancialRecordCreate(FinancialRecordBase):
    sme_id: int


class FinancialRecordResponse(FinancialRecordBase):
    id: int
    sme_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Credit Score Schemas
class CreditScoreBase(BaseModel):
    period: str
    credit_score: float
    credit_rating: str
    profitability_score: Optional[float] = None
    liquidity_score: Optional[float] = None
    leverage_score: Optional[float] = None
    efficiency_score: Optional[float] = None
    growth_score: Optional[float] = None


class CreditScoreCreate(CreditScoreBase):
    sme_id: int


class CreditScoreResponse(CreditScoreBase):
    id: int
    sme_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Forecast Schemas
class ForecastBase(BaseModel):
    forecast_period: str
    forecast_revenue: float
    lower_bound: Optional[float] = None
    upper_bound: Optional[float] = None
    forecast_method: Optional[str] = None


class ForecastCreate(ForecastBase):
    sme_id: int


class ForecastResponse(ForecastBase):
    id: int
    sme_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Recommendation Schemas
class RecommendationBase(BaseModel):
    category: str
    recommendation_text: str
    priority: str = 'medium'
    status: str = 'pending'


class RecommendationCreate(RecommendationBase):
    sme_id: int


class RecommendationResponse(RecommendationBase):
    id: int
    sme_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Analysis Request/Response Schemas
class AnalysisRequest(BaseModel):
    sme_id: int
    focus_area: Optional[str] = 'general'


class FinancialSummaryResponse(BaseModel):
    total_revenue: float
    total_profit: float
    avg_gross_margin: float
    avg_net_margin: float
    profitability_rate: float


class CreditSummaryResponse(BaseModel):
    latest_credit_score: float
    latest_credit_rating: str
    credit_trend: str


class CompleteDashboardResponse(BaseModel):
    sme: SMEResponse
    financial_summary: FinancialSummaryResponse
    credit_summary: CreditSummaryResponse
    latest_financials: List[FinancialRecordResponse]
    forecasts: List[ForecastResponse]
    recommendations: List[RecommendationResponse]


# Example usage
if __name__ == "__main__":
    print("API schemas loaded successfully")