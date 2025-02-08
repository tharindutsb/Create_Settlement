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
