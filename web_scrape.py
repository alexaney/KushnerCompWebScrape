from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def scrape_apartments_with_selenium(zipcode, city, state):
    url = f"https://www.apartments.com/{city.lower()}-{state.lower()}-{zipcode}/"
    print(url)

    # Set up Chrome options
    options = Options()
    options.headless = True  # Run in headless mode
    service = Service('C:/Users/Dell/Downloads/chromedriver-win32/chromedriver-win32/chromedriver.exe')  # Adjust the path to your ChromeDriver

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(5)  # Allow time for the page to load

    apartments = []
    listings = driver.find_elements(By.CLASS_NAME, 'placard') # Find all listings
    
    for listing in listings:
        if (listing.get_attribute('class') == 'listing reinforcement placard rounded'):
            continue
        try:
            apartment_url = listing.find_element(By.CLASS_NAME, 'property-link').get_attribute('href')
        except:
            apartment_url = 'No url'

        try:
            name = listing.find_element(By.CLASS_NAME, 'title').text.strip()
        except:
            name = 'No title'

        try:
            address = listing.find_element(By.CLASS_NAME, 'property-address').text.strip()
        except:
            try:
                address = listing.find_element(By.CLASS_NAME, 'title').text.strip()
            except:
                address = 'No address'

        try:
            price = listing.find_element(By.CLASS_NAME, 'property-pricing').text.strip()
        except:
            try:
                price = listing.find_element(By.CLASS_NAME, 'price-range').text.strip()
            except:
                price = 'No price'

        try:
            beds = listing.find_element(By.CLASS_NAME, 'property-beds').text.strip()
        except:
            try:
                beds = listing.find_element(By.CLASS_NAME, 'bed-range').text.strip()
            except:
                beds = 'No bed info'
        apartments.append({'apartment_url': apartment_url, 'name': name, 'address': address, 'price': price, 'beds': beds})
    driver.quit()
    return apartments


print(scrape_apartments_with_selenium('07020', 'Edgewater', 'NJ'))
