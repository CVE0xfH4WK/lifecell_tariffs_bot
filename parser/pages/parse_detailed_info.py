from parser.schema.DetailedInformation import DetailedInformation
from parser.utils.redirect_and_create_soup import redirect_and_create_soup

from selenium.webdriver.chrome.webdriver import WebDriver


async def parse_detailed_info(driver: WebDriver, page_link: str) -> DetailedInformation:
    await redirect_and_create_soup(driver, page_link)

    return DetailedInformation(
        
    )
