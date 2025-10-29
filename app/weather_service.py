import httpx

from datetime import datetime, timedelta

from app.config import API_KEY


path = "https://weather.visualcrossing.com/VisualCrossingWebServices/"\
"rest/services/timeline/{city}/{start_date}/{end_date}/"
params = {
    "unitGroup": 'metric',
    "elements": "cloudcover,datetime,precip,temp,windspeed",
    "include": "days",
    "key": API_KEY,
    "contentType": "json"
}


def get_period(period: int):
    now_date = datetime.now()
    # `days=period-1` - получаем количество дней с текущим включительно
    end_date = (now_date + timedelta(days=period-1)).strftime("%Y-%m-%d")
    start_date = now_date.strftime("%Y-%m-%d")
    return start_date, end_date

def data_parsing(response):
    response = response.json()
    context = {}
    context['address'] = response['address']
    context['days'] = response['days']
    return context


async def get_weather(city: str, period: int):
    async with httpx.AsyncClient() as client:
        start_date, end_date = get_period(period)

        full_path = path.format(
            city=city, start_date=start_date, end_date=end_date)
        
        try:
            response = await client.get(url=full_path, params=params)
        except Exception as err:
            response = err
        
        response = data_parsing(response)

        return response
