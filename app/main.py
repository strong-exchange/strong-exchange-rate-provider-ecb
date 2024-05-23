from typing import Union

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .data import rates, latest_daily_rate_for

app = FastAPI()


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
def latest_rates():
    return {
        'base': 'EUR',
        'rates': rates,
        'date': latest_daily_rate_for
    }

# ToDo: make history endpoint
# @app.get('/history')
