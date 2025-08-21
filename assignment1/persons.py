class CrossingNode:
    def __init__(self, positions, times, elapsed, lamp_side):
        self.positions = positions        # [0,0,0,0] -> all on left initially
        self.times = times               # crossing durations for each person
        self.elapsed = elapsed           # total time taken so far
        self.lamp_side = lamp_side       # 0 = left side, 1 = right side

    def is_goal(self):
        return self.positions == [1, 1, 1, 1] and self.elapsed <= 60

    def expand(self):
        successors = []
        for p1 in range(len(self.positions)):
            for p2 in range(p1, len(self.positions)):
                # only move those on the same side as the lamp
                if self.positions[p1] == self.positions[p2] == self.lamp_side:
                    updated_positions = self.positions.copy()
                    if p1 == p2:
                        # single person crosses
                        updated_positions[p1] = 1 - self.positions[p1]
                        next_time = self.elapsed + self.times[p1]
                    else:
                        # two people cross together
                        updated_positions[p1] = 1 - self.positions[p1]
                        updated_positions[p2] = 1 - self.positions[p2]
                        next_time = self.elapsed + max(self.times[p1], self.times[p2])

                    if next_time <= 60:
                        successors.append(
                            CrossingNode(updated_positions, self.times, next_time, 1 - self.lamp_side)
                        )
        return successors

    def __eq__(self, other):
        return (
            isinstance(other, CrossingNode)
            and self.positions == other.positions
            and self.lamp_side == other.lamp_side
            and self.elapsed == other.elapsed
        )

    def __hash__(self):
        return hash((tuple(self.positions), self.lamp_side, self.elapsed))

    def __repr__(self):
        side_str = ''.join(map(str, self.positions))
        return f"Node[{side_str}] | Time = {self.elapsed}"


def build_path(visited, target_node):
    backtrack = []
    parent_map = {node: parent for node, parent in visited}
    while target_node:
        backtrack.append(target_node)
        target_node = parent_map.get(target_node)
    return list(reversed(backtrack))


def filter_new_nodes(next_nodes, frontier, explored):
    frontier_nodes = [n for n, _ in frontier]
    explored_nodes = [n for n, _ in explored]
    return [n for n in next_nodes if n not in frontier_nodes and n not in explored_nodes]


def bfs_search(start):
    frontier = [(start, None)]
    explored = []

    while frontier:
        current_node, parent = frontier.pop(0)
        explored.append((current_node, parent))

        if current_node.is_goal():
            print("BFS found a solution:")
            for step in build_path(explored, current_node):
                print(step)
            return

        successors = filter_new_nodes(current_node.expand(), frontier, explored)
        frontier.extend((s, current_node) for s in successors)

    print("No BFS solution within time limit.")


def dfs_search(start):
    frontier = [(start, None)]
    explored = []

    while frontier:
        current_node, parent = frontier.pop()  # LIFO stack for DFS
        explored.append((current_node, parent))

        if current_node.is_goal():
            print("DFS found a solution:")
            for step in build_path(explored, current_node):
                print(step)
            return

        successors = filter_new_nodes(current_node.expand(), frontier, explored)
        frontier.extend((s, current_node) for s in successors)

    print("No DFS solution within time limit.")


# Initial configuration
def main():
    initial = CrossingNode([0, 0, 0, 0], [5, 10, 20, 25], 0, 0)
    print("Running BFS search...")
    bfs_search(initial)
    print("\nRunning DFS search...")
    dfs_search(initial)


if __name__ == "__main__":
    main()
