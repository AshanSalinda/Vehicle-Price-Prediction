import logging
from bs4 import BeautifulSoup
import requests

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def scrape_ikman():
    url = 'https://ikman.lk/en/ad/nissan-sunny-sb14-1998-for-sale-colombo'
    price_container_class = 'amount--3NTpl'
    details_container_class = 'ad-meta--17Bqm'
    label_div_class = 'word-break--2nyVq label--3oVZK'
    value_div_class = 'word-break--2nyVq value--1lKHt'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Initialize vehicle details dictionary
        vehicle_details = {}

        # Extract vehicle price
        price_container = soup.find('div', class_ = price_container_class)
        if price_container:
           vehicle_details['price'] = price_container.get_text(strip=True)
        else:
            logger.warning("Price not found")

        # Find the details container
        details_container = soup.find('div', class_ = details_container_class )
        if details_container:
            # Iterate over each detail row
            detail_rows = details_container.find_all('div', class_='full-width--XovDn')
            for row in detail_rows:
                label_div = row.find('div', class_ = label_div_class)
                value_div = row.find('div', class_= value_div_class)
                if label_div and value_div:
                    label = label_div.get_text(strip=True).replace(':', '')
                    # Handle cases where the value is wrapped in another tag
                    value = value_div.get_text(strip=True)
                    vehicle_details[label] = value
        else:
            logger.warning("Details table not found")

        # Print extracted details
        if vehicle_details:
            for key, value in vehicle_details.items():
                print(f"{key}: {value}")
        else:
            logger.info("No vehicle details found")

    except requests.RequestException as e:
        logger.error(f"Request failed: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"An error occurred during scraping: {e}", exc_info=True)

if __name__ == '__main__':
    scrape_ikman()
