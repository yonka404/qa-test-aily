import re
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

from utils.utils import wait_until_find_element


# Base XPath builder
def section(title: str) -> str:
    return f"//section[.//h2[normalize-space()='{title}']]"


# Common suffix for panel content spans
def first_span_xpath(title: str) -> str:
    return f"{section(title)}//*[@data-testid='data-testid panel content']//span[1]"


class Checks:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.title = wait_until_find_element(
            self.driver, "//main[@id='pageContent']//h1", By.XPATH
        )

        # Store important value elements at initialization
        # self.answer_records_span = wait_until_find_element(
        #     self.driver, first_span_xpath("Answer Records"), By.XPATH
        # )
        # Frequency has two spans (value + unit)
        # freq_base = section("Frequency")
        # self.frequency_value_span = wait_until_find_element(
        #     self.driver,
        #     f"{freq_base}//*[@data-testid='data-testid panel content']//span[1]",
        #     By.XPATH,
        # )
        # self.frequency_unit_span = wait_until_find_element(
        #     self.driver,
        #     f"{freq_base}//*[@data-testid='data-testid panel content']//span[2]",
        #     By.XPATH,
        # )

    def _parse_first_number(self, text: str) -> float:
        m = re.search(r"[-+]?\d*\.?\d+", text.replace(",", ""))
        if not m:
            raise ValueError(f"No number found in: {text!r}")
        return float(m.group(0))

    def _safe_text(self, element):
        try:
            return element.text.strip()
        except StaleElementReferenceException:
            raise

    def page_title(self) -> str:
        return self.title.text.strip()

    def get_uptime(self) -> float:
        return float(
            self._safe_text(
                wait_until_find_element(
                    self.driver, first_span_xpath("Uptime"), By.XPATH
                )
            )
        )

    def get_reachability(self) -> str:
        """Return the whole part of the reachability value as a string with '%'.
        Example: '100%' for source text like '100.00%'."""
        variable = wait_until_find_element(
            self.driver, first_span_xpath("Reachability"), By.XPATH
        )
        raw_text = self._safe_text(variable)
        number = int(self._parse_first_number(raw_text))
        return f"{number}%"

    def get_average_latency_ms(self) -> float:
        return float(
            self._safe_text(
                wait_until_find_element(
                    self.driver, first_span_xpath("Average latency"), By.XPATH
                )
            )
        )

    # def get_answer_records(self) -> int:
    #     return int(float(self._safe_text(self.answer_records_span)))

    # def get_frequency(self) -> Tuple[float, str]:
    #     value = float(self._safe_text(self.frequency_value_span))
    #     unit = self._safe_text(self.frequency_unit_span)
    #     return value, unit
