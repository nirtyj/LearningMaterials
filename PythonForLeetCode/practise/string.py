"""

Strings are IMMUTABLE sequences of single-character strings.

s[i]           index
s[a:b]         slice
s[::-1]        reverse
s + t          concat (creates new string)
s * n          repeat
c in s         substring or char check

len(s)         length
s.split(sep)   split on sep (default: whitespace)
sep.join(it)   join iterable of strings with sep between

s.startswith   prefix check
s.endswith     suffix check
s.find(t)      first index or -1
s.replace(a,b) replace all
s.strip()      remove leading and trailing whitespace
s.lower()      lowercase
s.upper()      uppercase

c.isalpha()    only letters
c.isdigit()    only digits
c.isalnum()    letters or digits
c.isspace()    whitespace

ord(c)         char to int    'a' -> 97, 'A' -> 65
chr(i)         int to char    65  -> 'A'

Important:
s[i] = 'x'     does NOT work (immutable). Rebuild via "".join(list(s)).

"""

"""
Python String Practice

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

from collections import Counter


NOT_IMPLEMENTED = object()


# ============================================================
# Exercise 1: Slicing Basics
# ============================================================

def slice_basics(s):
    """
    In words:

    Return a tuple of four slices of s:

    1. first three characters
    2. last three characters
    3. reverse of s
    4. every other character starting from index 0

    Example:
    s = "abcdefg"

    Return:
    ("abc", "efg", "gfedcba", "aceg")
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 2: Split And Join
# ============================================================

def split_join(s, sep_in, sep_out):
    """
    In words:

    Split s on sep_in, then re-join the pieces with sep_out.

    Example:
    s = "a-b-c", sep_in = "-", sep_out = ","
    Return: "a,b,c"

    s = "one two three", sep_in = " ", sep_out = "_"
    Return: "one_two_three"
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 3: ord And chr
# ============================================================

def alphabet_index(c):
    """
    In words:

    Given a single lowercase letter c, return its position in the alphabet
    (a -> 0, b -> 1, ..., z -> 25).

    Example:
    c = "a"  -> 0
    c = "f"  -> 5
    c = "z"  -> 25

    Try to use:
    ord(c) - ord("a").
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 4: Replace Char At Index
# ============================================================

def replace_at(s, i, c):
    """
    In words:

    Return a new string equal to s but with the character at index i
    replaced by c.

    Example:
    s = "hello", i = 1, c = "a"
    Return: "hallo"

    Important:
    s[i] = c does NOT work because strings are immutable.
    Build a new string instead (slicing or list + join).
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 5: Filter Characters
# ============================================================

def keep_alnum_lower(s):
    """
    In words:

    Return s with every non-alphanumeric character removed and the
    remaining characters lowercased.

    Example:
    s = "A man, a plan, a canal: Panama!"
    Return: "amanaplanacanalpanama"

    Try to use:
    A generator expression with isalnum and lower, fed to "".join.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 6: Reverse Only Letters
# ============================================================

def reverse_only_letters(s):
    """
    In words:

    Reverse only the alphabetic characters in s. Non-letters stay in place.

    Example:
    s = "a-bC-dEf-ghIj"
    Return: "j-Ih-gfE-dCba"

    s = "Test1ng-Leet=code-Q!"
    Return: "Qedo1ct-eeLg=ntse-T!"

    Try to use:
    Two pointers, one from each end.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 7: Count Vowels
# ============================================================

def count_vowels(s):
    """
    In words:

    Return the number of vowels in s. Treat both uppercase and lowercase
    a, e, i, o, u as vowels.

    Example:
    s = "Hello World"  -> 3
    s = ""             -> 0
    s = "bcd"          -> 0
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 8: Capitalize Each Word
# ============================================================

def capitalize_words(s):
    """
    In words:

    Capitalize the first letter of every whitespace-separated word.
    Leave the rest of each word unchanged. Preserve the single spaces
    between words (the input has only single spaces; no leading or
    trailing whitespace).

    Example:
    s = "hello world FROM python"
    Return: "Hello World FROM Python"

    Important:
    Do not use the built-in .title() method (it lowercases the rest).
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 9: Run-Length Encode
# ============================================================

def rle_encode(s):
    """
    In words:

    Replace each run of equal characters with the character followed by
    its run length (always include the count, even if it is 1).

    Example:
    s = "aaabbc"   -> "a3b2c1"
    s = "abcd"     -> "a1b1c1d1"
    s = ""         -> ""
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 10: Run-Length Decode
# ============================================================

def rle_decode(s):
    """
    In words:

    Inverse of rle_encode. The input is well-formed: alternating
    single character and integer (which can be multiple digits).

    Example:
    s = "a3b2c1"   -> "aaabbc"
    s = "a10"      -> "aaaaaaaaaa"
    s = ""         -> ""
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 11: Valid Palindrome (Alnum, Case-Insensitive)
# ============================================================

def is_valid_palindrome(s):
    """
    In words:

    Return True if s reads the same forward and backward after dropping
    all non-alphanumeric characters and lowering case.

    Example:
    s = "A man, a plan, a canal: Panama"   -> True
    s = "race a car"                       -> False
    s = " "                                 -> True
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 12: Anagram Via Sorted
# ============================================================

def is_anagram_sorted(a, b):
    """
    In words:

    Return True if b is an anagram of a (same letters, same counts).
    Use sorting to compare. Case sensitive.

    Example:
    a = "listen", b = "silent"   -> True
    a = "rat",    b = "car"      -> False
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 13: Anagram Via Counter
# ============================================================

def is_anagram_counter(a, b):
    """
    In words:

    Same as Exercise 12 but use collections.Counter (already imported).

    Example:
    a = "anagram", b = "nagaram"   -> True
    a = "ab",      b = "a"         -> False
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 14: Group Anagrams
# ============================================================

def group_anagrams(words):
    """
    In words:

    Group words that are anagrams of each other. Inside each group, the
    words should be sorted lexicographically. Return a list of groups
    sorted lexicographically by their first element.

    Example:
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]

    Return:
    [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]

    Try to use:
    A dict keyed by the sorted version of each word.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 15: Longest Common Prefix
# ============================================================

def longest_common_prefix(words):
    """
    In words:

    Return the longest string that is a prefix of every word in words.
    If words is empty or there is no common prefix, return "".

    Example:
    words = ["flower", "flow", "flight"]   -> "fl"
    words = ["dog", "racecar", "car"]      -> ""
    words = []                              -> ""
    words = ["single"]                      -> "single"
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 16: String Compression
# ============================================================

def compress(chars):
    """
    In words:

    Given a list of characters chars (single-character strings),
    compress runs in place using the rules:
    - A run of length 1 becomes just the character.
    - A run of length k > 1 becomes the character followed by the digits
      of k.

    Modify chars in place and return the new logical length.
    The portion of chars beyond the returned length may be anything.

    Example:
    chars = ["a", "a", "b", "b", "c", "c", "c"]

    After compression chars[:6] should be ["a", "2", "b", "2", "c", "3"].
    Return: 6

    chars = ["a"]
    Return: 1

    chars = ["a", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"]
    After: chars[:4] = ["a", "b", "1", "2"]
    Return: 4

    Try to use:
    Two pointers (read and write).
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 17: Roman To Integer
# ============================================================

def roman_to_int(s):
    """
    In words:

    Convert a valid Roman numeral string to its integer value.

    Symbol values:
    I=1, V=5, X=10, L=50, C=100, D=500, M=1000.

    Subtractive rule: if a smaller numeral appears before a larger one,
    subtract it.

    Example:
    "III"     -> 3
    "IV"      -> 4
    "IX"      -> 9
    "LVIII"   -> 58
    "MCMXCIV" -> 1994
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 18: Integer To Roman
# ============================================================

def int_to_roman(n):
    """
    In words:

    Convert an integer n (1 <= n <= 3999) to its canonical Roman numeral.

    Example:
    3       -> "III"
    4       -> "IV"
    9       -> "IX"
    58      -> "LVIII"
    1994    -> "MCMXCIV"

    Try to use:
    A descending list of (value, symbol) pairs including 900, 400, 90,
    40, 9, 4 for subtractive forms.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 19: Find All Substring Occurrences
# ============================================================

def find_all(s, t):
    """
    In words:

    Return a list of all starting indices where t occurs in s, including
    overlapping occurrences. If t is empty, return [].

    Example:
    s = "abababab", t = "aba"
    Return: [0, 2, 4]

    s = "aaaa", t = "aa"
    Return: [0, 1, 2]

    s = "abc", t = "z"
    Return: []

    Important:
    Do not use s.find() in a loop with the previous index advanced by
    len(t); that would skip overlaps. Slide by 1.
    """

    # YOUR CODE HERE

    return NOT_IMPLEMENTED


# ============================================================
# Exercise 20: Mixed Final Drill
# ============================================================

def analyze_sentence(s):
    """
    In words:

    Return a dictionary describing the sentence s.

    Assume s has only single spaces between words and no leading or
    trailing whitespace.

    Return:
    {
        "word_count":           number of whitespace-separated words,
        "char_count_no_spaces": number of non-space characters,
        "longest_word":         the longest word (ties: first one),
        "reversed_words":       words in reverse order joined by single space,
        "vowel_count":          number of vowels (a e i o u, both cases),
    }

    Example:
    s = "the quick brown fox jumps"

    Return:
    {
        "word_count":           5,
        "char_count_no_spaces": 21,
        "longest_word":         "quick",
        "reversed_words":       "jumps fox brown quick the",
        "vowel_count":          5,
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
        "Exercise 1: Slicing Basics",
        "first 3, last 3, reverse, every other from index 0.",
        slice_basics("abcdefg"),
        ("abc", "efg", "gfedcba", "aceg"),
    )

    sj_result = split_join("a-b-c", "-", ",")
    if sj_result is NOT_IMPLEMENTED:
        sj_actual = NOT_IMPLEMENTED
    else:
        sj_actual = (split_join("a-b-c", "-", ","), split_join("one two three", " ", "_"))
    check(
        "Exercise 2: Split And Join",
        "Split on sep_in, join on sep_out.",
        sj_actual,
        ("a,b,c", "one_two_three"),
    )

    ai_result = alphabet_index("a")
    if ai_result is NOT_IMPLEMENTED:
        ai_actual = NOT_IMPLEMENTED
    else:
        ai_actual = (alphabet_index("a"), alphabet_index("f"), alphabet_index("z"))
    check(
        "Exercise 3: ord And chr",
        "Return alphabet position 0..25.",
        ai_actual,
        (0, 5, 25),
    )

    check(
        "Exercise 4: Replace Char At Index",
        "Build a new string with the char at i replaced.",
        replace_at("hello", 1, "a"),
        "hallo",
    )

    check(
        "Exercise 5: Filter Characters",
        "Keep alnum chars only, lowercased.",
        keep_alnum_lower("A man, a plan, a canal: Panama!"),
        "amanaplanacanalpanama",
    )

    rol_result = reverse_only_letters("a-bC-dEf-ghIj")
    if rol_result is NOT_IMPLEMENTED:
        rol_actual = NOT_IMPLEMENTED
    else:
        rol_actual = (
            reverse_only_letters("a-bC-dEf-ghIj"),
            reverse_only_letters("Test1ng-Leet=code-Q!"),
        )
    check(
        "Exercise 6: Reverse Only Letters",
        "Reverse alphabetic characters; leave others in place.",
        rol_actual,
        ("j-Ih-gfE-dCba", "Qedo1ct-eeLg=ntse-T!"),
    )

    cv_result = count_vowels("Hello World")
    if cv_result is NOT_IMPLEMENTED:
        cv_actual = NOT_IMPLEMENTED
    else:
        cv_actual = (count_vowels("Hello World"), count_vowels(""), count_vowels("bcd"))
    check(
        "Exercise 7: Count Vowels",
        "Count aeiou (both cases).",
        cv_actual,
        (3, 0, 0),
    )

    check(
        "Exercise 8: Capitalize Each Word",
        "Capitalize first letter of each word; leave rest unchanged.",
        capitalize_words("hello world FROM python"),
        "Hello World FROM Python",
    )

    rle_e_result = rle_encode("aaabbc")
    if rle_e_result is NOT_IMPLEMENTED:
        rle_e_actual = NOT_IMPLEMENTED
    else:
        rle_e_actual = (rle_encode("aaabbc"), rle_encode("abcd"), rle_encode(""))
    check(
        "Exercise 9: Run-Length Encode",
        "Encode each run as char + count.",
        rle_e_actual,
        ("a3b2c1", "a1b1c1d1", ""),
    )

    rle_d_result = rle_decode("a3b2c1")
    if rle_d_result is NOT_IMPLEMENTED:
        rle_d_actual = NOT_IMPLEMENTED
    else:
        rle_d_actual = (rle_decode("a3b2c1"), rle_decode("a10"), rle_decode(""))
    check(
        "Exercise 10: Run-Length Decode",
        "Inverse of rle_encode.",
        rle_d_actual,
        ("aaabbc", "aaaaaaaaaa", ""),
    )

    vp_result = is_valid_palindrome("A man, a plan, a canal: Panama")
    if vp_result is NOT_IMPLEMENTED:
        vp_actual = NOT_IMPLEMENTED
    else:
        vp_actual = (
            is_valid_palindrome("A man, a plan, a canal: Panama"),
            is_valid_palindrome("race a car"),
            is_valid_palindrome(" "),
        )
    check(
        "Exercise 11: Valid Palindrome",
        "Strip non-alnum, lowercase, then palindrome check.",
        vp_actual,
        (True, False, True),
    )

    as_result = is_anagram_sorted("listen", "silent")
    if as_result is NOT_IMPLEMENTED:
        as_actual = NOT_IMPLEMENTED
    else:
        as_actual = (is_anagram_sorted("listen", "silent"), is_anagram_sorted("rat", "car"))
    check(
        "Exercise 12: Anagram Via Sorted",
        "Compare sorted character lists.",
        as_actual,
        (True, False),
    )

    ac_result = is_anagram_counter("anagram", "nagaram")
    if ac_result is NOT_IMPLEMENTED:
        ac_actual = NOT_IMPLEMENTED
    else:
        ac_actual = (is_anagram_counter("anagram", "nagaram"), is_anagram_counter("ab", "a"))
    check(
        "Exercise 13: Anagram Via Counter",
        "Compare Counters.",
        ac_actual,
        (True, False),
    )

    check(
        "Exercise 14: Group Anagrams",
        "Group anagrams, words sorted inside each group, groups sorted by first.",
        group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]),
        [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]],
    )

    lcp_result = longest_common_prefix(["flower", "flow", "flight"])
    if lcp_result is NOT_IMPLEMENTED:
        lcp_actual = NOT_IMPLEMENTED
    else:
        lcp_actual = (
            longest_common_prefix(["flower", "flow", "flight"]),
            longest_common_prefix(["dog", "racecar", "car"]),
            longest_common_prefix([]),
            longest_common_prefix(["single"]),
        )
    check(
        "Exercise 15: Longest Common Prefix",
        "Longest prefix common to every word.",
        lcp_actual,
        ("fl", "", "", "single"),
    )

    def compress_case(chars):
        n = compress(chars)
        if n is NOT_IMPLEMENTED:
            return NOT_IMPLEMENTED
        return (n, chars[:n])

    c1 = compress_case(["a", "a", "b", "b", "c", "c", "c"])
    if c1 is NOT_IMPLEMENTED:
        compress_actual = NOT_IMPLEMENTED
    else:
        compress_actual = (
            c1,
            compress_case(["a"]),
            compress_case(["a", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"]),
        )
    check(
        "Exercise 16: String Compression",
        "Compress runs in place; return new length.",
        compress_actual,
        (
            (6, ["a", "2", "b", "2", "c", "3"]),
            (1, ["a"]),
            (4, ["a", "b", "1", "2"]),
        ),
    )

    r2i_result = roman_to_int("III")
    if r2i_result is NOT_IMPLEMENTED:
        r2i_actual = NOT_IMPLEMENTED
    else:
        r2i_actual = (
            roman_to_int("III"),
            roman_to_int("IV"),
            roman_to_int("IX"),
            roman_to_int("LVIII"),
            roman_to_int("MCMXCIV"),
        )
    check(
        "Exercise 17: Roman To Integer",
        "Convert Roman numeral to int with subtractive rule.",
        r2i_actual,
        (3, 4, 9, 58, 1994),
    )

    i2r_result = int_to_roman(3)
    if i2r_result is NOT_IMPLEMENTED:
        i2r_actual = NOT_IMPLEMENTED
    else:
        i2r_actual = (
            int_to_roman(3),
            int_to_roman(4),
            int_to_roman(9),
            int_to_roman(58),
            int_to_roman(1994),
        )
    check(
        "Exercise 18: Integer To Roman",
        "Greedy with subtractive pairs (900, 400, 90, 40, 9, 4).",
        i2r_actual,
        ("III", "IV", "IX", "LVIII", "MCMXCIV"),
    )

    fa_result = find_all("abababab", "aba")
    if fa_result is NOT_IMPLEMENTED:
        fa_actual = NOT_IMPLEMENTED
    else:
        fa_actual = (
            find_all("abababab", "aba"),
            find_all("aaaa", "aa"),
            find_all("abc", "z"),
        )
    check(
        "Exercise 19: Find All Substring Occurrences",
        "Return all starting indices, including overlapping.",
        fa_actual,
        ([0, 2, 4], [0, 1, 2], []),
    )

    check(
        "Exercise 20: Mixed Final Drill",
        "Analyze a sentence: counts, longest, reversed words, vowels.",
        analyze_sentence("the quick brown fox jumps"),
        {
            "word_count": 5,
            "char_count_no_spaces": 21,
            "longest_word": "quick",
            "reversed_words": "jumps fox brown quick the",
            "vowel_count": 5,
        },
    )


if __name__ == "__main__":
    run_all_exercises()
