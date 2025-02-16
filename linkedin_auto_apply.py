import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime

# Kullanıcı bilgilerini credentials.json dosyasından okuyoruz
with open("credentials.json", "r") as file:
    credentials = json.load(file)

linkedin_email = credentials["username"]  # Email adresi
linkedin_password = credentials["password"]  # Şifre

# ChromeDriver yolunu belirtiyoruz
chrome_driver_path = '/Users/mehmetcelik/Documents/gelistirme/python/linkedin_auto_apply/basvuru/chromedriver-mac-arm64/chromedriver'

# Service nesnesini oluşturuyoruz
service = Service(executable_path=chrome_driver_path)

# ChromeDriver ile tarayıcıyı başlatıyoruz
driver = webdriver.Chrome(service=service)

# LinkedIn giriş sayfasına gidiyoruz
print(f"{datetime.datetime.now()}: Navigating to LinkedIn login page...")
driver.get('https://www.linkedin.com/login')

# Wait for the login button to be clickable
try:
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
    )
    print(f"{datetime.datetime.now()}: Login button is clickable.")
except Exception as e:
    print(f"{datetime.datetime.now()}: Failed to find login button. Error: {e}")
    driver.quit()

# Email ve şifre alanlarını bulup, verileri giriyoruz
email_input = driver.find_element(By.ID, 'username')  # Email alanını bul
password_input = driver.find_element(By.ID, 'password')  # Şifre alanını bul

email_input.send_keys(linkedin_email)  # Emaili gir
password_input.send_keys(linkedin_password)  # Şifreyi gir

# Giriş yap butonuna basıyoruz
login_button.click()

# Giriş yaptıktan sonra biraz bekleyelim
time.sleep(5)  # Allow page to load slightly

print(f"{datetime.datetime.now()}: Successfully logged in.")

# Navigate directly to the job search page with Easy Apply filter enabled and date filter for the past week
search_url = "https://www.linkedin.com/jobs/search/?currentJobId=4087957872&f_AL=true&f_WT=1%2C3&f_TPR=r604800&geoId=100878084&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true"
print(f"{datetime.datetime.now()}: Navigating to job search page with Easy Apply filter and date filter for the past week...")
driver.get(search_url)

# Wait until job search page is loaded (optional)
time.sleep(5)  # Give time for page to load

print(f"{datetime.datetime.now()}: Job search page loaded successfully with Easy Apply filter and date filter.")

# Add your search criteria here (e.g., 'Software Engineer' and 'Java')
search_bar = driver.find_element(By.CLASS_NAME, 'jobs-search-box__text-input')  # Job search bar element
search_bar.send_keys('Software Engineer')  # Enter the job title to search
search_bar.send_keys(Keys.RETURN)  # Press Enter to start the search

time.sleep(5)

# Now, let's apply to the first 3 jobs with 'Easy Apply'
print(f"{datetime.datetime.now()}: Applying to the first 3 jobs with 'Easy Apply'.")
job_count = 0
job_links = []

# We will loop through the job listings
job_listings = driver.find_elements(By.XPATH, '//a[@class="job-card-list__title"]')

# Iterate and apply to the first 3 jobs
for job in job_listings:
    if job_count >= 3:
        break
    
    job_link = job.get_attribute('href')
    job_links.append(job_link)
    
    # Open job listing
    driver.get(job_link)
    time.sleep(2)
    
    # Check if "Easy Apply" is available and click the apply button
    try:
        easy_apply_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Easy Apply"]'))
        )
        easy_apply_button.click()
        print(f"{datetime.datetime.now()}: Applied to job: {job_link}")
        job_count += 1
        
        # Wait for the application form to load and submit (if needed)
        time.sleep(2)
        submit_button = driver.find_element(By.XPATH, '//button[text()="Submit"]')
        submit_button.click()
        print(f"{datetime.datetime.now()}: Job application submitted.")
        
    except Exception as e:
        print(f"{datetime.datetime.now()}: Error applying to job {job_link}: {e}")

# Close the browser after applying to the jobs
driver.quit()
