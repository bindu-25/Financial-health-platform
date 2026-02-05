"""
Database Repository
CRUD operations for database
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional
import os
from dotenv import load_dotenv
import logging
import sys

# Fix import paths
if __name__ == "__main__":
    # When run directly
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from src.database.models import Base, SME, FinancialRecord, CreditScore, Forecast, Recommendation
else:
    # When imported as module
    try:
        from .models import Base, SME, FinancialRecord, CreditScore, Forecast, Recommendation
    except ImportError:
        from src.database.models import Base, SME, FinancialRecord, CreditScore, Forecast, Recommendation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class DatabaseRepository:
    """Database operations"""
    
    def __init__(self, connection_string: str = None):
        if connection_string is None:
            connection_string = os.getenv('DATABASE_URL', 
                'postgresql://username:password@localhost:5432/financial_health_db')
        
        try:
            self.engine = create_engine(connection_string)
            self.SessionLocal = sessionmaker(bind=self.engine)
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            self.engine = None
            self.SessionLocal = None
    
    def create_tables(self):
        """Create all tables"""
        if self.engine:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created")
        else:
            logger.error("Cannot create tables - no database connection")
    
    def get_session(self) -> Session:
        """Get database session"""
        if self.SessionLocal:
            return self.SessionLocal()
        else:
            raise Exception("No database connection available")
    
    # SME Operations
    def create_sme(self, business_name: str, industry: str, **kwargs) -> SME:
        """Create new SME"""
        session = self.get_session()
        try:
            sme = SME(business_name=business_name, industry=industry, **kwargs)
            session.add(sme)
            session.commit()
            session.refresh(sme)
            logger.info(f"Created SME: {business_name}")
            return sme
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating SME: {e}")
            raise
        finally:
            session.close()
    
    def get_sme(self, sme_id: int) -> Optional[SME]:
        """Get SME by ID"""
        session = self.get_session()
        try:
            return session.query(SME).filter(SME.id == sme_id).first()
        finally:
            session.close()
    
    def get_all_smes(self) -> List[SME]:
        """Get all SMEs"""
        session = self.get_session()
        try:
            return session.query(SME).all()
        finally:
            session.close()
    
    # Financial Record Operations
    def save_financial_record(self, sme_id: int, period: str, data: dict) -> FinancialRecord:
        """Save financial record"""
        session = self.get_session()
        try:
            record = FinancialRecord(sme_id=sme_id, period=period, **data)
            session.add(record)
            session.commit()
            session.refresh(record)
            return record
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving financial record: {e}")
            raise
        finally:
            session.close()
    
    def get_financial_records(self, sme_id: int) -> List[FinancialRecord]:
        """Get all financial records for SME"""
        session = self.get_session()
        try:
            return session.query(FinancialRecord)\
                .filter(FinancialRecord.sme_id == sme_id)\
                .order_by(FinancialRecord.period)\
                .all()
        finally:
            session.close()
    
    # Credit Score Operations
    def save_credit_score(self, sme_id: int, period: str, data: dict) -> CreditScore:
        """Save credit score"""
        session = self.get_session()
        try:
            score = CreditScore(sme_id=sme_id, period=period, **data)
            session.add(score)
            session.commit()
            session.refresh(score)
            return score
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving credit score: {e}")
            raise
        finally:
            session.close()
    
    def get_latest_credit_score(self, sme_id: int) -> Optional[CreditScore]:
        """Get latest credit score"""
        session = self.get_session()
        try:
            return session.query(CreditScore)\
                .filter(CreditScore.sme_id == sme_id)\
                .order_by(CreditScore.created_at.desc())\
                .first()
        finally:
            session.close()
    
    # Forecast Operations
    def save_forecast(self, sme_id: int, forecast_period: str, data: dict) -> Forecast:
        """Save forecast"""
        session = self.get_session()
        try:
            forecast = Forecast(sme_id=sme_id, forecast_period=forecast_period, **data)
            session.add(forecast)
            session.commit()
            session.refresh(forecast)
            return forecast
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving forecast: {e}")
            raise
        finally:
            session.close()
    
    # Recommendation Operations
    def save_recommendation(self, sme_id: int, category: str, 
                           recommendation_text: str, priority: str = 'medium') -> Recommendation:
        """Save recommendation"""
        session = self.get_session()
        try:
            rec = Recommendation(
                sme_id=sme_id,
                category=category,
                recommendation_text=recommendation_text,
                priority=priority
            )
            session.add(rec)
            session.commit()
            session.refresh(rec)
            return rec
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving recommendation: {e}")
            raise
        finally:
            session.close()
    
    def get_recommendations(self, sme_id: int, status: str = None) -> List[Recommendation]:
        """Get recommendations"""
        session = self.get_session()
        try:
            query = session.query(Recommendation).filter(Recommendation.sme_id == sme_id)
            if status:
                query = query.filter(Recommendation.status == status)
            return query.order_by(Recommendation.created_at.desc()).all()
        finally:
            session.close()


# Example usage
if __name__ == "__main__":
    print("Testing database repository...")
    print("\nNote: This requires PostgreSQL to be installed and running.")
    print("If you don't have PostgreSQL, the connection will fail (expected).\n")
    
    try:
        repo = DatabaseRepository()
        
        if repo.engine:
            print("[OK] Database connection successful")
            
            # Try to create tables
            repo.create_tables()
            print("[OK] Database tables created")
            
            # Try to create a test SME
            try:
                test_sme = repo.create_sme(
                    business_name="Test Business",
                    industry="Retail Electronics",
                    registration_number="TEST001"
                )
                print(f"[OK] Created test SME with ID: {test_sme.id}")
                
                # Fetch it back
                fetched = repo.get_sme(test_sme.id)
                print(f"[OK] Retrieved SME: {fetched.business_name}")
                
            except Exception as e:
                print(f"[WARNING] SME operations failed: {e}")
        else:
            print("[FAILED] Database connection failed")
            print("\nThis is expected if PostgreSQL is not installed.")
            print("The application will work without database - data will be in-memory only.")
        
    except Exception as e:
        print(f"[ERROR] Database error: {e}")
        print("\nThis is expected if PostgreSQL is not installed.")
        print("The application will work without database - data will be in-memory only.")
    
    print("\n" + "="*60)
    print("Database repository module loaded successfully")
    print("="*60)
    
    input("\nPress Enter to exit...")