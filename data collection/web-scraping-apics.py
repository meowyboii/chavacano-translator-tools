from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Set up Selenium WebDriver
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment to run in headless mode
service = Service("./chromedriver-win64/chromedriver.exe")  # Update this path

driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the target webpage
url = "https://apics-online.info/contributions/46"  # Replace with the actual URL
driver.get(url)

# Wait for page to load
time.sleep(2)

next_button = driver.find_element(By.XPATH, "//li[@class='next']/a")
next_button.click()

# Wait for page to load
time.sleep(3)

# Click all "more" buttons
more_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'more')]")
for button in more_buttons:
    try:
        button.click()
        time.sleep(1)  # Allow time for content to expand
    except Exception as e:
        print(f"Could not click button: {e}")

# Extract content from elements with class "object-language" and "translation"
object_language_elements = driver.find_elements(By.CLASS_NAME, "object-language")
translation_elements = driver.find_elements(By.CLASS_NAME, "translation")

# Store extracted data
object_languages = [obj.text for obj in object_language_elements]
translations = [trans.text for trans in translation_elements]

# Print object-language sentences first
print("\nObject Language Sentences:")
for sentence in object_languages:
    print(sentence)

# Print translation sentences thereafter
print("\nTranslation Sentences:")
for sentence in translations:
    print(sentence)

# Close the driver
driver.quit()
