from fastapi import FastAPI
from hotel_router.hotel_route import hotel_route
app=FastAPI()
app.include_router(hotel_route)