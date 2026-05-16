"""

from collections import Counter, defaultdict

Counter is a dict subclass for counting hashable items.

Counter(iterable)       count occurrences in any iterable
Counter(mapping)        copy a {key: count} dict
Counter(a=2, b=3)       keyword form

c[key]                   count for key (0 if missing, no KeyError)
c.most_common(n)         list of (key, count) by count desc, ties by insertion order
c.elements()             iterator that yields each key count times
c.update(it_or_mapping)  add counts (NOT replace, unlike dict.update)
c.subtract(other)        subtract counts (can produce zeros and negatives)
+c                       drop zero and negative counts

Multiset arithmetic (keeps only positive counts):
c1 + c2     add counts
c1 - c2     subtract; non-positive dropped
c1 & c2     min of each key (intersection)
c1 | c2     max of each key (union)

defaultdict(factory):
  d[k] auto-creates factory() on miss; great for grouping.
  defaultdict(list)  -> grouping
  defaultdict(int)   -> counting
  defaultdict(set)   -> unique-bucket grouping

Important:
- Counter is best for frequencies and multisets.
- For grouping where the value is a collection of items, use defaultdict.

"""

"""
Python Counter / DefaultDict Practice

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

from collections import Counter, defaultdict


NOT_IMPLEMENTED = object()


# ============================================================
# Exercise 1: Counter From Iterable
# ============================================================

def count_iterable(items):
    """
    In words:

    Return a Counter built from items (a list or string).

    Example:
    items = "banana"
    Return: Counter({"a": 3, "n": 2, "b": 1})

    items = [1, 1, 2, 3, 3, 3]
    Return: Counter({3: 3, 1: 2, 2: 1})

    Note:
    The test compares with == so the underlying dict equality is enough.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 2: Counter From Mapping And Kwargs
# ============================================================

def counter_constructors():
    """
    In words:

    Return a tuple (from_mapping, from_kwargs):

    from_mapping = Counter built from the dict {"a": 4, "b": 2}
    from_kwargs  = Counter built from keyword arguments a=4, b=2

    The two should compare equal.

    Return:
    (Counter({"a": 4, "b": 2}), Counter({"a": 4, "b": 2}))
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 3: most_common
# ============================================================

def top_n(items, n):
    """
    In words:

    Return the n most common items as a list of (item, count) pairs in
    descending count order.

    Example:
    items = "aabbbccccd", n = 2
    Return: [("c", 4), ("b", 3)]

    items = [1, 1, 1, 2, 2, 3], n = 5
    Return: [(1, 3), (2, 2), (3, 1)]    (only 3 distinct items exist)
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 4: Counter Arithmetic - Add And Subtract
# ============================================================

def counter_add_subtract(a, b):
    """
    In words:

    Return a tuple (a + b, a - b) where a and b are iterables converted
    to Counters and + / - is multiset arithmetic.

    Remember: a - b drops zero and negative counts.

    Example:
    a = "aaabbc", b = "abbcc"
    Counter(a) = {a:3, b:2, c:1}
    Counter(b) = {a:1, b:2, c:2}

    a + b = {a:4, b:4, c:3}
    a - b = {a:2}     (b: 0 dropped, c: -1 dropped)

    Return:
    (Counter({"a": 4, "b": 4, "c": 3}), Counter({"a": 2}))
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 5: Counter Intersection And Union
# ============================================================

def counter_and_or(a, b):
    """
    In words:

    Return a tuple (a & b, a | b) where & is min-per-key and | is
    max-per-key.

    Example:
    a = "aaab", b = "aabbb"
    Counter(a) = {a:3, b:1}
    Counter(b) = {a:2, b:3}

    a & b = {a:2, b:1}
    a | b = {a:3, b:3}

    Return:
    (Counter({"a": 2, "b": 1}), Counter({"a": 3, "b": 3}))
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 6: elements()
# ============================================================

def expand_counter(pairs):
    """
    In words:

    Build a Counter from a list of (key, count) pairs, then expand it
    back to a list using Counter.elements(). Return the elements sorted
    so the test is stable.

    Example:
    pairs = [("a", 3), ("b", 2)]

    elements() yields: a, a, a, b, b (insertion order; we sort for stability).

    Return:
    ["a", "a", "a", "b", "b"]
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 7: Top K Frequent Words
# ============================================================

def top_k_words(words, k):
    """
    In words:

    Return the k most frequent words, sorted by frequency descending,
    breaking ties alphabetically.

    Example:
    words = ["i", "love", "leetcode", "i", "love", "coding"], k = 2
    Return: ["i", "love"]

    words = ["a", "b", "c", "a", "b", "a"], k = 2
    Return: ["a", "b"]

    Try to use:
    Counter + sorted with a key like (-count, word).
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 8: Anagram Via Counter
# ============================================================

def is_anagram(a, b):
    """
    In words:

    Return True if b is an anagram of a (same letters, same counts).
    Use collections.Counter.

    Example:
    a = "listen", b = "silent"   -> True
    a = "ab",     b = "a"        -> False
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 9: Exactly k Occurrences
# ============================================================

def chars_with_count(s, k):
    """
    In words:

    Return the sorted list of characters in s that appear exactly k times.

    Example:
    s = "aabbbccccd", k = 2
    Return: ["a"]

    s = "aabbcc", k = 2
    Return: ["a", "b", "c"]

    s = "abc", k = 5
    Return: []
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 10: Group Words By First Letter
# ============================================================

def group_by_first_letter(words):
    """
    In words:

    Group words by their first character. Inside each group keep words
    in the order they appeared in the input.

    Return a regular dict (not defaultdict) where each value is a list.
    Keys sorted alphabetically in the output is not required.

    Example:
    words = ["apple", "ant", "bear", "banana", "cat"]

    Return:
    {
        "a": ["apple", "ant"],
        "b": ["bear", "banana"],
        "c": ["cat"],
    }

    Try to use:
    defaultdict(list).
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 11: Manual Count With defaultdict(int)
# ============================================================

def manual_count(items):
    """
    In words:

    Implement the same behaviour as Counter using defaultdict(int).
    Return a plain dict mapping each item to its count.

    Example:
    items = [1, 1, 2, 3, 3, 3]

    Return:
    {1: 2, 2: 1, 3: 3}

    Important:
    Do not use Counter directly here. Use defaultdict(int) and dict().
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 12: Unique Bucket Grouping
# ============================================================

def unique_neighbors(edges):
    """
    In words:

    Given a list of undirected edges (u, v) pairs, return a dict mapping
    each node to the SET of its unique neighbours. Self-loops and
    duplicate edges should collapse.

    Return a regular dict mapping each node to a sorted list of neighbours
    (for stable comparison in the test).

    Example:
    edges = [(1, 2), (2, 1), (2, 3), (1, 2), (3, 3)]

    Adjacency:
    1 -> {2}
    2 -> {1, 3}
    3 -> {2, 3}

    Return:
    {1: [2], 2: [1, 3], 3: [2, 3]}

    Try to use:
    defaultdict(set).
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 13: Subtract And Drop Non-Positive
# ============================================================

def clean_subtract(a, b):
    """
    In words:

    Build Counters from a and b. Use Counter.subtract (NOT the -
    operator) and then drop zero and negative counts using the unary
    plus trick.

    Return the cleaned Counter.

    Example:
    a = "aaabbc", b = "abbcc"
    After subtract: {a: 2, b: 0, c: -1}
    After +counter: {a: 2}

    Return:
    Counter({"a": 2})

    Note:
    c1 - c2 already drops non-positive automatically. The point of this
    exercise is to show subtract() does NOT, and that +counter cleans up.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 14: Ransom Note
# ============================================================

def can_build(note, letters):
    """
    In words:

    Return True if you can build the string `note` using each letter in
    `letters` at most once.

    Example:
    note = "aab", letters = "aabbcc"   -> True
    note = "aab", letters = "ab"       -> False

    Try to use:
    Counter(letters) - Counter(note) and check if anything would have
    been needed; OR check Counter(note) <= Counter(letters).
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 15: Find The Difference
# ============================================================

def find_added_letter(s, t):
    """
    In words:

    t is s with exactly one extra character inserted (the rest is a
    shuffle of s). Return that extra character.

    Example:
    s = "abcd", t = "abcde"   -> "e"
    s = "",     t = "y"       -> "y"
    s = "a",    t = "aa"      -> "a"

    Try to use:
    (Counter(t) - Counter(s)) leaves just the added letter.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 16: Most Common With First-Appearance Tie Break
# ============================================================

def most_common_first(items):
    """
    In words:

    Return the value with the highest count. If multiple values tie,
    return the one that appeared earliest in items.

    Example:
    items = [1, 2, 2, 3, 3]
    Counts: 1->1, 2->2, 3->2
    Tie between 2 and 3; 2 appeared first.
    Return: 2

    items = ["a", "b", "c"]
    Return: "a"

    items = []
    Return: None
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 17: Find All Anagrams Of p In s
# ============================================================

def find_anagrams(s, p):
    """
    In words:

    Return all starting indices in s where a contiguous substring of
    length len(p) is an anagram of p.

    Example:
    s = "cbaebabacd", p = "abc"
    Return: [0, 6]

    s = "abab", p = "ab"
    Return: [0, 1, 2]

    s = "a", p = "abc"
    Return: []

    Try to use:
    Sliding window with a Counter for p and a Counter for the current
    window; compare each step.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 18: Permutation In String
# ============================================================

def has_permutation(s, p):
    """
    In words:

    Return True if s contains any permutation of p as a contiguous
    substring.

    Example:
    s = "eidbaooo", p = "ab"   -> True   ("ba" appears)
    s = "eidboaoo", p = "ab"   -> False
    s = "ab",       p = "ba"   -> True

    Try to use:
    Same sliding-window Counter idea as Exercise 17, short-circuiting
    on the first match.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 19: Minimum Window Substring
# ============================================================

def min_window(s, t):
    """
    In words:

    Return the shortest substring of s that contains every character of
    t with at least the required counts. If no such substring exists,
    return "".

    Example:
    s = "ADOBECODEBANC", t = "ABC"
    Return: "BANC"

    s = "a", t = "a"
    Return: "a"

    s = "a", t = "aa"
    Return: ""

    Try to use:
    Sliding window with a Counter for t. Track the number of "satisfied"
    characters.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 20: Mixed Final Drill - Event Log
# ============================================================

def summarize_log(events):
    """
    In words:

    events is a list of (user, action) tuples. Return a dictionary
    with four things:

    {
        "actions_per_user":  dict[user] -> dict[action] -> count,
        "top_user":          user with the most events (ties: earliest first),
        "top_action":        action that occurs most overall (ties: earliest first),
        "total_events":      total number of events,
    }

    Inside actions_per_user every inner mapping must be a plain dict
    (NOT a defaultdict or Counter) so it compares as a normal dict in
    the test.

    Example:
    events = [
        ("alice", "click"),
        ("bob",   "click"),
        ("alice", "view"),
        ("alice", "click"),
        ("bob",   "view"),
    ]

    Return:
    {
        "actions_per_user": {
            "alice": {"click": 2, "view": 1},
            "bob":   {"click": 1, "view": 1},
        },
        "top_user":     "alice",   (3 events, more than bob's 2)
        "top_action":   "click",   (3 vs view's 2)
        "total_events": 5,
    }

    Try to use:
    defaultdict(Counter) for the per-user breakdown.
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
    ci_result = count_iterable("banana")
    if ci_result is NOT_IMPLEMENTED:
        ci_actual = NOT_IMPLEMENTED
    else:
        ci_actual = (count_iterable("banana"), count_iterable([1, 1, 2, 3, 3, 3]))
    check(
        "Exercise 1: Counter From Iterable",
        "Counter built from a string and a list.",
        ci_actual,
        (Counter({"a": 3, "n": 2, "b": 1}), Counter({3: 3, 1: 2, 2: 1})),
    )

    check(
        "Exercise 2: Counter From Mapping And Kwargs",
        "Two ways to build the same Counter.",
        counter_constructors(),
        (Counter({"a": 4, "b": 2}), Counter({"a": 4, "b": 2})),
    )

    tn_result = top_n("aabbbccccd", 2)
    if tn_result is NOT_IMPLEMENTED:
        tn_actual = NOT_IMPLEMENTED
    else:
        tn_actual = (top_n("aabbbccccd", 2), top_n([1, 1, 1, 2, 2, 3], 5))
    check(
        "Exercise 3: most_common",
        "Return n most common (item, count) pairs.",
        tn_actual,
        ([("c", 4), ("b", 3)], [(1, 3), (2, 2), (3, 1)]),
    )

    check(
        "Exercise 4: Counter Arithmetic - Add And Subtract",
        "a + b and a - b (drops non-positive).",
        counter_add_subtract("aaabbc", "abbcc"),
        (Counter({"a": 4, "b": 4, "c": 3}), Counter({"a": 2})),
    )

    check(
        "Exercise 5: Counter Intersection And Union",
        "a & b is min per key; a | b is max per key.",
        counter_and_or("aaab", "aabbb"),
        (Counter({"a": 2, "b": 1}), Counter({"a": 3, "b": 3})),
    )

    check(
        "Exercise 6: elements()",
        "Expand a Counter to a sorted list of repeated keys.",
        expand_counter([("a", 3), ("b", 2)]),
        ["a", "a", "a", "b", "b"],
    )

    tw_result = top_k_words(["i", "love", "leetcode", "i", "love", "coding"], 2)
    if tw_result is NOT_IMPLEMENTED:
        tw_actual = NOT_IMPLEMENTED
    else:
        tw_actual = (
            top_k_words(["i", "love", "leetcode", "i", "love", "coding"], 2),
            top_k_words(["a", "b", "c", "a", "b", "a"], 2),
        )
    check(
        "Exercise 7: Top K Frequent Words",
        "Most frequent words; ties broken alphabetically.",
        tw_actual,
        (["i", "love"], ["a", "b"]),
    )

    an_result = is_anagram("listen", "silent")
    if an_result is NOT_IMPLEMENTED:
        an_actual = NOT_IMPLEMENTED
    else:
        an_actual = (is_anagram("listen", "silent"), is_anagram("ab", "a"))
    check(
        "Exercise 8: Anagram Via Counter",
        "Compare Counters to decide anagram.",
        an_actual,
        (True, False),
    )

    cwc_result = chars_with_count("aabbbccccd", 2)
    if cwc_result is NOT_IMPLEMENTED:
        cwc_actual = NOT_IMPLEMENTED
    else:
        cwc_actual = (
            chars_with_count("aabbbccccd", 2),
            chars_with_count("aabbcc", 2),
            chars_with_count("abc", 5),
        )
    check(
        "Exercise 9: Exactly k Occurrences",
        "Characters that appear exactly k times, sorted.",
        cwc_actual,
        (["a"], ["a", "b", "c"], []),
    )

    check(
        "Exercise 10: Group Words By First Letter",
        "defaultdict(list) grouped by first character.",
        group_by_first_letter(["apple", "ant", "bear", "banana", "cat"]),
        {
            "a": ["apple", "ant"],
            "b": ["bear", "banana"],
            "c": ["cat"],
        },
    )

    check(
        "Exercise 11: Manual Count With defaultdict(int)",
        "Reproduce Counter behaviour using defaultdict(int).",
        manual_count([1, 1, 2, 3, 3, 3]),
        {1: 2, 2: 1, 3: 3},
    )

    check(
        "Exercise 12: Unique Bucket Grouping",
        "defaultdict(set) adjacency; output as sorted lists.",
        unique_neighbors([(1, 2), (2, 1), (2, 3), (1, 2), (3, 3)]),
        {1: [2], 2: [1, 3], 3: [2, 3]},
    )

    check(
        "Exercise 13: Subtract And Drop Non-Positive",
        "Use Counter.subtract then +counter to drop zeros and negatives.",
        clean_subtract("aaabbc", "abbcc"),
        Counter({"a": 2}),
    )

    cb_result = can_build("aab", "aabbcc")
    if cb_result is NOT_IMPLEMENTED:
        cb_actual = NOT_IMPLEMENTED
    else:
        cb_actual = (can_build("aab", "aabbcc"), can_build("aab", "ab"))
    check(
        "Exercise 14: Ransom Note",
        "Can `note` be built from letters in `letters`?",
        cb_actual,
        (True, False),
    )

    fal_result = find_added_letter("abcd", "abcde")
    if fal_result is NOT_IMPLEMENTED:
        fal_actual = NOT_IMPLEMENTED
    else:
        fal_actual = (
            find_added_letter("abcd", "abcde"),
            find_added_letter("", "y"),
            find_added_letter("a", "aa"),
        )
    check(
        "Exercise 15: Find The Difference",
        "Return the one extra character via Counter subtraction.",
        fal_actual,
        ("e", "y", "a"),
    )

    mcf_result = most_common_first([1, 2, 2, 3, 3])
    if mcf_result is NOT_IMPLEMENTED:
        mcf_actual = NOT_IMPLEMENTED
    else:
        mcf_actual = (
            most_common_first([1, 2, 2, 3, 3]),
            most_common_first(["a", "b", "c"]),
            most_common_first([]),
        )
    check(
        "Exercise 16: Most Common With First-Appearance Tie Break",
        "Value with highest count; tie -> earliest in input.",
        mcf_actual,
        (2, "a", None),
    )

    fa_result = find_anagrams("cbaebabacd", "abc")
    if fa_result is NOT_IMPLEMENTED:
        fa_actual = NOT_IMPLEMENTED
    else:
        fa_actual = (
            find_anagrams("cbaebabacd", "abc"),
            find_anagrams("abab", "ab"),
            find_anagrams("a", "abc"),
        )
    check(
        "Exercise 17: Find All Anagrams Of p In s",
        "Sliding-window Counter; return starting indices.",
        fa_actual,
        ([0, 6], [0, 1, 2], []),
    )

    hp_result = has_permutation("eidbaooo", "ab")
    if hp_result is NOT_IMPLEMENTED:
        hp_actual = NOT_IMPLEMENTED
    else:
        hp_actual = (
            has_permutation("eidbaooo", "ab"),
            has_permutation("eidboaoo", "ab"),
            has_permutation("ab", "ba"),
        )
    check(
        "Exercise 18: Permutation In String",
        "Does s contain any permutation of p as a substring?",
        hp_actual,
        (True, False, True),
    )

    mw_result = min_window("ADOBECODEBANC", "ABC")
    if mw_result is NOT_IMPLEMENTED:
        mw_actual = NOT_IMPLEMENTED
    else:
        mw_actual = (
            min_window("ADOBECODEBANC", "ABC"),
            min_window("a", "a"),
            min_window("a", "aa"),
        )
    check(
        "Exercise 19: Minimum Window Substring",
        "Shortest substring of s containing all chars of t.",
        mw_actual,
        ("BANC", "a", ""),
    )

    check(
        "Exercise 20: Mixed Final Drill - Event Log",
        "Summarize (user, action) events into a 4-field dict.",
        summarize_log(
            [
                ("alice", "click"),
                ("bob", "click"),
                ("alice", "view"),
                ("alice", "click"),
                ("bob", "view"),
            ]
        ),
        {
            "actions_per_user": {
                "alice": {"click": 2, "view": 1},
                "bob": {"click": 1, "view": 1},
            },
            "top_user": "alice",
            "top_action": "click",
            "total_events": 5,
        },
    )


if __name__ == "__main__":
    run_all_exercises()
