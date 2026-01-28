from fastapi import FastAPI

from app.weather_service import get_weather
from app.cashe import get_cached_response, set_cashed_response


app = FastAPI()


@app.get("/")
async def get(city: str | None = None, period: int = 1):
    if city:
        # пытаемся получить кэш ответ
        response = await get_cached_response(city, period)
        if not response:        
            # получаем данные со стороннего api
            response = await get_weather(city, period)

            # кэшируем полученные данные со стороннего апи
            await set_cashed_response(city, period, response)
        
        params = [
            ('температура, °C', 'temp'),
            ('ветер, км/ч', 'windspeed'),
            ('осадки, %', 'precip'),
            ('облачность, %', 'cloudcover')
        ]
        context = {}
        context.update(response)
        context["params"] = params

        return context
    return {"Плохой запрос!"}
