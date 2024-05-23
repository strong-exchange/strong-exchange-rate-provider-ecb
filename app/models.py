from pydantic import BaseModel

class Rate(BaseModel):
    currency: str
    rate: float


class LatestResponse(BaseModel):
    base:str = 'EUR'
    rates: list[Rate] = []
    date: str | None = None
