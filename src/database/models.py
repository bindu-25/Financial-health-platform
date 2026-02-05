"""
Database Models
SQLAlchemy ORM models for PostgreSQL
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class SME(Base):
    """SME Business Entity"""
    __tablename__ = 'smes'
    
    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String(255), nullable=False)
    industry = Column(String(100))
    registration_number = Column(String(100), unique=True)
    gst_number = Column(String(50))
    email = Column(String(255))
    phone = Column(String(20))
    address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    financial_records = relationship("FinancialRecord", back_populates="sme")
    credit_scores = relationship("CreditScore", back_populates="sme")


class FinancialRecord(Base):
    """Monthly Financial Records"""
    __tablename__ = 'financial_records'
    
    id = Column(Integer, primary_key=True, index=True)
    sme_id = Column(Integer, ForeignKey('smes.id'), nullable=False)
    period = Column(String(7), nullable=False)  # YYYY-MM
    
    # P&L Items
    total_revenue = Column(Float, default=0)
    total_cogs = Column(Float, default=0)
    gross_profit = Column(Float, default=0)
    operating_expenses = Column(Float, default=0)
    ebitda = Column(Float, default=0)
    net_profit = Column(Float, default=0)
    
    # Margins
    gross_margin = Column(Float)
    operating_margin = Column(Float)
    net_profit_margin = Column(Float)
    
    # Cash Flow
    cash_inflow = Column(Float, default=0)
    cash_outflow = Column(Float, default=0)
    net_cash_flow = Column(Float, default=0)
    ending_cash_balance = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sme = relationship("SME", back_populates="financial_records")


class CreditScore(Base):
    """Credit Score History"""
    __tablename__ = 'credit_scores'
    
    id = Column(Integer, primary_key=True, index=True)
    sme_id = Column(Integer, ForeignKey('smes.id'), nullable=False)
    period = Column(String(7), nullable=False)
    
    credit_score = Column(Float, nullable=False)
    credit_rating = Column(String(5))
    
    # Component Scores
    profitability_score = Column(Float)
    liquidity_score = Column(Float)
    leverage_score = Column(Float)
    efficiency_score = Column(Float)
    growth_score = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sme = relationship("SME", back_populates="credit_scores")


class Forecast(Base):
    """Revenue Forecasts"""
    __tablename__ = 'forecasts'
    
    id = Column(Integer, primary_key=True, index=True)
    sme_id = Column(Integer, ForeignKey('smes.id'), nullable=False)
    forecast_period = Column(String(7), nullable=False)
    
    forecast_revenue = Column(Float)
    lower_bound = Column(Float)
    upper_bound = Column(Float)
    forecast_method = Column(String(50))
    
    created_at = Column(DateTime, default=datetime.utcnow)


class Recommendation(Base):
    """AI Recommendations"""
    __tablename__ = 'recommendations'
    
    id = Column(Integer, primary_key=True, index=True)
    sme_id = Column(Integer, ForeignKey('smes.id'), nullable=False)
    
    category = Column(String(50))  # general, cost, growth, credit
    recommendation_text = Column(Text)
    priority = Column(String(20))  # high, medium, low
    status = Column(String(20), default='pending')  # pending, implemented, dismissed
    
    created_at = Column(DateTime, default=datetime.utcnow)


# Example usage
if __name__ == "__main__":
    print("Database models loaded successfully")
    print(f"Tables: {Base.metadata.tables.keys()}")