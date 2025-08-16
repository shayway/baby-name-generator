
import os
import pandas as pd
import random
from tqdm import tqdm

def load_baby_names(data_folder):
    names_by_gender = {'M': [], 'F': []}
    # Change name_occurrences to store occurrences per year
    name_occurrences = {} # {(name, gender): {year: count}}
    all_files = [f for f in os.listdir(data_folder) if f.endswith('.txt')]
    all_files.sort() # Ensure consistent order for taking the first 10
    files_to_process = all_files[:25] # Take only the first 25 files
    for filename in tqdm(files_to_process, desc="Loading baby names"):
        file_path = os.path.join(data_folder, filename)
        year = int(filename[3:7]) # Extract year from filename (e.g., 'yob1880.txt' -> 1880)
        df = pd.read_csv(file_path, header=None, names=['Name', 'Gender', 'Count'])
        for index, row in df.iterrows():
            gender = row['Gender']
            name = row['Name']
            count = row['Count']
            if gender in names_by_gender:
                names_by_gender[gender].append(name)
            
            # Aggregate occurrences by year
            key = (name, gender)
            if key not in name_occurrences:
                name_occurrences[key] = {}
            name_occurrences[key][year] = name_occurrences[key].get(year, 0) + count

    return names_by_gender, name_occurrences

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
        baby_names_by_gender, name_occurrences = load_baby_names(data_folder)
        
        # Check if any names were loaded at all
        if not any(baby_names_by_gender.values()):
            print(f"No CSV files found in the '{data_folder}' folder, or no names could be loaded.")
            print("Please ensure your CSV files are correctly placed and formatted.")
        else:
            liked_names = set() # Change to a set for unique names
            current_gender = None
            last_generated_name = None # Initialize last_generated_name
            while True:
                if current_gender is None:
                    user_input = input("\nEnter gender (M/F) or 'q' to quit: ").strip().upper()
                else:
                    like_option_text = ""
                    if last_generated_name and (last_generated_name, current_gender) not in liked_names:
                        like_option_text = f"'L' to like {last_generated_name}, "
                    user_input = input(f"Current gender: {current_gender}. Press Enter for new name, {like_option_text}'c' to change gender, 'q' to quit: \n").strip().upper()

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
                    elif user_input == 'L': # Like the last generated name
                        if last_generated_name:
                            name_gender_tuple = (last_generated_name, current_gender)
                            if name_gender_tuple not in liked_names:
                                liked_names.add(name_gender_tuple)
                                print(f"{last_generated_name} added to your liked names.\n")
                            else:
                                print(f"{last_generated_name} is already in your liked names.\n")
                        else:
                            print("No name generated yet to like.")
                    elif user_input == '': # Generate name on Enter
                        random_name = generate_random_name(baby_names_by_gender, current_gender)
                        print(f"Random Baby Name: {random_name}\n")
                        last_generated_name = random_name # Update last_generated_name
                    else:
                        print("Invalid input. Press Enter for new name, 'L' to like, 'c' to change gender, or 'q' to quit.")

    print("\nThank you for using the Baby Name Generator!")
    if liked_names:
        print("\n--- Your Liked Names ---")
        
        # Determine max widths for columns for better alignment
        # max_name_len = max(len(name) for name, _ in liked_names) if liked_names else 0
        # max_occ_len = max(len(str(sum(name_occurrences.get((name, gender), {}).values()))) for name, gender in liked_names) if liked_names else 0
        
        # Define header strings
        header_name = "Name"
        header_gender = "Gender"
        header_occurrences = "Occurrences"
        header_years = "Years"

        # Print header
        # print(f'{header_name:<{max_name_len}}  {header_gender:<6}  {header_occurrences:<{max_occ_len}}  {header_years}')
        # print("-" * max_name_len + "  " + "-" * 6 + "  " + "-" * max_occ_len + "  " + "-" * 5)

        for name, gender in sorted(list(liked_names)): # Convert back to list for sorting and printing
            # Calculate total occurrences by summing yearly data
            yearly_data_for_name = name_occurrences.get((name, gender), {})
            occurrences = sum(yearly_data_for_name.values())
            # Find the year(s) with the most occurrences for this name and gender
            yearly_data = name_occurrences.get((name, gender))
            most_popular_years = []
            if yearly_data:
                max_occurrence = 0
                for year, count in yearly_data.items():
                    if count > max_occurrence:
                        max_occurrence = count
                        most_popular_years = [str(year)]
                    elif count == max_occurrence:
                        most_popular_years.append(str(year))
                
            years_str = ", ".join(sorted(most_popular_years)[:3]) + ("..." if len(most_popular_years) > 3 else "") if most_popular_years else "N/A"
            print(f"{name}, {gender}, {occurrences} occurrences, Most popular in: {years_str}")
        print("----------------------")
