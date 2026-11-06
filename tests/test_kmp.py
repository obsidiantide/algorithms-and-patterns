"""Unit tests for the KMP substring search."""
import random

from algorithms.strings.kmp import build_prefix_table, kmp_search


def naive(text: str, pattern: str):
    return [i for i in range(len(text) - len(pattern) + 1) if text.startswith(pattern, i)]


def test_prefix_table_classic():
    assert build_prefix_table("ABABCABAB") == [0, 0, 1, 2, 0, 1, 2, 3, 4]
    assert build_prefix_table("aaaa") == [0, 1, 2, 3]
    assert build_prefix_table("abc") == [0, 0, 0]
    assert build_prefix_table("") == []


def test_basic_search():
    assert kmp_search("abracadabra", "abra") == [0, 7]


def test_overlapping_matches():
    assert kmp_search("aaaaa", "aa") == [0, 1, 2, 3]
    assert kmp_search("ababababa", "ababa") == [0, 2, 4]


def test_no_match_and_pattern_longer_than_text():
    assert kmp_search("hello", "world") == []
    assert kmp_search("ab", "abc") == []


def test_empty_inputs():
    assert kmp_search("abc", "") == [0, 1, 2, 3]
    assert kmp_search("", "") == [0]
    assert kmp_search("", "a") == []


def test_match_at_end_and_whole_text():
    assert kmp_search("xxabc", "abc") == [2]
    assert kmp_search("abc", "abc") == [0]


def test_unicode():
    assert kmp_search("çiçək çiçək", "çiçək") == [0, 6]


def test_random_against_naive():
    rng = random.Random(7)
    for _ in range(300):
        text = "".join(rng.choice("ab") for _ in range(rng.randint(0, 30)))
        pattern = "".join(rng.choice("ab") for _ in range(rng.randint(1, 5)))
        assert kmp_search(text, pattern) == naive(text, pattern)
