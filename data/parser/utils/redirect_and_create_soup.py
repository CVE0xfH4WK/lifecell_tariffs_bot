import asyncio

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver

from shared.logger import get_logger

logger = get_logger(__name__)


async def redirect_and_create_soup(driver: WebDriver, page_link: str) -> BeautifulSoup:
    logger.info(f'Redirecting to {page_link = }')
    driver.get(page_link)
    await asyncio.sleep(1)

    contents = driver.page_source
    return BeautifulSoup(contents, 'html.parser')
