import pygame.display
import pygame.font
import pygame.event
import pygame.mouse
import pygame.time
import pygame.draw
import math
import json
from cryptography.fernet import Fernet
from logic import *

# Constants
global NODE_COUNT

NODE_COUNT = 10  # Default number of nodes in the game

NODE_RADIUS = 30 / math.log(NODE_COUNT + 1)
LINE_COLOR = (0, 0, 0)
NODE_COLOR = (0, 0, 255)
BACKGROUND_COLOR = (230, 230, 230)
HIGHLIGHT_COLOR = (255, 0, 0)
SOLVED_COLOR = (0, 255, 0)
PROGRESS_COLOR = (0, 255, 0)
PROGRESS_BG_COLOR = (170, 170, 170)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (150, 150, 150)
TEXT_COLOR = (0, 0, 0)

# Initialize pygame
pygame.init()

# Get the screen dimensions
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h  # Screen resolution

# Set fullscreen mode
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

pygame.display.set_caption("Untangle")
font = pygame.font.Font(None, 24)

def draw_button(text, rect, is_hovered):
    """Draws a button with the given text and rectangle."""
    color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, LINE_COLOR, rect, 2)
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def draw_input_box(input_text, rect, is_active):
    """Draws an input box."""
    color = LINE_COLOR if is_active else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, 2)
    text_surface = font.render(input_text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(midleft=(rect.left + 5, rect.centery))
    screen.blit(text_surface, text_rect)

def load_key():
    return b'NwD-pjylTOlkX5JCIylTXI7t1lazuzHnsxjjgbsgN84='

# Encrypt the data before saving it
def encrypt_data(data):
    key = load_key()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

# Decrypt the data after loading it
def decrypt_data(encrypted_data):
    key = load_key()
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data

def save_game(filename, start_time, puzzle_solved, solved_time, remaining_overlaps, nodes, initial_overlaps):
    save_data = {
        'nodes': [],
        'elapsed_time': pygame.time.get_ticks() - start_time if start_time else 0,
        'puzzle_solved': puzzle_solved,
        'solved_time': solved_time,
        'remaining_overlaps': remaining_overlaps,
        'initial_overlaps': initial_overlaps  # Add initial_overlaps to the saved data
    }

    for node in nodes:
        node_data = {
            'x': node.x,
            'y': node.y,
            'index': node.index,
            'connections': [conn.index for conn in node.connections],
            'dragging': node.dragging,
            'highlighted': node.highlighted
        }
        save_data['nodes'].append(node_data)

    json_data = json.dumps(save_data)
    encrypted_data = encrypt_data(json_data)

    with open(filename, 'wb') as f:
        f.write(encrypted_data)

def load_game(filename):
    with open(filename, 'rb') as f:
        encrypted_data = f.read()

    # Decrypt the data
    decrypted_data = decrypt_data(encrypted_data)

    # Convert decrypted data back to a Python dictionary
    save_data = json.loads(decrypted_data)

    NODE_COUNT = len(save_data['nodes'])
    NODE_RADIUS = 30 / math.log(NODE_COUNT + 1)
    nodes = []

    for node_data in save_data['nodes']:
        node = Node(node_data['x'], node_data['y'], node_data['index'])
        node.dragging = node_data['dragging']
        node.highlighted = node_data['highlighted']
        nodes.append(node)

    for i, node_data in enumerate(save_data['nodes']):
        nodes[i].connections = [nodes[idx] for idx in node_data['connections']]

    initial_overlaps = save_data['initial_overlaps']
    start_time = pygame.time.get_ticks() - save_data['elapsed_time']
    solved_time = save_data['solved_time']
    puzzle_solved = save_data['puzzle_solved']
    remaining_overlaps = save_data['remaining_overlaps']

    return nodes, initial_overlaps, start_time, solved_time, puzzle_solved, remaining_overlaps, NODE_RADIUS

def main():
    global NODE_COUNT, NODE_RADIUS

    def reset_game():
        """Resets the game with the current NODE_COUNT."""
        nonlocal nodes, initial_overlaps, start_time, solved_time, puzzle_solved, remaining_overlaps
        NODE_RADIUS = 30 / math.log(NODE_COUNT + 1)
        nodes = generate_nodes()  # Pass NODE_COUNT to generate_nodes explicitly
        connect_nodes(nodes)
        arrange_nodes_in_circle(nodes)
        initial_overlaps = count_overlaps(nodes)
        start_time = pygame.time.get_ticks()
        solved_time = None
        puzzle_solved = False
        remaining_overlaps = count_overlaps(nodes)

    def save_game_button():
        save_game("UntangleSave.knot", start_time, puzzle_solved, solved_time, remaining_overlaps, nodes, initial_overlaps)

    def load_game_button():
        try:
            a = load_game("UntangleSave.knot")
            return a
        except FileNotFoundError:
            print("Save file not found.")

    try:
        nodes = generate_nodes()
        connect_nodes(nodes)
        arrange_nodes_in_circle(nodes)
    except RuntimeError as e:
        print(e)
        return

    initial_overlaps = count_overlaps(nodes)
    selected_node = None
    running = True
    start_time = pygame.time.get_ticks()
    solved_time = None
    puzzle_solved = False

    button_rect = pygame.Rect(SCREEN_WIDTH - 150, 10, 140, 30)
    input_box_rect = pygame.Rect(SCREEN_WIDTH - 150, 50, 140, 30)
    highlight_button_rect = pygame.Rect(SCREEN_WIDTH - 150, 90, 140, 30)
    load_button_rect = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 40, 140, 30)  # Bottom-right corner
    save_button_rect = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 80, 140, 30)  # Above the Load button
    input_text = ""
    input_active = False

    highlight_overlaps = False  # Track if overlaps should be highlighted
    remaining_overlaps = count_overlaps(nodes)

    while running:
        if puzzle_solved:
            elapsed_time = solved_time
        else:
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000

        if selected_node == None:
            remaining_overlaps = count_overlaps(nodes)
        if initial_overlaps != 0:
            progress = 1 - (remaining_overlaps / initial_overlaps)
        else:
            progress = 0

        message = None
        mouse_pos = pygame.mouse.get_pos()
        button_hovered = button_rect.collidepoint(mouse_pos)
        highlight_button_hovered = highlight_button_rect.collidepoint(mouse_pos)
        save_button_hovered = save_button_rect.collidepoint(mouse_pos)
        load_button_hovered = load_button_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_hovered:
                        if input_text.isdigit() and int(input_text) > 0:
                            set_node_count(int(input_text))
                            reset_game()
                            input_text = ""
                        else:
                            reset_game()
                            input_text = ""
                    elif highlight_button_hovered:
                        highlight_overlaps = not highlight_overlaps
                    elif save_button_hovered:
                        save_game_button()  # Call save game function
                    elif load_button_hovered:
                        try:
                            a = load_game_button()  # Call load game function
                            nodes = a[0]
                            initial_overlaps = a[1]
                            start_time = a[2]
                            solved_time = a[3]
                            puzzle_solved = a[4]
                            remaining_overlaps = a[5]
                            NODE_RADIUS = a[6]
                            set_node_count(len(nodes))
                        except:
                            pass
                    elif input_box_rect.collidepoint(mouse_pos):
                        input_active = True
                    else:
                        input_active = False

                    for node in nodes:
                        if node.is_hovered(event.pos):
                            node.dragging = True
                            selected_node = node
                            for connected_node in node.connections:
                                connected_node.highlighted = True
                            selected_node.highlighted = True
                            break

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if selected_node:
                        selected_node.dragging = False
                        for connected_node in selected_node.connections:
                            connected_node.highlighted = False
                        selected_node.highlighted = False
                        selected_node = None

            elif event.type == pygame.MOUSEMOTION:
                if selected_node:
                    selected_node.x, selected_node.y = event.pos

            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        input_active = False
                    else:
                        input_text += event.unicode

        if remaining_overlaps == 0 and not puzzle_solved:
            puzzle_solved = True
            solved_time = elapsed_time

        if remaining_overlaps == 0:
            message = "Puzzle Solved!"

        screen.fill(BACKGROUND_COLOR)
        draw_nodes_and_connections(nodes, message, progress, elapsed_time, highlight_overlaps, selected_node)
        draw_button("New Game", button_rect, button_hovered)
        draw_button("Peek Knots", highlight_button_rect, highlight_button_hovered)
        draw_button("Save Game", save_button_rect, save_button_hovered)  # Save button
        draw_button("Load Game", load_button_rect, load_button_hovered)  # Load button
        draw_input_box(input_text, input_box_rect, input_active)

        footer_text = font.render("Made by Oliver", True, (200, 200, 200))
        footer_rect = footer_text.get_rect()
        footer_rect.bottomleft = (10, SCREEN_HEIGHT - 10)
        screen.blit(footer_text, footer_rect)

        pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    main()
