from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import products, bill, customer

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(bill.router, prefix="/bills", tags=["Bills"])
app.include_router(customer.router, prefix="/customers", tags=["Customers"])