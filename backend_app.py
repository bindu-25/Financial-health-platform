from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import pandas as pd
import io
import os
from datetime import datetime

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/api/health")
def api_health_check():
    return {"status": "healthy", "message": "FinSight AI Backend Running"}

# File upload and analysis endpoint
@app.post("/api/analyze")
async def analyze_file(file: UploadFile = File(...), sme_id: int = Form(default=1)):
    """Upload and analyze Excel/CSV file"""
    try:
        contents = await file.read()
        
        # Parse file
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents))
        
        # Basic validation
        required_cols = ['date', 'revenue', 'expenses']
        missing = [col for col in required_cols if col.lower() not in [c.lower() for c in df.columns]]
        
        if missing:
            raise HTTPException(400, f"Missing columns: {missing}")
        
        # Process data
        total_revenue = df['revenue'].sum() if 'revenue' in df.columns else 0
        total_expenses = df['expenses'].sum() if 'expenses' in df.columns else 0
        
        return {
            "status": "success",
            "records": len(df),
            "sme_id": sme_id,
            "summary": {
                "total_revenue": float(total_revenue),
                "total_expenses": float(total_expenses),
                "profit": float(total_revenue - total_expenses)
            }
        }
        
    except Exception as e:
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