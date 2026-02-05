from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path

app = FastAPI()

# ============= ADD THIS CORS MIDDLEWARE =============
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= YOUR EXISTING ROUTES (KEEP THESE) =============
@app.get("/")
def health():
    return {"status": "Backend running successfully"}

# Add your other existing routes here...
# @app.get("/api/something")
# def something():
#     return {...}


# ============= ADD THESE MOCK API ROUTES FOR DEMO =============
@app.get("/api/health")
def api_health_check():
    return {"status": "healthy", "message": "FinSight AI Backend Running"}

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
        "forecasts": {
            "months": ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            "revenue": [540000, 560000, 580000, 600000, 620000, 640000]
        }
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

# ============= ADD THIS FRONTEND SERVING CODE AT THE END =============
# Serve React frontend
frontend_build_dir = Path(__file__).parent / "frontend" / "build"

if frontend_build_dir.exists():
    # Serve static files (JS, CSS, images)
    app.mount("/static", StaticFiles(directory=str(frontend_build_dir / "static")), name="static")
    
    # Serve index.html for all non-API routes (SPA routing)
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # If it's an API route, let FastAPI handle it
        if full_path.startswith("api/"):
            return {"error": "API endpoint not found"}
        
        # Check if file exists in build directory
        file_path = frontend_build_dir / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        
        # Otherwise serve index.html (for React Router)
        return FileResponse(frontend_build_dir / "index.html")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)