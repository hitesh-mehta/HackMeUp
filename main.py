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


from flask import Flask, jsonify
from src.scrape_devfolio import scrape_devfolio
from src.scrape_hackerearth import scrape_hackerearth
from src.scrape_hack2skill import scrape_hack2skill
from src.combine_data import combine_data
from src.organize_data import organize_data
from datetime import datetime
import time
import threading

app = Flask(__name__)

# Global variable to store the message
scraper_message = None
message_lock = threading.Lock()

def run_scraper():
    global scraper_message
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

    # Organize data and store the message
    with message_lock:
        scraper_message = organize_data()

@app.route('/run-scraper', methods=['GET'])
def trigger_scraper():
    # Run the scraper in a separate thread to avoid blocking the API
    threading.Thread(target=run_scraper).start()
    return jsonify({"message": "Scraper started!"}), 202

@app.route('/scraper-message', methods=['GET'])
def get_scraper_message():
    with message_lock:
        if scraper_message is not None:
            return jsonify({"message": scraper_message}), 200
        else:
            return jsonify({"message": "Scraping in progress or not yet started."}), 202

def scheduled_scraper():
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

if __name__ == "__main__":
    # Start the scheduled scraper in a separate thread
    threading.Thread(target=scheduled_scraper, daemon=True).start()
    
    # Run the Flask app
    app.run(port=5000)  # You can change the port if needed
