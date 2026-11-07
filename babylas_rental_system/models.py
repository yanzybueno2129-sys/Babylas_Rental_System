from pydantic import BaseModel
from typing import Literal

class TenantCreate(BaseModel):
    name: str
    unit: str
    rate: float
    billing_cycle: Literal["Weekly", "Semi-Monthly", "Monthly"]

class PaymentRequest(BaseModel):
    amount_paid: float