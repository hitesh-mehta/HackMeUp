import pandas as pd
import os

def organize_data():
    # Define the path for the `data` folder
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of this Python file
    data_dir = os.path.join(current_dir, "../data")           # Relative path to the `data` folder
    os.makedirs(data_dir, exist_ok=True)                     # Create the directory if it doesn't exist

    # Save data as a CSV in the `data` folder
    file_path = os.path.join(data_dir, "all_hackathons.csv")
    
    # Load the combined data
    df = pd.read_csv(file_path)

    # Sort by deadline/dates (assumes proper date formatting)
    df = df.sort_values(by="name", ascending=True)

    # Format data for WhatsApp messages
    messages = []
    for index, row in df.iterrows():
        message = f"""
🛠️ **{row['name']}**
📅 Dates: {row['date'].strip()}
🔗 Link: {row['link']}
💻 Mode: {row['mode']}
"""
        if not pd.isnull(row["theme"]):
            message += f"🎨 Theme: {row['theme']}"
        messages.append(message.strip())
    for message in messages:
        print(message)
        print("-----")
    # Return the formatted messages
    return messages
organize_data()