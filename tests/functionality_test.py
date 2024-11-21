from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

# Set up WebDriver
driver = webdriver.Chrome(executable_path='/path/to/chromedriver')

try:
    # Open the app
    driver.get('http://your-app-url.com')

    # Verify the page title
    assert "Polls" in driver.title

    # Locate the arrow button on a specific card
    arrow_buttons = driver.find_elements(By.XPATH, "//button[@aria-label='open-popup']")  # Adjust XPath if needed
    assert len(arrow_buttons) > 0, "No arrow buttons found!"

    # Click the first arrow button to open a popup
    arrow_buttons[0].click()

    # Wait for the popup to appear (you might need explicit waits here)
    time.sleep(2)  # Replace with WebDriverWait for better handling

    # Verify popup content (e.g., question and answers)
    popup = driver.find_element(By.CLASS_NAME, "popup")  # Adjust class name
    assert popup.is_displayed(), "Popup did not appear!"

    # Select a single-choice answer
    answers = popup.find_elements(By.CLASS_NAME, "answer-option")  # Adjust class name
    assert len(answers) > 0, "No answer options found!"
    answers[0].click()  # Select the first option

    # Submit the poll
    submit_button = popup.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
    submit_button.click()

    # Verify submission response (e.g., success message or updated data)
    success_message = driver.find_element(By.CLASS_NAME, "success-message")  # Adjust class name
    assert success_message.is_displayed(), "Submission failed or no response!"

    # Close the popup
    close_button = popup.find_element(By.XPATH, "//button[@aria-label='close-popup']")  # Adjust XPath
    close_button.click()

    # Verify popup is closed
    assert not popup.is_displayed(), "Popup did not close!"

finally:
    # Close the browser
    driver.quit()