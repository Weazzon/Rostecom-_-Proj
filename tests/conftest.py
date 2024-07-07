import pytest
from selenium import webdriver


@pytest.fixture(autouse=True)
def browser():
    driver = webdriver.Chrome()

    driver.set_window_size(1400, 1000)

    yield driver

    driver.quit()