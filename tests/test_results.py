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
    """
    Function to open poll results by clicking on the arrow down icon.
    """
    # Locate the arrow down icon for the given poll and click it
    arrow_down_icon = driver.find_element(By.XPATH, f"//a[@href='/poll/{poll_id}/']/i[@class='fa-solid fa-arrow-down ']")
    arrow_down_icon.click()
    time.sleep(1)

    # Click the button to display results (open modal)
    results_button = driver.find_element(By.ID, "openModal")
    results_button.click()
    time.sleep(2)

def is_modal_empty(driver):
    """
    Function to check if the modal is empty.
    A modal is considered empty if it contains no text other than "Votes Chart".
    Returns True if the modal is empty, False otherwise.
    """
    try:
        # Wait for the modal to appear
        modal = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "modal-content"))
        )

        # Get the text content of the modal and strip whitespace
        modal_text = modal.text.strip()

        # If modal contains only "Votes Chart", it's considered empty
        if modal_text == "Votes Chart":
            return True

        return False
    except Exception as e:
        print(f"Error while checking modal: {e}")
        return False

# Test Case: Verify Modal is Empty (only contains "Votes Chart")
def test_check_if_modal_is_empty(driver):
    """
    Test to verify if the modal is empty (only "Votes Chart" text).
    """
    poll_id = 4  # Replace with the poll ID you want to test
    open_poll_results(driver, poll_id)  # Open the poll results modal

    # Verify if the modal is empty
    assert is_modal_empty(driver), "Expected the modal to be empty, but it has content!"

# Test Case: Verify Modal Contains Content (more than "Votes Chart")
def test_check_if_modal_has_content(driver):
    """
    Test to verify if the modal contains additional content (beyond "Votes Chart").
    """
    poll_id = 1  # Replace with a poll ID that is expected to have content
    open_poll_results(driver, poll_id)  # Open the poll results modal

    # Verify if the modal is not empty
    assert not is_modal_empty(driver), "Expected the modal to have content, but it only contains 'Votes Chart'!"

