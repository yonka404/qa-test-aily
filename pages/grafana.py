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
        self.all_checks_table: WebElement = wait_until_find_element(
            self.driver,
            "(//*[@data-testid='data-testid panel content']//table)[1] | "
            "(//*[@data-testid='data-testid panel content']//*[@role='grid'])[1]",
            By.XPATH,
        )
        self.probe_dropdown: WebElement = wait_until_find_element(
            self.driver,
            "//*[@data-testid='data-testid template variable'][.//label[normalize-space()='probe']]",
            By.XPATH,
        )
        # self.error_percentage_graph: WebElement = wait_until_find_element(
        #     self.driver,
        #     "//*[@data-testid='data-testid Panel header All check error percentage']",
        #     By.XPATH,
        # )

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

    def get_all_checks_table(self, row_number: int) -> dict[str, str]:
        """
        Return the Nth data row (1-based) from the All checks table as a dict with keys:
        instance, job, check_type, state, reachability, latency.
        """
        if row_number < 1:
            raise IndexError("row_number must be >= 1 (1 = first data row)")

        # Determine whether the located element is a real <table> or a role=grid.
        try:
            tag = (self.all_checks_table.tag_name or "").lower()
        except Exception:
            tag = ""

        # Collect visible data rows (skip header) and normalize to text values.
        rows_values: list[list[str]] = []

        if tag == "table":
            # Use only rows that have <td> (skips header with <th>).
            candidate_rows = self.all_checks_table.find_elements(By.XPATH, ".//tr[td]")
            for r in candidate_rows:
                cells = r.find_elements(By.XPATH, "./td")
                values: list[str] = []
                for c in cells[:6]:
                    links = c.find_elements(By.XPATH, ".//a[1]")
                    txt = (links[0].text if links else c.text).strip()
                    values.append(txt)
                if len(values) >= 6:
                    rows_values.append(values)
        else:
            # React Data Grid: header is aria-rowindex=1; data rows start at >1.
            candidate_rows = self.all_checks_table.find_elements(
                By.XPATH, ".//*[@role='row'][@aria-rowindex>1]"
            )
            for r in candidate_rows:
                cells = r.find_elements(By.XPATH, ".//*[@role='gridcell']")
                values: list[str] = []
                for c in cells[:6]:
                    links = c.find_elements(By.XPATH, ".//a[1]")
                    txt = (links[0].text if links else c.text).strip()
                    values.append(txt)
                if len(values) >= 6:
                    rows_values.append(values)

        if row_number > len(rows_values):
            raise IndexError(
                f"row_number {row_number} is out of range (only {len(rows_values)} rows)."
            )

        vals = rows_values[row_number - 1]
        return {
            "instance": vals[0],
            "job": vals[1],
            "check_type": vals[2],
            "state": vals[3],
            "reachability": vals[4],
            "latency": vals[5],
        }

    def select_probe(self, probe_option: str) -> None:
        # Open dropdown
        toggle = self.probe_dropdown.find_element(
            By.XPATH, ".//div[contains(@class,'input-suffix')]"
        )
        toggle.click()

        # Focus the input
        combo_input = wait_until_find_element(
            self.driver,
            "//*[@data-testid='data-testid template variable']"
            "[.//label[normalize-space()='probe']]//input[@role='combobox']",
        )
        combo_input.send_keys(Keys.BACKSPACE)
        combo_input.send_keys(probe_option)
        combo_input.send_keys(Keys.ENTER)
        combo_input.send_keys(Keys.ESCAPE)

    def get_no_data_from_error_percentage_graph(self) -> str:
        return wait_until_find_element(
            self.driver,
            "//h2[normalize-space()='All check error percentage']"
            "/ancestor::section[1]//div[@data-testid='data-testid panel content']"
            "//*[contains(normalize-space(),'No data')]",
            By.XPATH,
        ).text
