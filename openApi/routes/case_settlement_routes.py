from fastapi import APIRouter, HTTPException, Body
from openApi.models.case_settlement_model import Settlement
from openApi.services.case_settlement_services import (
    create_settlement,
    get_settlements,
    get_settlement_by_id,
    update_settlement,
    delete_settlement
)

router = APIRouter()

@router.post("/settlements/", response_model=Settlement)
async def add_settlement(settlement: Settlement):
    # Validation logic
    if not settlement.created_by:
        raise HTTPException(status_code=400, detail="Created By cannot be null")
    if not settlement.settlement_type:
        raise HTTPException(status_code=400, detail="Settlement Type cannot be null")
    if not settlement.settlement_amount:
        raise HTTPException(status_code=400, detail="Settlement Amount cannot be null")
    if not settlement.case_id:
        raise HTTPException(status_code=400, detail="Case ID cannot be null")
    if settlement.settlement_type == 'A' and not settlement.array_installment:
        raise HTTPException(status_code=400, detail="Settlement A array cannot be null")
    if settlement.settlement_type == 'B' and not settlement.array_installment:
        raise HTTPException(status_code=400, detail="Settlement B array cannot be null")

    if not isinstance(settlement.settlement_amount, float):
        raise HTTPException(status_code=400, detail="Settlement Amount should be a double")

    if settlement.settlement_type == 'A':
        if not isinstance(settlement.array_installment, list):
            raise HTTPException(status_code=400, detail="Settlement A array should be an array")
        if len(settlement.array_installment) != 2:
            raise HTTPException(status_code=400, detail="Settlement A array should have 2 elements")
        if not isinstance(settlement.array_installment[0], float):
            raise HTTPException(status_code=400, detail="Initial amount should be a double")
        if not isinstance(settlement.array_installment[1], int):
            raise HTTPException(status_code=400, detail="Number of months should be an integer")
    elif settlement.settlement_type == 'B':
        if not isinstance(settlement.array_installment, list):
            raise HTTPException(status_code=400, detail="Settlement B array should be an array")
        if len(settlement.array_installment) < 2 or len(settlement.array_installment) > 13:
            raise HTTPException(status_code=400, detail="Settlement B array should have between 2 and 13 elements")
        for element in settlement.array_installment:
            if not isinstance(element, float):
                raise HTTPException(status_code=400, detail="Element of Settlement B array should be a double")
    else:
        raise HTTPException(status_code=400, detail="Invalid Settlement Type")

    # Simulate reading case details and getting settlement phase
    settlement_phase = "Negotiation"  # Placeholder for actual logic
    if settlement_phase in ['Negotiation', 'Mediation Board'] and not settlement.drc_id:
        raise HTTPException(status_code=400, detail="DRC ID cannot be null during Negotiation or Mediation Board phase")

    return await create_settlement(settlement)

@router.get("/settlements/", response_model=list[Settlement])
async def fetch_settlements():
    return await get_settlements()

@router.get("/settlements/{settlement_id}", response_model=Settlement)
async def fetch_settlement(settlement_id: str):
    settlement = await get_settlement_by_id(settlement_id)
    if not settlement:
        raise HTTPException(status_code=404, detail="Settlement not found")
    return settlement

@router.put("/settlements/{settlement_id}", response_model=Settlement)
async def modify_settlement(settlement_id: str, settlement_data: dict):
    updated = await update_settlement(settlement_id, settlement_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Settlement not found")
    return await get_settlement_by_id(settlement_id)

@router.delete("/settlements/{settlement_id}")
async def remove_settlement(settlement_id: str):
    deleted = await delete_settlement(settlement_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Settlement not found")
    return {"message": "Settlement deleted successfully"}
