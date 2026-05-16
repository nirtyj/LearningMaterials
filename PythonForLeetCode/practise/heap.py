"""

import heapq

A heap is just a plain list maintained in heap order.
Python's heapq is a min-heap. For max-heap, push negatives.

heappush(h, x)       push x                       O(log n)
heappop(h)           pop smallest                 O(log n)
heappushpop(h, x)    push x then pop smallest     O(log n) (fast combo)
heapreplace(h, x)    pop smallest then push x     O(log n) (fast combo)
heapify(list)        turn list into heap in place O(n)
h[0]                 peek smallest                O(1)
nlargest(k, it)      k largest items              O(n log k)
nsmallest(k, it)     k smallest items             O(n log k)

Tuple priorities:
- (priority, value) compares by priority first, then value.
- For tie-breaking with non-comparable values, push a counter:
  heappush(h, (priority, counter, value))

Max-heap trick:
- Push -x, pop, then negate again.

Common patterns:
- Top-K elements          : nlargest / heap of size K
- Streaming median         : two heaps (max-heap of lows, min-heap of highs)
- Merge K sorted lists     : heap of (val, list_index, elem_index)
- Schedule / cooldown      : heap of (next_available_time, ...)

"""

"""
Python Heap Practice

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

import heapq


NOT_IMPLEMENTED = object()


# ============================================================
# Exercise 1: Push And Pop
# ============================================================

def push_pop_sequence(values):
    """
    In words:

    Start with an empty heap.
    heappush every value in values.
    Then heappop every value off.
    Return the popped list.

    Example:
    values = [3, 1, 4, 1, 5, 9, 2, 6]

    Return:
    [1, 1, 2, 3, 4, 5, 6, 9]

    Try to use:
    heapq.heappush and heapq.heappop on a Python list.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 2: Heapify Existing List
# ============================================================

def heapify_and_drain(values):
    """
    In words:

    Build a heap from values in O(n) using heapify, then pop everything.

    Example:
    values = [9, 4, 7, 1, -3, 2]

    Return:
    [-3, 1, 2, 4, 7, 9]

    Try to use:
    Make a copy, heapq.heapify the copy, then repeatedly heappop.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 3: Peek Smallest
# ============================================================

def peek_smallest(values):
    """
    In words:

    Return the smallest value in values without removing it.
    If values is empty, return None.

    Example:
    values = [4, 2, 7, 1, 9]
    Return: 1

    values = []
    Return: None

    Try to use:
    heapify and then read h[0].
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 4: Max-Heap Via Negation
# ============================================================

def max_heap_sort_desc(values):
    """
    In words:

    Use a max-heap (negated values) to return values sorted descending.

    Example:
    values = [3, 1, 4, 1, 5, 9, 2]

    Return:
    [9, 5, 4, 3, 2, 1, 1]

    Important:
    Do not call sorted(values, reverse=True).
    Use heapq with negated values.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 5: K Largest
# ============================================================

def k_largest(values, k):
    """
    In words:

    Return the k largest values, sorted descending.

    Example:
    values = [3, 2, 1, 5, 6, 4], k = 3
    Return: [6, 5, 4]

    Try to use:
    heapq.nlargest(k, values).
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 6: K Smallest
# ============================================================

def k_smallest(values, k):
    """
    In words:

    Return the k smallest values, sorted ascending.

    Example:
    values = [3, 2, 1, 5, 6, 4], k = 3
    Return: [1, 2, 3]

    Try to use:
    heapq.nsmallest(k, values).
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 7: Kth Largest Element
# ============================================================

def kth_largest(values, k):
    """
    In words:

    Return the kth largest value in values (1-indexed).

    Example:
    values = [3, 2, 1, 5, 6, 4], k = 2
    Return: 5

    values = [3, 2, 3, 1, 2, 4, 5, 5, 6], k = 4
    Return: 4

    Try to use:
    A min-heap of size k. Push every value; if size > k, heappop.
    The root is the answer at the end.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 8: Top K Frequent Elements
# ============================================================

def top_k_frequent(values, k):
    """
    In words:

    Return the k most frequent values, sorted by frequency descending.
    Break ties by value ascending.

    Example:
    values = [1, 1, 1, 2, 2, 3], k = 2
    Return: [1, 2]

    values = [4, 4, 3, 3, 2, 2, 1], k = 2
    Return: [2, 3]    (both 3 and 2 appear twice; choose smaller values; tie broken by value asc)

    Try to use:
    collections.Counter and heapq.nlargest with a custom key.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 9: Merge K Sorted Lists
# ============================================================

def merge_k_sorted(lists):
    """
    In words:

    Merge k already-sorted lists into one sorted list using a heap.

    Example:
    lists = [
        [1, 4, 5],
        [1, 3, 4],
        [2, 6],
    ]

    Return:
    [1, 1, 2, 3, 4, 4, 5, 6]

    Try to use:
    Push (value, list_index, element_index) so duplicate values do not
    fail to compare.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 10: Last Stone Weight
# ============================================================

def last_stone_weight(stones):
    """
    In words:

    Repeatedly take the two heaviest stones.
    - If they are equal, both vanish.
    - Otherwise the lighter vanishes and the heavier is replaced by
      heavier - lighter.

    Return the weight of the remaining stone, or 0 if none remain.

    Example:
    stones = [2, 7, 4, 1, 8, 1]
    Return: 1

    stones = [1, 1]
    Return: 0

    Try to use:
    A max-heap (negate the weights).
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 11: Connect Ropes With Minimum Cost
# ============================================================

def connect_ropes(lengths):
    """
    In words:

    Each operation: pick any two ropes and join them. The cost equals
    the sum of their lengths. Repeat until one rope remains.
    Return the minimum total cost.

    Example:
    lengths = [4, 3, 2, 6]
    Return: 29

    lengths = [1, 2, 3, 4, 5]
    Return: 33

    Try to use:
    A min-heap. Repeatedly pop the two smallest, push their sum,
    accumulate the cost.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 12: K Closest Points To Origin
# ============================================================

def k_closest_points(points, k):
    """
    In words:

    Each point is a (x, y) tuple. Return the k points with smallest
    Euclidean distance to (0, 0). Sort the result ascending by distance,
    breaking ties by x then y.

    Example:
    points = [(1, 3), (-2, 2), (5, 8), (0, 1)], k = 2
    Return: [(0, 1), (-2, 2)]

    Try to use:
    heapq.nsmallest with key=lambda p: p[0]**2 + p[1]**2.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 13: Heap With Tuple Priorities
# ============================================================

def priority_drain(jobs):
    """
    In words:

    Each job is a (priority, name) tuple. Lower priority value runs first.
    For equal priorities, alphabetical name first.

    Return the names in execution order.

    Example:
    jobs = [(3, "B"), (1, "A"), (2, "Z"), (1, "C")]

    Sorted by (priority, name):
    (1, "A"), (1, "C"), (2, "Z"), (3, "B")

    Return:
    ["A", "C", "Z", "B"]
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 14: heappushpop vs heapreplace
# ============================================================

def push_pop_vs_replace(heap, x):
    """
    In words:

    Given a heap (already heapified) and a value x, return a tuple
    (result_pushpop, result_replace) where:

    - result_pushpop is heappushpop(copy_of_heap, x):
      pushes x then pops the smallest (so the popped value can be x itself
      if x is smaller than every element).

    - result_replace is heapreplace(copy_of_heap, x):
      pops the smallest first, then pushes x (so the popped value is
      whatever was on top before x, regardless of x).

    Example:
    heap = [1, 3, 5], x = 0
    heappushpop -> pops 0
    heapreplace -> pops 1

    Return:
    (0, 1)

    Example:
    heap = [1, 3, 5], x = 4
    heappushpop -> pops 1
    heapreplace -> pops 1

    Return:
    (1, 1)
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 15: Reorganize String
# ============================================================

def reorganize_string(s):
    """
    In words:

    Rearrange the characters of s so that no two adjacent characters are
    equal. If it cannot be done, return "".

    Example:
    s = "aab"   -> "aba"
    s = "aaab"  -> ""
    s = "aabb"  -> "abab" (any valid answer is fine, but we check this exact result below)

    For the test: when more than one valid result is possible, we use the
    greedy "most-frequent-first, alphabetic tie-break" approach. So for
    "aabb" return "abab".

    Try to use:
    Max-heap of (-count, char). Pop the top, append, then pop the next
    so the just-used char does not repeat. Push them back if they still
    have remaining count.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 16: Task Scheduler
# ============================================================

def task_scheduler(tasks, n):
    """
    In words:

    Given a list of task labels and a cooldown n (no two same tasks may
    run within n+1 consecutive slots), return the minimum number of slots
    needed.

    Example:
    tasks = ["A", "A", "A", "B", "B", "B"], n = 2
    Return: 8

    tasks = ["A", "C", "A", "B", "D", "B"], n = 1
    Return: 6

    tasks = ["A"] * 6, n = 0
    Return: 6

    Try to use:
    Math formula based on the most frequent task, OR a max-heap simulation.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 17: Sliding Window Median
# ============================================================

def sliding_window_median(nums, k):
    """
    In words:

    Return a list of medians of every window of size k as it slides
    across nums. If k is even, median is the average of the two middle
    values.

    Example:
    nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
    Return: [1, -1, -1, 3, 5, 6]

    nums = [1, 2, 3, 4], k = 2
    Return: [1.5, 2.5, 3.5]

    Try to use:
    Two heaps. Simplest correct version may use sorted insertion for
    clarity; that's fine.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 18: Median Of A Data Stream
# ============================================================

def stream_medians(stream):
    """
    In words:

    For each new value in stream, output the median of all values seen so
    far.

    Example:
    stream = [5, 2, 8, 1]
    after 5     -> 5
    after 5,2   -> 3.5
    after 5,2,8 -> 5
    after all   -> 3.5

    Return:
    [5, 3.5, 5, 3.5]

    Try to use:
    Two heaps:
    - lows: max-heap of the smaller half
    - highs: min-heap of the larger half
    Keep their sizes within 1 of each other.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 19: Smallest Range Covering K Lists
# ============================================================

def smallest_range(lists):
    """
    In words:

    Given k sorted ascending lists, return the smallest range [a, b]
    that contains at least one number from each list. If multiple ranges
    tie on length, prefer the smaller a.

    Example:
    lists = [[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]]
    Return: [20, 24]

    lists = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
    Return: [1, 1]

    Try to use:
    A min-heap of (value, list_index, element_index) with a tracked
    running max. Pop the smallest, update the candidate range, push the
    next element from that list.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 20: Mixed Final Drill - Kth Largest Stream
# ============================================================

def kth_largest_stream(k, initial, adds):
    """
    In words:

    Simulate a data structure that always tracks the kth largest value
    in a stream. After initializing with `initial`, process every value
    in `adds` and record the kth largest at that point.

    If there are fewer than k values seen so far, return None for that
    step.

    Example:
    k = 3
    initial = [4, 5, 8, 2]
    adds = [3, 5, 10, 9, 4]

    After init the kth largest = 4.
    add 3  -> [2,3,4,5,8]              kth largest = 4
    add 5  -> [2,3,4,5,5,8]            kth largest = 5
    add 10 -> [2,3,4,5,5,8,10]         kth largest = 5
    add 9  -> [2,3,4,5,5,8,9,10]       kth largest = 8
    add 4  -> [2,3,4,4,5,5,8,9,10]     kth largest = 8

    Return:
    [4, 5, 5, 8, 8]

    Try to use:
    A min-heap of size k. After each add, if size > k, heappop. The root
    is always the kth largest.
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
        "Exercise 1: Push And Pop",
        "Push every value, then pop everything; should come out sorted asc.",
        push_pop_sequence([3, 1, 4, 1, 5, 9, 2, 6]),
        [1, 1, 2, 3, 4, 5, 6, 9],
    )

    check(
        "Exercise 2: Heapify Existing List",
        "heapify in O(n), then pop everything in order.",
        heapify_and_drain([9, 4, 7, 1, -3, 2]),
        [-3, 1, 2, 4, 7, 9],
    )

    peek_result = peek_smallest([4, 2, 7, 1, 9])
    if peek_result is NOT_IMPLEMENTED:
        peek_actual = NOT_IMPLEMENTED
    else:
        peek_actual = (peek_smallest([4, 2, 7, 1, 9]), peek_smallest([]))
    check(
        "Exercise 3: Peek Smallest",
        "Return smallest without removing; None if empty.",
        peek_actual,
        (1, None),
    )

    check(
        "Exercise 4: Max-Heap Via Negation",
        "Sort descending using a negated min-heap.",
        max_heap_sort_desc([3, 1, 4, 1, 5, 9, 2]),
        [9, 5, 4, 3, 2, 1, 1],
    )

    check(
        "Exercise 5: K Largest",
        "Return the k largest values, descending.",
        k_largest([3, 2, 1, 5, 6, 4], 3),
        [6, 5, 4],
    )

    check(
        "Exercise 6: K Smallest",
        "Return the k smallest values, ascending.",
        k_smallest([3, 2, 1, 5, 6, 4], 3),
        [1, 2, 3],
    )

    kth_result = kth_largest([3, 2, 1, 5, 6, 4], 2)
    if kth_result is NOT_IMPLEMENTED:
        kth_actual = NOT_IMPLEMENTED
    else:
        kth_actual = (
            kth_largest([3, 2, 1, 5, 6, 4], 2),
            kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4),
        )
    check(
        "Exercise 7: Kth Largest Element",
        "Maintain a min-heap of size k; root is the answer.",
        kth_actual,
        (5, 4),
    )

    top_k_result = top_k_frequent([1, 1, 1, 2, 2, 3], 2)
    if top_k_result is NOT_IMPLEMENTED:
        top_k_actual = NOT_IMPLEMENTED
    else:
        top_k_actual = (
            top_k_frequent([1, 1, 1, 2, 2, 3], 2),
            top_k_frequent([4, 4, 3, 3, 2, 2, 1], 2),
        )
    check(
        "Exercise 8: Top K Frequent Elements",
        "k most frequent, ties broken by value asc.",
        top_k_actual,
        ([1, 2], [2, 3]),
    )

    check(
        "Exercise 9: Merge K Sorted Lists",
        "Merge k sorted lists with a heap.",
        merge_k_sorted([[1, 4, 5], [1, 3, 4], [2, 6]]),
        [1, 1, 2, 3, 4, 4, 5, 6],
    )

    stones_result = last_stone_weight([2, 7, 4, 1, 8, 1])
    if stones_result is NOT_IMPLEMENTED:
        stones_actual = NOT_IMPLEMENTED
    else:
        stones_actual = (
            last_stone_weight([2, 7, 4, 1, 8, 1]),
            last_stone_weight([1, 1]),
        )
    check(
        "Exercise 10: Last Stone Weight",
        "Simulate stone-smashing with a max-heap.",
        stones_actual,
        (1, 0),
    )

    ropes_result = connect_ropes([4, 3, 2, 6])
    if ropes_result is NOT_IMPLEMENTED:
        ropes_actual = NOT_IMPLEMENTED
    else:
        ropes_actual = (
            connect_ropes([4, 3, 2, 6]),
            connect_ropes([1, 2, 3, 4, 5]),
        )
    check(
        "Exercise 11: Connect Ropes With Minimum Cost",
        "Repeatedly merge the two cheapest ropes; accumulate cost.",
        ropes_actual,
        (29, 33),
    )

    check(
        "Exercise 12: K Closest Points To Origin",
        "Return k points with smallest distance to origin.",
        k_closest_points([(1, 3), (-2, 2), (5, 8), (0, 1)], 2),
        [(0, 1), (-2, 2)],
    )

    check(
        "Exercise 13: Heap With Tuple Priorities",
        "Drain (priority, name) heap; lower priority first, then name asc.",
        priority_drain([(3, "B"), (1, "A"), (2, "Z"), (1, "C")]),
        ["A", "C", "Z", "B"],
    )

    pp_result = push_pop_vs_replace([1, 3, 5], 0)
    if pp_result is NOT_IMPLEMENTED:
        pp_actual = NOT_IMPLEMENTED
    else:
        pp_actual = (
            push_pop_vs_replace([1, 3, 5], 0),
            push_pop_vs_replace([1, 3, 5], 4),
        )
    check(
        "Exercise 14: heappushpop vs heapreplace",
        "Show how pushpop pops the new value if smaller, replace never does.",
        pp_actual,
        ((0, 1), (1, 1)),
    )

    check(
        "Exercise 15: Reorganize String",
        "Most-frequent-first greedy; aabb -> abab.",
        reorganize_string("aabb"),
        "abab",
    )

    ts_result = task_scheduler(["A", "A", "A", "B", "B", "B"], 2)
    if ts_result is NOT_IMPLEMENTED:
        ts_actual = NOT_IMPLEMENTED
    else:
        ts_actual = (
            task_scheduler(["A", "A", "A", "B", "B", "B"], 2),
            task_scheduler(["A", "C", "A", "B", "D", "B"], 1),
            task_scheduler(["A"] * 6, 0),
        )
    check(
        "Exercise 16: Task Scheduler",
        "Min slots respecting cooldown n.",
        ts_actual,
        (8, 6, 6),
    )

    swm_result = sliding_window_median([1, 3, -1, -3, 5, 3, 6, 7], 3)
    if swm_result is NOT_IMPLEMENTED:
        swm_actual = NOT_IMPLEMENTED
    else:
        swm_actual = (
            sliding_window_median([1, 3, -1, -3, 5, 3, 6, 7], 3),
            sliding_window_median([1, 2, 3, 4], 2),
        )
    check(
        "Exercise 17: Sliding Window Median",
        "Median of every window of size k.",
        swm_actual,
        ([1, -1, -1, 3, 5, 6], [1.5, 2.5, 3.5]),
    )

    check(
        "Exercise 18: Median Of A Data Stream",
        "Running median after each new value using two heaps.",
        stream_medians([5, 2, 8, 1]),
        [5, 3.5, 5, 3.5],
    )

    sr_result = smallest_range([[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]])
    if sr_result is NOT_IMPLEMENTED:
        sr_actual = NOT_IMPLEMENTED
    else:
        sr_actual = (
            smallest_range([[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]]),
            smallest_range([[1, 2, 3], [1, 2, 3], [1, 2, 3]]),
        )
    check(
        "Exercise 19: Smallest Range Covering K Lists",
        "Smallest [a, b] that touches every input list.",
        sr_actual,
        ([20, 24], [1, 1]),
    )

    check(
        "Exercise 20: Mixed Final Drill - Kth Largest Stream",
        "Track kth largest after each insertion.",
        kth_largest_stream(3, [4, 5, 8, 2], [3, 5, 10, 9, 4]),
        [4, 5, 5, 8, 8],
    )


if __name__ == "__main__":
    run_all_exercises()
