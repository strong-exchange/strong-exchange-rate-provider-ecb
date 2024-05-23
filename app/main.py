from typing import Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse

from .data import rates, latest_daily_rate_for
from .tasks import update_daily_rates_from_ecb
from .models import Rate, LatestResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    update_daily_rates_from_ecb()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/", include_in_schema=False)
async def redirect_docs():
    return RedirectResponse(url="/docs")


@app.get("/info")
def info():
    return {"base": "EUR", "daily_rates_for": latest_daily_rate_for}


@app.get("/latest")
def latest_rates(
    symbols: Annotated[list[str] | None, Query()] = None,
) -> LatestResponse:
    # if parameters passed as comma separated string, probably there's a better way to do same
    if symbols and len(symbols) == 1 and "," in symbols[0]:
        symbols = symbols[0].split(",")

    if symbols:
        rates_to_show = [
            Rate(currency=symbol, rate=rates[symbol])
            for symbol in symbols
            if symbol in rates
        ]
    else:
        rates_to_show = [
            Rate(currency=currency, rate=rate) for currency, rate in rates.items()
        ]
    return LatestResponse(rates=rates_to_show, date=latest_daily_rate_for)


# ToDo: make history endpoint
# @app.get('/history')

# ToDo: add health endpoint
