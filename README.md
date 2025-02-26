Untangle Remake
A Python-based remake of the classic puzzle game Untangle originally created by Simon Tatham.

Overview
Untangle Remake challenges you to rearrange a network of interconnected nodes so that no lines cross. With every game, a new puzzle is randomly generated, testing your spatial reasoning and problem-solving skills. Enjoy smooth animations, progress tracking, and secure save/load functionality as you work to clear the tangled network.

Features
Dynamic Puzzle Generation:
Randomly generate nodes and connections to create a unique puzzle every time.

Interactive Gameplay:
Drag-and-drop nodes to reposition them. Selected nodes are highlighted, and overlapping lines can be visually marked for assistance.

Progress Tracking:
A built-in timer and progress bar display the elapsed time and how close you are to solving the puzzle.

Save & Load:
Securely save your game state with encryption (using Fernet from the cryptography package) and resume later.

Full-Screen Experience:
Designed to run in full-screen mode, offering an immersive gaming experience.

Adjustable Difficulty:
Customize the number of nodes to increase or decrease the puzzle’s difficulty.

Getting Started
Prerequisites
Ensure you have Python 3 installed. Additionally, install the following Python packages:
Pygame
Cryptography

New Game:
Click the New Game button to start a fresh puzzle. You can also enter a custom number in the input box to set a specific node count.

Drag & Drop:
Click on a node to select and drag it around the screen. Release the mouse button to drop it in a new position.

Peek Knots:
Toggle the Peek Knots button to highlight overlapping connections, making it easier to spot conflicts.

Save/Load Game:
Use the Save Game button to store your current progress (saved in an encrypted file), and the Load Game button to resume your previous session.

Objective:
Rearrange the nodes until none of the connecting lines overlap.

License
This project is licensed under the MIT License. See the LICENSE file for more details.

Acknowledgements
Simon Tatham:
The original creator of Untangle, whose inventive puzzle design continues to inspire game developers.

Pygame & Cryptography Libraries:
Thanks to the developers behind these libraries for making it easier to build engaging and secure games.
