from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    name: str
    category: str
    brand: Optional[str]
    price: float
    stock_qty: int
    low_stock_limit: Optional[int] = 5
    
class DeleteProduct(BaseModel):
    id: str
    
class ProductSearch(BaseModel):
    name: Optional[str] = ""
    category: Optional[str] = ""
    brand: Optional[str] = ""