import httpx
import asyncio
import os

from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse


load_dotenv()
API_KEY = os.getenv("API_KEY")
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

path = "https://weather.visualcrossing.com/VisualCrossingWebServices/"\
"rest/services/timeline/{city}/{start_date}/{end_date}/"
params = {
    "unitGroup": 'metric',
    "elements": "cloudcover,datetime,precip,temp,windspeed",
    "include": "days",
    "key": API_KEY,
    "contentType": "json"
}


async def get_weather(city: str, start_date: str, end_date: str):
    async with httpx.AsyncClient() as client:
        full_path = path.format(
            city=city, start_date=start_date, end_date=end_date)
        response = await client.get(url=full_path, params=params)
        return response.json()


@app.get("/")
async def get(city: str | None = None, period: int = 1):
    if city:
        now_date = datetime.now()
        # `days=period-1` - получаем количество дней с текущим включительно
        end_date = (now_date + timedelta(days=period-1)).strftime("%Y-%m-%d")
        start_date = now_date.strftime("%Y-%m-%d")

        response = await get_weather(city, start_date, end_date)

        context = {}
        context['address'] = response['address']
        context['days'] = response['days']

        return context
    return HTMLResponse(html)
