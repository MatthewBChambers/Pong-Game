# Pong Game

A classic Pong game implementation using Pygame, with web browser support through Pygbag.

## Features

- Classic two-player Pong gameplay
- Score tracking
- Increasing ball speed during rallies
- Web browser support
- Sound effects

## Installation

1. Clone this repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the Game

### Desktop Version
Run the game locally:
```bash
python main.py
```

### Web Version
Run the game in a web browser:
```bash
python -m pygbag main.py
```
Then open your web browser and navigate to `http://localhost:8000`

## Controls

- **Player 1 (Left):**
  - W: Move Up
  - S: Move Down

- **Player 2 (Right):**
  - ↑ (Up Arrow): Move Up
  - ↓ (Down Arrow): Move Down

- **Other Controls:**
  - R: Reset Game
  - ESC: Quit Game

## Requirements

- Python 3.x
- Pygame 2.5.2
- Pygbag 0.7.1 (for web version) 