from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

# Installment model
class InstallmentModel(BaseModel):
    Installment_Seq: int
    Installment_Settle_Amount: float
    Plan_Date: datetime
    Payment_Seq: Optional[int]
    Installment_Paid_Amount: Optional[float]

# Case Settlement Schema
class CaseSettlementModel(BaseModel):
    settlement_id: str
    created_by: str
    settlement_type: str  # "A" or "B"
    settlement_amount: float
    # DRC_ID: [str]
    case_id: str
    settlement_A: Optional[List[float]] = None  # [Initial_Amount, Number_of_Months]
    settlement_B: Optional[List[float]] = None  # [Initial_Amount, Amount_1...Amount_12]
    array_installment: Optional[List[InstallmentModel]] = None
    created_on: datetime = datetime.utcnow()

    @validator("settlement_type")
    def validate_settlement_type(cls, v):
        if v not in ["A", "B"]:
            raise ValueError("Invalid Settlement Type (Must be 'A' or 'B')")
        return v
