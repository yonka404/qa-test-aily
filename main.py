from selenium import webdriver
from pages.grafana import Grafrana

driver = webdriver.Chrome()
driver.get("https://play.grafana.org/a/grafana-synthetic-monitoring-app/home")

grafana = Grafrana(driver)
grafana.click_region_dropdown("AMER")
