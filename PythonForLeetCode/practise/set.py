"""

set()        create empty set (NOT {})
{}           empty dict, not set
{1, 2, 3}    set literal
{x for ...}  set comprehension

add          insert one element
discard      remove if present (no error)
remove       remove (raises KeyError if missing)
pop          remove and return arbitrary element
update       in-place union with iterable
clear        empty the set

|   union
&   intersection
-   difference
^   symmetric difference

|=  in-place union
&=  in-place intersection
-=  in-place difference
^=  in-place sym diff

in            O(1) membership
issubset      set <= other
issuperset    set >= other
isdisjoint    no common elements

frozenset     hashable, immutable, usable as dict key

Input convention for these exercises:
- Most exercises receive a set directly (parameter named s, a, b).
  Your job is to apply the set methods/operators listed above.
- A handful of exercises receive a list on purpose - when the point is
  list-to-set conversion (dedupe), or when "duplicates / order" only
  exist in a list. The docstring will say so explicitly.

"""

"""
Python Set Practice

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
# Exercise 1: Set Initialization
# ============================================================

def make_sets():
    """
    In words:

    Create four sets.

    1. a should be an empty set. (Use set(), not {}.)
    2. b should be {1, 2, 3}.
    3. c should be the set of unique characters in the string "banana".
    4. d should be the set of squares of 0..4 built with a set comprehension.

    Return them like this:
    return a, b, c, d

    Important:
    {} creates an empty dict, not an empty set.
    """

    a = set()
    b = {1, 2, 3}
    c = set("banana")
    d  = set(x*x for x in range(5))

    return a, b, c, d


# ============================================================
# Exercise 2: Add, Discard, Remove
# ============================================================

def add_discard_remove(s):
    """
    In words:

    You are given a set s.

    1. Add 100.
    2. Discard 999 (must not raise even though it is missing).
    3. Discard 1 (remove it if present).

    Return the resulting set sorted as a list (so the test is stable).

    Example:
    s = {1, 2, 3}

    Return:
    [2, 3, 100]

    Try to use:
    s.add, s.discard.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 3: Membership Test
# ============================================================

def has_value(s, target):
    """
    In words:

    Return True if target is in s, False otherwise.

    Example:
    s = {1, 2, 3}, target = 2   -> True
    s = {1, 2, 3}, target = 9   -> False

    Note:
    `in` on a set is O(1) average; on a list it is O(n). That is why
    this exercise takes a set.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 4: Union
# ============================================================

def union(a, b):
    """
    In words:

    Given two sets a and b, return their union as a sorted list.

    Example:
    a = {1, 2, 3}, b = {3, 4, 5}

    Return:
    [1, 2, 3, 4, 5]

    Try to use:
    a | b
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 5: Intersection
# ============================================================

def intersection(a, b):
    """
    In words:

    Given two sets a and b, return their intersection as a sorted list.

    Example:
    a = {1, 2, 3, 4}, b = {3, 4, 5}

    Return:
    [3, 4]

    Try to use:
    a & b
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 6: Difference
# ============================================================

def difference(a, b):
    """
    In words:

    Given two sets a and b, return the values in a but not in b
    as a sorted list.

    Example:
    a = {1, 2, 3, 4}, b = {3, 4, 5}

    Return:
    [1, 2]

    Try to use:
    a - b
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 7: Symmetric Difference
# ============================================================

def sym_difference(a, b):
    """
    In words:

    Given two sets a and b, return the values that are in exactly one
    of them as a sorted list.

    Example:
    a = {1, 2, 3, 4}, b = {3, 4, 5}

    Return:
    [1, 2, 5]

    Try to use:
    a ^ b
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 8: Subset, Superset, Disjoint
# ============================================================

def relation(a, b):
    """
    In words:

    Given two sets a and b, return a tuple of three booleans:

    (a is subset of b, a is superset of b, a and b are disjoint)

    Example:
    a = {1, 2}, b = {1, 2, 3}
    Return: (True, False, False)

    Example:
    a = {1, 2, 3}, b = {4, 5}
    Return: (False, False, True)

    Try to use:
    a <= b, a >= b, a.isdisjoint(b)
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 9: Deduplicate Preserving Order
# ============================================================

def dedupe_preserve_order(items):
    """
    In words:

    items is a list (order matters here).

    Return a new list with duplicates removed but the original order
    of first appearance preserved.

    Example:
    items = [3, 1, 2, 1, 3, 4]

    Return:
    [3, 1, 2, 4]

    Try to use:
    list(dict.fromkeys(items))

    Important:
    A plain set() does not preserve order. That is why this exercise
    takes a list, not a set.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 10: Find Duplicates
# ============================================================

def find_duplicates(items):
    """
    In words:

    items is a list (duplicates only exist in a list, not in a set).

    Return the values that appear more than once in items, as a sorted list.

    Example:
    items = [1, 2, 3, 2, 4, 3, 3]

    Return:
    [2, 3]

    Try to use:
    A "seen" set and a "dupes" set, walked in one pass.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 11: Two Sum Using Set
# ============================================================

def two_sum_exists(nums, target):
    """
    In words:

    nums is a list (the natural input shape for this algorithm).

    Return True if any two distinct values in nums sum to target,
    False otherwise.

    Example:
    nums = [2, 7, 11, 15], target = 9
    Return: True   (2 + 7)

    nums = [1, 2, 3], target = 10
    Return: False

    Try to use:
    Walk nums once, keep a "seen" set of values you have looked at,
    and check (target - current) in seen.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 12: Compare Two Lists As Sets
# ============================================================

def same_elements(a, b):
    """
    In words:

    a and b are lists (the function is "do these two lists match
    when viewed as sets?").

    Return True if a and b contain the same unique elements,
    regardless of order or duplicates. False otherwise.

    Example:
    a = [1, 2, 2, 3], b = [3, 1, 2]
    Return: True

    a = [1, 2, 3], b = [1, 2]
    Return: False
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 13: Frozen Set As Dict Key
# ============================================================

def group_by_unique_letters(words):
    """
    In words:

    words is a list of strings.

    Group them by the set of unique letters they contain.

    The grouping key must be a frozenset (because a regular set is not
    hashable and cannot be a dict key).

    Return a dict where each key is a frozenset and each value is the
    sorted list of matching words.

    Example:
    words = ["abc", "cab", "bca", "ab", "ba"]

    "abc", "cab", "bca" all share the same unique letters {a, b, c}.
    "ab", "ba" share the unique letters {a, b}.

    Return:
    {
        frozenset({"a", "b", "c"}): ["abc", "bca", "cab"],
        frozenset({"a", "b"}):       ["ab", "ba"],
    }
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 14: Update In Place
# ============================================================

def absorb(a, b):
    """
    In words:

    a is a set, b is any iterable.

    Update a in place with every element of b.
    Return the resulting set as a sorted list.

    Example:
    a = {1, 2}, b = [2, 3, 4]

    Return:
    [1, 2, 3, 4]

    Try to use:
    a.update(b)   or   a |= set(b)
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 15: Pop Arbitrary Element
# ============================================================

def pop_until_empty(s):
    """
    In words:

    You are given a set s.
    Repeatedly call s.pop() until s is empty.
    Return the popped elements in sorted order (the order of pops is
    not guaranteed, which is exactly the point of this exercise).

    Example:
    s = {3, 1, 2}

    Return:
    [1, 2, 3]

    Note:
    set.pop() removes and returns an arbitrary element.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 16: Count Unique Characters
# ============================================================

def unique_char_count(s):
    """
    In words:

    s is a string.

    Return the number of distinct characters in s.

    Example:
    s = "banana"

    Return:
    3

    Try to use:
    len(set(s))
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 17: Common Elements Across N Sets
# ============================================================

def common_in_all(sets):
    """
    In words:

    sets is a list of sets.

    Return the elements that appear in every set, as a sorted list.

    Example:
    sets = [
        {1, 2, 3, 4},
        {2, 3, 5},
        {0, 2, 3, 9},
    ]

    Return:
    [2, 3]

    Try to use:
    set.intersection(*sets)
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 18: Missing Number Using Set Difference
# ============================================================

def missing_number(nums, n):
    """
    In words:

    nums is a list that contains all integers from 0 to n except
    exactly one. Return the missing number.

    Example:
    nums = [0, 1, 3, 4], n = 4
    Return: 2

    Try to use:
    set(range(n + 1)) - set(nums)
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 19: Set Comprehension With Filter
# ============================================================

def even_squares(nums):
    """
    In words:

    nums is a list (may contain duplicates).

    Return a sorted list of the squares of the even numbers in nums.
    Squares must be unique (build them with a set comprehension).

    Example:
    nums = [1, 2, 2, 3, 4]

    Return:
    [4, 16]

    Try to use:
    {x * x for x in nums if x % 2 == 0}
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 20: Mixed Final Drill
# ============================================================

def compare_lists(a, b):
    """
    In words:

    a and b are lists.

    Return a dictionary with five things:

    {
        "only_a":       sorted list of values in a but not in b,
        "only_b":       sorted list of values in b but not in a,
        "both":         sorted list of values in both,
        "either":       sorted list of values in either,
        "count_unique": number of distinct values across a and b,
    }

    Example:
    a = [1, 2, 3, 3]
    b = [3, 4, 5]

    Return:
    {
        "only_a":       [1, 2],
        "only_b":       [4, 5],
        "both":         [3],
        "either":       [1, 2, 3, 4, 5],
        "count_unique": 5,
    }
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
        "Exercise 1: Set Initialization",
        "Create empty set, {1,2,3}, unique letters of 'banana', and squares 0..4 via comprehension.",
        make_sets(),
        (set(), {1, 2, 3}, {"b", "a", "n"}, {0, 1, 4, 9, 16}),
    )

    check(
        "Exercise 2: Add, Discard, Remove",
        "Given a set: add 100, discard missing 999, discard 1. Return sorted list.",
        add_discard_remove({1, 2, 3}),
        [2, 3, 100],
    )

    has_result = has_value({1, 2, 3}, 2)
    if has_result is NOT_IMPLEMENTED:
        has_actual = NOT_IMPLEMENTED
    else:
        has_actual = (has_value({1, 2, 3}, 2), has_value({1, 2, 3}, 9))
    check(
        "Exercise 3: Membership Test",
        "Return True if target is in s, else False.",
        has_actual,
        (True, False),
    )

    check(
        "Exercise 4: Union",
        "Return sorted list of the union of two sets via |.",
        union({1, 2, 3}, {3, 4, 5}),
        [1, 2, 3, 4, 5],
    )

    check(
        "Exercise 5: Intersection",
        "Return sorted list of the intersection of two sets via &.",
        intersection({1, 2, 3, 4}, {3, 4, 5}),
        [3, 4],
    )

    check(
        "Exercise 6: Difference",
        "Return sorted list of values in a but not in b via -.",
        difference({1, 2, 3, 4}, {3, 4, 5}),
        [1, 2],
    )

    check(
        "Exercise 7: Symmetric Difference",
        "Return sorted list of values in exactly one of a or b via ^.",
        sym_difference({1, 2, 3, 4}, {3, 4, 5}),
        [1, 2, 5],
    )

    rel_result = relation({1, 2}, {1, 2, 3})
    if rel_result is NOT_IMPLEMENTED:
        rel_actual = NOT_IMPLEMENTED
    else:
        rel_actual = (
            relation({1, 2}, {1, 2, 3}),
            relation({1, 2, 3}, {4, 5}),
        )
    check(
        "Exercise 8: Subset, Superset, Disjoint",
        "Return (is_subset, is_superset, is_disjoint) of two sets.",
        rel_actual,
        ((True, False, False), (False, False, True)),
    )

    check(
        "Exercise 9: Deduplicate Preserving Order",
        "Remove duplicates from a list but keep first-seen order.",
        dedupe_preserve_order([3, 1, 2, 1, 3, 4]),
        [3, 1, 2, 4],
    )

    check(
        "Exercise 10: Find Duplicates",
        "Return sorted list of values in a list that appear more than once.",
        find_duplicates([1, 2, 3, 2, 4, 3, 3]),
        [2, 3],
    )

    two_sum_result = two_sum_exists([2, 7, 11, 15], 9)
    if two_sum_result is NOT_IMPLEMENTED:
        two_sum_actual = NOT_IMPLEMENTED
    else:
        two_sum_actual = (
            two_sum_exists([2, 7, 11, 15], 9),
            two_sum_exists([1, 2, 3], 10),
        )
    check(
        "Exercise 11: Two Sum Using Set",
        "Return True if any two values in the list sum to target.",
        two_sum_actual,
        (True, False),
    )

    same_result = same_elements([1, 2, 2, 3], [3, 1, 2])
    if same_result is NOT_IMPLEMENTED:
        same_actual = NOT_IMPLEMENTED
    else:
        same_actual = (
            same_elements([1, 2, 2, 3], [3, 1, 2]),
            same_elements([1, 2, 3], [1, 2]),
        )
    check(
        "Exercise 12: Compare Two Lists As Sets",
        "Return True if two lists have the same unique elements.",
        same_actual,
        (True, False),
    )

    check(
        "Exercise 13: Frozen Set As Dict Key",
        "Group words by their frozenset of unique letters.",
        group_by_unique_letters(["abc", "cab", "bca", "ab", "ba"]),
        {
            frozenset({"a", "b", "c"}): ["abc", "bca", "cab"],
            frozenset({"a", "b"}): ["ab", "ba"],
        },
    )

    check(
        "Exercise 14: Update In Place",
        "Update set a with elements of iterable b in place, return sorted list.",
        absorb({1, 2}, [2, 3, 4]),
        [1, 2, 3, 4],
    )

    check(
        "Exercise 15: Pop Arbitrary Element",
        "Pop every element from a set until empty, return them sorted.",
        pop_until_empty({3, 1, 2}),
        [1, 2, 3],
    )

    check(
        "Exercise 16: Count Unique Characters",
        "Return the number of distinct characters in a string.",
        unique_char_count("banana"),
        3,
    )

    check(
        "Exercise 17: Common Elements Across N Sets",
        "Return sorted list of values that appear in every set.",
        common_in_all([{1, 2, 3, 4}, {2, 3, 5}, {0, 2, 3, 9}]),
        [2, 3],
    )

    check(
        "Exercise 18: Missing Number Using Set Difference",
        "Return the one missing number from 0..n given a list.",
        missing_number([0, 1, 3, 4], 4),
        2,
    )

    check(
        "Exercise 19: Set Comprehension With Filter",
        "Return sorted unique squares of even values in a list.",
        even_squares([1, 2, 2, 3, 4]),
        [4, 16],
    )

    check(
        "Exercise 20: Mixed Final Drill",
        "Compare two lists: only_a, only_b, both, either, count_unique.",
        compare_lists([1, 2, 3, 3], [3, 4, 5]),
        {
            "only_a": [1, 2],
            "only_b": [4, 5],
            "both": [3],
            "either": [1, 2, 3, 4, 5],
            "count_unique": 5,
        },
    )


if __name__ == "__main__":
    run_all_exercises()
