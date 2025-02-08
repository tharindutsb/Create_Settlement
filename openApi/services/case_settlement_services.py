from Config.database.connectDB import case_settlements_collection
from openApi.models.case_settlement_model import Settlement
from bson import ObjectId

# Convert MongoDB document to dictionary
def settlement_helper(settlement) -> dict:
    return {
        "settlement_id": str(settlement["_id"]),
        "created_by": settlement["created_by"],
        "created_on": settlement["created_on"],
        "settlement_phase": settlement["settlement_phase"],
        "settlement_status": settlement["settlement_status"],
        "settlement_type": settlement["settlement_type"],
        "settlement_amount": settlement["settlement_amount"],
        "drc_id": settlement.get("drc_id"),
        "last_monitoring_dtm": settlement.get("last_monitoring_dtm"),
        "installment_received": settlement.get("installment_received"),
        "array_installment": settlement.get("array_installment"),
        "case_id": settlement["case_id"],
        "expire_date": settlement.get("expire_date"),
        "remark": settlement.get("remark"),
        "ro_id": settlement.get("ro_id"),
    }

# Validate settlement data
def validate_settlement_data(created_by: str, settlement_type: str, settlement_amount: float, drc_id: str, case_id: str, settlement_A_array: list, settlement_B_array: list):
    if not created_by:
        raise ValueError("Created By cannot be null")
    if not settlement_type:
        raise ValueError("Settlement Type cannot be null")
    if not settlement_amount:
        raise ValueError("Settlement Amount cannot be null")
    if not case_id:
        raise ValueError("Case ID cannot be null")
    if settlement_A_array is None and settlement_B_array is None:
        raise ValueError("Settlement A array cannot be null")

    if not isinstance(settlement_amount, float):
        raise ValueError("Settlement Amount should be a double")

    if settlement_type == 'A':
        if not isinstance(settlement_A_array, list):
            raise ValueError("Settlement A array should be an array")
        if len(settlement_A_array) != 2:
            raise ValueError("Settlement A array should have 2 elements")
        if not isinstance(settlement_A_array[0], float):
            raise ValueError("Initial amount should be a double")
        if not isinstance(settlement_A_array[1], int):
            raise ValueError("Number of months should be an integer")
    elif settlement_type == 'B':
        if not isinstance(settlement_B_array, list):
            raise ValueError("Settlement B array should be an array")
        if len(settlement_B_array) < 2 or len(settlement_B_array) > 13:
            raise ValueError("Settlement B array should have between 2 and 13 elements")
        for element in settlement_B_array:
            if not isinstance(element, float):
                raise ValueError("Element of Settlement B array should be a double")
    else:
        raise ValueError("Invalid Settlement Type")

    # Simulate reading case details and getting settlement phase
    settlement_phase = "Negotiation"  # Placeholder for actual logic
    if settlement_phase in ['Negotiation', 'Mediation Board'] and not drc_id:
        raise ValueError("DRC ID cannot be null during Negotiation or Mediation Board phase")

    return {"status": "success", "status_description": "Validation passed", "case_phase": settlement_phase}

# Create a new settlement
async def create_settlement(settlement: Settlement):
    new_settlement = await case_settlements_collection.insert_one(settlement.model_dump())
    return settlement_helper(await case_settlements_collection.find_one({"_id": new_settlement.inserted_id}))

# Get all settlements
async def get_settlements():
    settlements = []
    async for settlement in case_settlements_collection.find():
        settlements.append(settlement_helper(settlement))
    return settlements

# Get settlement by ID
async def get_settlement_by_id(settlement_id: str):
    settlement = await case_settlements_collection.find_one({"_id": ObjectId(settlement_id)})
    if settlement:
        return settlement_helper(settlement)
    return None

# Update settlement
async def update_settlement(settlement_id: str, settlement_data: dict):
    settlement = await case_settlements_collection.find_one({"_id": ObjectId(settlement_id)})
    if settlement:
        await case_settlements_collection.update_one({"_id": ObjectId(settlement_id)}, {"$set": settlement_data})
        return True
    return False

# Delete settlement
async def delete_settlement(settlement_id: str):
    settlement = await case_settlements_collection.find_one({"_id": ObjectId(settlement_id)})
    if settlement:
        await case_settlements_collection.delete_one({"_id": ObjectId(settlement_id)})
        return True
    return False
