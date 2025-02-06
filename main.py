from fastapi import FastAPI
from routes.case_settlement_routes import router as case_settlement_router

app = FastAPI()

# Register API routes
app.include_router(case_settlement_router)

@app.get("/")
async def home():
    return {"message": "Welcome to Case Settlement API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
