from fastapi import APIRouter, HTTPException
from models.case_settlement import CaseSettlementModel
from services.case_settlement_service import (
    create_case_settlement,
    get_all_case_settlements,
    get_case_settlement,
    update_case_settlement,
    delete_case_settlement,
)

router = APIRouter()

@router.post("/case-settlement/")
async def create_settlement(settlement: CaseSettlementModel):
    return await create_case_settlement(settlement)

@router.get("/case-settlement/")
async def fetch_settlements():
    return await get_all_case_settlements()

@router.get("/case-settlement/{settlement_id}")
async def fetch_settlement(settlement_id: str):
    settlement = await get_case_settlement(settlement_id)
    if not settlement:
        raise HTTPException(status_code=404, detail="Settlement not found")
    return settlement

@router.put("/case-settlement/{settlement_id}")
async def modify_settlement(settlement_id: str, settlement: dict):
    updated = await update_case_settlement(settlement_id, settlement)
    if updated:
        return {"message": "Settlement updated successfully"}
    raise HTTPException(status_code=404, detail="Settlement not found")

@router.delete("/case-settlement/{settlement_id}")
async def remove_settlement(settlement_id: str):
    deleted = await delete_case_settlement(settlement_id)
    if deleted:
        return {"message": "Settlement deleted successfully"}
    raise HTTPException(status_code=404, detail="Settlement not found")
