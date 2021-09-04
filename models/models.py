from typing import Optional
from pydantic import BaseModel, Field

class Volume(BaseModel):
    max: float = Field(0)
    min: float = Field(0)
    volume: float = Field(0)
    
class Info(BaseModel):
    highest_buy_bid: float = Field(0)
    lowest_sell_bid: float = Field(0)
    last_traded_price: float = Field(0)
    yes_price: float = Field(0)
    volume: Optional[Volume] = None

class CryptoCurrency(BaseModel):
    symbol: str = Field('')
    info: Optional[Info] = None
    timestamp: int = Field(0)
    datetime: int = Field(0)
    high: str = Field('')
    low: str = Field('')
    bid: float = Field(0)
    bidVolume: str = Field('')
    ask: float = Field(0)
    askVolume: str = Field('')
    vwap: str = Field('')
    open: float = Field(0)
    close: float = Field(0)
    last: float = Field(0)
    baseVolume: float = Field(0)
    quoteVolume: str = Field('')
    previousClose: str = Field('')
    change: float = Field(0)
    percentage: float = Field(0)
    average: float = Field(0)