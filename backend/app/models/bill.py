from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class BillItem(BaseModel):
    product_id: str
    name: str
    quantity: int
    rate: float
    amount: float

class CreateBill(BaseModel):
    customer_id: Optional[str] = None
    customer_name: Optional[str] = "Walk-in"
    items: List[BillItem]
    total: float
    paid: float
    payment_mode: Optional[str] = "Cash"  # New
    payment_note: Optional[str] = None    # New
    date: Optional[datetime] = Field(default_factory=datetime.now)

class PaymentUpdate(BaseModel):
    customer_id: str
    amount_paid: float
    mode: Optional[str] = "Cash"
    note: Optional[str] = None
    date: Optional[datetime] = Field(default_factory=datetime.now)