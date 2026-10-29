"""Unit tests for Longest Common Subsequence (LCS)."""
from algorithms.dynamic.lcs import lcs_length, longest_common_subsequence, lcs_string


def test_empty_inputs():
    assert lcs_length("", "") == 0
    assert lcs_length("abc", "") == 0
    assert lcs_length("", "abc") == 0
    assert longest_common_subsequence([], []) == []
    assert longest_common_subsequence([1, 2], []) == []
    assert lcs_string("", "xyz") == ""


def test_identical_inputs():
    assert lcs_length("abcdef", "abcdef") == 6
    assert longest_common_subsequence(["a", "b", "c"], ["a", "b", "c"]) == ["a", "b", "c"]
    assert lcs_string("hello", "hello") == "hello"


def test_no_common_subsequence():
    assert lcs_length("abc", "def") == 0
    assert longest_common_subsequence([1, 2, 3], [4, 5, 6]) == []
    assert lcs_string("abc", "xyz") == ""


def test_classic_examples():
    s1 = "AGGTAB"
    s2 = "GXTXAYB"
    assert lcs_length(s1, s2) == 4
    assert lcs_string(s1, s2) == "GTAB"

    s3 = "ABCDGH"
    s4 = "AEDFHR"
    assert lcs_length(s3, s4) == 3
    assert lcs_string(s3, s4) == "ADH"


def test_with_integer_sequences():
    seq1 = [10, 20, 30, 40, 50]
    seq2 = [15, 20, 35, 40]
    assert lcs_length(seq1, seq2) == 2
    assert longest_common_subsequence(seq1, seq2) == [20, 40]


def test_consistency_between_length_and_subsequence():
    s1 = "dynamicprogramming"
    s2 = "algorithmimplementation"
    length = lcs_length(s1, s2)
    seq = longest_common_subsequence(s1, s2)
    assert len(seq) == length
