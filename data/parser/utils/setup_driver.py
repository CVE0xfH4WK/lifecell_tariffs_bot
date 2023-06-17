from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from shared.logger import get_logger

logger = get_logger(__name__)


def setup_driver() -> WebDriver:
    option = webdriver.ChromeOptions()
    logger.info("Setting up the WebDriver (chrome)")

    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-sh-usage')

    driver = webdriver.Chrome(options=option)
    logger.info("WebDriver setup")

    return driver
