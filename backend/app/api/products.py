from fastapi import APIRouter, HTTPException, status, Depends
from models.product import Product, DeleteProduct, ProductSearch
from db.mongo import get_db
from typing import List
from bson import ObjectId
import constants as constants

router = APIRouter()

@router.post("/add-product")
async def add_product(product: Product, db=Depends(get_db)):
    result = db[constants.PRODUCTS_COLLECTION].insert_one(product.dict(by_alias=True))
    return {"message": f"Product added with id: {result.inserted_id}"}

@router.post("/list-products")
async def list_products(db=Depends(get_db)):
    products = db[constants.PRODUCTS_COLLECTION].find(filter={}, projection={"_id": 0}).to_list(100)
    return products

@router.post("/update-product")
def update_product(product: Product, id:str, db=Depends(get_db)):
    product_id = id
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid ID")

    update_data = product.dict(by_alias=True)

    result = db[constants.PRODUCTS_COLLECTION].update_one({"_id": ObjectId(product_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"message": f"Product updated with id {product_id}"}

@router.post("/delete-product")
def delete_product(data: DeleteProduct, db=Depends(get_db)):
    product_id = data.id
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid ID")

    result = db[constants.PRODUCTS_COLLECTION].delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted successfully"}

@router.post("/search-products")
def search_products(search: ProductSearch, db=Depends(get_db)):
    query = {}

    if search.name:
        query["name"] = {"$regex": search.name, "$options": "i"}  # case-insensitive
    if search.category:
        query["category"] = {"$regex": search.category, "$options": "i"}
    if search.brand:
        query["brand"] = {"$regex": search.brand, "$options": "i"}

    results = list(db[constants.PRODUCTS_COLLECTION].find(filter=query, projection={"_id": 0}))
    return results