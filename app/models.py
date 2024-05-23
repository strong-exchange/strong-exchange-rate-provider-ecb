from datetime import date

from pydantic import BaseModel


class Rate(BaseModel):
    currency: str
    rate: float


class LatestResponse(BaseModel):
    base: str = "EUR"
    rates: list[Rate] = []
    date: str | None = None


class HistoryResponse(BaseModel):
    base: str = "EUR"
    start_at: date
    end_at: date
    rates: dict[str, dict[str, float]] = {}
