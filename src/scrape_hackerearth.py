import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
def scrape_hackerearth():
    url = "https://www.hackerearth.com/challenges/hackathon/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    data = []
    # Find hackathon cards
    outer_div = soup.find("div",class_="layout-container")
    hackathons = outer_div.find_all("a",class_="challenge-card-wrapper challenge-card-link")
    for hackathon in hackathons:
        try:
            name = hackathon.find("span",class_="challenge-list-title challenge-card-wrapper").text.strip()
            link = hackathon["href"]
            theme = ""
            days= hackathon.find("div",id="days")
            if(days==None):
                continue
            response = requests.get(link)
            soup = BeautifulSoup(response.text, "html.parser")
            outer = soup.find("div",class_="hack-phase time-location-specification")
            startdate=outer.find("div",class_="start-time-block")
            enddate=outer.find("div",class_="end-time-block")
            mode = outer.find("div",class_="location-block").find("div",class_="regular bold desc dark").text.strip()
            startdate=startdate.find("div",class_="regular bold desc dark").text.strip()
            enddate=enddate.find("div",class_="regular bold desc dark").text.strip()
            date = startdate+" to "+enddate
            data.append({"name": name, "link": link, "theme": theme, "mode": mode, "date": date})
        except AttributeError:
            continue

    # Define the path for the `data` folder
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of this Python file
    data_dir = os.path.join(current_dir, "../data")           # Relative path to the `data` folder
    os.makedirs(data_dir, exist_ok=True)                     # Create the directory if it doesn't exist

    # Save data as a CSV in the `data` folder
    file_path = os.path.join(data_dir, "hackerearth_hackathons.csv")
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)

scrape_hackerearth()
