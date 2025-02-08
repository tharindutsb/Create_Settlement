from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from bson import ObjectId

# Installment Model
class Installment(BaseModel):
    installment_seq: int
    installment_settle_amount: float
    plan_date: datetime
    payment_seq: Optional[int] = None
    installment_paid_amount: Optional[float] = None

    @field_validator("installment_settle_amount", "installment_paid_amount")
    def validate_amounts(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Installment amounts must be positive")
        return v

# Settlement Model
class Settlement(BaseModel):
    settlement_id: UUID = Field(..., description="Unique identifier for the settlement")
    created_by: str
    created_on: datetime
    settlement_phase: str
    settlement_status: str
    settlement_type: str
    settlement_amount: float
    drc_id: Optional[str] = None
    last_monitoring_dtm: Optional[datetime] = None
    installment_received: Optional[List[float]] = None
    array_installment: Optional[List[Installment]] = None
    case_id: str
    expire_date: Optional[datetime] = None
    remark: Optional[str] = None
    ro_id: Optional[str] = None

    # Validators
    @field_validator('settlement_status')
    def validate_settlement_status(cls, v):
        expected_statuses = {"Open", "Pending", "Active", "WithDraw", "Completed"}
        if v not in expected_statuses:
            raise ValueError(f"Invalid settlement status: {v}. Expected one of: {expected_statuses}")
        return v

    @field_validator('settlement_phase')
    def validate_settlement_phase(cls, v):
        expected_phases = {"Negotiation", "Mediation Board", "LOD", "Litigation", "WRIT"}
        if v not in expected_phases:
            raise ValueError(f"Invalid settlement phase: {v}. Expected one of: {expected_phases}")
        return v

    @field_validator("settlement_amount")
    def validate_settlement_amount(cls, v):
        if v <= 0:
            raise ValueError("Settlement Amount must be a positive number")
        return v

    @field_validator("installment_received", mode="before")
    def validate_installments(cls, v):
        if v and any(i <= 0 for i in v):
            raise ValueError("All installment values must be positive")
        return v

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v),
            ObjectId: lambda v: str(v),
        }
