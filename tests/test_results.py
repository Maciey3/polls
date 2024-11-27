import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("http://localhost:8000/")
    yield driver
    driver.quit()

def open_poll_results(driver, poll_id):
    arrow_down_icon = driver.find_element(By.XPATH, f"//a[@href='/poll/{poll_id}/']/i[@class='fa-solid fa-arrow-down ']")
    arrow_down_icon.click()
    time.sleep(1)

    results_button = driver.find_element(By.ID, "openModal")
    results_button.click()
    time.sleep(2)

def is_modal_empty(driver):
    try:
        modal = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "modal-content"))
        )
        modal_text = modal.text.strip()
        if modal_text == "Votes Chart":
            return True

        return False
    except Exception as e:
        print(f"Error while checking modal: {e}")
        return False

def test_check_if_modal_is_empty(driver):
    """
    Test to verify if the modal is empty (only "Votes Chart" text).
    """
    poll_id = 4
    open_poll_results(driver, poll_id)

    assert is_modal_empty(driver), "Expected the modal to be empty, but it has content!"

def test_check_if_modal_has_content(driver):
    poll_id = 1
    open_poll_results(driver, poll_id)
    assert not is_modal_empty(driver), "Expected the modal to have content, but it only contains 'Votes Chart'!"

