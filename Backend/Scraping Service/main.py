import logging
from scrapers.patpat_scraper import scrape_patpat
# from scrapers.ikman_scraper import scrape_ikman

# Set up logging
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more detailed logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraping_service.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    logger.info("Starting the scraping service...")
    try:
        scrape_patpat()
        # scrape_ikman()
        logger.info("Scraping completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()
