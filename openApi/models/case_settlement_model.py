from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime

class Settlement(BaseModel):
    settlement_id: str
    created_by: str
    created_on: datetime
    settlement_phase: str
    settlement_status: str
    settlement_type: str
    settlement_amount: float
    drc_id: Optional[str] = None
    last_monitoring_dtm: Optional[datetime] = None
    installment_received: Optional[List[float]] = None
    array_installment: Optional[List[dict]] = None
    case_id: str
    expire_date: Optional[datetime] = None
    remark: Optional[str] = None
    ro_id: Optional[str] = None

    @field_validator('settlement_status')
    def validate_settlement_status(cls, v):
        expected_statuses = {"Open", "Pending", "Active", "WithDraw", "Completed"}
        if v not in expected_statuses:
            raise ValueError(f"Invalid settlement status: {v}. Expected one of: {expected_statuses}")
        return v

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
