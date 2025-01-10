from src.scrape_devfolio import scrape_devfolio
from src.scrape_hackerearth import scrape_hackerearth
from src.scrape_hack2skill import scrape_hack2skill
from src.combine_data import combine_data
from src.organize_data import organize_data
import pywhatkit as kit


if __name__ == "__main__":
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


    
