import matplotlib.pyplot as plt
import numpy as np
import math

# ------------------------------------------
# 1. THE CLASS (Stores info about each square)
# ------------------------------------------
class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        
        self.g = 0  # Distance from Start
        self.h = 0  # Distance to Goal (Heuristic)
        self.f = 0  # Total Cost

    def __eq__(self, other):
        return self.position == other.position

# ------------------------------------------
# 2. THE ALGORITHM (The "Thinking" Part)
# ------------------------------------------
def astar(maze, start, end):
    # Create Start and End Nodes
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize lists
    open_list = []    # Nodes we need to check
    closed_list = []  # Nodes we have already checked

    # Add start node to open list
    open_list.append(start_node)

    # LOOP until we find the end
    while len(open_list) > 0:

        # A. Get the current node (the one with lowest F score)
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # B. Found the Goal?
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # C. Generate Children (Neighbors: Up, Down, Left, Right)
        children = []
        # (0, -1) = Left, (0, 1) = Right, (-1, 0) = Up, (1, 0) = Down
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: 

            # Get node position
            node_position = (current_node.position[0] + new_position[0], 
                             current_node.position[1] + new_position[1])

            # Check: Is it within range?
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or \
               node_position[1] > (len(maze[len(maze)-1]) - 1) or node_position[1] < 0:
                continue

            # Check: Is it a wall? (1 is a wall)
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)
            children.append(new_node)

        # D. Loop through children
        for child in children:
            # Child is already in the closed list?
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Calculate the F, G, H values
            child.g = current_node.g + 1
            # Heuristic: Pythagorean distance to end ((x1-x2)^2 + (y1-y2)^2)
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + \
                      ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list?
            if len([open_node for open_node in open_list if child == open_node and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            open_list.append(child)
            
    return None # No path found


# ------------------------------------------
# 3. SETUP & VISUALIZATION
# ------------------------------------------
# 0 = Road, 1 = Obstacle
grid_map = [
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

start = (0, 0)
goal = (9, 9)

def main():
    print("Thinking... Calculating Shortest Path...")
    path = astar(grid_map, start, goal)
    print(f"Path Found: {path}")

    # Visualization
    grid = np.array(grid_map)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(grid, cmap='Greys', origin='upper')
    
    # Draw Start/Goal
    ax.plot(start[1], start[0], 'go', markersize=12, label='Start') 
    ax.plot(goal[1], goal[0], 'rx', markersize=12, label='Goal')
    
    # Draw Path
    if path:
        path_y = [p[0] for p in path]
        path_x = [p[1] for p in path]
        ax.plot(path_x, path_y, 'b-', linewidth=3, label='A* Path')
        
    ax.legend()
    ax.set_title("Project 4: A* Path Planning")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()