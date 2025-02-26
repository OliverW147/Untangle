# Untangle Remake  

A Python-based remake of the classic puzzle game **Untangle**, originally created by Simon Tatham.  

![1](https://github.com/OliverW147/Untangle/blob/main/image2.png?raw=true)  
![2](https://github.com/OliverW147/Untangle/blob/main/image.png?raw=true)  

## Overview  
**Untangle Remake** challenges you to rearrange a network of interconnected nodes so that no lines cross. Every game generates a new puzzle, testing your spatial reasoning and problem-solving skills. Enjoy smooth animations, progress tracking, and secure save/load functionality as you work to clear the tangled network.  

## Features  

### 🎲 **Dynamic Puzzle Generation**  
- Randomly generates nodes and connections, ensuring a unique puzzle every time.  

### 🖱 **Interactive Gameplay**  
- Drag-and-drop nodes to reposition them.  
- Selected nodes are highlighted.  
- Overlapping lines can be visually marked for assistance.  

### ⏳ **Progress Tracking**  
- Built-in timer displays elapsed time.  
- Progress bar shows how close you are to solving the puzzle.  

### 💾 **Save & Load**  
- Securely save your game state with encryption (using **Fernet** from the `cryptography` package).  
- Resume your progress at any time.  

### 🖥 **Full-Screen Experience**  
- Runs in full-screen mode for an immersive experience.  

### ⚙ **Adjustable Difficulty**  
- Customize the number of nodes to increase or decrease the puzzle’s difficulty.  

## Getting Started  

### 🔧 **Prerequisites**  
Ensure you have **Python 3** installed. Then install the required packages:  
`pip install pygame cryptography`

## 🎮 How to Play  

### 🆕 **New Game**  
- Click the **New Game** button to start a fresh puzzle.  
- Enter a custom number in the input box to set a specific node count.  

### 🖱 **Drag & Drop**  
- Click on a node to select it.  
- Drag it around the screen.  
- Release the mouse button to drop it in a new position.  

### 🔍 **Peek Knots**  
- Toggle the **Peek Knots** button to highlight overlapping connections.  
- Makes it easier to spot conflicts.  

### 💾 **Save/Load Game**  
- **Save Game** button: Stores your current progress (encrypted).  
- **Load Game** button: Resumes your previous session.  

### 🎯 **Objective**  
- Rearrange the nodes until none of the connecting lines overlap.  

## 📜 License  
This project is licensed under the **MIT License**.

### 👏 **Simon Tatham**  
The original creator of Untangle, whose inventive puzzle design continues to inspire game developers.  
