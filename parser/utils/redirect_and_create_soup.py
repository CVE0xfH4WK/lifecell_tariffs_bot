import asyncio

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver


async def redirect_and_create_soup(driver: WebDriver, page_link: str) -> BeautifulSoup:
    driver.get(page_link)
    await asyncio.sleep(1)

    contents = driver.page_source
    return BeautifulSoup(contents, 'html.parser')
