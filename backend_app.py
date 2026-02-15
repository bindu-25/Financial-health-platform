from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import pandas as pd
import io
import os
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for uploaded data
uploaded_data_store = {}

# Health check
@app.get("/api/health")
def api_health_check():
    return {"status": "healthy", "message": "FinSight AI Backend Running"}

# File upload and analysis endpoint
@app.post("/api/analyze")
async def analyze_file(file: UploadFile = File(...), sme_id: int = Form(default=1)):
    """Upload and analyze Excel/CSV file"""
    try:
        logger.info(f"Received file: {file.filename}")
        contents = await file.read()
        
        # Parse file
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents))
        
        logger.info(f"Parsed file with {len(df)} rows and columns: {df.columns.tolist()}")
        
        # Normalize column names (case insensitive)
        df.columns = df.columns.str.lower().str.strip()
        
        # Basic validation
        required_cols = ['date', 'revenue', 'expenses']
        missing = [col for col in required_cols if col not in df.columns]
        
        if missing:
            raise HTTPException(400, f"Missing required columns: {missing}. Found columns: {df.columns.tolist()}")
        
        # Convert date column
        df['date'] = pd.to_datetime(df['date'])
        
        # Calculate metrics
        total_revenue = float(df['revenue'].sum())
        total_expenses = float(df['expenses'].sum())
        profit = total_revenue - total_expenses
        margin = (profit / total_revenue * 100) if total_revenue > 0 else 0
        
        # Calculate GST if columns exist
        gst_collected = float(df['gst_collected'].sum()) if 'gst_collected' in df.columns else total_revenue * 0.18
        gst_paid = float(df['gst_paid'].sum()) if 'gst_paid' in df.columns else total_expenses * 0.18
        net_gst = gst_collected - gst_paid
        
        # Calculate credit score (simplified)
        profitability_score = min(100, max(0, margin * 5))
        liquidity_score = 80  # Simplified
        credit_score = (profitability_score * 0.4 + liquidity_score * 0.6)
        
        # Determine rating
        if credit_score >= 85:
            rating = 'AA'
        elif credit_score >= 70:
            rating = 'A'
        elif credit_score >= 55:
            rating = 'B'
        elif credit_score >= 40:
            rating = 'C'
        else:
            rating = 'D'
        
        # Store processed data
        processed_data = {
            'credit_score': {
                'score': credit_score,
                'rating': rating,
                'factors': {
                    'profitability': profitability_score,
                    'liquidity': liquidity_score,
                    'leverage': 75,
                    'efficiency': 72
                }
            },
            'profit_loss': {
                'revenue': total_revenue,
                'expenses': total_expenses,
                'net_profit': profit,
                'margin': margin
            },
            'gst': {
                'collected': gst_collected,
                'paid': gst_paid,
                'net': net_gst,
                'compliance_score': 95
            },
            'metrics': {
                'totalRevenue': total_revenue,
                'netProfit': profit,
                'profitMargin': margin,
                'creditScore': credit_score
            },
            'cashFlow': {
                'months': df['date'].dt.strftime('%b').tolist()[-6:],
                'inflow': df['revenue'].tolist()[-6:],
                'outflow': df['expenses'].tolist()[-6:]
            },
            'forecasts': {
                'next_6_months': [total_revenue/len(df) * 1.05**i for i in range(1, 7)]
            },
            'last_updated': datetime.now().isoformat()
        }
        
        # Store in memory
        uploaded_data_store[sme_id] = processed_data
        
        logger.info(f"Successfully processed file for SME {sme_id}")
        
        return {
            "status": "success",
            "records": len(df),
            "sme_id": sme_id,
            "summary": {
                "total_revenue": total_revenue,
                "total_expenses": total_expenses,
                "profit": profit,
                "margin": margin,
                "credit_score": credit_score,
                "rating": rating
            }
        }
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/smes")
def get_smes():
    return {
        "smes": [
            {"id": 1, "name": "Sample SME", "industry": "Retail", "creditScore": 75}
        ]
    }

@app.get("/api/smes/{sme_id}/dashboard")
def get_dashboard(sme_id: int):
    # Return uploaded data if available, otherwise return default data
    if sme_id in uploaded_data_store:
        logger.info(f"Returning uploaded data for SME {sme_id}")
        return uploaded_data_store[sme_id]
    
    # Default data
    logger.info(f"Returning default data for SME {sme_id}")
    return {
        "sme_id": sme_id,
        "credit_score": {
            "score": 75,
            "rating": "A",
            "factors": {
                "profitability": 80,
                "liquidity": 70,
                "leverage": 75,
                "efficiency": 72
            }
        },
        "profit_loss": {
            "revenue": 1000000,
            "expenses": 750000,
            "net_profit": 250000,
            "margin": 25
        },
        "forecasts": {
            "next_6_months": [105000, 110000, 115000, 120000, 125000, 130000],
            "confidence_interval": [0.9, 0.95]
        },
        "gst": {
            "collected": 180000,
            "paid": 135000,
            "net": 45000,
            "compliance_score": 95
        },
        "metrics": {
            "totalRevenue": 5000000,
            "netProfit": 750000,
            "profitMargin": 15.0,
            "creditScore": 75
        },
        "cashFlow": {
            "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "inflow": [400000, 450000, 420000, 480000, 500000, 520000],
            "outflow": [350000, 380000, 360000, 400000, 420000, 440000]
        },
        "last_updated": datetime.now().isoformat()
    }

@app.get("/api/smes/{sme_id}/credit-score")
def get_credit_score(sme_id: int):
    if sme_id in uploaded_data_store:
        return uploaded_data_store[sme_id]['credit_score']
    
    return {
        "score": 75,
        "rating": "B+",
        "factors": {
            "profitability": 80,
            "liquidity": 75,
            "leverage": 70,
            "efficiency": 72
        }
    }

@app.get("/api/smes/{sme_id}/recommendations")
def get_recommendations(sme_id: int):
    return {
        "recommendations": [
            {
                "title": "Improve Working Capital",
                "description": "Reduce inventory holding period by 10 days to free up ₹50,000 in cash",
                "priority": "high",
                "impact": "High",
                "timeline": "30 days"
            },
            {
                "title": "Optimize Payment Terms",
                "description": "Negotiate with suppliers for 45-day payment terms instead of 30",
                "priority": "medium",
                "impact": "Medium",
                "timeline": "60 days"
            }
        ]
    }

# Serve React frontend (MUST BE LAST)
frontend_build_dir = Path(__file__).parent / "frontend" / "build"

if frontend_build_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_build_dir / "static")), name="static")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("api/"):
            return {"error": "API endpoint not found"}
        
        file_path = frontend_build_dir / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        
        return FileResponse(frontend_build_dir / "index.html")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)