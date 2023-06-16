from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver


def setup_driver() -> WebDriver:
    option = webdriver.ChromeOptions()

    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-sh-usage')
    driver = webdriver.Chrome(options=option)
    return driver
