# 🔮 Guess My Number 
A dynamic web game that guesses your secret number (0-9) using a **Binary Tree** decision path. Built with Python (Flask) and a modern, gradient-rich UI.

## 🚀 Setup & Run

### Prerequisites
- Python 3.x installed (check with `python3 --version`)

### Installation
1. Open your terminal.
2. Navigate to this folder:
   ```bash
   cd "guess a number"
   ```
3. Create and activate a virtual environment (recommended for macOS):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Game
1. Start the server:
   ```bash
   python app.py
   ```
2. Open your browser and go to: `http://127.0.0.1:8080`

---

## 🌲 How It Works (The Binary Tree)

The game uses a **Binary Decision Tree** to narrow down the possibilities. 
- **Root Node**: We start at the top asking about properties (e.g., "Is it prime?").
- **Branches**: 
  - If you answer **YES**, we move to the `left` child node.
  - If you answer **NO**, we move to the `right` child node.
- **Leaf Node**: When we reach the bottom of the tree, there are no more questions—only the Answer (your number!).

### The Specific Logic Used:
1. **Prime Check**: Splits numbers into {2,3,5,7} vs {0,1,4,6,8,9}.
2. **Magnitude Check**: Asks if it's `< 5`.
3. **Divisibility**: Checks divisibility by 2, 3, or parity (even/odd) to isolate the final number.

This guarantees we find any number from 0-9 in just a few efficient steps!

---

## 💅 Tech Stack
- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3 (Glassmorphism, CSS Variables), JavaScript (Fetch API)
- **Style**: Gen-Z aesthetic (Gradients, Emojis, Animations)

Enjoy getting your mind read! 🧠✨
