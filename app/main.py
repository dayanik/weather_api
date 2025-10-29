from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.weather_service import get_weather
from app.cashe import redis_client, get_cached_response, set_cashed_response


app = FastAPI()

html = """
<!DOCTYPE html>
<html style="background-color: grey;">
    <head>
        <title>Weather</title>
    </head>
    <body>
        <form action="/" method="get">
            <label for="city">Выберите city:</label>
            <select name="city" id="city">
                <option value="ufa">ufa</option>
                <option value="sibay">sibay</option>
                <option value="moscow">moscow</option>
            </select>

            <label for="period">Выберите period:</label>
            <select name="period" id="period">
                <option value="1">1</option>
                <option value="3">3</option>
                <option value="7">7</option>
            </select>
            <button>Send</button>
        </form>

        <h2 id=city_name></h2>
        <p>Средняя температура: <span id="temp"></span></p>
        <p>Вероятность осадков: <span id="pop"></span></p>
        <p>Скорость ветра: <span id="wind"></span></p>
        <p>Облачность: <span id="clouds"></span></p>
        
        <table>
            <caption>Прогноз погоды в <span id=city_name></span></caption>
            <thead>
                <tr>
                <th></th>
                <th>ночь</th>
                <th>утро</th>
                <th>день</th>
                <th>вечер</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                <th scope="row">температура, °C</th>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                </tr>
                <tr>
                <th scope="row">ветер, км/ч</th>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                </tr>
                <tr>
                <th scope="row">осадки, %</th>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                </tr>
                <tr>
                <th scope="row">облачность, %</th>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                </tr>
            </tbody>
        </table>

    </body>
</html>
"""


@app.get("/")
async def get(city: str | None = None, period: int = 1):
    if city:
        # пытаемся получить кэш ответ
        cashed_response = await get_cached_response(city, period)
        if cashed_response:
            return cashed_response
        
        # получаем данные со стороннего api
        response = await get_weather(city, period)

        # кэшируем полученные данные со стороннего апи
        await set_cashed_response(city, period, response)

        return response
    return HTMLResponse(html)
