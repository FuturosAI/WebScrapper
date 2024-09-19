import requests
from bs4 import BeautifulSoup

# Define the URL
url = "https://wbgeprocure-rfxnow.worldbank.org/rfxnow/public/advertisement/index.html;jsessionid=0025193598E6E34458428048B21EBAC9"

# Send a request to the page
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table or list that contains the procurement data (This is based on the structure of the page)
    # Modify the class or tag accordingly
    rows = soup.find_all('tr')  # Assuming the data is in table rows
    
    for row in rows[1:]:  # Skipping the header row if it exists
        cells = row.find_all('td')  # Extract each cell
        
        if len(cells) > 4:  # Make sure there are enough columns
            # Extract the data
            procurement_number = cells[0].text.strip()
            procurement = cells[1].text.strip()
            publication_date = cells[2].text.strip()
            eoi_deadline = cells[3].text.strip()
            href = cells[1].find('a')['href'] if cells[1].find('a') else 'N/A'
            
            # Output the results
            print(f"Procurement Number: {procurement_number}")
            print(f"Procurement: {procurement}")
            print(f"Publication Date: {publication_date}")
            print(f"EOI Deadline: {eoi_deadline}")
            print(f"Link: {href}")
            print('-' * 50)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
