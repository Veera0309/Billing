from fastapi import APIRouter, HTTPException, Depends
from db.mongo import get_db
from models.bill import CreateBill, BillItem, PaymentUpdate
import constants
from bson import ObjectId

router = APIRouter()

@router.post("/create-bill")
def create_bill(bill: CreateBill, db=Depends(get_db)):
    # Deduct stock for each product
    for item in bill.items:
        product = db[constants.PRODUCTS_COLLECTION].find_one({"_id": ObjectId(item.product_id)})
        if not product:
            raise HTTPException(status_code=404, detail=f"Product not found: {item.name}")
        if product["stock_qty"] < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for: {item.name}")
        
        db[constants.PRODUCTS_COLLECTION].update_one(
            {"_id": ObjectId(item.product_id)},
            {"$inc": {"stock_qty": -item.quantity}}
        )
        
    if bill.customer_id:
        customer = db[constants.CUSTOMERS_COLLECTION].find_one({"_id": ObjectId(bill.customer_id)})
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        bill.customer_name = customer["name"]
        
        due = bill.total - bill.paid
        if due > 0:
            db[constants.CUSTOMERS_COLLECTION].update_one(
                {"_id": ObjectId(bill.customer_id)},
                {"$inc": {"outstanding": due}}
            )
    
    # Insert bill
    bill_dict = bill.dict()
    db[constants.BILLS_COLLECTION].insert_one(bill_dict)
    return {"message": "Bill created successfully"}

@router.post("/list-bills")
def list_bills(db=Depends(get_db)):
    bills = list(db[constants.BILLS_COLLECTION].find(filter={}, projection={"_id": 0}).sort("date", -1))
    return bills

@router.post("/record-payment")
def record_payment(data: PaymentUpdate, db=Depends(get_db)):
    if not ObjectId.is_valid(data.customer_id):
        raise HTTPException(status_code=400, detail="Invalid customer ID")

    # Update outstanding balance
    db[constants.CUSTOMERS_COLLECTION].update_one(
        {"_id": ObjectId(data.customer_id)},
        {"$inc": {"outstanding": -data.amount_paid}}
    )

    # Log payment in a separate collection
    db[constants.PAYMENTS_COLLECTION].insert_one(data.dict())

    return {"message": f"₹{data.amount_paid} payment recorded"}