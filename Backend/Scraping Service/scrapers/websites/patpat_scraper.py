from utils.logger import info, warn, err
from ..web_scraper import WebScraper
from .site_data import patpat


class PatpatScraper(WebScraper):
    name = "patpat"

    def __init__(self, storage):
        selectors = patpat['selectors']
        url = patpat['url']
        ad_selector = selectors['ads_link']
        self.next_button = selectors['next_button']
        self.title = selectors['title']
        self.price = selectors['price']
        self.rows = selectors['rows']
        self.storage = storage
        super(PatpatScraper, self).__init__(url, ad_selector)


    def is_last_page(self, response):
        try:
            disabled_next_button = response.css(self.next_button).get()
            return disabled_next_button != None
  
        except Exception as e:
            err(f"Failed to check if it is_last_page for {response.url} \n {e}")


    def get_key(self, key):
        keys = {
            'Manufacturer': 'Make',
            'Model': 'Model',
            'Model Year': 'YOM',
            'Transmission': 'Transmission',
            'Engine Capacity': 'Engine Capacity',
            'Fuel Type': 'Fuel Type',
            'Mileage': 'Mileage',
        } 
       
        key = key.strip() if key and type(key) == str else None
        return keys.get(key)


    def get_vehicle_info(self, response, vehicle_details):
        title = response.css(f"{self.title}::text").get()
        price = response.css(f"{self.price}::text").get()
        table = response.css(self.rows)

        if price:
            if price == ': Negotiable':
                raise Exception("Price is negotiable") 
            else:
                vehicle_details['price'] = price.strip()
        else:
            raise Exception("Price not found")


        if title:
            vehicle_details['title'] = title.strip()
        else:
            raise Exception("Title not found")


        for row in table:
            key = self.get_key(row.css('td:nth-child(1)::text').get())
            value = row.css('td:nth-child(2)::text').get()
            if key and value and type(value) == str:
                vehicle_details[key] = value.strip()

        return vehicle_details