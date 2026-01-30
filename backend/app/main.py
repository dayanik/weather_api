from fastapi import FastAPI
from redis.exceptions import ConnectionError, RedisError

from app.weather_service import get_weather, ApiUnavailableError
from app.cashe import get_cached_response, set_cashed_response


app = FastAPI()
app.router.redirect_slashes = False


@app.get("/api/")
@app.get("/api")
async def get(city: str | None = None, period: int = 1):
    if city:
        try:
            response = await get_cached_response(city, period)
        except ConnectionError:
            print('Redis is not awailable')
            response = None
        except RedisError:
            print('Another Redis error')
            response = None

        if not response:
            try:
                response = await get_weather(city, period)
            except ApiUnavailableError:
                print('Сервер api не доступен')
                return {"api server not awailable"}

            try:
                await set_cashed_response(city, period, response)
            except ConnectionError:
                print('Redis is not awailable')
            except RedisError:
                print('Another Redis error')

        return response
    return {"Плохой запрос!"}
