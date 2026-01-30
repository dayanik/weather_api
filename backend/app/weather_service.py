import httpx

from dataclasses import dataclass
from datetime import date, timedelta

from app.config import API_KEY


@dataclass
class WeatherDay:
    datetime: date
    tempmax: float
    tempmin: float
    temp: float
    precip: float
    windspeed: float
    cloudcover: float
    normal: dict[str: list]


@dataclass
class WeatherResponse:
    querycost: int
    latitude: float
    longitude: float
    resolvedAddress: str
    address: str
    timezone: str
    tzoffset: int
    days: list[WeatherDay]


path = "https://weather.visualcrossing.com/VisualCrossingWebServices/"\
"rest/services/timeline/{city}/{start_date}/{end_date}/"
params = {
    "unitGroup": 'metric',
    "elements": "cloudcover,datetime,precip,temp,tempmax,tempmin,windspeed",
    "include": "days",
    "key": API_KEY,
    "contentType": "json"
}


def get_period(period: int):
    now_date = date.today()
    # `days=period-1` - получаем количество дней с текущим включительно
    end_date = (now_date + timedelta(days=period-1)).isoformat()
    start_date = now_date.isoformat()
    return start_date, end_date


def data_parsing(response: WeatherResponse) -> dict:
    context = {}
    context['days'] = response['days']
    return context


async def get_weather(city: str, period: int):
    async with httpx.AsyncClient() as client:
        start_date, end_date = get_period(period)

        full_path = path.format(
            city=city, start_date=start_date, end_date=end_date)
        
        try:
            response: WeatherResponse = await client.get(url=full_path, params=params)
        except Exception as err:
            response = err
        response = data_parsing(response.json())
        return response
