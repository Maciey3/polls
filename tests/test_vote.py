import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
import time


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("http://localhost:8000/")
    yield driver
    driver.quit()


def open_poll(driver, poll_id=2):
    poll_arrow = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//a[@href='/poll/{poll_id}/']/i"))
    )
    poll_arrow.click()
    time.sleep(1)

def test_guest_user_cannot_vote(driver):
    open_poll(driver, poll_id=2)

    option_7_radio_button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@name='vote' and @value='7']"))
    )
    option_7_radio_button.click()

    vote_button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Vote')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", vote_button)
    vote_button.click()

    try:
        modal = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "modal"))
        )
        assert modal.is_displayed(), "Login modal not displayed."
    except:
        assert "/login" in driver.current_url, "User was not redirected to the login page."

    print("Test passed: Guest user cannot vote.")


def test_vote_submission(driver):
    driver.find_element(By.ID, "login-button").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys("testuser")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    assert "Logout" in driver.page_source, "Login failed."
    open_poll(driver, poll_id=2)

    first_option_radio_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "clickTest"))
    )

    first_option_radio_button.click()

    vote_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Vote')]"))
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", vote_button)
    vote_button.click()

    error_message = driver.find_element(By.CLASS_NAME, "toast-success")
    assert error_message.is_displayed()
    assert "Voted successfully!" in error_message.text


    print("Test passed: First option selected and vote submitted successfully.")


def test_vote_removal(driver):

    driver.find_element(By.ID, "login-button").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys("testuser")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    assert "Logout" in driver.page_source, "Login failed."

    open_poll(driver, poll_id=2)

    vote_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "deleteVote"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", vote_button)
    vote_button.click()
    time.sleep(1)
    error_message = driver.find_element(By.CLASS_NAME, "toast-success")
    assert error_message.is_displayed()
    assert "Vote deleted successfully!" in error_message.text


