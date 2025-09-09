import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function")
def driver():
    chrome_opts = Options()
    chrome_opts.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_opts)
    yield driver
    driver.quit()
