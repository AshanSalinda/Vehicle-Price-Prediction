import scrapy
from utils.logger import info, warn, err
from datetime import datetime, timezone
from urllib.parse import urlparse, parse_qs, urlencode


class WebScraper(scrapy.Spider):
    """Base class for website-specific scrapers"""
    def __init__(self, *args):
        super(WebScraper, self).__init__()
        self.start_urls = [args[0]]
        self.ad_selector = args[1]


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
            current_url = response.url
            query_params = parse_qs(urlparse(current_url).query)
            page_no = int(query_params.get('page', [1])[0] )
            info(f"Scraping page: {page_no}")

            # Extract All Ads links
            ad_links = response.css(f"{self.ad_selector}::attr(href)").getall()

            # Get the vehicle info for each ad
            for index, link in enumerate(ad_links):
                if self.name == "ikman_scraper":
                    link = f"https://ikman.lk{link}"

                yield response.follow(
                    link, 
                    callback=self.process_ads, 
                    errback=self.on_error, 
                    meta={'index': f"{self.name}:{page_no}:{index + 1}"}
                )

            # Handle pagination
            last_page = self.is_last_page(response)
            if not last_page:
                query_params['page'] = page_no + 1
                new_query = urlencode(query_params)
                next_page_url = f"{current_url.split('?')[0]}?{new_query}"

                yield response.follow(
                    next_page_url, 
                    callback=self.scrape, 
                    errback=self.on_error,
                    meta={'index': f"{self.name}:{page_no + 1}:0"}
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
            err(f"{index}\t{url}\n{e}")


    def get_vehicle_info(self, response, vehicle_details):
        """
        get_vehicle_info(response: dict, vehicle_details: dict) -> dict

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
        """
        err(f"{self.name} must implement a own get_vehicle_info method")


    def is_last_page(self, response):
        err(f"{self.name} must implement a own is_last_page method")


