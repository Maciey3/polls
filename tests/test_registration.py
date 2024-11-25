import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time  # For small delays between actions

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("http://localhost:8000/")
    yield driver
    driver.quit()

def test_register_new_account(driver):
    driver.get("http://localhost:8000")  # Update to your actual app's URL

    login_button = driver.find_element(By.ID, "login-button")
    assert login_button.is_displayed()
    login_button.click()

    time.sleep(1)
    sign_up_link = driver.find_element(By.LINK_TEXT, "Sign Up")
    assert sign_up_link.is_displayed()
    sign_up_link.click()

    time.sleep(1)
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    re_password_field = driver.find_element(By.ID, "re-password")
    register_button = driver.find_element(By.XPATH, "//button[@type='submit']")

    username_field.send_keys("newtestuser1")
    password_field.send_keys("securepassword123")
    re_password_field.send_keys("securepassword123")

    register_button.click()

    time.sleep(2)
    assert "Welcome" in driver.page_source or "Successfully registered!" in driver.page_source
