from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from app.weather_service import get_weather
from app.cashe import get_cached_response, set_cashed_response


app = FastAPI()

# Подключаем папку со статикой
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Настраиваем шаблонизатор Jinja2
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def get(request: Request, city: str | None = None, period: int = 1):
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

        return templates.TemplateResponse(
            request, name="index.html", context=context)
    return templates.TemplateResponse(request, "index.html")
