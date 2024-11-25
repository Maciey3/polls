import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    # Konfiguracja przeglądarki
    # options = Options()
    # options.add_argument('--headless')  # W tle
    # options.add_argument('--disable-gpu')
    # service = Service('/path/to/chromedriver')  # Ścieżka do chromedriver
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# 1. Rejestracja z nieistniejącą w bazie nazwą użytkownika
def test_registration_new_user(driver):
    driver.get("http://localhost:8000/members/register")
    login_button = driver.find_element(By.LINK_TEXT, "Login")
    login_button.click()

    login_button = driver.find_element(By.LINK_TEXT, "Sign Up")
    login_button.click()
    driver.find_element(By.ID, "username").send_keys("newuser123")
    driver.find_element(By.ID, "password").send_keys("securepassword123")
    driver.find_element(By.ID, "re-password").send_keys("securepassword123")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Sprawdzenie poprawnego komunikatu rejestracji
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "toast-success")))
    assert "Account created successfully" in driver.page_source

# 2. Rejestracja z istniejącą w bazie nazwą użytkownika
def test_registration_existing_user(driver):
    driver.get("http://localhost:8000/members/register")
    driver.find_element(By.ID, "username").send_keys("existinguser")
    driver.find_element(By.ID, "password").send_keys("securepassword123")
    driver.find_element(By.ID, "re-password").send_keys("securepassword123")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Sprawdzenie komunikatu o istniejącym użytkowniku
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "toast-error")))
    assert "Username already exists" in driver.page_source

# 3. Próba rejestracji przy pustych polach formularza
def test_registration_empty_fields(driver):
    driver.get("http://localhost:8000/members/register")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Sprawdzenie komunikatu o błędzie
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "toast-error")))
    assert "Please fill out all fields" in driver.page_source

# 4. Rejestracja gdy hasło i powtórzone hasło nie są zgodne
def test_registration_password_mismatch(driver):
    driver.get("http://localhost:8000/members/register")
    driver.find_element(By.ID, "username").send_keys("newuser123")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.ID, "re-password").send_keys("differentpassword")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Sprawdzenie komunikatu o niezgodnych hasłach
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "toast-error")))
    assert "Passwords do not match" in driver.page_source
