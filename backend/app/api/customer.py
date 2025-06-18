from fastapi import APIRouter, HTTPException, Depends
from db.mongo import get_db
from models.customer import Customer
import constants
from bson import ObjectId

router = APIRouter()

@router.post("/add-customer")
def add_customer(customer: Customer, db=Depends(get_db)):
    result = db[constants.CUSTOMERS_COLLECTION].insert_one(customer.dict())
    return {"message": "Customer added", "id": str(result.inserted_id)}

@router.post("/list-customers")
def list_customers(db=Depends(get_db)):
    return list(db[constants.CUSTOMERS_COLLECTION].find(filter={}, projection={"_id": 0}))

@router.post("/update-customer")
def update_customer(customer: Customer, id: str, db=Depends(get_db)):
    customer_id = id
    if not customer_id or not ObjectId.is_valid(customer_id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    
    update_data = customer.dict()
    for key,value in customer.dict().items():
        if not value:
            del update_data[key]

    result = db[constants.CUSTOMERS_COLLECTION].update_one(
        {"_id": ObjectId(customer_id)},
        {"$set": update_data}
    )
    return {"message": "Customer updated"} if result.modified_count else {"message": "No changes made"}
