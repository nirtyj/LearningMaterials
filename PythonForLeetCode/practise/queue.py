"""

from collections import deque

deque()              empty double-ended queue
deque(iterable)      build from any iterable
deque(it, maxlen=k)  bounded; oldest auto-evicts when full

append       push right    O(1)
appendleft   push left     O(1)
pop          pop right     O(1)
popleft      pop left      O(1)
extend       extend right  O(k)
extendleft   extend left   O(k) (reversed!)

rotate(n)    rotate right by n (negative = left)
reverse()    in place

q[0]         peek front
q[-1]        peek back
len(q)       size
not q        is empty

Patterns:
- FIFO queue:      append + popleft
- LIFO stack:      append + pop
- Sliding window:  deque of indices, popleft when out of window
- BFS:             enqueue start, popleft, enqueue neighbours

Important:
- list.pop(0) is O(n). Use deque.popleft for FIFO.
- deque slicing (q[1:3]) does NOT work; convert to list first.

Input convention for these exercises:
- Most exercises receive a deque directly (parameter named dq).
  Your job is to apply the deque methods listed above.
- Some exercises receive a list when the point is conversion (list -> deque),
  a streaming input (one element at a time), or a problem where a deque is
  the internal tool over a non-deque input (BFS over a grid, etc.).
  The docstring will say so explicitly.

"""

"""
Python Queue / Deque Practice

How to use:
1. Run this whole file.
2. It will print every exercise.
3. Unimplemented exercises will show as PENDING, not crash.
4. Implement one function at a time.
5. Run the whole file again after each change.

Rule:
Only edit the functions marked with "YOUR CODE HERE".
Do not edit the test runner at the bottom.
"""

from collections import deque


NOT_IMPLEMENTED = object()


# ============================================================
# Exercise 1: Basic Deque Operations
# ============================================================

def basic_deque_ops():
    """
    In words:

    Build a deque and exercise both ends.

    1. Start with deque([1, 2, 3]).
    2. append(4)        -> right end.
    3. appendleft(0)    -> left end.
    4. popleft()        -> remove left.
    5. pop()            -> remove right.

    Return the final deque converted to a list.

    Example return:
    [1, 2, 3]
    """
    dq = deque([1, 2, 3])
    dq.append(4)
    dq.appendleft(0)
    dq.popleft()
    dq.pop()
    return list(dq)


# ============================================================
# Exercise 2: List To Deque And Back
# ============================================================

def roundtrip(items):
    """
    In words:

    Convert items (a list) into a deque, then back to a list.
    Return the final list.

    Example:
    items = [10, 20, 30]
    Return: [10, 20, 30]
    """
    dq = deque(items)
    return list(dq)


# ============================================================
# Exercise 3: Rotate
# ============================================================

def rotate_deque(dq, n):
    """
    In words:

    You are given a deque dq. Rotate it right by n in place
    (n can be negative for left rotation).
    Return the final deque converted to a list.

    Example:
    dq = deque([1, 2, 3, 4, 5]), n = 2
    Return: [4, 5, 1, 2, 3]

    dq = deque([1, 2, 3, 4, 5]), n = -1
    Return: [2, 3, 4, 5, 1]

    Try to use:
    dq.rotate(n)

    Important:
    dq.rotate(n) returns None; do not write `return dq.rotate(n)`.
    """
    dq.rotate(n)
    return list(dq)


# ============================================================
# Exercise 4: Bounded Deque
# ============================================================

def last_n(stream, n):
    """
    In words:

    Walk through stream, keeping only the most recent n values.
    Return the final state as a list.

    Example:
    stream = [1, 2, 3, 4, 5], n = 3
    Return: [3, 4, 5]

    stream = [1, 2], n = 5
    Return: [1, 2]

    Try to use:
    deque(maxlen=n)
    """

    dq = deque(maxlen = n)
    for i in stream:
        dq.append(i)
    return list(dq)


# ============================================================
# Exercise 5: Reverse A Deque In Place
# ============================================================

def reverse_in_place(dq):
    """
    In words:

    You are given a deque dq. Reverse it in place using deque.reverse()
    and return it as a list.

    Example:
    dq = deque([1, 2, 3])
    Return: [3, 2, 1]

    Important:
    dq.reverse() returns None, so do not write `return dq.reverse()`.
    """
    dq.reverse()
    return list(dq)


# ============================================================
# Exercise 6: Peek Front And Back
# ============================================================

def peek_ends(dq):
    """
    In words:

    You are given a deque dq. Return a tuple (front, back) without
    removing them. If dq is empty, return (None, None).

    Example:
    dq = deque([1, 2, 3])
    Return: (1, 3)

    dq = deque()
    Return: (None, None)

    Try to use:
    dq[0] for the front, dq[-1] for the back.
    """
    if not dq:
        return None, None

    return dq[0], dq[-1]


# ============================================================
# Exercise 7: Ticket Queue
# ============================================================

def serve_tickets(tickets):
    """
    In words:

    A list of ticket numbers arrives in order. Serve them in FIFO order
    and return the served list.

    Example:
    tickets = [101, 102, 103]
    Return: [101, 102, 103]

    Important:
    Use deque.popleft so the queue is O(1).
    Do not use list.pop(0).
    """
    dq = deque(tickets)
    served = []
    while dq:
        served.append(dq.popleft())
    return served


# ============================================================
# Exercise 8: Queue Using Two Stacks
# ============================================================

def queue_via_two_stacks(ops):
    """
    In words:

    Simulate a FIFO queue using only two Python lists as stacks
    (append + pop).

    ops is a list of operations:
    ("push", v)   enqueue value v
    ("pop",)      dequeue and return the front value

    Return the list of values returned by every "pop".

    Example:
    ops = [
        ("push", 1), ("push", 2), ("pop",),
        ("push", 3), ("pop",), ("pop",),
    ]

    Return: [1, 2, 3]

    Try to use:
    Two stacks: "in" and "out". When "out" is empty, drain "in" into "out".
    Do not use deque or list.pop(0).
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 9: Josephus Hot Potato
# ============================================================

def hot_potato(names, k):
    """
    In words:

    People stand in a circle. Pass the potato k times (rotate left by 1
    each step), then eliminate the person now holding it. Repeat until
    one remains. Return that survivor's name.

    Example:
    names = ["A", "B", "C", "D", "E"], k = 3
    Return: "C"

    Try to use:
    A deque. For each round: rotate left by k, then popleft.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 10: Sliding Window Maximum
# ============================================================

def sliding_window_max(nums, k):
    """
    In words:

    Return a list of the maximum value in every window of size k as it
    slides from left to right across nums.

    Example:
    nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
    Return: [3, 3, 5, 5, 6, 7]

    Try to use:
    A monotonic decreasing deque of indices.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 11: First Non-Repeating Character In A Stream
# ============================================================

def first_non_repeating(stream):
    """
    In words:

    For each character processed so far, output the first character that
    appears exactly once. If there is none, output '#'.

    Return the resulting string of length len(stream).

    Example:
    stream = "aabc"
    Return: "a#bb"

    Step by step:
    after 'a'   -> "a"
    after 'aa'  -> "#"
    after 'aab' -> "b"
    after 'aabc'-> "b"

    Try to use:
    A deque of characters not yet known to be repeating, plus a Counter.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 12: Recent Requests
# ============================================================

def recent_requests(times, window):
    """
    In words:

    Each value in times is a non-decreasing timestamp. For each timestamp t,
    report how many timestamps (including t) fall in the inclusive range
    [t - window, t].

    Example:
    times = [1, 100, 3001, 3002], window = 3000
    Return: [1, 2, 3, 3]

    Try to use:
    A deque of recent timestamps; popleft anything older than t - window.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 13: BFS Level Order Of A Tree
# ============================================================

def level_order(tree, root):
    """
    In words:

    The tree is represented as a dict mapping each node to a list of its
    children, in order. Return a list of lists, one per BFS level,
    starting from root.

    Example:
    tree = {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": [],
        "D": [],
        "E": ["F"],
        "F": [],
    }
    root = "A"

    Return:
    [["A"], ["B", "C"], ["D", "E"], ["F"]]

    Try to use:
    A deque of nodes for the BFS frontier; process one level at a time.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 14: BFS Shortest Path In A Grid
# ============================================================

def shortest_path(grid):
    """
    In words:

    grid is a 2D list of 0s (passable) and 1s (wall).
    Return the length of the shortest path from (0,0) to (rows-1, cols-1)
    moving in 4 directions through 0 cells. Count the cells on the path
    (start and end included). If unreachable or start/end is a wall,
    return -1.

    Example:
    grid = [
        [0, 0, 1],
        [1, 0, 1],
        [1, 0, 0],
    ]
    Return: 5

    grid = [
        [0, 1],
        [1, 0],
    ]
    Return: -1

    Try to use:
    BFS with a deque and a visited set.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 15: Word Ladder Length
# ============================================================

def word_ladder(begin, end, word_list):
    """
    In words:

    Two words are connected if they differ by exactly one letter.
    Return the number of words in the shortest sequence from begin to end
    where every intermediate word is in word_list and the last word is end.
    Return 0 if no such sequence exists.

    The begin word is counted; the end word must be in word_list.

    Example:
    begin = "hit", end = "cog"
    word_list = ["hot","dot","dog","lot","log","cog"]
    Return: 5    (hit -> hot -> dot -> dog -> cog)

    begin = "hit", end = "cog"
    word_list = ["hot","dot","dog","lot","log"]
    Return: 0

    Try to use:
    BFS with a deque of (word, steps).
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 16: Rotting Oranges
# ============================================================

def rotting_oranges(grid):
    """
    In words:

    0 = empty, 1 = fresh orange, 2 = rotten orange.
    Each minute every fresh orange adjacent (4-directionally) to a rotten
    one becomes rotten. Return the minimum minutes until no fresh oranges
    remain. Return -1 if some fresh orange never rots. Return 0 if there
    are no fresh oranges to begin with.

    Example:
    grid = [
        [2,1,1],
        [1,1,0],
        [0,1,1],
    ]
    Return: 4

    grid = [
        [2,1,1],
        [0,1,1],
        [1,0,1],
    ]
    Return: -1

    Try to use:
    Multi-source BFS: start with every rotten cell already in the queue.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 17: Open The Lock
# ============================================================

def open_lock(deadends, target):
    """
    In words:

    A 4-wheel lock starts at "0000". Each move rotates one wheel forward
    or backward (with wraparound). Return the minimum moves needed to
    reach target without ever showing a code in deadends.
    Return -1 if impossible.

    Example:
    deadends = ["0201","0101","0102","1212","2002"], target = "0202"
    Return: 6

    deadends = ["8888"], target = "0009"
    Return: 1

    deadends = ["0000"], target = "8888"
    Return: -1

    Try to use:
    BFS over strings; deque of (code, steps); visited set.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 18: Walls And Gates
# ============================================================

def walls_and_gates(rooms):
    """
    In words:

    rooms is a 2D grid:
        -1 = wall
         0 = gate
      INF (use 2**31 - 1) = empty room

    Fill every empty room with the distance to its nearest gate.
    Modify the grid in place AND return it.

    Example input:
    INF = 2**31 - 1
    rooms = [
        [INF, -1,  0, INF],
        [INF, INF, INF, -1],
        [INF, -1,  INF, -1],
        [0,   -1,  INF, INF],
    ]

    Expected after fill:
    [
        [3, -1, 0, 1],
        [2,  2, 1, -1],
        [1, -1, 2, -1],
        [0, -1, 3, 4],
    ]

    Try to use:
    Multi-source BFS from every gate at once.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 19: Snake Tail Simulation
# ============================================================

def simulate_snake(moves, start, grid_size):
    """
    In words:

    A snake of length 3 starts at coordinate `start` and extends to the
    left for 2 more cells. Use a deque where the head is at the right end
    and the tail is at the left end.

    Apply each move as a (dr, dc) tuple. After each move:
    - append the new head,
    - popleft the old tail.

    Movement that goes outside grid_size = (rows, cols) is rejected
    (skip that move entirely).

    Return the snake body as a list of (row, col), tail first, after all moves.

    Example:
    moves = [(0,1), (1,0), (0,-1)]
    start = (1, 2)
    grid_size = (3, 4)

    Initial snake (tail -> head): [(1,0), (1,1), (1,2)]
    After (0,1):   [(1,1), (1,2), (1,3)]
    After (1,0):   [(1,2), (1,3), (2,3)]
    After (0,-1):  [(1,3), (2,3), (2,2)]

    Return:
    [(1, 3), (2, 3), (2, 2)]
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 20: Mixed Final Drill - Moving Average
# ============================================================

def moving_average(values, k):
    """
    In words:

    Return a list where the i-th element is the average of the most recent
    k values seen so far in values[0..i]. If fewer than k values have
    arrived yet, average all of them.

    Round each average to 4 decimal places.

    Example:
    values = [1, 10, 3, 5], k = 3

    Step by step:
    after 1                 -> 1.0
    after 1, 10             -> 5.5
    after 1, 10, 3          -> 4.6667
    after 10, 3, 5  (1 drops)-> 6.0

    Return:
    [1.0, 5.5, 4.6667, 6.0]

    Try to use:
    deque(maxlen=k) plus a running sum.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Test Runner
# ============================================================

def check(name, requirement, actual, expected):
    print("=" * 70)
    print(name)
    print("-" * 70)
    print("Requirement:")
    print(requirement)
    print()

    if actual is NOT_IMPLEMENTED:
        print("Status: PENDING")
        print("This exercise is not implemented yet.")
        print()
        return

    if actual == expected:
        print("Status: PASSED")
        print("Your result:")
        print(actual)
        print()
        return

    print("Status: FAILED")
    print("Expected:")
    print(expected)
    print()
    print("Got:")
    print(actual)
    print()


def run_all_exercises():
    check(
        "Exercise 1: Basic Deque Operations",
        "Build deque, append, appendleft, popleft, pop, return as list.",
        basic_deque_ops(),
        [1, 2, 3],
    )

    check(
        "Exercise 2: List To Deque And Back",
        "Round-trip a list through a deque.",
        roundtrip([10, 20, 30]),
        [10, 20, 30],
    )

    rot_result = rotate_deque(deque([1, 2, 3, 4, 5]), 2)
    if rot_result is NOT_IMPLEMENTED:
        rot_actual = NOT_IMPLEMENTED
    else:
        rot_actual = (
            rotate_deque(deque([1, 2, 3, 4, 5]), 2),
            rotate_deque(deque([1, 2, 3, 4, 5]), -1),
        )
    check(
        "Exercise 3: Rotate",
        "Rotate a deque right by n (negative = left).",
        rot_actual,
        ([4, 5, 1, 2, 3], [2, 3, 4, 5, 1]),
    )

    last_result = last_n([1, 2, 3, 4, 5], 3)
    if last_result is NOT_IMPLEMENTED:
        last_actual = NOT_IMPLEMENTED
    else:
        last_actual = (last_n([1, 2, 3, 4, 5], 3), last_n([1, 2], 5))
    check(
        "Exercise 4: Bounded Deque",
        "Keep only the most recent n values from a stream.",
        last_actual,
        ([3, 4, 5], [1, 2]),
    )

    check(
        "Exercise 5: Reverse A Deque In Place",
        "Reverse a deque in place and return it as a list.",
        reverse_in_place(deque([1, 2, 3])),
        [3, 2, 1],
    )

    pe_result = peek_ends(deque([1, 2, 3]))
    if pe_result is NOT_IMPLEMENTED:
        pe_actual = NOT_IMPLEMENTED
    else:
        pe_actual = (peek_ends(deque([1, 2, 3])), peek_ends(deque()))
    check(
        "Exercise 6: Peek Front And Back",
        "Return (front, back) without removing; (None, None) if empty.",
        pe_actual,
        ((1, 3), (None, None)),
    )

    check(
        "Exercise 7: Ticket Queue",
        "Serve tickets FIFO via deque.popleft.",
        serve_tickets([101, 102, 103]),
        [101, 102, 103],
    )

    check(
        "Exercise 8: Queue Using Two Stacks",
        "Simulate FIFO using two stacks; return pop results in order.",
        queue_via_two_stacks([
            ("push", 1), ("push", 2), ("pop",),
            ("push", 3), ("pop",), ("pop",),
        ]),
        [1, 2, 3],
    )

    check(
        "Exercise 9: Josephus Hot Potato",
        "Rotate left by k then popleft until one survivor remains.",
        hot_potato(["A", "B", "C", "D", "E"], 3),
        "C",
    )

    check(
        "Exercise 10: Sliding Window Maximum",
        "Return max of each size-k window using a monotonic deque.",
        sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3),
        [3, 3, 5, 5, 6, 7],
    )

    check(
        "Exercise 11: First Non-Repeating Character In A Stream",
        "After each char, output the first non-repeating one or '#'.",
        first_non_repeating("aabc"),
        "a#bb",
    )

    check(
        "Exercise 12: Recent Requests",
        "Count timestamps in [t - window, t] for each t.",
        recent_requests([1, 100, 3001, 3002], 3000),
        [1, 2, 3, 3],
    )

    check(
        "Exercise 13: BFS Level Order Of A Tree",
        "Return BFS levels of a child-map tree starting at root.",
        level_order(
            {
                "A": ["B", "C"],
                "B": ["D", "E"],
                "C": [],
                "D": [],
                "E": ["F"],
                "F": [],
            },
            "A",
        ),
        [["A"], ["B", "C"], ["D", "E"], ["F"]],
    )

    sp_result = shortest_path([[0, 0, 1], [1, 0, 1], [1, 0, 0]])
    if sp_result is NOT_IMPLEMENTED:
        sp_actual = NOT_IMPLEMENTED
    else:
        sp_actual = (
            shortest_path([[0, 0, 1], [1, 0, 1], [1, 0, 0]]),
            shortest_path([[0, 1], [1, 0]]),
        )
    check(
        "Exercise 14: BFS Shortest Path In A Grid",
        "Shortest path length (cells) from (0,0) to bottom-right via 0s.",
        sp_actual,
        (5, -1),
    )

    wl_result = word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"])
    if wl_result is NOT_IMPLEMENTED:
        wl_actual = NOT_IMPLEMENTED
    else:
        wl_actual = (
            word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]),
            word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log"]),
        )
    check(
        "Exercise 15: Word Ladder Length",
        "Shortest one-letter-change ladder length from begin to end.",
        wl_actual,
        (5, 0),
    )

    ro_result = rotting_oranges([[2, 1, 1], [1, 1, 0], [0, 1, 1]])
    if ro_result is NOT_IMPLEMENTED:
        ro_actual = NOT_IMPLEMENTED
    else:
        ro_actual = (
            rotting_oranges([[2, 1, 1], [1, 1, 0], [0, 1, 1]]),
            rotting_oranges([[2, 1, 1], [0, 1, 1], [1, 0, 1]]),
        )
    check(
        "Exercise 16: Rotting Oranges",
        "Minutes until no fresh oranges; -1 if some remain.",
        ro_actual,
        (4, -1),
    )

    ol_result = open_lock(["0201", "0101", "0102", "1212", "2002"], "0202")
    if ol_result is NOT_IMPLEMENTED:
        ol_actual = NOT_IMPLEMENTED
    else:
        ol_actual = (
            open_lock(["0201", "0101", "0102", "1212", "2002"], "0202"),
            open_lock(["8888"], "0009"),
            open_lock(["0000"], "8888"),
        )
    check(
        "Exercise 17: Open The Lock",
        "Min wheel moves from '0000' to target avoiding deadends.",
        ol_actual,
        (6, 1, -1),
    )

    INF = 2 ** 31 - 1
    wg_input = [
        [INF, -1, 0, INF],
        [INF, INF, INF, -1],
        [INF, -1, INF, -1],
        [0, -1, INF, INF],
    ]
    wg_expected = [
        [3, -1, 0, 1],
        [2, 2, 1, -1],
        [1, -1, 2, -1],
        [0, -1, 3, 4],
    ]
    check(
        "Exercise 18: Walls And Gates",
        "Multi-source BFS from every gate; fill empty rooms in place.",
        walls_and_gates([row[:] for row in wg_input]),
        wg_expected,
    )

    check(
        "Exercise 19: Snake Tail Simulation",
        "Move snake-as-deque; skip out-of-bounds moves.",
        simulate_snake([(0, 1), (1, 0), (0, -1)], (1, 2), (3, 4)),
        [(1, 3), (2, 3), (2, 2)],
    )

    check(
        "Exercise 20: Mixed Final Drill - Moving Average",
        "Streaming average over last k values, rounded to 4 decimals.",
        moving_average([1, 10, 3, 5], 3),
        [1.0, 5.5, 4.6667, 6.0],
    )


if __name__ == "__main__":
    run_all_exercises()
