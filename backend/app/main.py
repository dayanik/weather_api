from fastapi import FastAPI

from app.weather_service import get_weather
from app.cashe import get_cached_response, set_cashed_response


app = FastAPI()
app.router.redirect_slashes = False


@app.get("/api/")
@app.get("/api")
async def get(city: str | None = None, period: int = 1):
    if city:
        # пытаемся получить кэш ответ
        response = await get_cached_response(city, period)
        if not response:        
            # получаем данные со стороннего api
            response = await get_weather(city, period)

            # кэшируем полученные данные со стороннего апи
            await set_cashed_response(city, period, response)

        return response
    return {"Плохой запрос!"}
