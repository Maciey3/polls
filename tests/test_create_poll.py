import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("http://localhost:8000/")
    yield driver
    driver.quit()

def choose_poll_style(driver):
    toggle_button = driver.find_element(By.XPATH, "//div[contains(@class, 'peer')]")  # Przełącznik toggle
    toggle_button.click()  # Kliknij, aby włączyć edycję stylu
    time.sleep(1)

    style_to_select = driver.find_element(By.XPATH, "//div[@id='check']//i[contains(@class, 'fa-check')]")
    style_to_select.click()
    time.sleep(1)

    toggle_button.click()
    time.sleep(1)

def test_create_poll_with_empty_form(driver):
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)
    driver.find_element(By.ID, "username").send_keys("testuser")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Create Poll").click()
    time.sleep(1)

    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(1)

    question_field = driver.find_element(By.ID, "question")
    validation_message = question_field.get_attribute("validationMessage")
    print(validation_message)
    assert validation_message == "Wypełnij to pole.", f"Expected 'Wypełnij to pole.' but got '{validation_message}'"


def test_create_poll_with_valid_data(driver):
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)
    driver.find_element(By.ID, "username").send_keys("testuser")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)

    driver.find_element(By.LINK_TEXT, "Create Poll").click()
    time.sleep(1)

    choose_poll_style(driver)

    driver.find_element(By.ID, "question").send_keys("What is your favorite color?")
    driver.find_element(By.ID, "option1").send_keys("Red")
    driver.find_element(By.ID, "option2").send_keys("Blue")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(1)

    assert "Poll created successfully!" in driver.page_source, "Poll creation failed."

def test_create_poll_with_missing_option(driver):
    driver.find_element(By.ID, "login-button").click()
    time.sleep(1)
    driver.find_element(By.ID, "username").send_keys("testuser")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Create Poll").click()
    time.sleep(1)

    choose_poll_style(driver)

    driver.find_element(By.ID, "question").send_keys("What is your favorite color?")
    driver.find_element(By.ID, "option1").send_keys("Red")

    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(1)

    question_field = driver.find_element(By.ID, "option2")
    validation_message = question_field.get_attribute("validationMessage")
    assert validation_message == "Wypełnij to pole.", f"Expected 'Wypełnij to pole.' but got '{validation_message}'"

