from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from utils.utils import wait_until_find_element

class Grafana:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        # Use waits during initialization
        self.region: WebElement = wait_until_find_element(
            self.driver, By.XPATH, "//*[@data-testid='data-testid template variable']"
        )
        self.all_checks_table: WebElement = wait_until_find_element(
            self.driver, By.XPATH, "//*[@data-testid='data-testid panel content']"
        )

    def get_region_dropdown(self, region_option: str) -> None:
        option = wait_until_find_element(
            self.driver,
            By.XPATH,
            f".//li[contains(text(), '{region_option}')]",
            parent=self.region
        )
        option.click()

    def click_instance_inside_row(self, instance: str) -> None:
        link = wait_until_find_element(
            self.driver,
            By.XPATH,
            f".//a[contains(text(), '{instance}')]",
            parent=self.all_checks_table
        )
        link.click()
