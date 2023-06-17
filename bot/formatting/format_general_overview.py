from bot.formatting.utils.format_constant_or_range import \
    format_constant_or_range
from data import GeneralTariffInfo

FORMAT_TEMPLATE = '''
{name} від {price} грн / {duration} тижні

Умови:
    Інтернет {cellular_string}

    Дзвінки {phone_minutes_string}
    {phone_minutes_additional}

Додатково:
{additional_string}
'''

def format_general_overview(data: GeneralTariffInfo) -> str:
    additional_string = ''.join(map(lambda item: f'    {item}\n', data.additional_info))

    result = FORMAT_TEMPLATE.format(
        name=data.name,
        price=data.min_price,
        duration=data.duration_weeks,
        cellular_string=format_constant_or_range(data.cellular_gb, 'cellular'),
        phone_minutes_string=format_constant_or_range(
            data.phone_minutes.value, 'phone'
        ),
        phone_minutes_additional=data.phone_minutes.description,
        additional_string=additional_string
    )

    return result
