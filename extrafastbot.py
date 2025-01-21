import requests
import random
from multiprocessing import Process

# Flask server URL
base_url = "http://localhost:80"  # Replace with the actual URL if hosted remotely

# Load word list from file
def load_word_list(file_path):
    with open(file_path, 'r') as file:
        return [word.strip().lower() for word in file.readlines()]

# Function to submit a guess
def submit_guess(session, guess):
    url = f"{base_url}/student"
    response = session.post(url, data={"guess": guess})
    return response.text

# Function to submit a student's name
def submit_student_name(session, name):
    url = f"{base_url}/student"
    response = session.post(url, data={"name": name})
    return response.text

# Main bot logic
def bot_logic(word_list, player_name, guess_limit=6):
    session = requests.Session()

    # Submit the student's name
    submit_student_name(session, player_name)

    guesses_made = 0
    while guesses_made < guess_limit:
        guess = random.choice(word_list)  # Randomly pick a word from the word list
        print(f"{player_name}: Submitting guess: {guess}")
        result = submit_guess(session, guess)
        print(f"{player_name}: {result}")

        # Check status after each guess
        status_url = f"{base_url}/status"
        status = session.get(status_url).json()
        if status["winner"]:
            print(f"{player_name}: The winner is: {status['winner']}")
            return
        guesses_made += 1

# Run multiple instances of the bot
def run_multiple_bots(num_bots):
    word_list = load_word_list("word_list.txt")
    name_base = "BotPlayer"

    processes = []
    for i in range(num_bots):
        player_name = f"{name_base}_{i}"
        print(f"Starting bot: {player_name}")
        p = Process(target=bot_logic, args=(word_list, player_name))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()  # Wait for all bots to finish

if __name__ == '__main__':
    run_multiple_bots(num_bots=1000)  # Change this number to run more bots
