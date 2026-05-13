"""

=       assign
==      equal value
!=      not equal

{}              empty dict   (use set() for an empty set!)
{k: v}          dict literal
{x: y for ...}  dict comprehension

d[k]            indexed access  — raises KeyError if missing
d.get(k, def)   safe access     — returns default if missing
d.pop(k, def)   remove & return — safe form takes a default
d.setdefault(k, def)  return existing OR insert default

in              membership test on KEYS:  "k" in d
not in          opposite of in

**d             keyword-unpack a dict into a function call
**d1, **d2      merge dicts via unpacking  (works any version)
|               merge dicts (Python 3.9+)  — right wins on collision
|=              merge in place (3.9+)

d.items()       view of (key, value) pairs
d.keys()        view of keys
d.values()      view of values

max(d, key=d.get)               argmax over a dict
sorted(d.items(), key=...)      sort entries by a custom key
{k: v for k, v in d.items() if cond}    filter entries

defaultdict(int)    auto-init missing keys to 0  (counting)
defaultdict(list)   auto-init missing keys to [] (grouping)

"""

"""
Python Dict / Hashmap Practice

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


from collections import defaultdict


NOT_IMPLEMENTED = object()


# ============================================================
# Exercise 1: Dict Initialization
# ============================================================

def make_dicts():
    """
    In words:

    Create five dicts.

    1. a should be an empty dict.
    2. b should be {"a": 1, "b": 2, "c": 3} using a literal.
    3. c should be {"a": 1, "b": 2} using the dict(...) constructor with keyword args.
    4. d should be built by zipping ["x", "y", "z"] with [10, 20, 30].
    5. e should be {0: 0, 1: 1, 2: 4, 3: 9} built from a comprehension over range(4).

    Return them like this:
    return a, b, c, d, e

    Example return:
    (
        {},
        {"a": 1, "b": 2, "c": 3},
        {"a": 1, "b": 2},
        {"x": 10, "y": 20, "z": 30},
        {0: 0, 1: 1, 2: 4, 3: 9},
    )
    """
    a = {}
    b = { "a" : 1, "b" : 2, "c": 3}
    c = dict({"a" : 1, "b" : 2})
    d = dict(zip(["x", "y", "z"], [10,20,30]))
    e = dict((x, x*x) for x in range(4))
    return a, b, c, d, e


# ============================================================
# Exercise 2: Safe Lookup with .get
# ============================================================

def safe_lookup(d, keys):
    """
    In words:

    For every key in keys, look it up in d.

    If the key is missing, use 0 as the default (do NOT raise KeyError).

    Return a list of the looked-up values in the same order as keys.

    Try to use:
    d.get(k, 0)

    Example:
    d = {"a": 1, "b": 2}
    keys = ["a", "b", "x"]

    Return:
    [1, 2, 0]
    """
    return [d.get(x, 0) for x in keys ]


# ============================================================
# Exercise 3: Insert, Update, Delete
# ============================================================

def insert_update_delete():
    """
    In words:

    Start with d = {"a": 1, "b": 2}.

    1. Add a new key "c" with value 3.
    2. Update the value of "a" to 10.
    3. Remove the key "b" using pop. Capture the popped value.

    Return:
    1. The final dict.
    2. The value that was popped.

    Example return:
    ({"a": 10, "c": 3}, 2)
    """
    d = {"a": 1, "b": 2}
    d["c"]= 3;
    d["a"]= 10;
    x = d.pop("b");
    return d, x


# ============================================================
# Exercise 4: Invert Dict (Swap Keys and Values)
# ============================================================

def invert_dict(d):
    """
    In words:

    Return a new dict where each (key, value) pair becomes (value, key).

    Assume the values in d are all unique.

    Try to use:
    a dict comprehension over d.items()

    Example:
    d = {"a": 1, "b": 2, "c": 3}

    Return:
    {1: "a", 2: "b", 3: "c"}
    """
    return {v: k for k, v in d.items()}


# ============================================================
# Exercise 5: Merge Two Dicts (Second Wins)
# ============================================================

def merge_dicts(d1, d2):
    """
    In words:

    Merge d1 and d2 into a new dict.

    If a key exists in both, the value from d2 wins.

    Do NOT mutate d1 or d2.

    Try to use:
    {**d1, **d2}      (works any Python version)
    or
    d1 | d2           (Python 3.9+)

    Example:
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 99, "c": 3}

    Return:
    {"a": 1, "b": 99, "c": 3}
    """

    # YOUR CODE HERE

    return d1 | d2


# ============================================================
# Exercise 5b: Merge In Place (|=)
# ============================================================

def merge_in_place(d1, d2):
    """
    In words:

    Merge d2 INTO d1, mutating d1 in place.

    If a key exists in both, the value from d2 wins.

    Do NOT build a new dict. d1 should be the SAME object after,
    just with extra / overwritten entries.

    Try to use:
    d1 |= d2          (Python 3.9+, the in-place merge operator)
    or
    d1.update(d2)     (works any version, same effect)

    Return d1 (the same object you mutated).

    Example:
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 99, "c": 3}

    After the merge:
    d1 is now {"a": 1, "b": 99, "c": 3}
    d2 is still {"b": 99, "c": 3}

    Return:
    {"a": 1, "b": 99, "c": 3}

    Note:
    This is the "I own d1, just update it" pattern.
    Compare to Exercise 5 (merge_dicts) which BUILDS A NEW dict
    and leaves both inputs untouched.
    """

    # YOUR CODE HERE
    d1 |= d2
    return d1


# ============================================================
# Exercise 6: Squares Dict (Comprehension)
# ============================================================

def squares_dict(nums):
    """
    In words:

    Build a dict that maps each number in nums to its square.

    Try to use:
    {x: x * x for x in nums}

    Example:
    nums = [1, 2, 3, 4]

    Return:
    {1: 1, 2: 4, 3: 9, 4: 16}
    """
    return { x: x*x for x in nums}


# ============================================================
# Exercise 7: Filter Entries by Value
# ============================================================

def filter_by_value(d, threshold):
    """
    In words:

    Return a new dict containing only the entries whose value
    is strictly greater than threshold.

    Try to use:
    {k: v for k, v in d.items() if v > threshold}

    Example:
    d = {"a": 1, "b": 5, "c": 3}
    threshold = 2

    Return:
    {"b": 5, "c": 3}
    """
    return {x: y for x, y in d.items() if y > threshold}


# ============================================================
# Exercise 8: Keys with the Maximum Value
# ============================================================

def keys_with_max_value(d):
    """
    In words:

    Find the largest value in d.

    Return a list of every key whose value equals that largest value.

    Sort the returned list so the answer is deterministic.

    Example:
    d = {"a": 1, "b": 3, "c": 3}

    The largest value is 3.
    Keys with value 3 are "b" and "c".

    Return:
    ["b", "c"]
    """
    maxval = max(d.values())
    return [x for x, y in d.items() if y == maxval]  


# ============================================================
# Exercise 9: Build Dict from a List of Pairs
# ============================================================

def from_pairs(pairs):
    """
    In words:

    Given a list of (key, value) tuples, build a single dict.

    If the same key appears more than once, the LATER pair wins.

    Try to use:
    dict(pairs)

    Example:
    pairs = [("a", 1), ("b", 2), ("a", 10)]

    The key "a" appears twice. The later value 10 should win.

    Return:
    {"a": 10, "b": 2}
    """
    return dict({x[0]:x[1] for x in pairs})


# ============================================================
# Exercise 10: Count Characters in a String
# ============================================================
from collections import Counter
def count_chars(s):
    """
    In words:

    Count how many times each character appears in the string s.

    Return a dict mapping character -> count.

    Try to use this classic pattern:
    counts[ch] = counts.get(ch, 0) + 1

    Example:
    s = "banana"

    Return:
    {"b": 1, "a": 3, "n": 2}
    """
    return Counter(s)


# ============================================================
# Exercise 11: Group Words by First Letter
# ============================================================

def group_by_first_letter(words):
    """
    In words:

    Group the words by their first letter.

    Return a dict where the key is the first letter and the value is
    a list of all words that start with that letter, in the order
    they appeared in the input.

    Try to use:
    groups.setdefault(letter, []).append(word)

    Example:
    words = ["apple", "ant", "bee", "banana"]

    Return:
    {"a": ["apple", "ant"], "b": ["bee", "banana"]}
    """
    count = {}
    for word in words:
        count.setdefault(word[0], []).append(word)
    return count


# ============================================================
# Exercise 12: Count with defaultdict(int)
# ============================================================

def defaultdict_count(s):
    """
    In words:

    Same task as Exercise 10 (count characters in s),
    but use collections.defaultdict(int) instead of .get(ch, 0).

    Notice how the body becomes shorter:
    counts[ch] += 1

    Return a regular dict (you can convert with dict(...) at the end,
    or just return the defaultdict — it compares equal to a regular dict).

    Example:
    s = "banana"

    Return:
    {"b": 1, "a": 3, "n": 2}
    """

    d = defaultdict(int)
    for ch in s:
        d[ch] = d[ch] + 1
    return d


# ============================================================
# Exercise 13: The fromkeys Trap (Independent Lists per Key)
# ============================================================

def fromkeys_trap():
    """
    In words:

    Build a dict where the keys are "a", "b", "c"
    and each value is its OWN independent empty list.

    Then append 1 to the list stored at key "a".

    Important:
    Do NOT use dict.fromkeys(["a","b","c"], []) — that shares ONE list
    across all keys, so appending to "a" would mutate "b" and "c" too.

    Use a dict comprehension to give each key its own fresh list:
        {k: [] for k in keys}

    After appending 1 only to "a", the other two keys should still
    point to empty lists.

    Return the final dict.

    Example return:
    {"a": [1], "b": [], "c": []}
    """
    d = dict({k:[] for k in ["a", "b", "c"]})
    d["a"].append(1)
    return d


# ============================================================
# Exercise 14: Sort Entries by Value Descending
# ============================================================

def sort_by_value_desc(d):
    """
    In words:

    Return a list of (key, value) tuples sorted by:
    1. value descending (largest first)
    2. key ascending as the tiebreaker (alphabetical when values tie)

    Try to use:
    sorted(d.items(), key=lambda x: (-x[1], x[0]))

    Example:
    d = {"a": 1, "b": 3, "c": 3}

    Values 3 and 3 tie, so "b" and "c" are sorted alphabetically.
    Value 1 comes last.

    Return:
    [("b", 3), ("c", 3), ("a", 1)]
    """
    return sorted(d.items(), key = lambda x: (-x[1], x[0]))


# ============================================================
# Exercise 15: Key With the Largest Value (argmax)
# ============================================================

def argmax_key(d):
    """
    In words:

    Return the key whose value is the largest.

    If multiple keys tie for the largest, you may return any of them.
    For this exercise, the test uses a dict with a unique max so
    there is no ambiguity.

    Try to use:
    max(d, key=d.get)

    Example:
    d = {"a": 1, "b": 5, "c": 3}

    The largest value is 5, at key "b".

    Return:
    "b"
    """
    return max(d, key=d.get)


# ============================================================
# Exercise 16: Iterate Keys, Values, and Items
# ============================================================

def dict_iteration(d):
    """
    In words:

    Given a dict d, return three things:
    1. A SORTED list of the keys.
    2. A SORTED list of the values.
    3. A list of (key, value) pairs, sorted by key.

    Try to use:
    d.keys(), d.values(), d.items()

    Example:
    d = {"b": 2, "a": 1, "c": 3}

    Return:
    (
        ["a", "b", "c"],
        [1, 2, 3],
        [("a", 1), ("b", 2), ("c", 3)],
    )
    """
    return sorted(d.keys(), key = lambda d: d), sorted(d.values(), key = lambda d: d), sorted(d.items(), key = lambda d : (d[0], d[1]))


# ============================================================
# Exercise 17: Word Frequencies in a List
# ============================================================
from collections import Counter
def word_frequencies(words):
    """
    In words:

    Given a list of words, return a dict mapping each word to
    how many times it appears in the list.

    This is the classic "build a histogram from a list" pattern.

    Example:
    words = ["the", "cat", "sat", "on", "the", "mat"]

    "the" appears 2 times. The rest appear once.

    Return:
    {"the": 2, "cat": 1, "sat": 1, "on": 1, "mat": 1}
    """
    c = Counter(words)
    return c


# ============================================================
# Exercise 18: Find Duplicates in a List
# ============================================================

def find_duplicates(nums):
    """
    In words:

    Given a list of integers, return a SORTED list of every value
    that appears more than once.

    Steps that usually work:
    1. Build a count dict from nums.
    2. Filter the keys whose count is > 1.
    3. Sort the result so the answer is deterministic.

    Example:
    nums = [1, 2, 3, 2, 4, 1, 5, 1]

    Counts:
    1 -> 3, 2 -> 2, 3 -> 1, 4 -> 1, 5 -> 1

    Values appearing more than once: 1 and 2.

    Return:
    [1, 2]
    """
    c = Counter(nums)
    return [x for x, y in c.items() if y > 1]


# ============================================================
# Exercise 19: Two Sum (Indices, O(n) with a Dict)
# ============================================================

def two_sum_indices(nums, target):
    """
    In words:

    Given a list nums and an integer target, find two distinct indices
    i and j (with i < j) such that nums[i] + nums[j] == target.

    If no such pair exists, return (-1, -1).

    The O(n) trick is to walk the list once and remember every value
    you have already seen in a dict:
        seen[value_we_already_saw] = its_index

    For each new value v at index j, check whether (target - v) is in
    seen. If yes, you have your pair (seen[target - v], j).

    Example:
    nums = [2, 7, 11, 15]
    target = 9

    2 + 7 == 9, found at indices 0 and 1.

    Return:
    (0, 1)

    Example with no answer:
    nums = [1, 2, 3]
    target = 100

    Return:
    (-1, -1)
    """

    c = {}
    for i, v in enumerate(nums):
        if target - v in c:
            return c[target - v], i
        else:
            c[v] = i

    return -1, -1


# ============================================================
# Exercise 20: Mixed Final Drill — Analyze Records
# ============================================================

def analyze_records(records):
    """
    In words:

    You are given a list of records. Each record is a tuple:
        (name, age, city)

    Build and return a dict with four entries:

    {
        "count_by_city":
            dict mapping city -> number of records in that city,

        "max_age_by_name":
            dict mapping name -> the LARGEST age seen for that name,

        "names_in_ny":
            SORTED list of unique names whose city is "ny",

        "oldest":
            the single record (tuple) with the largest age overall,
    }

    Example:
    records = [
        ("alice", 25, "ny"),
        ("bob",   30, "sf"),
        ("alice", 35, "ny"),
        ("carol", 30, "ny"),
    ]

    Working it out:
    - count_by_city:
          "ny" appears 3 times, "sf" appears 1 time
          -> {"ny": 3, "sf": 1}

    - max_age_by_name:
          alice ages are 25 and 35, max is 35
          bob age is 30
          carol age is 30
          -> {"alice": 35, "bob": 30, "carol": 30}

    - names_in_ny:
          names whose city is "ny" are alice, alice, carol
          unique + sorted -> ["alice", "carol"]

    - oldest:
          largest age is 35, that record is ("alice", 35, "ny")

    Return:
    {
        "count_by_city":   {"ny": 3, "sf": 1},
        "max_age_by_name": {"alice": 35, "bob": 30, "carol": 30},
        "names_in_ny":     ["alice", "carol"],
        "oldest":          ("alice", 35, "ny"),
    }
    """
    max_age_by_name = {}
    for name, age, city in records:
        max_age_by_name[name] = max(age, max_age_by_name.get(name, age))

    a = {
        "count_by_city" : Counter(city for name, age, city in records),
        "max_age_by_name": max({name: age for name, age, city in records}, key 
        "names_in_ny": 0,
        "oldest" : 0
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
        "Exercise 1: Dict Initialization",
        "Create an empty dict, a literal, dict(a=1,b=2), zip-built, and a comprehension.",
        make_dicts(),
        (
            {},
            {"a": 1, "b": 2, "c": 3},
            {"a": 1, "b": 2},
            {"x": 10, "y": 20, "z": 30},
            {0: 0, 1: 1, 2: 4, 3: 9},
        ),
    )

    check(
        "Exercise 2: Safe Lookup with .get",
        "Use d.get(k, 0) so missing keys return 0 instead of raising.",
        safe_lookup({"a": 1, "b": 2}, ["a", "b", "x"]),
        [1, 2, 0],
    )

    check(
        "Exercise 3: Insert, Update, Delete",
        "Start from {'a':1,'b':2}, add 'c':3, set 'a'=10, pop 'b'. Return (dict, popped).",
        insert_update_delete(),
        ({"a": 10, "c": 3}, 2),
    )

    check(
        "Exercise 4: Invert Dict",
        "Swap keys and values using a dict comprehension over d.items().",
        invert_dict({"a": 1, "b": 2, "c": 3}),
        {1: "a", 2: "b", 3: "c"},
    )

    check(
        "Exercise 5: Merge Two Dicts (Second Wins)",
        "Use {**d1, **d2} or d1 | d2 — colliding key takes value from d2.",
        merge_dicts({"a": 1, "b": 2}, {"b": 99, "c": 3}),
        {"a": 1, "b": 99, "c": 3},
    )

    # Exercise 5b: must mutate d1 in place AND return it (so we can verify both)
    d1_for_5b = {"a": 1, "b": 2}
    d2_for_5b = {"b": 99, "c": 3}
    returned_5b = merge_in_place(d1_for_5b, d2_for_5b)
    if returned_5b is NOT_IMPLEMENTED:
        actual_5b = NOT_IMPLEMENTED
    else:
        # Pack three things: the returned value, the (mutated) d1, the (untouched) d2
        actual_5b = (returned_5b, d1_for_5b, d2_for_5b)
    check(
        "Exercise 5b: Merge In Place (|=)",
        "Mutate d1 with d2 (use d1 |= d2 or d1.update(d2)). d1 must change; d2 must not. Return d1.",
        actual_5b,
        (
            {"a": 1, "b": 99, "c": 3},
            {"a": 1, "b": 99, "c": 3},
            {"b": 99, "c": 3},
        ),
    )

    check(
        "Exercise 6: Squares Dict",
        "Comprehension {x: x*x for x in nums}.",
        squares_dict([1, 2, 3, 4]),
        {1: 1, 2: 4, 3: 9, 4: 16},
    )

    check(
        "Exercise 7: Filter by Value",
        "Keep only entries whose value > threshold.",
        filter_by_value({"a": 1, "b": 5, "c": 3}, 2),
        {"b": 5, "c": 3},
    )

    check(
        "Exercise 8: Keys with Max Value",
        "Return sorted list of every key whose value equals the largest value.",
        keys_with_max_value({"a": 1, "b": 3, "c": 3}),
        ["b", "c"],
    )

    check(
        "Exercise 9: Build Dict from Pairs",
        "dict(pairs) — later pair wins on duplicate keys.",
        from_pairs([("a", 1), ("b", 2), ("a", 10)]),
        {"a": 10, "b": 2},
    )

    check(
        "Exercise 10: Count Characters",
        "Classic counts[ch] = counts.get(ch, 0) + 1 pattern.",
        count_chars("banana"),
        {"b": 1, "a": 3, "n": 2},
    )

    check(
        "Exercise 11: Group Words by First Letter",
        "Use setdefault(letter, []).append(word).",
        group_by_first_letter(["apple", "ant", "bee", "banana"]),
        {"a": ["apple", "ant"], "b": ["bee", "banana"]},
    )

    defaultdict_result = defaultdict_count("banana")
    if defaultdict_result is not NOT_IMPLEMENTED:
        defaultdict_result = dict(defaultdict_result)
    check(
        "Exercise 12: Count with defaultdict(int)",
        "Same as Exercise 10 but with collections.defaultdict(int) — body becomes counts[ch] += 1.",
        defaultdict_result,
        {"b": 1, "a": 3, "n": 2},
    )

    check(
        "Exercise 13: fromkeys Trap (Independent Lists)",
        "Use {k: [] for k in keys} so each value is its OWN list. Append 1 only to 'a'.",
        fromkeys_trap(),
        {"a": [1], "b": [], "c": []},
    )

    check(
        "Exercise 14: Sort by Value Desc, Key Asc",
        "sorted(d.items(), key=lambda x: (-x[1], x[0])).",
        sort_by_value_desc({"a": 1, "b": 3, "c": 3}),
        [("b", 3), ("c", 3), ("a", 1)],
    )

    check(
        "Exercise 15: Argmax Key",
        "max(d, key=d.get) returns the key with the largest value.",
        argmax_key({"a": 1, "b": 5, "c": 3}),
        "b",
    )

    check(
        "Exercise 16: Iterate Keys, Values, Items",
        "Return sorted keys, sorted values, and items sorted by key.",
        dict_iteration({"b": 2, "a": 1, "c": 3}),
        (
            ["a", "b", "c"],
            [1, 2, 3],
            [("a", 1), ("b", 2), ("c", 3)],
        ),
    )

    check(
        "Exercise 17: Word Frequencies",
        "Build {word: count} from a list of words.",
        word_frequencies(["the", "cat", "sat", "on", "the", "mat"]),
        {"the": 2, "cat": 1, "sat": 1, "on": 1, "mat": 1},
    )

    check(
        "Exercise 18: Find Duplicates",
        "Return SORTED list of values that appear more than once in nums.",
        find_duplicates([1, 2, 3, 2, 4, 1, 5, 1]),
        [1, 2],
    )

    check(
        "Exercise 19: Two Sum Indices (O(n) with a dict)",
        "Return (i, j) with i < j and nums[i] + nums[j] == target, or (-1, -1).",
        (
            two_sum_indices([2, 7, 11, 15], 9),
            two_sum_indices([1, 2, 3], 100),
        )
        if two_sum_indices([2, 7, 11, 15], 9) is not NOT_IMPLEMENTED
        else NOT_IMPLEMENTED,
        ((0, 1), (-1, -1)),
    )

    check(
        "Exercise 20: Analyze Records (Mixed Final Drill)",
        "Build count_by_city, max_age_by_name, sorted unique names_in_ny, and the oldest record.",
        analyze_records([
            ("alice", 25, "ny"),
            ("bob",   30, "sf"),
            ("alice", 35, "ny"),
            ("carol", 30, "ny"),
        ]),
        {
            "count_by_city":   {"ny": 3, "sf": 1},
            "max_age_by_name": {"alice": 35, "bob": 30, "carol": 30},
            "names_in_ny":     ["alice", "carol"],
            "oldest":          ("alice", 35, "ny"),
        },
    )


if __name__ == "__main__":
    run_all_exercises()
