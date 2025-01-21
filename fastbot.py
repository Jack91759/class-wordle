import requests
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

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

# Step 3: Check the status of the game
def check_status(session):
    url = f"{base_url}/status"
    response = session.get(url)
    return response.json()

# Main bot logic
def bot_logic(word_list, player_name, guess_limit=6):
    session = requests.Session()
    submit_student_name(session, player_name)

    guesses_made = 0
    while guesses_made < guess_limit:
        # Prepare guess tasks
        guess_tasks = []
        with ThreadPoolExecutor(max_workers=3) as executor:
            for _ in range(min(3, guess_limit - guesses_made)):  # Guess in batches of 3
                guess = random.choice(word_list)
                future = executor.submit(submit_guess, session, guess)
                guess_tasks.append(future)

            # Collect results
            for future in as_completed(guess_tasks):
                result = future.result()
                print(result)

        # Check status after the guesses
        status = check_status(session)
        if status["winner"]:
            print(f"The winner is: {status['winner']}")
            break
        else:
            print(f"Guesses so far: {status['guesses']}")
            guesses_made += len(guess_tasks)

# Run the bot
def run_bot():
    word_list = load_word_list("word_list.txt")
    name_base = "FastBotPlayer"
    player_count = 0

    while True:
        player_name = f"{name_base}_{player_count}"
        print(f"Submitting student name: {player_name}")
        bot_logic(word_list, player_name)

        player_count += 1
        # Check if you want to continue or break the loop based on some condition
        if player_count > 100:  # Example condition to stop after 10 players
            break

    print("Game finished.")

run_bot()
