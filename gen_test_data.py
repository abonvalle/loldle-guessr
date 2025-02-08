import pandas as pd
import random

# Define possible values for each property
properties = {
    "Color": ["Red", "Blue", "Green", "Yellow", "Black", "White"],
    "Size": ["Small", "Medium", "Large"],
    "Shape": ["Circle", "Square", "Triangle", "Hexagon", "Pentagon"],
    "Material": ["Metal", "Plastic", "Wood", "Glass", "Fabric"],
    "Weight": ["Light", "Heavy"],
    "Finish": ["Shiny", "Matte"],
    "Rarity": ["Common", "Uncommon", "Rare"]
}

# Function to generate random character data
def generate_character_data(num_characters=100):
    data = []
    for i in range(1, num_characters + 1):
        character = {
            "ID": i,
            "Color": random.choice(properties["Color"]),
            "Size": random.choice(properties["Size"]),
            "Shape": random.choice(properties["Shape"]),
            "Material": random.choice(properties["Material"]),
            "Weight": random.choice(properties["Weight"]),
            "Finish": random.choice(properties["Finish"]),
            "Rarity": random.choice(properties["Rarity"]),
        }
        data.append(character)
    return data

# Generate 100 random characters
num_entries = 100  # Change this to generate more or fewer entries
characters = generate_character_data(num_entries)

# Convert to Pandas DataFrame
df = pd.DataFrame(characters)

# Save to CSV
csv_filename = "characters_db.csv"
df.to_csv(csv_filename, index=False)

print(f"CSV file '{csv_filename}' generated successfully with {num_entries} entries.")
