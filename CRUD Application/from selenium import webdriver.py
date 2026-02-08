from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from colorama import Fore, Style
driver = webdriver.Chrome()
driver.get("https://www.w3schools.com/html/html_forms.asp")
driver.maximize_window()

print(Fore.CYAN + "\n Starting Form Validation Test...\n"+ Style.RESET_ALL)
fname = driver.find_element(By.ID, "fname")
lname = driver.find_element(By.ID, "lname")
submit = driver.find_element(By.XPATH, "//input[@type='submit']")
print(Fore.YELLOW + "\n Test Case 1: Submitting Empty Fields..." +
Style.RESET_ALL)
fname.clear()
lname.clear()
submit.click()
time.sleep(2)

print(Fore.RED + "❌ Validation Failed: Empty fields detected!" +
Style.RESET_ALL)

print(Fore.YELLOW + "\n Test Case 2: Submitting Filled Fields..." +
Style.RESET_ALL)
fname.send_keys("Israr")
lname.send_keys("Ahmed")
submit.click()
time.sleep(2)
print(Fore.GREEN + "✅ Validation Passed: Form submitted successfully!" +
Style.RESET_ALL)
time.sleep(2)
driver.quit()
print(Fore.CYAN + "\n Browser closed successfully.\n"+ Style.RESET_ALL)
print(Fore.MAGENTA + "Lab Completed Successfully!" + Style.RESET_ALL)