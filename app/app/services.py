import datetime
from motor.motor_asyncio import AsyncIOMotorClient


def get_weight(x: int):
    if x == 0:
        return 1
    elif x == 1:
        return 0.9
    elif x == 2:
        return 0.8
    elif x == 3:
        return 0.75
    elif 3 < x <= 7:
        return 0.7
    elif 7 < x <= 14:
        return 0.6
    elif 14 < x <= 30:
        return 0.5
    elif 30 < x <= 60:
        return 0.3
    elif 60 < x <= 90:
        return 0.15
    else:
        return 0.1


async def insert_click_info(client: AsyncIOMotorClient, origin: int, destination: int, dt: datetime.datetime):
    db = client.db
    collection = db.routes
    route_name = f'{str(origin)}_{str(destination)}'
    route = await collection.insert_one({
        'route': route_name,
        'weight': get_weight((dt - datetime.datetime.now()).days),
    })
    db.log_events.create_index({"_id": route.inserted_id}, {'expireAfterSeconds': 3600 * 24})
    # не работает возврат объекта
    # return await collection.find_one({"_id": route.inserted_id})


async def get_weight_sum(client: AsyncIOMotorClient, origin: int, destination: int):
    db = client.db
    collection = db.routes
    route_name = f'{str(origin)}_{str(destination)}'
    weight_sum = 0
    async for item in collection.find({"route": route_name}):
        weight_sum += item["weight"]
    return weight_sum


async def get_coefficient(client: AsyncIOMotorClient, origin: int, destination: int):
    return await get_weight_sum(client, origin, destination) / await get_middle_coefficient(client, origin, destination)


async def get_middle_coefficient(client: AsyncIOMotorClient, origin: int, destination: int):
    db = client.db
    collection = db.days
    route_name = f'{str(origin)}_{str(destination)}'
    weight_sum = 0
    k = 0
    async for item in collection.find({"route": route_name}):
        weight_sum += item["weight"]
        k += 1
    return weight_sum / k


async def add_day_weight(client: AsyncIOMotorClient, origin: int, destination: int, day_weight: float):
    db = client.db
    collection = db.days
    route_name = f'{str(origin)}_{str(destination)}'
    day = await collection.insert_one({
        'route': route_name,
        'weight': day_weight,
    })
    db.log_events.create_index({"_id": day.inserted_id}, {'expireAfterSeconds': 3600 * 24 * 30})
