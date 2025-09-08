from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By


def wait_until_find_element(
    driver: WebDriver,
    locator: str,
    type_of_search=By.XPATH,
    timeout: int = 10
) -> WebElement:
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((type_of_search, locator))
    )
