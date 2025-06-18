from pydantic import BaseModel
from typing import Optional

class Customer(BaseModel):
    name: Optional[str] = ""
    phone: Optional[str] = ""
    email: Optional[str] = ""
    address: Optional[str] = ""
    outstanding: Optional[float] = 0.0