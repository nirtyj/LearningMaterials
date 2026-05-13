"""

=       assign
==      equal value
!=      not equal
>       greater than
<       less than
>=      greater or equal
<=      less or equal

+       add
-       subtract
*       multiply / unpack / repeat
/       normal division
//      floor division
%       remainder
**      power / dictionary unpacking

[]      indexing
[:]     slicing
[::-1]  reverse

and     both conditions true
or      at least one condition true
not     reverse boolean

is      same object
in      contains
~i      equals -(i + 1), useful for mirror indexing

//      row calculation
%       column calculation
divmod  row and column together
[::-1]  reverse
*       unpack rows
zip     group columns
==      compare values
!=      detect mismatch

[EXPRESSION for A in outer for B in A]

"""

"""
Python List / Array Practice

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


NOT_IMPLEMENTED = object()


# ============================================================
# Exercise 1: List Initialization
# ============================================================

def make_lists():
    """
    In words:

    Create five lists.

    1. a should be an empty list.
    2. b should contain 1, 2, 3.
    3. c should contain ten zeros.
    4. d should contain numbers from 0 to 4.
    5. e should contain the squares of numbers from 0 to 4.

    Return them like this:
    return a, b, c, d, e
    """

    a = []
    b = [1, 2, 3]
    c = [0] * 10
    d = [x for x in range(5)]
    e = [x * x for x in range(5)]

    return a, b, c, d, e


# ============================================================
# Exercise 2: 2D Grid Initialization
# ============================================================

def make_grid(rows, cols):
    """
    In words:

    Create a 2D grid with the given number of rows and columns.

    Every cell should be 0.

    Important:
    Each row should be a separate list.
    Do not use the shared-reference bug pattern.

    Example:
    rows = 2, cols = 3

    Return:
    [
        [0, 0, 0],
        [0, 0, 0]
    ]
    """

    a = [[0] * cols for _ in range(rows)]

    return a


# ============================================================
# Exercise 3: Copy vs Reference
# ============================================================

def copy_and_modify(a):
    """
    In words:

    Make a shallow copy of the input list a.

    Then append 99 to the copied list.

    Return both:
    1. The original list unchanged
    2. The copied list with 99 added

    Example:
    input: [1, 2, 3]

    Return:
    ([1, 2, 3], [1, 2, 3, 99])
    """

    # YOUR CODE HERE
    b = a.copy()
    b.append(99)
    return a, b


# ============================================================
# Exercise 4: Append vs Extend
# ============================================================

def append_vs_extend(a, b):
    """
    In words:

    You are given two lists: a and b.

    Create x:
    - x should be a copy of a
    - then append b as one single element

    Create y:
    - y should be a copy of a
    - then extend y with the individual elements of b

    Example:
    a = [1, 2]
    b = [3, 4]

    x should be:
    [1, 2, [3, 4]]

    y should be:
    [1, 2, 3, 4]

    Return:
    x, y
    """

    c = a.copy()
    c.append(b)

    d = a.copy()
    d.extend(b)

    return c, d


# ============================================================
# Exercise 5: Find First Index Greater Than k
# ============================================================

def first_greater_than(arr, k):
    """
    In words:

    Find the index of the first number in arr that is greater than k.

    If no number is greater than k, return -1.

    Try to use:
    - enumerate
    - next
    - a generator expression

    Example:
    arr = [3, 1, 7, 2, 9]
    k = 5

    The first value greater than 5 is 7.
    Its index is 2.

    Return:
    2
    """

    return next((i for i,v in enumerate(arr) if v > k), -1)


# ============================================================
# Exercise 6: Adjacent Differences
# ============================================================

def adjacent_diffs(arr):
    """
    In words:

    Look at every adjacent pair of numbers.

    For each pair, subtract the second number from the first number.

    Example:
    arr = [10, 7, 3, 8]

    Adjacent pairs are:
    10 and 7
    7 and 3
    3 and 8

    Differences are:
    10 - 7 = 3
    7 - 3 = 4
    3 - 8 = -5

    Return:
    [3, 4, -5]

    Try to use:
    zip(arr, arr[1:])
    """
    c = [a - b for a, b in zip(arr, arr[1:])]
    return c


# ============================================================
# Exercise 7: Reverse Values
# ============================================================

def reversed_values(arr):
    """
    In words:

    Return the values of arr in reverse order.

    Example:
    arr = [1, 2, 3]

    Return:
    [3, 2, 1]

    Try to use:
    reversed(arr)

    Do not use arr[::-1] for this exercise.
    """
    return [a for a in reversed(arr)]


# ============================================================
# Exercise 8: Reverse Indices
# ============================================================

def reversed_indices(arr):
    """
    In words:

    Return the indices of arr from last to first.

    Example:
    arr = [10, 20, 30]

    The indices are:
    0, 1, 2

    In reverse order:
    2, 1, 0

    Return:
    [2, 1, 0]

    Try to use:
    range(len(arr) - 1, -1, -1)
    """
    return [x for x in range(len(arr)-1, -1, -1)]


# ============================================================
# Exercise 9: Sort Numbers Descending
# ============================================================

def sort_desc(nums):
    """
    In words:

    Return a new list with the numbers sorted from largest to smallest.

    Example:
    nums = [3, 1, 5, 2]

    Return:
    [5, 3, 2, 1]

    Try to use:
    sorted(nums, key=lambda x: -x)
    """

    # YOUR CODE HERE

    return sorted(nums, key=lambda x: -x)


# ============================================================
# Exercise 10: Multi-Key Sort
# ============================================================

def sort_people(people):
    """
    In words:

    Each item is a pair:
    (age, name)

    Sort the people by:
    1. age descending
    2. name ascending when ages are the same

    Example:
    people = [
        (25, "Bob"),
        (30, "Tom"),
        (30, "Alice"),
        (25, "Eve")
    ]

    Return:
    [
        (30, "Alice"),
        (30, "Tom"),
        (25, "Bob"),
        (25, "Eve")
    ]

    Try to use:
    key=lambda x: (-x[0], x[1])
    """
    return sorted(people, key = lambda x: (-x[0], x[1]))


# ============================================================
# Exercise 11: Transpose Matrix
# ============================================================

def transpose(matrix):
    """
    In words:

    Convert rows into columns.

    Example:
    matrix = [
        [1, 2, 3],
        [4, 5, 6]
    ]

    The first column becomes the first row:
    [1, 4]

    The second column becomes the second row:
    [2, 5]

    The third column becomes the third row:
    [3, 6]

    Return:
    [
        [1, 4],
        [2, 5],
        [3, 6]
    ]

    Try to use:
    zip(*matrix)
    """

    return [list(row) for row in zip(*matrix)]


# ============================================================
# Exercise 12: Rotate Matrix Clockwise
# ============================================================

def rotate_clockwise(matrix):
    """
    In words:

    Return a new matrix rotated 90 degrees clockwise.

    Example:
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    Return:
    [
        [7, 4, 1],
        [8, 5, 2],
        [9, 6, 3]
    ]

    Hint:
    Reverse the rows first, then transpose.

    One possible pattern:
    zip(*matrix[::-1])
    """

    # YOUR CODE HERE

    return [list(rows) for rows in zip(*matrix[::-1])]

def rotate_clockwise(matrix):       # -90 degrees - reverse rows, then transpose
    return [list(row) for row in zip(*matrix[::-1])]


def rotate_counter_clockwise(matrix):  # +90 degrees - transpose, then reverse rows
    return [list(row) for row in zip(*matrix)][::-1]


def rotate_180(matrix):             # +180 or -180 degrees - reverse rows and reverse each row
    return [row[::-1] for row in matrix[::-1]]


# ============================================================
# Exercise 13: Flat Index to Row and Column
# ============================================================

def flat_to_coords(rows, cols):
    """
    In words:

    Imagine a 2D grid flattened into one long list.

    For every flat index, return its row and column.

    Example:
    rows = 2
    cols = 3

    Flat index 0 means row 0, column 0.
    Flat index 1 means row 0, column 1.
    Flat index 2 means row 0, column 2.
    Flat index 3 means row 1, column 0.
    Flat index 4 means row 1, column 1.
    Flat index 5 means row 1, column 2.

    Return:
    [
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2)
    ]

    Try to use:
    divmod(i, cols)
    """
    a = []
    for i in range(rows * cols):
        x, y = divmod(i, cols)
        a.append((x, y))
    return a


# ============================================================
# Exercise 14: Row and Column to Flat Index
# ============================================================

def coord_to_flat(r, c, cols):
    """
    In words:

    Convert a row and column back into a flat index.

    Formula:
    flat index = row * number_of_columns + column

    Example:
    r = 2
    c = 1
    cols = 3

    flat index = 2 * 3 + 1 = 7

    Return:
    7
    """

    # YOUR CODE HERE

    return r * cols + c


# ============================================================
# Exercise 15: Palindrome Using Mirror Index
# ============================================================

def is_palindrome(s):
    """
    In words:

    Return True if the string reads the same forward and backward.

    Return False otherwise.

    Example:
    "racecar" returns True.
    "hello" returns False.
    "abba" returns True.

    Try to compare:
    s[i] with s[~i]

    Reminder:
    ~0 means -1
    ~1 means -2
    ~2 means -3
    """

    for i in range(len(s) // 2):
        if s[i] != s[~i]:
            return False

    return True


# ============================================================
# Exercise 16: Flatten 2D List
# ============================================================

def flatten(grid):
    """
    In words:

    Convert a 2D list into a single flat list.

    Example:
    grid = [
        [1, 2],
        [3, 4],
        [5]
    ]

    Return:
    [1, 2, 3, 4, 5]

    Try to use a list comprehension.
    """
    return [y for x in grid for y in x]


# ============================================================
# Exercise 17: Filter Even Numbers
# ============================================================

def only_evens(nums):
    """
    In words:

    Return only the even numbers from the input list.

    Example:
    nums = [1, 2, 3, 4, 5, 6]

    Return:
    [2, 4, 6]

    Try to use a list comprehension.
    """
    return [x for x in nums if x%2==0]


# ============================================================
# Exercise 18: Safe Index Lookup
# ============================================================

def safe_index(arr, target):
    """
    In words:

    Return the first index where target appears in arr.

    If target does not appear, return -1.

    Example:
    arr = [4, 5, 6]
    target = 5

    Return:
    1

    Example:
    arr = [4, 5, 6]
    target = 9

    Return:
    -1

    Important:
    Do not let your code crash when the target is missing.
    """
    return next((z for z, y in enumerate(arr) if y == target) ,-1)


# ============================================================
# Exercise 19: Reverse In Place
# ============================================================

def reverse_in_place_and_return(a):
    """
    In words:

    Reverse the input list in place.

    Then return the same list.

    Example:
    a = [1, 2, 3]

    After reversing:
    a becomes [3, 2, 1]

    Return:
    [3, 2, 1]

    Important:
    a.reverse() changes the list but returns None.

    So do not write:
    return a.reverse()
    """
    a.reverse()
    return a


# ============================================================
# Exercise 20: Mixed Final Drill
# ============================================================

def analyze_grid(grid):
    """
    In words:

    Given a 2D grid of numbers, return a dictionary with six things.

    Return:

    {
        "rows": number of rows,
        "cols": number of columns,
        "flat": the grid converted to one flat list,
        "transpose": the transposed grid,
        "max_value": the largest number in the grid,
        "first_gt_10": the flat index of the first number greater than 10
    }

    Example:
    grid = [
        [1, 12, 3],
        [4, 5, 6]
    ]

    The flat list is:
    [1, 12, 3, 4, 5, 6]

    The first value greater than 10 is 12.
    Its flat index is 1.

    Return:
    {
        "rows": 2,
        "cols": 3,
        "flat": [1, 12, 3, 4, 5, 6],
        "transpose": [[1, 4], [12, 5], [3, 6]],
        "max_value": 12,
        "first_gt_10": 1
    }
    """

    a = {
        "rows" : len(grid),
        "cols" : len(next(rows for rows in grid)),
        "flat" : [y for x in grid for y in x],
        "transpose" : [list(rows) for rows in zip(*grid)],
        "max_value" : max(y for x in grid for y in x),
        "first_gt_10" : next((i for x in grid for i, y in enumerate(x) if y > 10), -1)
    }

    return a


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
        "Exercise 1: List Initialization",
        "Create an empty list, [1,2,3], ten zeros, range 0 to 4, and squares 0 to 4.",
        make_lists(),
        (
            [],
            [1, 2, 3],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 2, 3, 4],
            [0, 1, 4, 9, 16],
        ),
    )

    grid_result = make_grid(2, 3)
    expected_grid = [[0, 0, 0], [0, 0, 0]]

    if grid_result is not NOT_IMPLEMENTED:
        grid_copy_check = make_grid(2, 3)
        if grid_copy_check is not NOT_IMPLEMENTED:
            grid_copy_check[0][0] = 99
            shared_reference_ok = grid_copy_check == [[99, 0, 0], [0, 0, 0]]
        else:
            shared_reference_ok = False

        grid_expected_result = expected_grid if shared_reference_ok else "Grid rows should not share the same inner list."
    else:
        grid_expected_result = expected_grid

    check(
        "Exercise 2: 2D Grid Initialization",
        "Create a rows x cols grid of zeros. Each row must be a separate list.",
        grid_result if grid_result is NOT_IMPLEMENTED else grid_result,
        grid_expected_result,
    )

    check(
        "Exercise 3: Copy vs Reference",
        "Copy the list, append 99 to the copy, and keep the original unchanged.",
        copy_and_modify([1, 2, 3]),
        ([1, 2, 3], [1, 2, 3, 99]),
    )

    check(
        "Exercise 4: Append vs Extend",
        "Create one list where b is appended as one element, and one list where b's elements are extended.",
        append_vs_extend([1, 2], [3, 4]),
        ([1, 2, [3, 4]], [1, 2, 3, 4]),
    )

    check(
        "Exercise 5: First Index Greater Than k",
        "Return the first index where the value is greater than k, or -1 if none exists.",
        (
            first_greater_than([3, 1, 7, 2, 9], 5),
            first_greater_than([1, 2, 3], 5),
        )
        if first_greater_than([3, 1, 7, 2, 9], 5) is not NOT_IMPLEMENTED
        else NOT_IMPLEMENTED,
        (2, -1),
    )

    check(
        "Exercise 6: Adjacent Differences",
        "Use adjacent pairs and return first minus second for each pair.",
        adjacent_diffs([10, 7, 3, 8]),
        [3, 4, -5],
    )

    check(
        "Exercise 7: Reverse Values",
        "Return values from the list in reverse order.",
        reversed_values([1, 2, 3]),
        [3, 2, 1],
    )

    check(
        "Exercise 8: Reverse Indices",
        "Return the indices of the list from last to first.",
        reversed_indices([10, 20, 30]),
        [2, 1, 0],
    )

    check(
        "Exercise 9: Sort Descending",
        "Return a new list sorted from largest to smallest.",
        sort_desc([3, 1, 5, 2]),
        [5, 3, 2, 1],
    )

    check(
        "Exercise 10: Multi-Key Sort",
        "Sort by age descending, then name ascending.",
        sort_people([(25, "Bob"), (30, "Tom"), (30, "Alice"), (25, "Eve")]),
        [(30, "Alice"), (30, "Tom"), (25, "Bob"), (25, "Eve")],
    )

    check(
        "Exercise 11: Transpose Matrix",
        "Convert rows into columns.",
        transpose([[1, 2, 3], [4, 5, 6]]),
        [[1, 4], [2, 5], [3, 6]],
    )

    check(
        "Exercise 12: Rotate Matrix Clockwise",
        "Return a new matrix rotated 90 degrees clockwise.",
        rotate_clockwise([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
        [[7, 4, 1], [8, 5, 2], [9, 6, 3]],
    )

    check(
        "Exercise 13: Flat Index to Coordinates",
        "Return row and column for every flat index in a rows x cols grid.",
        flat_to_coords(2, 3),
        [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)],
    )

    check(
        "Exercise 14: Coordinates to Flat Index",
        "Convert row and column into a flat index.",
        coord_to_flat(2, 1, 3),
        7,
    )

    palindrome_result = is_palindrome("racecar")
    if palindrome_result is NOT_IMPLEMENTED:
        palindrome_actual = NOT_IMPLEMENTED
    else:
        palindrome_actual = (
            is_palindrome("racecar"),
            is_palindrome("hello"),
            is_palindrome("abba"),
            is_palindrome("abcba"),
        )

    check(
        "Exercise 15: Palindrome Using Mirror Index",
        "Return True if the string reads the same forward and backward.",
        palindrome_actual,
        (True, False, True, True),
    )

    check(
        "Exercise 16: Flatten 2D List",
        "Convert a 2D list into one flat list.",
        flatten([[1, 2], [3, 4], [5]]),
        [1, 2, 3, 4, 5],
    )

    check(
        "Exercise 17: Filter Even Numbers",
        "Return only the even numbers.",
        only_evens([1, 2, 3, 4, 5, 6]),
        [2, 4, 6],
    )

    safe_index_result = safe_index([4, 5, 6], 5)
    if safe_index_result is NOT_IMPLEMENTED:
        safe_index_actual = NOT_IMPLEMENTED
    else:
        safe_index_actual = (
            safe_index([4, 5, 6], 5),
            safe_index([4, 5, 6], 9),
        )

    check(
        "Exercise 18: Safe Index Lookup",
        "Return the first index of target, or -1 if target is missing.",
        safe_index_actual,
        (1, -1),
    )

    reverse_input = [1, 2, 3]
    reverse_result = reverse_in_place_and_return(reverse_input)

    if reverse_result is NOT_IMPLEMENTED:
        reverse_actual = NOT_IMPLEMENTED
    else:
        reverse_actual = (reverse_result, reverse_input)

    check(
        "Exercise 19: Reverse In Place",
        "Reverse the list in place and return the same list.",
        reverse_actual,
        ([3, 2, 1], [3, 2, 1]),
    )

    check(
        "Exercise 20: Mixed Final Drill",
        "Analyze a grid: rows, cols, flat list, transpose, max value, and first flat index greater than 10.",
        analyze_grid([[1, 12, 3], [4, 5, 6]]),
        {
            "rows": 2,
            "cols": 3,
            "flat": [1, 12, 3, 4, 5, 6],
            "transpose": [[1, 4], [12, 5], [3, 6]],
            "max_value": 12,
            "first_gt_10": 1,
        },
    )


if __name__ == "__main__":
    run_all_exercises()