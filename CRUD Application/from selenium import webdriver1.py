from selenium import webdriver
from selenium.webdriver.common.by import By

# Step 1: Open Chrome browser
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True) # Keeps browser open
driver = webdriver.Chrome(options=options)

# Step 2: Open the login page
driver.get("https://practicetestautomation.com/practice-test-login/")

# --------- Test Case 1: Valid Login ---------
driver.find_element(By.ID, "username").send_keys("student") # Enter correct username
driver.find_element(By.ID, "password").send_keys("Password123") # Enter correct password

driver.find_element(By.ID, "submit").click() # Click login button

# Verify success message
if "Logged In Successfully" in driver.page_source:
    print("✓ TC-01 Passed: Valid login successful")
else:
    print("✕ TC-01 Failed: Valid login not working")

# --------- Test Case 2: Invalid Login ---------
driver.get("https://practicetestautomation.com/practice-test-login/") # Reload page
driver.find_element(By.ID, "username").send_keys("wronguser") # Wrong username
driver.find_element(By.ID, "password").send_keys("wrongpass") # Wrong password
driver.find_element(By.ID, "submit").click() # Click login button

# Verify error message
if "Your username is invalid!" in driver.page_source or "Your password is invalid!" in driver.page_source:
    print("✓ TC-02 Passed: Invalid login detected properly")
else:
    print("✕ TC-02 Failed: Invalid login not detected")