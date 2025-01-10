import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
def scrape_hack2skill():
    url = "https://hack2skill.com/#ongoin-initiatives"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find hackathon cards
    outer_div = soup.find_all("div",class_="container-fluid py-4 position-relative")
    next_div = outer_div[0].find_all("div",class_="d-none d-md-block")
    hackathons = next_div[0].find_all("div",class_="swiper-slide newCard")
    data = []
    count=0
    # print(len(hackathons))
    for hackathon in hackathons:
        try:
            isLive = hackathon.find("a",class_="btn btn-gradient w-100").text.strip()
            if isLive=="Registrations Closed":
                continue
            count+=1
            name = str(hackathon.find("h6").text).strip()
            link = hackathon.find("a",class_="text-link")["href"]
            theme = hackathon.find("p",class_="hack-description").text.strip()
            mode = hackathon.find("span",class_="text-success").text.strip()
            date = hackathon.find("p",class_="last-date").text.strip().replace("\n"," ")  
            date_temp = date.split(": ")
            date = date_temp[1].strip()
            data.append({"name": name, "link": link, "theme": theme, "mode": mode, "date": date})
        except AttributeError:
            continue

    # Define the path for the `data` folder
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of this Python file
    data_dir = os.path.join(current_dir, "../data")           # Relative path to the `data` folder
    os.makedirs(data_dir, exist_ok=True)                     # Create the directory if it doesn't exist

    # Save data as a CSV in the `data` folder
    file_path = os.path.join(data_dir, "hack2skill_hackathons.csv")
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)

scrape_hack2skill()
