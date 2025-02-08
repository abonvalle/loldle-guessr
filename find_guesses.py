import numpy as np
import pandas as pd
from sklearn.metrics import mutual_info_score

# Load character database (Assumed to be in CSV format)
df = pd.read_csv("populated_champions.csv")

# Convert categorical data into sets (for handling partial matches)
for col in df.columns[1:]:  # Ignore ID column if present
    df[col] = df[col].astype(str).apply(lambda x: set(x.split(";")))

# Function to compute entropy of a dataset
def compute_entropy(data, feature):
    return mutual_info_score(data[feature].astype(str), data.index)

# Function to select the best first move
def get_best_guess(data):
    if data.empty:
        print("No candidates left! Returning None.")
        return None  # Avoid trying to index empty DataFrame

    if len(data) == 1:
        print("Only one candidate left, returning it directly.")
        return data.iloc[0]

    entropy_scores = {
        index: sum(compute_entropy(data, col) for col in data.columns[1:])
        for index in data.index
    }

    if not entropy_scores:  # Check if dictionary is empty
        print("No entropy scores available. Returning None.")
        return None

    best_index = max(entropy_scores, key=entropy_scores.get)
    return data.loc[best_index]  # Use .loc instead of .iloc for safety


# Function to filter candidates based on feedback
def filter_candidates(data, guess, feedback):
    """
    - 'G' (True): Keep only exact matches.
    - 'R' (False): Remove characters with any overlapping values.
    - 'O' (Partial): Keep characters with at least some overlap, but not exact matches.
    """
    mask = np.ones(len(data), dtype=bool)
    
    for i, fb in enumerate(feedback):
        col = data.columns[i + 1]  # Offset by 1 to skip ID
        guess_value = guess[i + 1]  # Offset to match column index
        
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
    print("Best initial guess:", best_guess.values)
    
    remaining_candidates = df.copy()
    
    while len(remaining_candidates) > 1:
        # Get user feedback
        feedback = input("Enter feedback for each property (G=Correct, R=Wrong, O=Partial): ").strip().upper()
        
        if len(feedback) != 7 or any(f not in "GRO" for f in feedback):
            print("Invalid feedback! Enter 7 characters using G, R, O.")
            continue

        # Filter remaining candidates
        remaining_candidates = filter_candidates(remaining_candidates, best_guess.values, feedback)
        
        if remaining_candidates.empty:
            print("No valid candidates left! Please check the feedback entered.")
            break
        elif len(remaining_candidates) == 1:
            print("The character is:", remaining_candidates.iloc[0].values)
            break
        else:
            best_guess = get_best_guess(remaining_candidates)
            print("Next best guess:", best_guess.values)
            print("Remaining candidates: ",remaining_candidates)


if __name__ == "__main__":
    wordle_solver()
