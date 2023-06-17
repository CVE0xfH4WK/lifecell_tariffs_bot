from math import isinf
from typing import Literal, cast

from data.db.models.GeneralTariffInfo import DataRange, ServiceAmountData

DataType = Literal['cellular'] | Literal['phone']
CONVERATION_MAPPING = {
    'cellular': {
        'GB': ('ГБ', 1),
        'MB': ('МБ', 1000)
    },
    'phone': {
        'min': ('хв', 1)
    }
}


def format_constant(constant: ServiceAmountData, data_type: DataType) -> str:
    if isinstance(constant, float) and isinf(constant):
        return 'Безліміт'

    constant = cast(int | float, constant)

    if data_type == 'cellular':
        if constant < 1:
            access_key = 'MB'
        else:
            access_key = 'GB'
    elif data_type == 'phone':
        access_key = 'min'

    data_type_name, multiplier = CONVERATION_MAPPING[data_type][access_key]
    return f'{constant * multiplier} {data_type_name}'


def format_constant_or_range(
    data: DataRange | ServiceAmountData,
    data_type: DataType
) -> str:
    if isinstance(data, tuple):
        start, stop = map(lambda item: format_constant(item, data_type), data)

        return f'від {start} до {stop}'
    else:
        return format_constant(data, data_type)
