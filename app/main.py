from typing import Union
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .data import rates, latest_daily_rate_for
from .tasks import update_daily_rates_from_ecb
from .models import Rate, LatestResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    update_daily_rates_from_ecb()
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/', include_in_schema=False)
async def redirect_docs():
    return RedirectResponse(url='/docs')


@app.get('/info')
def info():
    return {
        'base': 'EUR',
        'daily_rates_for': latest_daily_rate_for
    }


@app.get('/latest')
def latest_rates() -> LatestResponse:
    return LatestResponse(
        rates=[Rate(currency=currency, rate=rate) for currency, rate in rates.items()],
        date=latest_daily_rate_for
    ) 

# ToDo: make history endpoint
# @app.get('/history')

# ToDo: add health endpoint