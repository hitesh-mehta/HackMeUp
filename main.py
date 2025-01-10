from src.scrape_devfolio import scrape_devfolio
from src.scrape_hackerearth import scrape_hackerearth
from src.scrape_hack2skill import scrape_hack2skill
from src.combine_data import combine_data
from src.organize_data import organize_data
from datetime import datetime
import time
def run_scraper():
    print("Starting hackathon scraper...")

    # Step 1: Scrape data from individual platforms
    print("Scraping Devfolio...")
    scrape_devfolio()

    print("Scraping HackerEarth...")
    scrape_hackerearth()

    print("Scraping Hack2Skill...")
    scrape_hack2skill()

    # Step 2: Combine data
    print("Combining all hackathon data...")
    combine_data()
    print("Hackathon scraping completed!")

    message = organize_data()

if __name__ == "__main__":
    while True:
        # Get the current time
        now = datetime.now()
        
        # Check if the current time is midnight
        if now.hour == 0 and now.minute == 0:
            run_scraper()
            # Sleep for a minute to avoid running multiple times within the same minute
            time.sleep(60)
        else:
            # Sleep for a short time before checking again
            time.sleep(30)


    
