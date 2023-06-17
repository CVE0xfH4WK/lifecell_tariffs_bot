from bot.formatting.format_general_overview import format_general_overview
from data import GeneralTariffInfo

FORMAT_STRING = '''
Тариф ({current_index} з {total_count})
{formatted_tariff_data}
'''

def format_list_item(
    current_index: int,
    total_count: int,
    data: GeneralTariffInfo
) -> str:
    return FORMAT_STRING.format(
        current_index=current_index,
        total_count=total_count,
        formatted_tariff_data=format_general_overview(data)
    )