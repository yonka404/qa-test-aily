from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.grafana import Grafana
from pages.checks import Checks

driver = webdriver.Chrome()
driver.get("https://play.grafana.org/a/grafana-synthetic-monitoring-app/home")

# Initialize the webdriver with options
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
grafana = Grafana(driver)
grafana.get_region_dropdown("AMER")

# Store an instance of the filtered table
filtered_table = grafana.all_checks_table

# Click on a row that id AMER only
grafana.click_instance_inside_row("grafana.com")

# Now we compare the stored table with the current data of the page

checks = Checks(driver)

grafana_uptime = checks.get_uptime()
table_uptime = filtered_table.find_element(By.XPATH, ".//td[3]").text.strip()
assert grafana_uptime == float(table_uptime), f"Uptime mismatch: {grafana_uptime} != {table_uptime}"
print("Uptime values match:", grafana_uptime)

grafana_reachability = checks.get_reachability()
table_reachability = filtered_table.find_element(By.XPATH, ".//td[4]").text.strip()
assert grafana_reachability == float(table_reachability), f"Reachability mismatch: {grafana_reachability} != {table_reachability}"

