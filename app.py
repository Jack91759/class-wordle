from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from threading import Lock
import os
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key


def load_word_list(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Word list file not found: {file_path}")

    with open(file_path, 'r') as file:
        return set(word.strip().lower() for word in file.readlines())


# Game settings
MAX_GUESSES = 6  # Set the maximum number of guesses allowed
TEACHER_PASSWORD = 'Idamiddle'  # Set your desired teacher password
WORD_LIST = load_word_list('word_list.txt')

# Global variables to store game state
word_to_guess = ""
all_guesses = {}
feedback_summary = {}
winner_name = ""
lock = Lock()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/words')
def display_text():
    # Path to the txt file
    with open('word_list.txt', 'r') as file:
        content = file.read()
    return f"<pre>{content}</pre>"


@app.route('/teacher', methods=['GET', 'POST'])
def teacher():
    global word_to_guess, winner_name, all_guesses, feedback_summary

    # Check for password entry
    if 'teacher_logged_in' not in session:
        if request.method == 'POST':
            if request.form.get('password') == TEACHER_PASSWORD:
                session['teacher_logged_in'] = True
                return redirect(url_for('teacher'))
            else:
                return render_template('teacher_password.html', error='Invalid password')

        return render_template('teacher_password.html')

    if request.method == 'POST':
        word_to_guess = request.form.get('word').lower()
        winner_name = ""
        all_guesses = {}
        feedback_summary = {}
        return redirect(url_for('teacher'))

    return render_template('teacher.html', word=word_to_guess, winner=winner_name, feedback_summary=feedback_summary)


@app.route('/random_word')
def random_word():
    global word_to_guess, winner_name, all_guesses, feedback_summary
    # Pick a random word from the word list
    with lock:
        # Check if a variable is a set
        if isinstance(WORD_LIST, set):
            # Convert to list if needed
            WORD_LIST1 = list(WORD_LIST)

        word_to_guess = random.choice(WORD_LIST1)
        winner_name = ""
        all_guesses = {}
        feedback_summary = {}
    return redirect(url_for('teacher'))


@app.route('/student', methods=['GET', 'POST'])
def student():
    global word_to_guess, winner_name, all_guesses, feedback_summary

    if not word_to_guess:
        return "The game has not started yet. Please wait for the teacher to set the word."

    # Check if the student's name is in the session
    if 'student_name' not in session:
        if request.method == 'POST':
            session['student_name'] = request.form.get('name')
            return redirect(url_for('student'))
        return render_template('student_name.html')

    student_name = session['student_name']

    # Prevent guesses if there is already a winner
    if winner_name:
        return render_template('student.html', guesses=all_guesses.get(student_name, []), max_guesses=MAX_GUESSES, winner=winner_name)

    if request.method == 'POST':
        student_guess = request.form.get('guess').lower()

        # Validate the guess against the word list

        if student_guess not in WORD_LIST:
            return f"'{student_guess}' is not a valid word. Please try again."

        if len(student_guess) != len(word_to_guess):
            return "Your guess must be of length " + str(len(word_to_guess))

        # Check if the student has exceeded max guesses
        if student_name in all_guesses and len(all_guesses[student_name]) >= MAX_GUESSES:
            return "You've used all your guesses!"

        # Check the guess against the word
        green_count = yellow_count = gray_count = 0
        # Check the guess against the word
        feedback = []
        for i, char in enumerate(student_guess):
            if char == word_to_guess[i]:
                feedback.append((char, 'correct'))  # Correct letter, correct position
            elif char in word_to_guess:
                feedback.append((char, 'present'))  # Correct letter, wrong position
            else:
                feedback.append((char, 'absent'))  # Incorrect letter

        # print(feedback)  # Should output something like [('a', 'correct'), ('b', 'absent'), ('c', 'present')]
        # print(session)  # This will show the current session data
        # print("Current all_guesses:", all_guesses)  # Check the structure of all_guesses
        # print("Current feedback_summary:", feedback_summary)  # Check the structure of feedback_summary
        # print("Current student_name:", student_name)  # Check the current student name

        # Update the student's guesses
        # Update the student's guesses
        with lock:
            # Ensure the student is present in all_guesses and feedback_summary
            if student_name not in all_guesses:
                all_guesses[student_name] = []  # Initialize an empty list for guesses
                feedback_summary[student_name] = {'greens': 0, 'yellows': 0, 'grays': 0}  # Initialize feedback counts

            # Append the guess and feedback tuple
            all_guesses[student_name].append((student_guess, feedback))

            # Calculate and update feedback summary counts
            green_count = sum(1 for _, status in feedback if status == 'correct')
            yellow_count = sum(1 for _, status in feedback if status == 'present')
            gray_count = sum(1 for _, status in feedback if status == 'absent')

            # Update the feedback summary
            feedback_summary[student_name]['greens'] += green_count
            feedback_summary[student_name]['yellows'] += yellow_count
            feedback_summary[student_name]['grays'] += gray_count

            # Check for the winner
            if student_guess == word_to_guess and not winner_name:
                winner_name = student_name

            print("Updated all_guesses:", all_guesses)  # Check the structure of all_guesses after update
            print("Updated feedback_summary:", feedback_summary)  # Check the structure of feedback_summary after update

        return redirect(url_for('student'))

    # Render the student's guesses
    return render_template('student.html', guesses=all_guesses.get(student_name, []), max_guesses=MAX_GUESSES, winner=winner_name)


@app.route('/status')
def status():
    return jsonify({"guesses": all_guesses, "winner": winner_name, "feedback_summary": feedback_summary})


@app.route('/all_guesses')
def all_guesses():
    return render_template('all_guesses.html', guesses=all_guesses, winner=winner_name, word=word_to_guess)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, ssl_context=('cert.pem', 'key_without_passphrase.pem'))
