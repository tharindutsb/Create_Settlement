from fastapi import APIRouter, HTTPException, Body
from openApi.models.case_settlement_model import Settlement
from openApi.services.case_settlement_services import (
    create_settlement,
    get_settlements,
    get_settlement_by_id,
    update_settlement,
    delete_settlement,
    validate_settlement_data
)

router = APIRouter()

@router.post("/settlements/", response_model=Settlement, tags=["Settlements"], summary="Create a new settlement")
async def add_settlement(settlement: Settlement):
    """
    Create a new settlement.

    - **settlement_id**: Unique identifier for the settlement
    - **created_by**: User who created the settlement
    - **created_on**: Date and time when the settlement was created
    - **settlement_phase**: Current phase of the settlement
    - **settlement_status**: Status of the settlement (Open, Pending, Active, WithDraw, Completed)
    - **settlement_type**: Type of the settlement (A or B)
    - **settlement_amount**: Amount of the settlement
    - **drc_id**: ID of the DRC (optional)
    - **last_monitoring_dtm**: Last monitoring date and time (optional)
    - **installment_received**: List of received installments (optional)
    - **array_installment**: List of installment details (optional)
    - **case_id**: ID of the case
    - **expire_date**: Expiry date of the settlement (optional)
    - **remark**: Remarks about the settlement (optional)
    - **ro_id**: ID of the RO (optional)
    """
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
        if not isinstance(settlement.array_installment[0]['installment_settle_amount'], float):
            raise HTTPException(status_code=400, detail="Initial amount should be a double")
        if not isinstance(settlement.array_installment[1]['installment_settle_amount'], int):
            raise HTTPException(status_code=400, detail="Number of months should be an integer")
    elif settlement.settlement_type == 'B':
        if not isinstance(settlement.array_installment, list):
            raise HTTPException(status_code=400, detail="Settlement B array should be an array")
        if len(settlement.array_installment) < 2 or len(settlement.array_installment) > 13:
            raise HTTPException(status_code=400, detail="Settlement B array should have between 2 and 13 elements")
        for element in settlement.array_installment:
            if not isinstance(element['installment_settle_amount'], float):
                raise HTTPException(status_code=400, detail="Element of Settlement B array should be a double")
    else:
        raise HTTPException(status_code=400, detail="Invalid Settlement Type")

    # Simulate reading case details and getting settlement phase
    settlement_phase = "Negotiation"  # Placeholder for actual logic
    if settlement_phase in ['Negotiation', 'Mediation Board'] and not settlement.drc_id:
        raise HTTPException(status_code=400, detail="DRC ID cannot be null during Negotiation or Mediation Board phase")

    return await create_settlement(settlement)

@router.get("/settlements/", response_model=list[Settlement], tags=["Settlements"], summary="Get all settlements")
async def fetch_settlements():
    """
    Get all settlements.
    """
    return await get_settlements()

@router.get("/settlements/{settlement_id}", response_model=Settlement, tags=["Settlements"], summary="Get a settlement by ID")
async def fetch_settlement(settlement_id: str):
    """
    Get a settlement by ID.

    - **settlement_id**: Unique identifier for the settlement
    """
    settlement = await get_settlement_by_id(settlement_id)
    if not settlement:
        raise HTTPException(status_code=404, detail="Settlement not found")
    return settlement

@router.put("/settlements/{settlement_id}", response_model=Settlement, tags=["Settlements"], summary="Update a settlement")
async def modify_settlement(settlement_id: str, settlement_data: dict):
    """
    Update a settlement.

    - **settlement_id**: Unique identifier for the settlement
    - **settlement_data**: Data to update the settlement
    """
    updated = await update_settlement(settlement_id, settlement_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Settlement not found")
    return await get_settlement_by_id(settlement_id)

@router.delete("/settlements/{settlement_id}", tags=["Settlements"], summary="Delete a settlement")
async def remove_settlement(settlement_id: str):
    """
    Delete a settlement.

    - **settlement_id**: Unique identifier for the settlement
    """
    deleted = await delete_settlement(settlement_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Settlement not found")
    return {"message": "Settlement deleted successfully"}

@router.post("/settlements/validate", response_model=dict, tags=["Settlements"], summary="Validate settlement data")
async def validate_settlement(
    created_by: str = Body(...),
    settlement_type: str = Body(...),
    settlement_amount: float = Body(...),
    drc_id: str = Body(None),
    case_id: str = Body(...),
    settlement_A_array: list = Body(None),
    settlement_B_array: list = Body(None)
):
    """
    Validate settlement data.

    - **created_by**: User who created the settlement
    - **settlement_type**: Type of the settlement (A or B)
    - **settlement_amount**: Amount of the settlement
    - **drc_id**: ID of the DRC (optional)
    - **case_id**: ID of the case
    - **settlement_A_array**: Array of initial amount and number of months (optional)
    - **settlement_B_array**: Array of initial amount and monthly amounts (optional)
    """
    try:
        return validate_settlement_data(created_by, settlement_type, settlement_amount, drc_id, case_id, settlement_A_array, settlement_B_array)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
