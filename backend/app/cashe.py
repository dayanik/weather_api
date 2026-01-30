import json

import redis.asyncio as redis

from app.config import REDIS_URL


TTL = 30  # ttl cash time

redis_client = redis.Redis.from_url(REDIS_URL)


def create_cash_key(city: str, period: int):
     return city + ':' + str(period)


async def get_cached_response(city: str, period: int):
    cash_key = create_cash_key(city, period)

    response = await redis_client.get(cash_key)

    if response:
        response = json.loads(response)
    return response


async def set_cashed_response(city: str, period: int, cash_data: dict):
        cash_key = create_cash_key(city, period)
        cash_data = json.dumps(cash_data)
        try:
            await redis_client.set(cash_key, cash_data, ex=TTL)
        except Exception:
             print('set failed')
