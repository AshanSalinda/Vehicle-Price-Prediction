import scrapy
from utils.logger import info, warn, err
from datetime import datetime, timezone
from urllib.parse import urlparse, parse_qs, urlencode
from .storage import Storage


class WebScraper(scrapy.Spider):
    """Base class for website-specific scrapers"""
    def __init__(self, *args):
        super(WebScraper, self).__init__()
        self.start_urls = [f"{args[0]}?page={args[1]}"]
        self.ad_selector = args[2]
        self.ad_links = set()
        self.page_no = args[1]
        self.storage = Storage()


    def start_requests(self):
        """Called when the spider starts crawling"""
        for url in self.start_urls:
            yield scrapy.Request(
                url, 
                callback=self.scrape, 
                errback=self.on_error, 
                meta={'index': f"{self.name}:1:0"}
            )

    
    def on_error(self, failure):
        """Handle request errors"""
        url = failure.request.url
        index = failure.request.meta.get('index', 'None:0:0')
        err(f"{index}\t{url}")
        print(failure)


    def scrape(self, response):
        """This is the default callback for every request for pages, made by the spider"""
        try:
            # current_url = response.url
            # query_params = parse_qs(urlparse(current_url).query)
            # page_no = int(query_params.get('page', [1])[0] )
            # info(f"Scraping page: {page_no}")

            # Extract All Ad's links
            new_ad_links = response.css(f"{self.ad_selector}::attr(href)").getall()
            self.ad_links.update(new_ad_links)

            print("url", response.url)
            print("new Ads: ", len(new_ad_links))
            print("Total Ads:", len(self.ad_links))

            # Get the vehicle info for each ad
            # for index, link in enumerate(ad_links):
            #     if self.name == "ikman_scraper":
            #         link = f"https://ikman.lk{link}"

            #     yield response.follow(
            #         link, 
            #         callback=self.process_ads, 
            #         errback=self.on_error, 
            #         meta={'index': f"{self.name}:{page_no}:{index + 1}"}
            #     )

            # Handle pagination
            last_page = self.is_last_page(response)
            if not last_page:
                # query_params['page'] = page_no + 1
                # new_query = urlencode(query_params)
                # next_page_url = f"{current_url.split('?')[0]}?{new_query}"
                self.page_no += 1
                next_page_url = f"{(response.url).split('?page=')[0]}?page={self.page_no}"


                yield response.follow(
                    next_page_url, 
                    callback=self.scrape, 
                    errback=self.on_error,
                    meta={'index': f"{self.name}:{self.page_no}:0"}
                )

            else:
                for index, link in enumerate(self.ad_links):
                    if self.name == "ikman_scraper":
                        link = f"https://ikman.lk{link}"

                    yield response.follow(
                        link, 
                        callback=self.process_ads, 
                        errback=self.on_error, 
                        meta={'index': f"{self.name}:{self.page_no}:{index + 1}"}
                    )
        
        except Exception as e:
            err(f"An error occurred during scraping: {e}")


    def process_ads(self, response):
        try:
            url = response.url
            index = response.meta.get('index')
            vehicle_details = self.get_vehicle_info(response, {'url': url, 'index': index})
            self.storage.add(vehicle_details)
            print(f"{index}\t{url}")
        
        except Exception as e:
            # err(f"{index}\t{url}\n{e}")
            pass

    
    def get_key(self, key):
        keys = {
            'Brand:': 'Make',
            'Manufacturer': 'Make',
            'Make': 'Make',
            'Model:': 'Model',
            'Model': 'Model',
            'Year of Manufacture:': 'YOM',
            'Model Year': 'YOM',
            'YOM': 'YOM',
            'Transmission:': 'Transmission',
            'Transmission': 'Transmission',
            'Gear': 'Transmission',
            'Engine capacity:': 'Engine Capacity',
            'Engine Capacity': 'Engine Capacity',
            'Engine (cc)': 'Engine Capacity',
            'Fuel type:': 'Fuel type',
            'Fuel Type': 'Fuel Type',
            'Mileage:': 'Mileage',
            'Mileage': 'Mileage',
            'Mileage (km)': 'Mileage',
        } 

        key = key.strip() if key and type(key) == str else None
        return keys.get(key)


    def get_vehicle_info(self, response, vehicle_details):
        """
        get_vehicle_info(self, response: scrapy.http.Response, vehicle_details: dict) -> dict

        Extracts vehicle information from the provided response object and return the updated vehicle_details dictionary.

        Args:
            response: The HTTP response containing the webpage's content for a vehicle ad.
            vehicle_details: A dictionary to store extracted vehicle information 

        Returns:
            dict: Updated vehicle_details dictionary containing the extracted data.
            {   
                url: Provided,
                index: Provided,
                Price: Must Include,
                Title: Must Include,
                Make: Must Include,
                Model: Must Include,
                YOM: Must Include,
                Transmission: Must Include,
                Engine Capacity: Must Include,
                Fuel type: Must Include,
                Mileage: Must Include,
            }

        Raises:
            No need to handle any exceptions here.
        """
        err(f"{self.name} must implement a own get_vehicle_info method")


    def is_last_page(self, response):
        """
        is_last_page(self, response: scrapy.http.Response) -> bool

        Checks if the current page is the last page by looking for the pagination element 
        in the given response object.

        Args:
            response: The HTTP response object containing the content of the webpage.

        Returns:
            bool: True if  it's the last page; False otherwise.

        Raises:
            Exception: If an error occurs during the check, logs an error message with 
            this format.
            (f"Failed to check if it is_last_page for {response.url} \n {e}")
        """
        err(f"{self.name} must implement a own is_last_page method")


