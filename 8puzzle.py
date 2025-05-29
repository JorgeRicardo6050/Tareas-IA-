from collections import deque
import heapq
import time
from tabulate import tabulate

# Node class to represent a state of the puzzle
class Node:
    def __init__(self, state, parent=None, move=None, cost=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = parent.depth + 1 if parent else 0
        self.cost = cost

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(tuple(self.state))

    def __lt__(self, other):
        return self.cost < other.cost

# SearchingTree class to explore possible moves and solve the puzzle
class SearchingTree:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.goal_state = sorted(initial_state)

    # Find the possible moves from the current state
    def get_possible_moves(self, state):
        index = state.index(0)
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

    # Heuristic: number of misplaced tiles
    def misplaced_tiles(self, state):
        return sum(1 for i, val in enumerate(state) if val != 0 and val != self.goal_state[i])

    # Heuristic: sum of Manhattan distances
    def manhattan_distance(self, state):
        distance = 0
        for i, val in enumerate(state):
            if val != 0:
                goal_index = self.goal_state.index(val)
                x1, y1 = divmod(i, 3)
                x2, y2 = divmod(goal_index, 3)
                distance += abs(x1 - x2) + abs(y1 - y2)
        return distance

    # Main search method to measure efficiency and solve the puzzle
    def search(self, method, time_limit=5):
        start_time = time.time()
        nodes_explored = 0
        solution_found = False
        solution_path = None
        visited_states = set()

        # A* search with misplaced tiles heuristic
        if method == "astar_misplaced":
            pq = []
            h = self.misplaced_tiles(self.initial_state)
            heapq.heappush(pq, (h, Node(self.initial_state, cost=0)))
            while pq:
                if time.time() - start_time > time_limit:
                    break
                _, current_node = heapq.heappop(pq)
                nodes_explored += 1

                if current_node.state == self.goal_state:
                    solution_found = True
                    solution_path = self.get_solution_path(current_node)
                    break

                visited_states.add(tuple(current_node.state))
                for new_state, move in self.get_possible_moves(current_node.state):
                    if tuple(new_state) not in visited_states:
                        g = current_node.cost + 1
                        h = self.misplaced_tiles(new_state)
                        f = g + h
                        heapq.heappush(pq, (f, Node(new_state, current_node, move, g)))

        # A* search with Manhattan distance heuristic
        elif method == "astar_manhattan":
            pq = []
            h = self.manhattan_distance(self.initial_state)
            heapq.heappush(pq, (h, Node(self.initial_state, cost=0)))
            while pq:
                if time.time() - start_time > time_limit:
                    break
                _, current_node = heapq.heappop(pq)
                nodes_explored += 1

                if current_node.state == self.goal_state:
                    solution_found = True
                    solution_path = self.get_solution_path(current_node)
                    break

                visited_states.add(tuple(current_node.state))
                for new_state, move in self.get_possible_moves(current_node.state):
                    if tuple(new_state) not in visited_states:
                        g = current_node.cost + 1
                        h = self.manhattan_distance(new_state)
                        f = g + h
                        heapq.heappush(pq, (f, Node(new_state, current_node, move, g)))

        # Breadth-First Search (BFS)
        elif method == "bfs":
            queue = deque([Node(self.initial_state)])
            while queue:
                if time.time() - start_time > time_limit:
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

        # Depth-First Search (DFS)
        elif method == "dfs":
            stack = [Node(self.initial_state)]
            while stack:
                if time.time() - start_time > time_limit:
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

        # Uniform Cost Search (UCS)
        elif method == "ucs":
            pq = []
            heapq.heappush(pq, Node(self.initial_state, cost=0))
            while pq:
                if time.time() - start_time > time_limit:
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

        # Depth-Limited Search (DLS)
        elif method == "dls":
            def recursive_dls(node, depth):
                nonlocal nodes_explored, solution_found
                if time.time() - start_time > time_limit:
                    return None

                nodes_explored += 1
                if node.state == self.goal_state:
                    solution_found = True
                    return self.get_solution_path(node)
                elif depth == 10:
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

    # Trace back the solution path from goal to start
    def get_solution_path(self, node):
        path = []
        while node:
            path.append((node.state, node.move))
            node = node.parent
        return path[::-1]

# App class to execute the puzzle solver and show results
class App:
    def __init__(self, initial_state):
        self.tree = SearchingTree(initial_state)

    def run(self):
        # List of search methods to compare
        methods = ["dfs", "bfs", "ucs", "dls", "astar_misplaced", "astar_manhattan"]
        results = []

        # Run each method and collect results
        for method in methods:
            result = self.tree.search(method, time_limit=5)
            results.append(result)
            solution_status = "Yes" if result[3] else "No"
            results[-1] = (result[0], result[1], result[2], solution_status)

        # Print a comparison table of the results
        print("\nComparison Table:")
        print(tabulate(results, headers=["Method", "Time (s)", "Nodes Explored", "Solution Found"], tablefmt="grid"))

    # Print the state as a 3x3 matrix
    def print_state(self, state):
        for i in range(0, 9, 3):
            print(state[i:i+3])
        print()

# Main entry point: get initial state from user and run the app
if __name__ == "__main__":
    initial_state = list(map(int, input("Enter the initial state as 9 space-separated numbers: ").split()))
    app = App(initial_state)
    app.run()

