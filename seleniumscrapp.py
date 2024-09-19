from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pymongo import MongoClient
import os



# MongoDB connection setup
mongo_uri = os.getenv('MONGO_URI')
mongo_client = MongoClient(mongo_uri)
db = mongo_client['ScrapperWorldBank']  # Replace with your database name
collection = db['Advertisement']  # Replace with your collection name

# Setup Firefox options (without headless mode)
firefox_options = Options()
firefox_options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'  # Specify the Firefox binary location

# Specify the path to the geckodriver
service = Service(r'C:\Users\jphid\Downloads\geckodriver-v0.35.0-win64\geckodriver.exe')  # Update to your geckodriver path

# Start the WebDriver for Firefox
driver = webdriver.Firefox(service=service, options=firefox_options)

# Define the URL
url = "https://wbgeprocure-rfxnow.worldbank.org/rfxnow/public/advertisement/index.html;jsessionid=0025193598E6E34458428048B21EBAC9"

# Open the page
driver.get(url)

# Wait for the page to be fully loaded (including JS execution)
WebDriverWait(driver, 20).until(
    lambda d: d.execute_script('return document.readyState') == 'complete'
)

# Optional: Scroll to the bottom to ensure all rows are loaded (if applicable)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)  # Wait for additional rows to load, if necessary

try:
    # Wait until the table is present
    table = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'table'))
    )

    # Print out the number of rows and headers for debugging
    rows = table.find_elements(By.XPATH, ".//tbody/tr")
    print(f"Total rows found: {len(rows)}")

    for i, row in enumerate(rows):  # Iterate over each row
        cells = row.find_elements(By.TAG_NAME, 'td')  # Get all cells for each row
        print(f"Row {i+1} has {len(cells)} cells")

        # Debug output for each cell
        for j, cell in enumerate(cells):
            print(f"Cell {j+1}: {cell.text.strip()}")

        if len(cells) >= 4:  # Ensure there are enough cells
            procurement_number = cells[0].text.strip()
            procurement = cells[1].find_element(By.TAG_NAME, 'a').text.strip() if cells[1].find_elements(By.TAG_NAME, 'a') else cells[1].text.strip()
            publication_date = cells[2].text.strip()
            eoi_deadline = cells[3].text.strip()
            href = cells[1].find_element(By.TAG_NAME, 'a').get_attribute('href') if cells[1].find_elements(By.TAG_NAME, 'a') else 'N/A'

            # Prepare data for MongoDB insertion
            data = {
                'procurement_number': procurement_number,
                'procurement': procurement,
                'publication_date': publication_date,
                'eoi_deadline': eoi_deadline,
                'link': href
            }

            # Insert the data into MongoDB
            collection.insert_one(data)

            # Output the results
            print(f"Procurement Number: {procurement_number}")
            print(f"Procurement: {procurement}")
            print(f"Publication Date: {publication_date}")
            print(f"EOI Deadline: {eoi_deadline}")
            print(f"Link: {href}")
            print('-' * 50)


finally:
    # Only quit after Enter is pressed
    driver.quit()
