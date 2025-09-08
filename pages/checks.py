import re
from typing import Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

from utils.utils import wait_until_find_element


class Checks:
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout

        # Base XPath builder
        def section(title: str) -> str:
            return f"//section[.//h2[normalize-space()='{title}']]"

        # Common suffix for panel content spans
        def first_span_xpath(title: str) -> str:
            return f"{section(title)}//*[@data-testid='data-testid panel content']//span[1]"

        # Store important value elements at initialization
        self.uptime_span = wait_until_find_element(
            self.driver, first_span_xpath("Uptime"), By.XPATH, self.timeout
        )
        self.reachability_span = wait_until_find_element(
            self.driver, first_span_xpath("Reachability"), By.XPATH, self.timeout
        )
        self.average_latency_span = wait_until_find_element(
            self.driver, first_span_xpath("Average latency"), By.XPATH, self.timeout
        )
        self.answer_records_span = wait_until_find_element(
            self.driver, first_span_xpath("Answer Records"), By.XPATH, self.timeout
        )

        # Frequency has two spans (value + unit)
        freq_base = section("Frequency")
        self.frequency_value_span = wait_until_find_element(
            self.driver,
            f"{freq_base}//*[@data-testid='data-testid panel content']//span[1]",
            By.XPATH,
            self.timeout,
        )
        self.frequency_unit_span = wait_until_find_element(
            self.driver,
            f"{freq_base}//*[@data-testid='data-testid panel content']//span[2]",
            By.XPATH,
            self.timeout,
        )

    def _parse_first_number(self, text: str) -> float:
        m = re.search(r"[-+]?\d*\.?\d+", text.replace(",", ""))
        if not m:
            raise ValueError(f"No number found in: {text!r}")
        return float(m.group(0))

    def _safe_text(self, element):
        try:
            return element.text.strip()
        except StaleElementReferenceException:
            # If the element got refreshed in the DOM, re-find by XPath stored in element._id is not possible.
            # Caller should implement a refresh strategy if live updating panels cause staleness.
            raise

    # ---- Public getters ------------------------------------------------------

    def get_uptime(self) -> float:
        return float(self._safe_text(self.uptime_span))

    def get_reachability(self) -> float:
        return float(self._safe_text(self.reachability_span))

    def get_average_latency_ms(self) -> float:
        return float(self._safe_text(self.average_latency_span))

    def get_answer_records(self) -> int:
        return int(float(self._safe_text(self.answer_records_span)))

    def get_frequency(self) -> Tuple[float, str]:
        value = float(self._safe_text(self.frequency_value_span))
        unit = self._safe_text(self.frequency_unit_span)
        return value, unit
