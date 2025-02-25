from collections import deque
import heapq
import time
from tabulate import tabulate

# Node class to represent a state of the puzzle
class Node:
    def __init__(self, state, parent=None, move=None, cost=0):
        self.state = state  # The current state of the puzzle
        self.parent = parent  # The parent node
        self.move = move  # The move that led to this state
        self.depth = parent.depth + 1 if parent else 0  # Depth of the node
        self.cost = cost  # Cost for priority queue
    
    def __eq__(self, other):
        return self.state == other.state
    
    def __hash__(self):
        return hash(tuple(self.state))
    
    def __lt__(self, other):
        return self.cost < other.cost  # For priority queue ordering

# SearchingTree class to explore possible moves
class SearchingTree:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.goal_state = sorted(initial_state)  # Goal state: sorted values
    
    # Find the possible moves from the current state
    def get_possible_moves(self, state):
        index = state.index(0)  # Find the empty space (0)
        moves = []
        row, col = divmod(index, 3)
        directions = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
        
        for move, offset in directions.items():
            new_index = index + offset
            if 0 <= new_index < 9:
                new_row, new_col = divmod(new_index, 3)
                if abs(new_row - row) + abs(new_col - col) == 1:
                    new_state = state[:]
                    new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
                    moves.append((new_state, move))
        
        return moves
    
    # Generic search method to measure efficiency
    def search(self, method, time_limit=5):
        start_time = time.time()
        nodes_explored = 0
        solution_found = False
        solution_path = None
        visited_states = set()
        
        if method == "bfs":
            queue = deque([Node(self.initial_state)])
            while queue:
                if time.time() - start_time > time_limit:  # Check time limit
                    break
                current_node = queue.popleft()
                nodes_explored += 1
                
                if current_node.state == self.goal_state:
                    solution_found = True
                    solution_path = self.get_solution_path(current_node)
                    break
                
                visited_states.add(tuple(current_node.state))
                for new_state, move in self.get_possible_moves(current_node.state):
                    if tuple(new_state) not in visited_states:
                        queue.append(Node(new_state, current_node, move))
        
        elif method == "dfs":
            stack = [Node(self.initial_state)]
            while stack:
                if time.time() - start_time > time_limit:  # Check time limit
                    break
                current_node = stack.pop()
                nodes_explored += 1
                
                if current_node.state == self.goal_state:
                    solution_found = True
                    solution_path = self.get_solution_path(current_node)
                    break
                
                visited_states.add(tuple(current_node.state))
                for new_state, move in self.get_possible_moves(current_node.state):
                    if tuple(new_state) not in visited_states:
                        stack.append(Node(new_state, current_node, move))
        
        elif method == "ucs":
            pq = []
            heapq.heappush(pq, Node(self.initial_state, cost=0))
            while pq:
                if time.time() - start_time > time_limit:  # Check time limit
                    break
                current_node = heapq.heappop(pq)
                nodes_explored += 1
                
                if current_node.state == self.goal_state:
                    solution_found = True
                    solution_path = self.get_solution_path(current_node)
                    break
                
                visited_states.add(tuple(current_node.state))
                for new_state, move in self.get_possible_moves(current_node.state):
                    if tuple(new_state) not in visited_states:
                        heapq.heappush(pq, Node(new_state, current_node, move, current_node.cost + 1))
        
        elif method == "dls":
            def recursive_dls(node, depth):
                nonlocal nodes_explored, solution_found
                if time.time() - start_time > time_limit:  # Check time limit
                    return None
                
                nodes_explored += 1
                if node.state == self.goal_state:
                    solution_found = True
                    return self.get_solution_path(node)
                elif depth == 10:  # Change limit here if needed
                    return None
                
                visited_states.add(tuple(node.state))
                for new_state, move in self.get_possible_moves(node.state):
                    if tuple(new_state) not in visited_states:
                        result = recursive_dls(Node(new_state, node, move), depth + 1)
                        if result:
                            return result
                return None
            
            recursive_dls(Node(self.initial_state), 0)
        
        execution_time = time.time() - start_time
        return method.upper(), execution_time, nodes_explored, solution_found
    
    # Trace back the solution path
    def get_solution_path(self, node):
        path = []
        while node:
            path.append((node.state, node.move))
            node = node.parent
        return path[::-1]  # Reverse to start from the initial state

# App class to execute the puzzle solver
class App:
    def __init__(self, initial_state):
        self.tree = SearchingTree(initial_state)
    
    def run(self):
        methods = ["dfs", "bfs", "ucs", "dls"]
        results = []
    
        for method in methods:
            result = self.tree.search(method, time_limit=5)  # Set time limit for each method
            results.append(result)
            # Prepare result for the comparison table
            solution_status = "Yes" if result[3] else "No"
            results[-1] = (result[0], result[1], result[2], solution_status)
    
        # Print comparison table
        print("\nComparison Table:")
        print(tabulate(results, headers=["Method", "Time (s)", "Nodes Explored", "Solution Found"], tablefmt="grid"))
    
    # Print the state as a 3x3 matrix
    def print_state(self, state):
        for i in range(0, 9, 3):
            print(state[i:i+3])
        print()

# Example usage
if __name__ == "__main__":
    initial_state = list(map(int, input("Enter the initial state as 9 space-separated numbers: ").split()))
    app = App(initial_state)
    app.run()
