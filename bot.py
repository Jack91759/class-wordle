import requests
import random

# Flask server URL
base_url = "http://localhost:80"  # Replace with the actual URL if hosted remotely

# Load word list from file
def load_word_list(file_path):
    with open(file_path, 'r') as file:
        return [word.strip().lower() for word in file.readlines()]

# Step 1: Submit the student's name
def submit_student_name(session, name):
    url = f"{base_url}/student"
    response = session.post(url, data={"name": name})
    return response.text

# Step 2: Submit a guess
def submit_guess(session, guess):
    url = f"{base_url}/student"
    response = session.post(url, data={"guess": guess})
    return response.text

# Step 3: Check the status of the game (whether a winner exists or not)
def check_status(session):
    url = f"{base_url}/status"
    response = session.get(url)
    return response.json()

# Example bot usage
word_list = load_word_list("word_list.txt")
name_base = "BotPlayer"
guess_limit = 6
player_count = 0

while True:
    # Create a new session for each new player
    session = requests.Session()

    # Update the bot's name to simulate a new player after every 6 guesses
    player_name = f"{name_base}_{player_count}"
    print(f"Submitting student name: {player_name}")
    submit_student_name(session, player_name)

    # Bot makes 6 guesses or until a winner is found
    for guess_number in range(guess_limit):
        guess = random.choice(word_list)  # Randomly pick a word from the word list
        print(f"Submitting guess: {guess}")
        result = submit_guess(session, guess)
        print(result)

        # Check game status after each guess
        status = check_status(session)
        if status["winner"]:
            print(f"The winner is: {status['winner']}")
            break
        else:
            print(f"Guesses so far: {status['guesses']}")

    # If a winner is found, stop the bot
    if status["winner"]:
        break

    # If no winner, increment the player count to simulate a new player and continue
    player_count += 1

print("Game finished.")
