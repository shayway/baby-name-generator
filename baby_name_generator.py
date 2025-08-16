
import os
import pandas as pd
import random
from tqdm import tqdm

def load_baby_names(data_folder):
    names_by_gender = {'M': [], 'F': []}
    all_files = [f for f in os.listdir(data_folder) if f.endswith('.txt')]
    all_files.sort() # Ensure consistent order for taking the first 10
    files_to_process = all_files[:10] # Take only the first 10 files
    for filename in tqdm(files_to_process, desc="Loading baby names"):
        file_path = os.path.join(data_folder, filename)
        df = pd.read_csv(file_path, header=None, names=['Name', 'Gender', 'Count'])
        for index, row in df.iterrows():
            gender = row['Gender']
            name = row['Name']
            if gender in names_by_gender:
                names_by_gender[gender].append(name)
    return names_by_gender

def generate_random_name(names_by_gender, gender):
    if gender not in names_by_gender or not names_by_gender[gender]:
        return f"No names loaded for gender '{gender}'. Please check your data folder or gender input."
    return random.choice(names_by_gender[gender])

if __name__ == "__main__":
    data_folder = 'data'

    if not os.path.exists(data_folder):
        print(f"Error: The '{data_folder}' folder was not found.")
        print("Please create a folder named 'data' and place the SSA CSV files inside it.")
    else:
        baby_names_by_gender = load_baby_names(data_folder)
        
        # Check if any names were loaded at all
        if not any(baby_names_by_gender.values()):
            print(f"No CSV files found in the '{data_folder}' folder, or no names could be loaded.")
            print("Please ensure your CSV files are correctly placed and formatted.")
        else:
            current_gender = None
            while True:
                if current_gender is None:
                    user_input = input("\nEnter gender (M/F) or 'q' to quit: ").strip().upper()
                else:
                    user_input = input(f"Current gender: {current_gender}. Press Enter to generate, or type 'c' to change gender, 'q' to quit: ").strip().upper()

                if user_input == 'Q':
                    break

                if current_gender is None: # Only if no gender selected yet
                    if user_input in ['M', 'F']:
                        current_gender = user_input
                        selected_names = baby_names_by_gender[current_gender]
                        if not selected_names:
                            print(f"No names found for gender '{current_gender}'. Please try another gender or check your data.")
                            current_gender = None # Reset gender if no names
                    else:
                        print("Invalid gender input. Please enter 'M' for Male, 'F' for Female, or 'q' to quit.")
                else: # Gender is already selected
                    if user_input == 'C': # Change gender
                        current_gender = None
                    elif user_input == '': # Generate name
                        random_name = generate_random_name(baby_names_by_gender, current_gender)
                        print(f"Random Baby Name: {random_name}\n")
                    else:
                        print("Invalid input. Press Enter to generate, 'c' to change gender, or 'q' to quit.")

    print("\nThank you for using the Baby Name Generator!")
