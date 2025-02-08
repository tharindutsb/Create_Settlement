from fastapi import FastAPI
from openApi.routes.case_settlement_routes import router as settlement_router

app = FastAPI()

app.include_router(settlement_router)

@app.get("/")
def root():
    return {"message": "Settlement API is running!"}
