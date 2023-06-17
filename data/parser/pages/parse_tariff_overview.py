import re

from bs4 import Tag
from selenium.webdriver.chrome.webdriver import WebDriver

from data.db.models.GeneralTariffInfo import (INFINITE_DATA_STRING, DataRange,
                                              GeneralTariffInfo,
                                              PhoneMinutesInfo,
                                              ServiceAmountData)
from data.parser.utils.redirect_and_create_soup import redirect_and_create_soup
from shared.logger import get_logger

logger = get_logger(__name__)
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


async def parse_tariff_overview(driver: WebDriver) -> list[GeneralTariffInfo]:
    soup = await redirect_and_create_soup(driver, TARIFF_OVERVIEW_URL)

    tariff_containers = soup.find_all(class_='css-ieznkm')
    info: list[GeneralTariffInfo] = []

    for container in tariff_containers:
        general_info = container.contents[0].contents[0]

        details_page_link_a = general_info.contents[0]
        details_page_link = f'https://www.lifecell.ua/{details_page_link_a["href"]}'

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

        additional_info_container = container.contents[-2]
        additional_info: list[str] = []

        for child in additional_info_container.contents:
            additional_info.append(child.text)
        
        info.append(GeneralTariffInfo(
            details_page_link=details_page_link,
            name=general_info.contents[0].text,
            min_price=price,
            duration_weeks=duration,
            cellular_gb=cellular,
            phone_minutes=PhoneMinutesInfo(
                value=phone_minutes,
                description=services_container.contents[1].contents[-1].text
            ),
            additional_info=additional_info
        ))


    await GeneralTariffInfo.insert_many(info)

    logger.info(f'Parsed the general tariffs overview at {TARIFF_OVERVIEW_URL = }')
    return info
