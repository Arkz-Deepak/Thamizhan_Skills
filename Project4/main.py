import matplotlib.pyplot as plt
import numpy as np
import math

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        
        self.g = 0  
        self.h = 0  
        self.f = 0  

    def __eq__(self, other):
        return self.position == other.position

def astar(maze, start, end):
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []    
    closed_list = []  

    open_list.append(start_node)

    while len(open_list) > 0:

        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: 

            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or \
               node_position[1] > (len(maze[len(maze)-1]) - 1) or node_position[1] < 0:
                continue

            if maze[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + \
                      ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            if len([open_node for open_node in open_list if child == open_node and child.g > open_node.g]) > 0:
                continue

            open_list.append(child)
            
    return None 


grid_map = [
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
    [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

start = (0, 0)
goal = (9, 9)

def main():
    print("Calculating Shortest Path...")
    path = astar(grid_map, start, goal)
    print(f"Path Found: {path}")

    grid = np.array(grid_map)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(grid, cmap='Greys', origin='upper')
    
    ax.plot(start[1], start[0], 'go', markersize=12, label='Start') 
    ax.plot(goal[1], goal[0], 'rx', markersize=12, label='Goal')
    
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
