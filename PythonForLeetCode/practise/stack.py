"""

A Python list IS the stack. Use list operations as stack operations:

append       push      O(1)
pop()        pop top   O(1)
stack[-1]    peek      O(1)
len(stack)   size      O(1)
not stack    is empty

Monotonic stack:
- Keep elements in strict increasing or decreasing order.
- Pop while the top breaks the order, then push the new element.
- Indexes are often stored instead of values.

Common patterns:
- Match opening/closing brackets.
- Next greater / next smaller element.
- Histogram / rain water.
- Path simplification.
- Decode nested strings.
- Browser-like back / forward.

"""

"""
Python Stack Practice

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
# Exercise 1: Push and Pop
# ============================================================

def push_pop_sequence(values):
    """
    In words:

    Start with an empty stack.
    Push every value in values in order.
    Then pop everything off, in pop order, and return the popped list.

    Example:
    values = [1, 2, 3]

    Push 1, 2, 3, then pop -> 3, then 2, then 1.

    Return:
    [3, 2, 1]

    Try to use:
    stack.append(x) to push, stack.pop() to pop.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 2: Peek
# ============================================================

def peek(stack):
    """
    In words:

    Return the top of the stack without removing it.
    If the stack is empty, return None.

    Example:
    stack = [1, 2, 3]
    Return: 3

    stack = []
    Return: None
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 3: Reverse a String Using a Stack
# ============================================================

def reverse_string(s):
    """
    In words:

    Reverse s by pushing every character onto a stack and then popping.

    Example:
    s = "hello"

    Return:
    "olleh"

    Important:
    Solve it using stack operations, not s[::-1] or reversed().
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 4: Valid Parentheses
# ============================================================

def is_valid_parens(s):
    """
    In words:

    Return True if every opening bracket in s has a matching closing
    bracket of the same kind, properly nested. False otherwise.

    Brackets supported: () [] {}

    Example:
    s = "([]{})"   -> True
    s = "([)]"     -> False
    s = "("        -> False
    s = ""         -> True

    Try to use:
    Push opens; on close, check the top and pop.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 5: Decimal To Binary
# ============================================================

def to_binary(n):
    """
    In words:

    Convert a non-negative integer n to its binary representation
    as a string, using a stack of remainders.

    Example:
    n = 0  -> "0"
    n = 1  -> "1"
    n = 5  -> "101"
    n = 13 -> "1101"

    Important:
    Do not use bin().
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 6: Reverse Polish Notation
# ============================================================

def eval_rpn(tokens):
    """
    In words:

    Evaluate an arithmetic expression in Reverse Polish Notation.

    Operators: "+", "-", "*", "/"
    Numbers are given as strings (may be negative).
    Division must truncate toward zero (use int(a / b)).

    Example:
    tokens = ["2", "1", "+", "3", "*"]   -> (2 + 1) * 3 = 9
    tokens = ["4", "13", "5", "/", "+"]  -> 4 + (13 // 5) = 6

    Try to use:
    Push numbers; on operator, pop b then a, compute, push result.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 7: Next Greater Element
# ============================================================

def next_greater(nums):
    """
    In words:

    For each index i, return the next value to the right of i that is
    strictly greater than nums[i]. If none exists, use -1.

    Example:
    nums = [2, 1, 3, 0, 4]

    Return:
    [3, 3, 4, 4, -1]

    Try to use:
    A decreasing monotonic stack of indices.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 8: Daily Temperatures
# ============================================================

def daily_temperatures(temps):
    """
    In words:

    For each day i, return the number of days you must wait until
    a strictly warmer temperature. Use 0 if no warmer day exists.

    Example:
    temps = [73, 74, 75, 71, 69, 72, 76, 73]

    Return:
    [1, 1, 4, 2, 1, 1, 0, 0]

    Try to use:
    A decreasing monotonic stack of indices.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 9: Largest Rectangle In Histogram
# ============================================================

def largest_rectangle(heights):
    """
    In words:

    Each bar has width 1. Return the largest rectangular area you can
    form using contiguous bars.

    Example:
    heights = [2, 1, 5, 6, 2, 3]
    Return: 10   (the 5 and 6 form 5 wide 2 tall? actually 5 * 2 = 10)

    heights = [2, 4]
    Return: 4

    Try to use:
    An increasing monotonic stack. Append a sentinel 0 at the end so
    every bar is finalized.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 10: Min Stack
# ============================================================

def min_stack_ops(ops):
    """
    In words:

    Simulate a stack that also supports getMin() in O(1).
    ops is a list of operations. Each operation is one of:

    ("push", v)   push value v
    ("pop",)      pop top
    ("top",)      peek top
    ("min",)      current minimum

    Return a list with the result of every "top" or "min" call,
    in the order they happened.

    Example:
    ops = [
        ("push", 3), ("push", 5), ("min",),
        ("push", 2), ("min",),
        ("pop",), ("top",), ("min",),
    ]

    Return:
    [3, 2, 5, 3]

    Try to use:
    A second "mins" stack that tracks the minimum at each level.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 11: Remove Adjacent Duplicates
# ============================================================

def remove_adjacent_duplicates(s):
    """
    In words:

    Repeatedly remove pairs of equal adjacent characters until none remain.
    Return the resulting string.

    Example:
    s = "abbaca"  -> "ca"
    s = "azxxzy"  -> "ay"

    Try to use:
    Push each char. If it matches stack[-1], pop instead of pushing.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 12: Backspace String Compare
# ============================================================

def backspace_compare(s, t):
    """
    In words:

    The character '#' acts as a backspace. Return True if s and t
    represent the same final string.

    Example:
    s = "ab#c", t = "ad#c"   -> True   (both become "ac")
    s = "a##c", t = "#a#c"   -> True   (both become "c")
    s = "a#c",  t = "b"      -> False

    Try to use:
    Build each final string with a stack, then compare.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 13: Decode String
# ============================================================

def decode_string(s):
    """
    In words:

    Decode a string in the form k[encoded], where the encoded part is
    repeated k times. The encoding can be nested.

    Example:
    s = "3[a]2[bc]"       -> "aaabcbc"
    s = "3[a2[c]]"        -> "accaccacc"
    s = "2[abc]3[cd]ef"   -> "abcabccdcdcdef"

    Try to use:
    Two stacks (or a single stack of pairs): one for counts,
    one for the partial string before each '['.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 14: Validate Push Pop Sequence
# ============================================================

def validate_push_pop(pushed, popped):
    """
    In words:

    Return True if popped is a possible pop-order for the elements
    given in pushed, assuming each value is pushed in pushed order
    and may be popped at any time.

    Example:
    pushed = [1, 2, 3, 4, 5]
    popped = [4, 5, 3, 2, 1]   -> True

    pushed = [1, 2, 3, 4, 5]
    popped = [4, 3, 5, 1, 2]   -> False

    Try to use:
    Simulate with a stack and a pointer into popped.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 15: Sort A Stack
# ============================================================

def sort_stack(stack):
    """
    In words:

    Sort the input stack so the smallest value is on top.
    Return the stack as a list (bottom on the left, top on the right).

    You may use only one extra stack and basic stack operations.

    Example:
    stack = [3, 1, 4, 1, 5, 2]

    Return:
    [5, 4, 3, 2, 1, 1]

    Important:
    Do not call sorted() on the whole input.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 16: Simplify Unix Path
# ============================================================

def simplify_path(path):
    """
    In words:

    Given an absolute Unix-style path, return its canonical form.

    Rules:
    - "." means current directory (skip).
    - ".." means go up one level (pop).
    - Multiple "/" collapse to a single "/".
    - The result must start with "/" and must not end with "/" unless it is "/".

    Example:
    path = "/home/"           -> "/home"
    path = "/../"             -> "/"
    path = "/home//foo/"      -> "/home/foo"
    path = "/a/./b/../../c/"  -> "/c"
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 17: Asteroid Collision
# ============================================================

def asteroid_collision(asteroids):
    """
    In words:

    Each integer represents an asteroid. Positive = right, negative = left.
    Two asteroids collide only when one is positive (on stack) and the
    next is negative. The smaller in absolute value explodes; if equal,
    both explode.

    Return the surviving asteroids in order.

    Example:
    [5, 10, -5]    -> [5, 10]
    [8, -8]        -> []
    [10, 2, -5]    -> [10]
    [-2, -1, 1, 2] -> [-2, -1, 1, 2]

    Try to use:
    A stack; push on top, then resolve collisions in a while-loop.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 18: Trapping Rain Water
# ============================================================

def trap_rain_water(heights):
    """
    In words:

    Each bar has width 1. Return the total water that can be trapped
    between the bars after raining.

    Example:
    heights = [0,1,0,2,1,0,1,3,2,1,2,1]
    Return: 6

    heights = [4,2,0,3,2,5]
    Return: 9

    Try to use:
    A decreasing monotonic stack of indices. Each time the new bar is
    taller than the top, pop and add a horizontal slab of water.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 19: Stock Span
# ============================================================

def stock_span(prices):
    """
    In words:

    For each day i, return how many consecutive days up to and
    including i had a price less than or equal to prices[i].

    Example:
    prices = [100, 80, 60, 70, 60, 75, 85]

    Return:
    [1, 1, 1, 2, 1, 4, 6]

    Try to use:
    A decreasing monotonic stack of (price, span) pairs.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 20: Mixed Final Drill - Browser History
# ============================================================

def browser_history(ops):
    """
    In words:

    Simulate a browser using two stacks: a "back" stack and a "forward" stack.
    The current page is tracked separately.

    Process the operations in order. Each operation is one of:

    ("visit", url)   navigate to a new page; this clears forward.
    ("back",  k)     go back up to k steps; return the current url.
    ("forward", k)   go forward up to k steps; return the current url.
    ("current",)     return the current url without moving.

    Return a list with the result of every operation that has a result
    (back, forward, current), in order.

    Example:
    ops = [
        ("visit", "a"),
        ("visit", "b"),
        ("visit", "c"),
        ("back", 1),       -> "b"
        ("back", 5),       -> "a"
        ("forward", 1),    -> "b"
        ("visit", "d"),
        ("forward", 2),    -> "d"
        ("current",),      -> "d"
    ]

    Return:
    ["b", "a", "b", "d", "d"]
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
        "Exercise 1: Push and Pop",
        "Push every value, then pop everything and return the pop order.",
        push_pop_sequence([1, 2, 3]),
        [3, 2, 1],
    )

    peek_result = peek([1, 2, 3])
    if peek_result is NOT_IMPLEMENTED:
        peek_actual = NOT_IMPLEMENTED
    else:
        peek_actual = (peek([1, 2, 3]), peek([]))
    check(
        "Exercise 2: Peek",
        "Return top of stack, or None if empty.",
        peek_actual,
        (3, None),
    )

    check(
        "Exercise 3: Reverse a String Using a Stack",
        "Reverse the string using stack operations.",
        reverse_string("hello"),
        "olleh",
    )

    parens_result = is_valid_parens("([]{})")
    if parens_result is NOT_IMPLEMENTED:
        parens_actual = NOT_IMPLEMENTED
    else:
        parens_actual = (
            is_valid_parens("([]{})"),
            is_valid_parens("([)]"),
            is_valid_parens("("),
            is_valid_parens(""),
        )
    check(
        "Exercise 4: Valid Parentheses",
        "Return True if brackets are properly matched and nested.",
        parens_actual,
        (True, False, False, True),
    )

    bin_result = to_binary(0)
    if bin_result is NOT_IMPLEMENTED:
        bin_actual = NOT_IMPLEMENTED
    else:
        bin_actual = (to_binary(0), to_binary(1), to_binary(5), to_binary(13))
    check(
        "Exercise 5: Decimal To Binary",
        "Convert n to binary string using a stack of remainders.",
        bin_actual,
        ("0", "1", "101", "1101"),
    )

    rpn_result = eval_rpn(["2", "1", "+", "3", "*"])
    if rpn_result is NOT_IMPLEMENTED:
        rpn_actual = NOT_IMPLEMENTED
    else:
        rpn_actual = (
            eval_rpn(["2", "1", "+", "3", "*"]),
            eval_rpn(["4", "13", "5", "/", "+"]),
        )
    check(
        "Exercise 6: Reverse Polish Notation",
        "Evaluate an RPN expression with +, -, *, / (truncated).",
        rpn_actual,
        (9, 6),
    )

    check(
        "Exercise 7: Next Greater Element",
        "For each i return next strictly greater value to the right, or -1.",
        next_greater([2, 1, 3, 0, 4]),
        [3, 3, 4, 4, -1],
    )

    check(
        "Exercise 8: Daily Temperatures",
        "Days to wait until a strictly warmer day; 0 if never.",
        daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]),
        [1, 1, 4, 2, 1, 1, 0, 0],
    )

    rect_result = largest_rectangle([2, 1, 5, 6, 2, 3])
    if rect_result is NOT_IMPLEMENTED:
        rect_actual = NOT_IMPLEMENTED
    else:
        rect_actual = (largest_rectangle([2, 1, 5, 6, 2, 3]), largest_rectangle([2, 4]))
    check(
        "Exercise 9: Largest Rectangle In Histogram",
        "Largest rectangle formed by contiguous bars of width 1.",
        rect_actual,
        (10, 4),
    )

    check(
        "Exercise 10: Min Stack",
        "Simulate a stack with O(1) getMin via a second mins stack.",
        min_stack_ops([
            ("push", 3), ("push", 5), ("min",),
            ("push", 2), ("min",),
            ("pop",), ("top",), ("min",),
        ]),
        [3, 2, 5, 3],
    )

    rm_result = remove_adjacent_duplicates("abbaca")
    if rm_result is NOT_IMPLEMENTED:
        rm_actual = NOT_IMPLEMENTED
    else:
        rm_actual = (
            remove_adjacent_duplicates("abbaca"),
            remove_adjacent_duplicates("azxxzy"),
        )
    check(
        "Exercise 11: Remove Adjacent Duplicates",
        "Repeatedly remove equal adjacent pairs until none remain.",
        rm_actual,
        ("ca", "ay"),
    )

    bs_result = backspace_compare("ab#c", "ad#c")
    if bs_result is NOT_IMPLEMENTED:
        bs_actual = NOT_IMPLEMENTED
    else:
        bs_actual = (
            backspace_compare("ab#c", "ad#c"),
            backspace_compare("a##c", "#a#c"),
            backspace_compare("a#c", "b"),
        )
    check(
        "Exercise 12: Backspace String Compare",
        "Compare strings after applying '#' as a backspace.",
        bs_actual,
        (True, True, False),
    )

    dec_result = decode_string("3[a]2[bc]")
    if dec_result is NOT_IMPLEMENTED:
        dec_actual = NOT_IMPLEMENTED
    else:
        dec_actual = (
            decode_string("3[a]2[bc]"),
            decode_string("3[a2[c]]"),
            decode_string("2[abc]3[cd]ef"),
        )
    check(
        "Exercise 13: Decode String",
        "Decode k[encoded] with arbitrary nesting.",
        dec_actual,
        ("aaabcbc", "accaccacc", "abcabccdcdcdef"),
    )

    vp_result = validate_push_pop([1, 2, 3, 4, 5], [4, 5, 3, 2, 1])
    if vp_result is NOT_IMPLEMENTED:
        vp_actual = NOT_IMPLEMENTED
    else:
        vp_actual = (
            validate_push_pop([1, 2, 3, 4, 5], [4, 5, 3, 2, 1]),
            validate_push_pop([1, 2, 3, 4, 5], [4, 3, 5, 1, 2]),
        )
    check(
        "Exercise 14: Validate Push Pop Sequence",
        "Check whether popped is a valid pop order for pushed.",
        vp_actual,
        (True, False),
    )

    check(
        "Exercise 15: Sort A Stack",
        "Sort the stack with smallest on top using one auxiliary stack.",
        sort_stack([3, 1, 4, 1, 5, 2]),
        [5, 4, 3, 2, 1, 1],
    )

    sp_result = simplify_path("/home/")
    if sp_result is NOT_IMPLEMENTED:
        sp_actual = NOT_IMPLEMENTED
    else:
        sp_actual = (
            simplify_path("/home/"),
            simplify_path("/../"),
            simplify_path("/home//foo/"),
            simplify_path("/a/./b/../../c/"),
        )
    check(
        "Exercise 16: Simplify Unix Path",
        "Return canonical absolute path.",
        sp_actual,
        ("/home", "/", "/home/foo", "/c"),
    )

    ast_result = asteroid_collision([5, 10, -5])
    if ast_result is NOT_IMPLEMENTED:
        ast_actual = NOT_IMPLEMENTED
    else:
        ast_actual = (
            asteroid_collision([5, 10, -5]),
            asteroid_collision([8, -8]),
            asteroid_collision([10, 2, -5]),
            asteroid_collision([-2, -1, 1, 2]),
        )
    check(
        "Exercise 17: Asteroid Collision",
        "Simulate asteroid collisions; return survivors in order.",
        ast_actual,
        ([5, 10], [], [10], [-2, -1, 1, 2]),
    )

    trap_result = trap_rain_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])
    if trap_result is NOT_IMPLEMENTED:
        trap_actual = NOT_IMPLEMENTED
    else:
        trap_actual = (
            trap_rain_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]),
            trap_rain_water([4, 2, 0, 3, 2, 5]),
        )
    check(
        "Exercise 18: Trapping Rain Water",
        "Compute total trapped water using a monotonic stack.",
        trap_actual,
        (6, 9),
    )

    check(
        "Exercise 19: Stock Span",
        "Span of consecutive days with price <= today's price.",
        stock_span([100, 80, 60, 70, 60, 75, 85]),
        [1, 1, 1, 2, 1, 4, 6],
    )

    check(
        "Exercise 20: Mixed Final Drill - Browser History",
        "Two-stack browser with visit / back / forward / current.",
        browser_history([
            ("visit", "a"),
            ("visit", "b"),
            ("visit", "c"),
            ("back", 1),
            ("back", 5),
            ("forward", 1),
            ("visit", "d"),
            ("forward", 2),
            ("current",),
        ]),
        ["b", "a", "b", "d", "d"],
    )


if __name__ == "__main__":
    run_all_exercises()
