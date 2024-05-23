from typing import Annotated
from contextlib import asynccontextmanager
from datetime import date, timedelta

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse

from .data import rates, history_data, latest_daily_rate_for
from .tasks import update_daily_rates_from_ecb
from .models import Rate, LatestResponse, HistoryResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    await update_daily_rates_from_ecb()
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


@app.get("/history")
def history(
    symbols: Annotated[list[str] | None, Query()] = None,
    start_at: Annotated[date | None, Query()] = None,
    end_at: Annotated[date | None, Query()] = None,
) -> HistoryResponse:
    # if parameters passed as comma separated string, probably there's a better way to do same
    if symbols and len(symbols) == 1 and "," in symbols[0]:
        symbols = symbols[0].split(",")

    if not start_at and not end_at:
        end_at = date.today()

    if start_at and not end_at:
        end_at = start_at + timedelta(days=6)

    if not start_at and end_at:
        start_at = end_at - timedelta(days=6)

    if start_at > end_at:
        raise HTTPException(422, "Wrong interval.")

    if not history_data:
        return HistoryResponse(start_at=start_at, end_at=end_at, rates={})

    dates = [d for d in history_data.keys() if str(start_at) <= d <= str(end_at)]
    return HistoryResponse(
        start_at=start_at,
        end_at=end_at,
        rates={
            date: {
                symbol: rate
                for symbol, rate in history_data[date].items()
                if symbols is None or symbol in symbols
            }
            for date in dates
        },
    )
    history_data
    return {"message": "History endpoint is not implemented yet."}


# ToDo: add health endpoint
