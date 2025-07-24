from collections import deque

def goal_reached(config):
    return config == "EEE_WWW"


def next_moves(config):
    moves = []
    chars = list(config)
    gap_idx = config.index('_')

    # slide right neighbor
    if gap_idx < 6 and chars[gap_idx + 1] == 'E':
        temp = chars[:]
        temp[gap_idx], temp[gap_idx + 1] = temp[gap_idx + 1], temp[gap_idx]
        moves.append("".join(temp))

    # jump over one tile to the right
    if gap_idx < 5 and chars[gap_idx + 2] == 'E' and chars[gap_idx + 1] == 'W':
        temp = chars[:]
        temp[gap_idx], temp[gap_idx + 2] = temp[gap_idx + 2], temp[gap_idx]
        moves.append("".join(temp))

    # slide left neighbor
    if gap_idx > 0 and chars[gap_idx - 1] == 'W':
        temp = chars[:]
        temp[gap_idx], temp[gap_idx - 1] = temp[gap_idx - 1], temp[gap_idx]
        moves.append("".join(temp))

    # jump over one tile to the left
    if gap_idx > 1 and chars[gap_idx - 2] == 'W' and chars[gap_idx - 1] == 'E':
        temp = chars[:]
        temp[gap_idx], temp[gap_idx - 2] = temp[gap_idx - 2], temp[gap_idx]
        moves.append("".join(temp))

    return moves


def bfs_solver(start):
    visited = set()
    queue = deque([[start]])

    while queue:
        sequence = queue.popleft()
        node = sequence[-1]

        if goal_reached(node):
            return sequence

        for nxt in next_moves(node):
            if nxt not in visited:
                visited.add(nxt)
                queue.append(sequence + [nxt])

    return []


def dfs_solver(start):
    visited = set()
    stack = [[start]]

    while stack:
        sequence = stack.pop()
        node = sequence[-1]

        if goal_reached(node):
            return sequence

        for nxt in next_moves(node):
            if nxt not in visited:
                visited.add(nxt)
                stack.append(sequence + [nxt])

    return []


def main():
    start_state = "WWW_EEE"
    print("BFS Path:")
    bfs_path = bfs_solver(start_state)
    if bfs_path:
        for step in bfs_path:
            print(step)
    else:
        print("No BFS solution")

    print("\nDFS Path:")
    dfs_path = dfs_solver(start_state)
    if dfs_path:
        for step in dfs_path:
            print(step)
    else:
        print("No DFS solution")


if __name__ == "__main__":
    main()
