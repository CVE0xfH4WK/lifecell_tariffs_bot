import asyncio
import re
from parser.schema import (INFINITE_DATA_STRING, DataRange, GeneralOverview,
                           GeneralTariffInfo, PhoneMinutesInfo,
                           ServiceAmountData)
from parser.utils.setup_driver import setup_driver

from bs4 import BeautifulSoup, Tag

TARIFF_OVERVIEW_URL = 'https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/'
INFINITE_STRING = 'безліміт'
DATA_UNITS = {
    'мб': 1000,
    'гб': 1,
    'хв': 1
}

def parse_traffic_number_gb(number_string: str) -> ServiceAmountData:
    if number_string.lower().startswith(INFINITE_STRING[:5]):
        return INFINITE_DATA_STRING

    splitted = number_string.strip().split(' ')
    amount_str, data_unit = splitted
    return int(amount_str) / DATA_UNITS[data_unit.lower()]


def parse_range_or_constant(
    tag: Tag
) -> DataRange | ServiceAmountData:
    if len(tag.contents) >= 4:
        return (
            parse_traffic_number_gb(tag.contents[1].text),
            parse_traffic_number_gb(tag.contents[-1].text)
        )
    else:
        return parse_traffic_number_gb(
            tag.contents[1].text
        )


async def parse_tariff_overview() -> GeneralOverview:
    driver = setup_driver()

    driver.get(TARIFF_OVERVIEW_URL)
    await asyncio.sleep(1)

    contents = driver.page_source
    driver.close()

    soup = BeautifulSoup(contents, 'html.parser')

    tariff_containers = soup.find_all(class_='css-ieznkm')
    info: list[GeneralTariffInfo] = []

    for container in tariff_containers:
        general_info = container.contents[0].contents[0]

        price_and_duration_regex = r'[0-9]+'
        price, duration = re.findall(
            price_and_duration_regex,
            general_info.contents[1].text
        )

        services_container = container.contents[1]
        cellular_traffic_container = services_container.contents[0].contents[0].contents[1]
        cellular = parse_range_or_constant(cellular_traffic_container)

        phone_minutes_container = services_container.contents[1].contents[0].contents[1]
        phone_minutes = parse_range_or_constant(phone_minutes_container)
        
        info.append(GeneralTariffInfo(
            name=general_info.contents[0].text,
            price=price,
            duration_weeks=duration,
            cellular_gb=cellular,
            phone_minutes=PhoneMinutesInfo(
                value=phone_minutes,
                description=services_container.contents[1].contents[-1].text
            ),
            additional_info=[]
        ))

    return GeneralOverview(
        tariffs=info
    )
