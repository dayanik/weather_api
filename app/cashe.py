import json

import redis.asyncio as redis

from app.config import REDIS_HOST, REDIS_PORT


TTL = 30  # ttl cash time

redis_client = redis.Redis(
    host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def create_cash_key(city: str, period: int):
     return city + ':' + str(period)


async def get_cached_response(city: str, period: int):
    cash_key = create_cash_key(city, period)

    try:
        response = await redis_client.get(cash_key)
    except Exception as err:
         print('get failed')

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
