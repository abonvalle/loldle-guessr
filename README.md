# Loldle Game Solver

This project is a Python-based solver specifically designed for **Loldle.net**. The game requires players to guess a League of Legends character daily based on seven properties. Each guess receives feedback indicating whether each property is **correct (G)**, **incorrect (R)**, **partially correct (O)**, or for the year, **lower (L) / higher (H)**.

## Features

- Algorithm that determine the best guess by maximizing the number of eliminated possibilities.
- Dynamically filters remaining candidates based on game feedback.
- Allows users to iteratively enter feedback until the correct character is found.

## Installation & Setup

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/abonvalle/loldle-solver.git
cd loldle-solver
```

### 2️⃣ Create & Activate a Virtual Environment

```sh
python3 -m venv venv
source ./venv/bin/activate
```

### 3️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

## Running the Solver

To start the program, run:

```sh
python3 find_guesses.py
```

The script will suggest the best initial guess and prompt you to enter feedback after each guess.

## How to Play

1. Run the script and use the suggested first guess.
2. Enter the feedback for each property:
   - **G** → Correct.
   - **R** → Incorrect.
   - **O** → Partially correct (e.g., Color = Red, but actual character has Red & Blue).
   - **L** → Year is **lower** than guessed.
   - **H** → Year is **higher** than guessed.
3. The script will suggest the next best guess.
4. Repeat until the correct character is found!

## Example Run

```
Best initial guess: Zilean
Enter feedback: RROGRRH
Candidates left after filtering: 9
Next best guess: Vi
GRGGGRG
The character is: Fiora
```

## About Loldle.net

This tool is designed to assist players in the **Loldle Classic mode** available at:
🔗 [Loldle.net](https://loldle.net/classic)

> **Disclaimer**: This is an independent project and is not affiliated with Riot Games or Loldle.net.

## License

This project is licensed under the **MIT License**.

---

### 🚀 Happy Guessing! 🎮
