# baby-name-generator
Generates random baby names based off of the Social Security Administration's National Data set

## How it Works

This application generates random baby names from historical U.S. Social Security Administration (SSA) data.

### Features:

*   **Gender Selection**: Generate names for a specific gender (M/F).
*   **Name Generation**: Press Enter for a new random name.
*   **Like Names**: Save favorite names by pressing 'L'.
*   **Change Gender**: Type 'c' to switch gender.
*   **Liked Names Summary**: View a list of liked names, their total occurrences, and most popular years upon quitting.
*   **Easy Exit**: Type 'q' to quit at any time.

### Setup and Usage:

1.  **Get Data**: Download `.txt` baby name data files from the [SSA website](https://www.ssa.gov/oact//babynames/limits.html) and place them in a `data` folder next to the script.
2.  **Install**: Run `pip3 install -r requirements.txt`.
3.  **Run**: Execute `python3 baby_name_generator.py`.

**Interaction:** Follow prompts. Enter/L/c/q for actions.
