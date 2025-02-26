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
```sh
pip install pygame cryptography
