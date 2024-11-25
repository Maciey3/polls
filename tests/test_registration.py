import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

@pytest.fixture
def driver():
    # Setup ChromeDriver
    driver = webdriver.Chrome()
    driver.get("http://localhost:8000/")
    yield driver
    driver.quit()

def test_register_new_account(driver):
    driver.get("http://localhost:8000")

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

    username_field.send_keys(f"testuser{random.randint(1000, 9999)}")
    password_field.send_keys("securepassword123")
    re_password_field.send_keys("securepassword123")

    register_button.click()

    time.sleep(2)

    if "Successfully registered!" in driver.page_source:
        print("Registration succeeded with a unique username.")
    elif "already exists" in driver.page_source or "UNIQUE constraint failed" in driver.page_source:
        print("Error: Username already exists. Test failed.")
        assert False, "Test failed due to username duplication."
    else:
        print("Unexpected response. Test failed.")
        assert False, "Unexpected server response during registration."

def test_register_empty_form(driver):
    driver.get("http://localhost:8000")

    login_button = driver.find_element(By.ID, "login-button")
    assert login_button.is_displayed()
    login_button.click()

    time.sleep(1)

    sign_up_link = driver.find_element(By.LINK_TEXT, "Sign Up")
    assert sign_up_link.is_displayed()
    sign_up_link.click()

    time.sleep(1)

    register_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    register_button.click()

    time.sleep(1)

    username_field = driver.find_element(By.ID, "username")
    assert username_field.get_attribute("validationMessage") == "Wypełnij to pole."

    password_field = driver.find_element(By.ID, "password")
    assert password_field.get_attribute("validationMessage") == "Wypełnij to pole."

    re_password_field = driver.find_element(By.ID, "re-password")
    assert re_password_field.get_attribute("validationMessage") == "Wypełnij to pole."

def test_register_existing_username(driver):
    driver.get("http://localhost:8000")

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

    username_field.send_keys("existinguser")
    password_field.send_keys("securepassword123")
    re_password_field.send_keys("securepassword123")

    register_button.click()

    time.sleep(2)
    assert "Username already exists" in driver.page_source


def test_register_mismatched_passwords(driver):
    driver.get("http://localhost:8000")

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

    username_field.send_keys("newtestuser2")
    password_field.send_keys("securepassword123")
    re_password_field.send_keys("differentpassword123")

    register_button.click()

    time.sleep(2)
    assert "Passwords dont match" in driver.page_source
