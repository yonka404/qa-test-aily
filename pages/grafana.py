from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from utils.utils import wait_until_find_element


class Grafana:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        # Locators
        self.region: WebElement = wait_until_find_element(
            self.driver,
            "//*[@data-testid='data-testid template variable'][.//label[normalize-space()='region']]",
        )

    def get_region_dropdown(self, region_option: str) -> None:
        # Open dropdown
        toggle = self.region.find_element(
            By.XPATH, ".//div[contains(@class,'input-suffix')]"
        )
        toggle.click()
        # Focus the input
        combo_input = wait_until_find_element(
            self.driver,
            "//*[@data-testid='data-testid template variable']"
            "[.//label[normalize-space()='region']]//input[@role='combobox']",
        )
        combo_input.clear()
        # It is not possible to click the option directly, so we type it and press Enter
        combo_input.send_keys(region_option)
        combo_input.send_keys(Keys.ENTER)

    def click_instance_inside_row(self, instance: str) -> None:
        link = wait_until_find_element(
            self.driver,
            f"//*[@data-testid='data-testid panel content']"
            f"//a[contains(normalize-space(), '{instance}')]",
            By.XPATH,
        )
        link.click()
