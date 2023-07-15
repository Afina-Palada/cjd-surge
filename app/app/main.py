import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from .services import insert_click_info, get_coefficient, add_day_weight

app = FastAPI()

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncIOMotorClient('mongo', 27017)


@app.post("/click")
async def add_click(origin: int, destination: int, dt: datetime.datetime):
    return await insert_click_info(client, origin, destination, dt)


@app.get("/coefficient")
async def get_coefficient_of_marga(origin: int, destination: int):
    return await get_coefficient(client, origin, destination)


@app.post("/add_weight")
async def add_weight(origin: int, destination: int, weight: float):
    return await add_day_weight(client, origin, destination, weight)
