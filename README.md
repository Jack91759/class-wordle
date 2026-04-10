# Class Wordle 🎓

A customizable Wordle-style game designed for classroom or personal use.
Guess the hidden word within a limited number of attempts using logic and deduction!

---
## Give it a Try

You can try my game at ([https://classwordle.pythonanywhere.com/][2]). This is a live demo so it may have other people playing while you check it out.

---

## 📌 Features

* Classic Wordle gameplay (color-coded feedback)
* Custom word lists (great for classes or themed games)
* Simple and lightweight implementation
* Easy to modify and extend

---

## 🎮 How to Play

1. Enter a valid word guess.
2. After each guess, you'll receive feedback:

   * 🟩 **Green**: Correct letter in the correct position
   * 🟨 **Yellow**: Correct letter in the wrong position
   * ⬜ **Gray**: Letter is not in the word
3. Use the clues to guess the correct word within the allowed number of tries.

Wordle-style games rely on iterative guessing and feedback to narrow down possibilities.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Jack91759/class-wordle.git
cd class-wordle
```

### 2. Install dependencies

*(Modify this section depending on your project)*

```bash
pip install -r requirements.txt
```

---

### 3. Run the project

```bash
python app.py
```

---

## 🛠️ Configuration

You can customize the game by:

* Editing the word list file
* Changing word length
* Adjusting number of guesses
* Modifying UI or logic

This makes it ideal for:

* Classroom vocabulary practice
* Themed word games
* Programming exercises

---

## 📂 Project Structure

```
class-wordle/
│── templates/           # HTML Files
│── main.*          # Entry point
│── README.md
```

*(Adjust this section to match your actual repo structure.)*

---

## 🧠 How It Works

The game compares each guess to the target word and assigns feedback based on:

* Correct letter + correct position → green
* Correct letter + wrong position → yellow
* Not in word → gray

This logic is similar to Mastermind-style deduction games.

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch
3. Make your changes
4. Submit a pull request

---

## 📜 License

This project is open source.

---

## 🙌 Acknowledgements

Inspired by the original Wordle game and its many open-source adaptations.

---

## 📧 Contact

Created by ([**Hack37 Studios**][1])
Feel free to reach out or open an issue for suggestions or bugs!

[1]: https://hack37studios.pythonanywhere.com/
[2]: https://classwordle.pythonanywhere.com/
