import math
from typing import Literal, TypedDict

from bot.data_provider import data_provider
from data import GeneralTariffInfo
from data.db.models.GeneralTariffInfo import DataRange, ServiceAmountData

VALUES_DATASET = {
    'gb': [0.15, 7.0, 8.0, 20.0, 25.0, 50.0],
    'price': [90, 90, 120, 150, 180, 250, 375],
    'min': [15.0, 50.0, 300.0, 500.0, 800.0, 1500.0, 1600.0]
}

def closest_value(data, value):
    return data[min(range(len(data)), key = lambda closest: abs(data[closest]-value))]


class UserData(TypedDict):
    price: int
    internet_minutes_prio: Literal['act_minutes', 'act_internet']
    internet_minutes: str
    sms: str
    roaming: bool
    

def near_number(first: float, second: float) -> bool:
    return math.fabs(first - second) <= 50


#DATA: {'price': 375, 'internet_minutes_prio': 'act_minutes', 'internet_minutes': 'mins_500.0', 'sms': 'sms_often', 'roaming': 'roum_false'}
async def pick_tariffs(user_data: UserData) -> list[GeneralTariffInfo] | None:
    all_tariffs = await data_provider.get_tariffs_overview()
    if all_tariffs is None:
        return

    possible_tariffs: list[GeneralTariffInfo] = []
    preferred_price = user_data['price']

    preferred_criteria = user_data['internet_minutes_prio']
    if preferred_criteria == 'act_minutes':
        preferred_value = float(user_data['internet_minutes'][5:].strip())
    else:
        preferred_value = float(user_data['internet_minutes'][3:].strip())

    
    def value_from_tuple(value: float | tuple[float, float]) -> float:
        if isinstance(value, tuple):
            first, second = value
            return (first + second) / 2

        return value
            
    def resolve_matching_tariff(
        all_tariffs: list[GeneralTariffInfo],
        value: float,
        key_to_check: str
    ) -> list[GeneralTariffInfo]:
        matching: list[GeneralTariffInfo] = []
        for tariff in all_tariffs:
            if near_number(getattr(tariff, key_to_check), value):
                matching.append(tariff)

        return matching
    

    possible_tariffs = resolve_matching_tariff(
        all_tariffs,
        preferred_price,
        'min_price'
    )

    # for tariff in all_tariffs:
    #     if not near_number(tariff.min_price, preferred_price):
    #         continue

    #     phone_minutes = tariff.phone_minutes.value
    #     if preferred_criteria == 'act_minutes':
    #         if isinstance(phone_minutes, float) \
    #             or isinstance(phone_minutes, tuple):
    #             average = value_from_tuple(phone_minutes) # type: ignore
    #         else:
    #             return

    #         near_number(average, preferred_value)
            
            

    # for item in range(len(all_tariffs)):
    #     if all_tariffs[item].min_price == user_data['price']:
    #         possible_tariffs.append(all_tariffs[item])

    #     if (float(all_tariffs[item].cellular_gb) == float(user_data['internet_minutes'].replace('gb_', ''))
    #         or float(all_tariffs[item].phone_minutes) == float(user_data['internet_minutes'].replace('mins_', ''))):
    #         possible_tariffs.append(all_tariffs[item])

    return possible_tariffs        
