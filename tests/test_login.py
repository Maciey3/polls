from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
import time

@pytest.fixture
def setup():
    driver = webdriver.Chrome()
    driver.get("http://localhost:8000/")
    yield driver
    driver.quit()

def test_successful_login(setup):
    """Test poprawnego logowania."""
    driver = setup

    login_button = driver.find_element(By.LINK_TEXT, "Login")
    login_button.click()

    time.sleep(2)

    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")

    username_field.send_keys("testuser")
    password_field.send_keys("password123")

    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()

    time.sleep(2)

    logout_button = driver.find_element(By.LINK_TEXT, "Logout")
    assert logout_button.is_displayed()

def test_unsuccessful_login(setup):
    driver = setup

    login_button = driver.find_element(By.LINK_TEXT, "Login")
    login_button.click()

    time.sleep(2)

    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")

    username_field.send_keys("wronguser")
    password_field.send_keys("wrongpassword")

    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()

    time.sleep(2)

    error_message = driver.find_element(By.CLASS_NAME, "toast-error")
    assert error_message.is_displayed()
    assert "User doesn't exist or password is incorrect" in error_message.text
