from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class Grafana:
    def __init__(self, driver: WebDriver):
        self.driver = driver

        # Locators
        self.region: WebElement = self.driver.find_element(
            By.XPATH, "//*[@data-testid='data-testid template variable']"
        )

    def get_region_dropdown(self, region_option: str) -> None:
        self.region.find_element(
            By.XPATH, f".//li[contains(text(), '{region_option}')]"
        ).click()
