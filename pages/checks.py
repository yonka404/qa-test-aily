import re
from typing import Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Checks:
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def _panel_section(self, title: str):
        # section that contains an h2 with the exact title
        xpath = f"//section[.//h2[normalize-space()='{title}']]"
        return self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    def _first_number_span_text(self, title: str) -> str:
        section = self._panel_section(title)
        # first <span> inside the content area is always the numeric part
        num_span = section.find_element(
            By.XPATH,
            ".//*[@data-testid='data-testid panel content']//span[1]"
        )
        return num_span.text.strip()

    def _first_number_in_text(self, text: str) -> float:
        m = re.search(r"[-+]?\d*\.?\d+", text.replace(",", ""))
        if not m:
            raise ValueError(f"No number found in: {text!r}")
        return float(m.group(0))

    # ---- Public getters ------------------------------------------------------

    def get_uptime(self) -> float:
        """e.g. '100.00' (percent as float, without the % sign)."""
        txt = self._first_number_span_text("Uptime")       # '100.00'
        return float(txt)

    def get_reachability(self) -> float:
        """e.g. '100.00' (percent as float, without the % sign)."""
        txt = self._first_number_span_text("Reachability") # '100.00'
        return float(txt)

    def get_average_latency_ms(self) -> float:
        """e.g. '4.86' (milliseconds as float, without the ' ms')."""
        txt = self._first_number_span_text("Average latency")  # '4.86'
        return float(txt)

    def get_answer_records(self) -> int:
        """e.g. '1' (int)."""
        txt = self._first_number_span_text("Answer Records")   # '1'
        return int(float(txt))

    def get_frequency(self) -> Tuple[float, str]:
        """
        Returns (value, unit), e.g. (1.0, 'hour').
        The unit is in the second span.
        """
        section = self._panel_section("Frequency")
        value = section.find_element(
            By.XPATH, ".//*[@data-testid='data-testid panel content']//span[1]"
        ).get_text().strip() if hasattr(WebDriver, "get_text") else section.find_element(
            By.XPATH, ".//*[@data-testid='data-testid panel content']//span[1]"
        ).text.strip()

        # second span might be ' ms' / ' hour' / similar
        unit = section.find_element(
            By.XPATH, ".//*[@data-testid='data-testid panel content']//span[2]"
        ).text.strip()

        return (float(value), unit)
