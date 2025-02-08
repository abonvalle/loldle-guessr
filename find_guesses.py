import numpy as np
import pandas as pd
from collections import defaultdict

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Load character database (Assumed to be in CSV format)
df = pd.read_csv("populated_champions.csv")

# Convert categorical data into sets (for handling partial matches)
for col in df.columns[1:-1]:  # Ignore Champ name column if present
    df[col] = df[col].astype(str).apply(lambda x: set(x.split(";")))

# Ensure Year is treated as an integer
df["Release year"] = df["Release year"].astype(int)

def compute_elimination_score(data, test_guess):
    """
    Calculates how many characters each test_guess would eliminate
    based on the feedback it would generate against all other characters.
    """
    feedback_patterns = defaultdict(int)

    for _, target in data.iterrows():
        if (test_guess == target).all():
            continue  # Skip if comparing with itself

        feedback = []
        for col in data.columns[1:]:  # Skip Champ name
            guess_value = test_guess[col]
            target_value = target[col]

            if col == "Year":
                if guess_value == target_value:
                    feedback.append("G")
                elif guess_value < target_value:
                    feedback.append("H")  # Guess is lower → actual is greater
                else:
                    feedback.append("L")  # Guess is greater → actual is lower
            else:
                if guess_value == target_value:
                    feedback.append("G")
                elif guess_value & target_value:  # Overlapping sets
                    feedback.append("O")
                else:
                    feedback.append("R")

        feedback_tuple = tuple(feedback)
        feedback_patterns[feedback_tuple] += 1

    # The score is how many candidates are eliminated on average
    total_tests = len(data) - 1  # Exclude itself
    avg_elimination = sum(total_tests - count for count in feedback_patterns.values()) / total_tests

    return avg_elimination

def get_best_guess(data):
    """
    Selects the best first guess by evaluating which character 
    has the highest elimination potential.
    """
    if data.empty:
        print("No candidates available!")
        return None

    best_guess = None
    best_score = -1

    for index, row in data.iterrows():
        score = compute_elimination_score(data, row)
        if score > best_score:
            best_score = score
            best_guess = row

    # print(f"Best initial guess chosen with elimination score: {best_score:.2f}")
    return best_guess

# Function to filter candidates based on feedback
def filter_candidates(data, guess, feedback):
    """
    - 'G' (True): Keep only exact matches.
    - 'R' (False): Remove characters with any overlapping values.
    - 'O' (Partial): Keep characters with at least some overlap, but not exact matches.
    - 'L' (Lower) / 'H' (Higher): Only for Year property, filter accordingly.
    """
    mask = np.ones(len(data), dtype=bool)
    
    for i, fb in enumerate(feedback):
        col = data.columns[i + 1]  # Offset by 1 to skip Champ name
        guess_value = guess[i + 1]  # Offset to match column index
        
        if col == "Year":  # Special handling for Year
            if fb == "G":
                mask &= data[col] == guess_value
            elif fb == "L":
                mask &= data[col] < guess_value
            elif fb == "H":
                mask &= data[col] > guess_value
        
        else:  # Normal filtering for other properties
            if fb == "G":
                mask &= data[col] == guess_value  # Exact match required
            elif fb == "R":
                mask &= ~data[col].apply(lambda x: bool(x & guess_value))  # No overlap
            elif fb == "O":
                mask &= data[col].apply(lambda x: bool(x & guess_value) and x != guess_value)  # Some overlap, but not exact
            
    return data[mask]

# Main game loop
def wordle_solver():
    print("Starting Wordle Solver...")
    
    # First move
    best_guess = get_best_guess(df)
    print(f"Best initial guess: {bcolors.WARNING}{bcolors.BOLD}{best_guess.values[0]}{bcolors.ENDC}")
    
    remaining_candidates = df.copy()
    
    while len(remaining_candidates) > 1:
        # Get user feedback
        feedback = input(f"Enter feedback for each property ({bcolors.BOLD}{bcolors.OKGREEN}G{bcolors.ENDC}=Correct, {bcolors.BOLD}{bcolors.FAIL}R{bcolors.ENDC}=Wrong, {bcolors.BOLD}{bcolors.WARNING}O{bcolors.ENDC}=Partial, {bcolors.BOLD}{bcolors.HEADER}L{bcolors.ENDC}=Lower (only for year), {bcolors.BOLD}{bcolors.HEADER}H{bcolors.ENDC}=Higher (only for year)): \n").strip().upper()
        
        if len(feedback) != 7 or any(f not in "GRO" for f in feedback[:-1]) or feedback[-1] not in "GRLH" :
            print(f"{bcolors.WARNING}Invalid feedback!{bcolors.ENDC} Enter 6 characters using {bcolors.BOLD}{bcolors.OKGREEN}G{bcolors.ENDC}, {bcolors.BOLD}{bcolors.FAIL}R{bcolors.ENDC}, {bcolors.BOLD}{bcolors.WARNING}O{bcolors.ENDC} and 1 using {bcolors.BOLD}{bcolors.HEADER}L{bcolors.ENDC}, {bcolors.BOLD}{bcolors.HEADER}H{bcolors.ENDC}{bcolors.ENDC}.{bcolors.ENDC}")
            continue

        # Filter remaining candidates
        remaining_candidates = filter_candidates(remaining_candidates, best_guess.values, feedback)
        
        if remaining_candidates.empty:
            print(f"{bcolors.BOLD}{bcolors.FAIL}No valid candidates left! Please check the feedback entered.{bcolors.ENDC}")
            break
        elif len(remaining_candidates) == 1:
            print(f"\nThe character is: {bcolors.OKGREEN}{bcolors.BOLD}{remaining_candidates.iloc[0].values[0]}{bcolors.ENDC}\n\n")
            break
        else:
            best_guess = get_best_guess(remaining_candidates)
            print(f"Next best guess: {bcolors.WARNING}{bcolors.BOLD}{best_guess.values[0]}{bcolors.ENDC}")
            print(f"Remaining candidates: {bcolors.OKCYAN}{bcolors.BOLD}{', '.join(remaining_candidates.iloc[:, 0].astype(str))}{bcolors.ENDC}")


if __name__ == "__main__":
    wordle_solver()


