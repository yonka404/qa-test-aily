from pages.grafana import Grafana
from pages.checks import Checks


def test_checks_details(driver):
    # Step 0: Navigate to the Grafana home page
    driver.get("https://play.grafana.org/a/grafana-synthetic-monitoring-app/home")

    # Step 1: Select the "AMER" region from the dropdown in the Grafana home page
    grafana = Grafana(driver)
    grafana.get_region_dropdown("AMER")

    # Step 2: Web scrappe the values instance, job, check_type,
    # state (up or down), reachability and latency.
    grafana_row_values: dict[str, str] = grafana.get_all_checks_table(row_number=1)

    # Step 3: Click on the first row now (must match the previous test step)
    grafana.click_instance_inside_row("grafana.com")

    # Step 4: Now we compare the stored table with the current data of the page
    checks = Checks(driver)

    assert grafana_row_values["job"] == checks.page_title(), "Job/Title mismatch"
    assert (
        grafana_row_values["state"].strip().lower() != "up"
        or int(float(checks.get_uptime())) == 100
    ), "Expected uptime 100% when state is up"
    assert grafana_row_values["reachability"] == checks.get_reachability(), (
        "Reachability mismatch"
    )
    assert (
        abs(
            float(grafana_row_values["latency"].replace("ms", "").strip())
            - checks.get_average_latency_ms()
        )
        < 0.3
    ), "Latency mismatch"


def test_no_data_in_table(driver):
    # Step 0: Navigate to the Grafana home page
    driver.get("https://play.grafana.org/a/grafana-synthetic-monitoring-app/home")
    # Step 1: Select the "AMER" region from the dropdown in the Grafana home page
    grafana = Grafana(driver)
    grafana.get_region_dropdown("AMER")
