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
    files_to_process = all_files # Process all files
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

def generate_random_names_batch(names_by_gender, gender, batch_size=20):
    if gender not in names_by_gender or not names_by_gender[gender]:
        return []
    available_names = names_by_gender[gender]
    if len(available_names) < batch_size:
        return random.sample(available_names, len(available_names)) # Return all if less than batch_size
    return random.sample(available_names, batch_size)

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
            batch_history = [] # Stores lists of names (batches) generated
            current_batch_idx = -1 # Index of the current batch in batch_history (-1 means no batch loaded)
            
            while True:
                if current_gender is None:
                    user_input = input("\nEnter gender (M/F) or 'q' to quit: ").strip().upper()
                else:
                    user_input = input(f"Current gender: {current_gender}. Select names to like (e.g., 1 3 5), 'N' for next, 'B' for back, 'C' to change gender, 'Q' to quit: \n").strip().upper()

                if user_input == 'Q':
                    break

                if current_gender is None: # Only if no gender selected yet
                    if user_input in ['M', 'F']:
                        current_gender = user_input
                        # Initial batch generation when gender is selected
                        current_batch = generate_random_names_batch(baby_names_by_gender, current_gender)
                        if current_batch:
                            batch_history.append(current_batch)
                            current_batch_idx = 0
                            print(f"Names loaded for {current_gender}!")
                            # Display the first batch immediately
                            for i, name in enumerate(batch_history[current_batch_idx]):
                                print(f"{i+1}. {name}")
                            print("\nSelect names to like (e.g., 1 3 5), 'N' for next, 'B' for back, 'C' to change gender, 'Q' to quit: ")
                        else:
                            print(f"No names found for gender '{current_gender}'. Please try another gender or check your data.")
                            current_gender = None # Reset gender if no names
                    else:
                        print("Invalid gender input. Please enter 'M' for Male, 'F' for Female, or 'q' to quit.")
                else: # Gender is already selected
                    # Handle commands for batch navigation and liking
                    if user_input == 'C': # Change gender
                        current_gender = None
                        batch_history = [] # Clear history on gender change
                        current_batch_idx = -1
                    elif user_input == 'N': # Next batch
                        if current_batch_idx < len(batch_history) - 1:
                            current_batch_idx += 1
                        else:
                            # Generate new batch if at the end of history
                            new_batch = generate_random_names_batch(baby_names_by_gender, current_gender)
                            if new_batch:
                                batch_history.append(new_batch)
                                current_batch_idx = len(batch_history) - 1
                            else:
                                print("No more new names to generate for this gender.")
                        
                        if 0 <= current_batch_idx < len(batch_history):
                            print(f"\nDisplaying batch {current_batch_idx + 1}/{len(batch_history)}:")
                            for i, name in enumerate(batch_history[current_batch_idx]):
                                print(f"{i+1}. {name}")
                            print("\nSelect names to like (e.g., 1 3 5), 'N' for next, 'B' for back, 'C' to change gender, 'Q' to quit: ")
                    elif user_input == 'B': # Previous batch
                        if current_batch_idx > 0:
                            current_batch_idx -= 1
                            print(f"\nDisplaying batch {current_batch_idx + 1}/{len(batch_history)}:")
                            for i, name in enumerate(batch_history[current_batch_idx]):
                                print(f"{i+1}. {name}")
                            print("\nSelect names to like (e.g., 1 3 5), 'N' for next, 'B' for back, 'C' to change gender, 'Q' to quit: ")
                        else:
                            print("Already at the first batch.\n")
                    else: # Try to parse as liked names or invalid input
                        try:
                            liked_indices = [int(x) - 1 for x in user_input.split() if x.isdigit()]
                            current_batch = batch_history[current_batch_idx]
                            for idx in liked_indices:
                                if 0 <= idx < len(current_batch):
                                    name_to_like = current_batch[idx]
                                    name_gender_tuple = (name_to_like, current_gender)
                                    if name_gender_tuple not in liked_names:
                                        liked_names.add(name_gender_tuple)
                                        print(f"{name_to_like} added to your liked names.\n")
                                    else:
                                        print(f"{name_to_like} is already in your liked names.\n")
                                else:
                                    print(f"Invalid number: {idx+1}. Please enter valid numbers from the list.\n")
                        except ValueError:
                            print("Invalid input. Please enter numbers to like names, 'N' for next, 'B' for back, 'C' to change gender, or 'Q' to quit.\n")

    print("\nThank you for using the Baby Name Generator!")
    if liked_names:
        print("\n--- Your Liked Names ---")
        
        # Define header strings
        header_name = "Name"
        header_gender = "Gender"
        header_occurrences = "Occurrences"
        header_years = "Years"

        # Dynamically calculate max_name_len and max_occ_len for printing liked names
        max_name_len = max(len(name) for name, _ in liked_names) if liked_names else 0
        max_occ_len = max(len(str(sum(name_occurrences.get((name, gender), {}).values()))) for name, gender in liked_names) if liked_names else 0

        # Print header
        print(f'{header_name:<{max_name_len}}  {header_gender:<6}  {header_occurrences:<{max_occ_len}}  {header_years}')
        print("-" * max_name_len + "  " + "-" * 6 + "  " + "-" * max_occ_len + "  " + "-" * 20)

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