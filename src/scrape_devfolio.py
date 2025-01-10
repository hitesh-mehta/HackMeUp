import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
def scrape_devfolio():
    url = "https://devfolio.co/hackathons"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find hackathon cards
    outer_div = soup.find_all("div",id="__next")
    inner1_div = outer_div[0].find_all("div",class_="sc-edUIhV sc-cSFexR bFqggl czaYVc")
    inner1_section = inner1_div[0].find_all("section",class_="sc-bWijRQ tIsSH")
    hackathons = (inner1_section[0]).find_all("div",class_="sc-fmGnzW iXcaew CompactHackathonCard__StyledCard-sc-9ff45231-0 fudhHJ")
    data = []
    for hackathon in hackathons:
        try:
            name = str(hackathon.find("h3",class_="sc-hZgfyJ oSdsf")).strip().split(">")[1].split("<")[0]
            link = hackathon.find("a",class_="Link__LinkBase-sc-e5d23d99-0 bnxtME")["href"]
            theme = hackathon.find_all("p",class_="sc-hZgfyJ hZQPen")[1].text.strip()
            mode = hackathon.find_all("p",class_="sc-hZgfyJ ifkmYk")[0].text.strip()
            date = hackathon.find_all("p",class_="sc-hZgfyJ ifkmYk")[2].text.strip()
            data.append({"name": name, "link": link, "theme": theme, "mode": mode, "date": date})
        except AttributeError:
            continue

    # Define the path for the `data` folder
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of this Python file
    data_dir = os.path.join(current_dir, "../data")           # Relative path to the `data` folder
    os.makedirs(data_dir, exist_ok=True)                     # Create the directory if it doesn't exist

    # Save data as a CSV in the `data` folder
    file_path = os.path.join(data_dir, "devfolio_hackathons.csv")
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)

scrape_devfolio()
