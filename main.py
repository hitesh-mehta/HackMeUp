# from src.scrape_devfolio import scrape_devfolio
# from src.scrape_hackerearth import scrape_hackerearth
# from src.scrape_hack2skill import scrape_hack2skill
# from src.combine_data import combine_data
# from src.organize_data import organize_data
# from datetime import datetime
# import time
# def run_scraper():
#     print("Starting hackathon scraper...")

#     # Step 1: Scrape data from individual platforms
#     print("Scraping Devfolio...")
#     scrape_devfolio()

#     print("Scraping HackerEarth...")
#     scrape_hackerearth()

#     print("Scraping Hack2Skill...")
#     scrape_hack2skill()

#     # Step 2: Combine data
#     print("Combining all hackathon data...")
#     combine_data()
#     print("Hackathon scraping completed!")

#     message = organize_data()

# if __name__ == "__main__":
#     while True:
#         # Get the current time
#         now = datetime.now()
        
#         # Check if the current time is midnight
#         if now.hour == 0 and now.minute == 0:
#             run_scraper()
#             # Sleep for a minute to avoid running multiple times within the same minute
#             time.sleep(60)
#         else:
#             # Sleep for a short time before checking again
#             time.sleep(30)


from fastapi import FastAPI, HTTPException
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import time
from typing import Dict
from pydantic import BaseModel

# Import your scraping modules
from src.scrape_devfolio import scrape_devfolio
from src.scrape_hackerearth import scrape_hackerearth
from src.scrape_hack2skill import scrape_hack2skill
from src.combine_data import combine_data
from src.organize_data import organize_data

app = FastAPI(title="Hackathon Scraper API")

# Global variable to store the latest scraping result
latest_data = None

class ScrapingResponse(BaseModel):
    last_updated: str
    data: Dict

def run_scraper():
    """Function to run the scraping process"""
    global latest_data
    
    try:
        print(f"Starting hackathon scraper at {datetime.now()}")
        
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
        
        # Step 3: Organize and store the data
        latest_data = {
            "last_updated": datetime.now().isoformat(),
            "data": organize_data()
        }
        
        print("Hackathon scraping completed successfully!")
        
    except Exception as e:
        print(f"Error during scraping: {str(e)}")
        raise e

# Initialize with existing data
try:
    latest_data = {
        "last_updated": datetime.now().isoformat(),
        "data": organize_data()
    }
except Exception as e:
    print(f"Error loading initial data: {str(e)}")
    latest_data = None

# Set up the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(
    run_scraper,
    trigger=CronTrigger(hour=0, minute=0),  # Run at midnight every day
    id='scraper_job',
    name='Daily Hackathon Scraping',
    replace_existing=True
)

@app.on_event("startup")
async def start_scheduler():
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_scheduler():
    scheduler.shutdown()

@app.get("/", response_model=ScrapingResponse)
async def get_hackathon_data():
    """
    Get the latest hackathon data
    """
    if latest_data is None:
        raise HTTPException(status_code=503, detail="Data not yet available")
    return latest_data

@app.post("/trigger-scrape")
async def trigger_manual_scrape():
    """
    Manually trigger the scraping process
    """
    try:
        run_scraper()
        return {"message": "Scraping completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
