from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement  

def wait_until_find_element(driver, by, value, timeout: int = 10, parent=None) -> WebElement:
    """
    Wait until an element is present. If parent is provided, search within it.
    """
    if parent is not None:
        return WebDriverWait(driver, timeout).until(
            lambda d: parent.find_element(by, value)
        )
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )