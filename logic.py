from main import *
import random

class Node:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index
        self.connections = []
        self.dragging = False
        self.highlighted = False  # To track if a node should be highlighted

    def connect(self, other):
        if other not in self.connections and len(self.connections) < 4 and len(other.connections) < 4:
            self.connections.append(other)
            other.connections.append(self)

    def draw(self):
        # Draw a black outline
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), NODE_RADIUS + 1)  # Outline (1 pixel larger)

        # Highlight if the node is being dragged or should be highlighted
        color = HIGHLIGHT_COLOR if self.highlighted else NODE_COLOR
        pygame.draw.circle(screen, color, (self.x, self.y), NODE_RADIUS)  # Fill the node

    def is_hovered(self, pos):
        return math.hypot(pos[0] - self.x, pos[1] - self.y) <= NODE_RADIUS

def generate_nodes():
    nodes = []
    grid_size = 2 * math.ceil(math.sqrt(NODE_COUNT))
    spacing = SCREEN_WIDTH // grid_size  # Size of each grid cell
    grid_positions = []

    # Generate all possible grid positions
    for i in range(grid_size):
        for j in range(grid_size):
            x = spacing // 2 + i * spacing
            y = spacing // 2 + j * spacing
            grid_positions.append((x, y))

    # Randomly shuffle the grid positions and select positions for nodes
    random.shuffle(grid_positions)
    for i in range(NODE_COUNT):
        x, y = grid_positions.pop()
        nodes.append(Node(x, y, i))

    return nodes

def arrange_nodes_in_circle(nodes):
    # Arrange nodes in a circle
    angle_step = 2 * math.pi / NODE_COUNT
    radius = SCREEN_HEIGHT // 3  # Dynamic radius based on screen height
    center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

    for i, node in enumerate(nodes):
        angle = i * angle_step
        node.x = int(center_x + radius * math.cos(angle))
        node.y = int(center_y + radius * math.sin(angle))

def do_lines_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    def orientation(p, q, r):
        """Calculate the orientation of the triplet (p, q, r).
        0 -> p, q and r are collinear
        1 -> Clockwise
        2 -> Counterclockwise
        """
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        return 1 if val > 0 else 2

    def on_segment(p, q, r):
        """Check if point q lies on segment pr"""
        if (min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and
                min(p[1], r[1]) <= q[1] <= max(p[1], r[1])):
            return True
        return False

    # Convert coordinates into points for easier handling
    p1, q1 = (x1, y1), (x2, y2)
    p2, q2 = (x3, y3), (x4, y4)

    # Find the four orientations needed for the general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case: lines intersect if orientations are different
    if o1 != o2 and o3 != o4:
        return True

    # Special cases: Check if the points are collinear and lie on the segments
    if o1 == 0 and on_segment(p1, p2, q1):
        return True
    if o2 == 0 and on_segment(p1, q2, q1):
        return True
    if o3 == 0 and on_segment(p2, p1, q2):
        return True
    if o4 == 0 and on_segment(p2, q1, q2):
        return True

    # Otherwise, the lines do not intersect
    return False

def check_line_overlap(node1, node2, nodes):
    for other in nodes:
        if other == node1 or other == node2:
            continue
        for connected in other.connections:
            if connected == node1 or connected == node2:
                continue
            if do_lines_intersect(
                    node1.x, node1.y, node2.x, node2.y, other.x, other.y, connected.x, connected.y
            ):
                return True
    return False

def connect_nodes(nodes):
    # Ensure all nodes are part of one chain
    unconnected_nodes = nodes[:]
    connected_nodes = [unconnected_nodes.pop(0)]

    while unconnected_nodes:
        current_node = connected_nodes[-1]

        # Find a nearest unconnected node
        nearest_node = min(unconnected_nodes, key=lambda n: math.hypot(n.x - current_node.x, n.y - current_node.y))

        if not check_line_overlap(current_node, nearest_node, nodes):
            current_node.connect(nearest_node)
            connected_nodes.append(nearest_node)
            unconnected_nodes.remove(nearest_node)
        else:
            # Backtrack if connection fails
            connected_nodes.pop()

    # Ensure every node has at least 2 connections
    for node in nodes:
        while len(node.connections) < 2:
            connected = False  # Flag to check if a valid connection was made
            for other in nodes:
                if node == other or other in node.connections or len(other.connections) >= 4:
                    continue

                if not check_line_overlap(node, other, nodes):
                    node.connect(other)
                    connected = True
                    break  # Exit the loop once a valid connection is made

            if not connected:
                break  # Exit if there are no valid connections left to make

    # Add extra connections to some nodes, ensuring no node exceeds 4 connections
    for node in nodes:
        for other in nodes:
            random_number = random.uniform(3, 15)
            if(random_number >= 5):
                random_number = 3
            if node != other and len(node.connections) < random_number and len(other.connections) < random_number and other not in node.connections:
                if not check_line_overlap(node, other, nodes):
                    node.connect(other)

def draw_nodes_and_connections(nodes, message=None, progress=None, elapsed_time=None, highlight_overlaps=False, selected_node=True):
    screen.fill(BACKGROUND_COLOR)
    for node in nodes:
        for connected_node in node.connections:
            color = LINE_COLOR
            if selected_node == None and highlight_overlaps and check_line_overlap(node, connected_node, nodes):
                color = (255, 0, 0)  # Red for overlapping lines
            pygame.draw.line(screen, color, (node.x, node.y), (connected_node.x, connected_node.y), 2)
    for node in nodes:
        node.draw()

    # Draw the message if provided
    if message:
        # Increase font size
        large_font = pygame.font.Font(None, 48)  # Larger font size
        text_surface = large_font.render(message, True, SOLVED_COLOR)  # Text with original color

        # Calculate the position to center the message
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # Draw the black outline around the text
        outline_color = (0, 0, 0)  # Black outline color
        outline_offset = 2  # Adjust this for thicker or thinner outline

        # Draw the outline (multiple times with offsets)
        for dx in [-outline_offset, 0, outline_offset]:
            for dy in [-outline_offset, 0, outline_offset]:
                if dx != 0 or dy != 0:
                    # Draw the outline in black around the text
                    outline_surface = large_font.render(message, True, outline_color)
                    screen.blit(outline_surface, (text_rect.x + dx, text_rect.y + dy))

        # Draw the main text (in SOLVED_COLOR)
        screen.blit(text_surface, text_rect)

    # Display the number of nodes and elapsed time
    font_small = pygame.font.Font(None, 24)
    node_count_text = font_small.render(f"{NODE_COUNT} Nodes", True, (0, 0, 0))
    screen.blit(node_count_text, (20, 50))

    # Inside the main game loop where you're calculating elapsed time:
    if elapsed_time is not None:
        # Calculate hours, minutes, and seconds
        hours = int(elapsed_time // 3600)  # Total hours
        minutes = int((elapsed_time % 3600) // 60)  # Remaining minutes after hours
        seconds = int(elapsed_time % 60)  # Remaining seconds after minutes

        # Format the time as per the requirement:
        if hours > 0:
            time_text = font_small.render(f"{hours}h {minutes}m {seconds}s", True, (0, 0, 0))
        elif minutes > 0:
            time_text = font_small.render(f"{minutes}m {seconds}s", True, (0, 0, 0))
        else:
            time_text = font_small.render(f"{seconds}s", True, (0, 0, 0))

        # Draw the time on the screen
        screen.blit(time_text, (20, 70))

    # Simplified Progress Bar (Smooth Animation + Outline)
    if progress is not None:
        progress_width = SCREEN_WIDTH // 16
        progress_height = 20
        progress_rect = pygame.Rect(20, 20, progress_width, progress_height)

        # Draw the background of the progress bar
        pygame.draw.rect(screen, PROGRESS_BG_COLOR, progress_rect)

        # Initialize a variable to store the current width of the progress bar
        if not hasattr(pygame, 'current_progress_width'):
            pygame.current_progress_width = 0  # Initialize on the first run

        # Calculate the target width of the progress bar
        target_width = int(progress * progress_width)

        # Smoothly update the current width towards the target width
        if pygame.current_progress_width < target_width:
            pygame.current_progress_width += 1  # Increment smoothly
        elif pygame.current_progress_width > target_width:
            pygame.current_progress_width -= 1  # Decrement smoothly

        # Draw the progress bar with the current width
        progress_bar_rect = pygame.Rect(20, 20, pygame.current_progress_width, progress_height)
        pygame.draw.rect(screen, PROGRESS_COLOR, progress_bar_rect)

        # Draw the outline of the progress bar (black)
        pygame.draw.rect(screen, (0, 0, 0), progress_rect, 2)  # Black outline with 2px thickness

def is_solved(nodes):
    for node in nodes:
        for connected_node in node.connections:
            if check_line_overlap(node, connected_node, nodes):
                return False
    return True

def count_overlaps(nodes):
    overlaps = 0
    for node1 in nodes:
        for node2 in node1.connections:
            if node1.index < node2.index:  # To avoid counting the same pair twice
                if check_line_overlap(node1, node2, nodes):
                    overlaps += 1
    return overlaps

def print_node_connection_counts(nodes):
    connection_counts = {}
    for node in nodes:
        count = len(node.connections)
        if count not in connection_counts:
            connection_counts[count] = 0
        connection_counts[count] += 1

    # Print the results
    print("Node Connection Counts:")
    for connection_count, node_count in sorted(connection_counts.items()):
        print(f"{node_count} nodes with {connection_count} connections")

def set_node_count(count):
    global NODE_COUNT, NODE_RADIUS
    NODE_COUNT = count
    NODE_RADIUS = 30 / math.log(NODE_COUNT + 1)