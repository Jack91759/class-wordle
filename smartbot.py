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

# Step 4: Filter the word list based on feedback
def filter_word_list(word_list, feedback, guess):
    filtered_words = []

    for word in word_list:
        valid_word = True

        for i, (letter, status) in enumerate(feedback):
            if status == "correct" and word[i] != letter:
                valid_word = False
                break
            if status == "present" and (letter not in word or word[i] == letter):
                valid_word = False
                break
            if status == "absent" and letter in word:
                valid_word = False
                break

        if valid_word:
            filtered_words.append(word)

    return filtered_words

# Example bot usage
word_list = load_word_list("word_list.txt")
name_base = "SmartBotPlayer"
guess_limit = 6
player_count = 0

while True:
    # Create a new session for each new player
    session = requests.Session()

    # Update the bot's name to simulate a new player after every 6 guesses
    player_name = f"{name_base}_{player_count}"
    print(f"Submitting student name: {player_name}")
    submit_student_name(session, player_name)

    # Initialize the remaining word list and start guessing
    remaining_words = word_list[:]
    for guess_number in range(guess_limit):
        # Pick a word from the remaining word list (random for the first guess, then filtered)
        guess = random.choice(remaining_words)
        print(f"Submitting guess: {guess}")
        result = submit_guess(session, guess)

        # Check game status after each guess
        status = check_status(session)
        if status["winner"]:
            print(f"The winner is: {status['winner']}")
            break
        else:
            guesses = status["guesses"].get(player_name, [])
            if guesses:
                # Get feedback from the latest guess
                latest_guess, feedback = guesses[-1]

                # Filter the word list based on feedback
                remaining_words = filter_word_list(remaining_words, feedback, latest_guess)
                print(f"Remaining possible words: {len(remaining_words)}")

    # If a winner is found, stop the bot
    if status["winner"]:
        break

    # If no winner, increment the player count to simulate a new player and continue
    player_count += 1

print("Game finished.")
