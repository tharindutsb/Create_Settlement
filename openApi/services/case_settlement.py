from database import database
from models.case_settlement import CaseSettlementModel

collection = database["case_settlements"]

# Create Settlement
async def create_case_settlement(settlement: CaseSettlementModel):
    result = await collection.insert_one(settlement.dict())
    return {"message": "Case settlement created", "id": str(result.inserted_id)}

# Get All Settlements
async def get_all_case_settlements():
    settlements = await collection.find().to_list(100)
    return settlements

# Get Settlement by ID
async def get_case_settlement(settlement_id: str):
    settlement = await collection.find_one({"settlement_id": settlement_id})
    return settlement

# Update Settlement
async def update_case_settlement(settlement_id: str, settlement: dict):
    result = await collection.update_one({"settlement_id": settlement_id}, {"$set": settlement})
    return result.modified_count

# Delete Settlement
async def delete_case_settlement(settlement_id: str):
    result = await collection.delete_one({"settlement_id": settlement_id})
    return result.deleted_count
