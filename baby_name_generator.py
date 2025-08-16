
import os
import pandas as pd
import random

def load_baby_names(data_folder):
    all_names = []
    for filename in os.listdir(data_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(data_folder, filename)
            # The SSA data typically has columns: Name, Gender, Count (sometimes Year, State)
            # Assuming basic format from web search: Name, Gender, Count
            df = pd.read_csv(file_path, header=None, names=['Name', 'Gender', 'Count'])
            all_names.extend(df['Name'].tolist())
    return all_names

def generate_random_name(names_list):
    if not names_list:
        return "No names loaded. Please check your data folder."
    return random.choice(names_list)

if __name__ == "__main__":
    print("Hello! This application generates random baby names from SSA data.\n")
    print("To use this application, please download the baby name data from the SSA website:")
    print("https://www.ssa.gov/oact//babynames/limits.html")
    print("Extract the content into a folder named 'data' in the same directory as this script.")
    print("\nOnce you have downloaded and extracted the data, run this script again.\n")

    data_folder = 'data'

    if not os.path.exists(data_folder):
        print(f"Error: The '{data_folder}' folder was not found.")
        print("Please create a folder named 'data' and place the SSA CSV files inside it.")
    else:
        baby_names = load_baby_names(data_folder)
        if baby_names:
            print("Names loaded successfully! Press Enter to generate a random name, or type 'q' to quit.")
            while True:
                user_input = input("> ").strip().lower()
                if user_input == 'q':
                    break
                else:
                    random_name = generate_random_name(baby_names)
                    print(f"Random Baby Name: {random_name}")
        else:
            print(f"No CSV files found in the '{data_folder}' folder, or no names could be loaded.")
            print("Please ensure your CSV files are correctly placed and formatted.")

    print("\nThank you for using the Baby Name Generator!")
