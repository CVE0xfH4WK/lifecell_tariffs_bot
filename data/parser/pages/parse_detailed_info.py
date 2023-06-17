from selenium.webdriver.chrome.webdriver import WebDriver

from data.db.models.DetailedInformation import DetailedInformation
from data.parser.utils.redirect_and_create_soup import redirect_and_create_soup
from shared.logger import get_logger

logger = get_logger(__name__)


async def parse_detailed_info(driver: WebDriver, page_link: str) -> DetailedInformation:
    await redirect_and_create_soup(driver, page_link)

    logger.info(f'Parsed detailed information for {page_link = }')

    # FIXME: Saturate with detailed information
    return DetailedInformation(
        tariff_name="",
        details_page_link=page_link
    )
