import os
import pandas as pd

def combine_data():
    # Define the path to the `data` folder
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of this Python file
    data_dir = os.path.join(current_dir, "../data")           # Relative path to the `data` folder

    # Load data from individual files
    devfolio_path = os.path.join(data_dir, "devfolio_hackathons.csv")
    hackerearth_path = os.path.join(data_dir, "hackerearth_hackathons.csv")
    hack2skill_path = os.path.join(data_dir, "hack2skill_hackathons.csv")
    
    devfolio = pd.read_csv(devfolio_path)
    hackerearth = pd.read_csv(hackerearth_path)
    hack2skill = pd.read_csv(hack2skill_path)

    # Combine into a single DataFrame
    combined = pd.concat([devfolio, hackerearth, hack2skill], ignore_index=True)
    
    # Save combined data
    combined_path = os.path.join(data_dir, "all_hackathons.csv")
    combined.to_csv(combined_path, index=False)

combine_data()
