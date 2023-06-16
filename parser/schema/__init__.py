from typing import Literal

from pydantic import BaseModel

ServiceAmountData = float | int | Literal['infinity']
DataRange = tuple[ServiceAmountData, ServiceAmountData]
INFINITE_DATA_STRING: ServiceAmountData = 'infinity'

class PhoneMinutesInfo(BaseModel):
    value: ServiceAmountData | DataRange
    description: str


class GeneralTariffInfo(BaseModel):
    name: str
    min_price: int
    duration_weeks: int
    additional_info: list[str]

    cellular_gb: ServiceAmountData | DataRange
    phone_minutes: PhoneMinutesInfo


class GeneralOverview(BaseModel):
    tariffs: list[GeneralTariffInfo]
    

class Tariffs(BaseModel):
    general_overview: GeneralOverview
