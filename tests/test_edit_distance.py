"""Unit tests for Levenshtein edit distance."""
import pytest

from algorithms.dynamic.edit_distance import is_one_edit_distance, levenshtein_distance


def test_empty_inputs():
    assert levenshtein_distance("", "") == 0
    assert levenshtein_distance("kitten", "") == 6
    assert levenshtein_distance("", "kitten") == 6
    assert is_one_edit_distance("", "") is False
    assert is_one_edit_distance("", "a") is True
    assert is_one_edit_distance("a", "") is True


def test_identical_sequences():
    assert levenshtein_distance("kitten", "kitten") == 0
    assert levenshtein_distance([1, 2, 3], [1, 2, 3]) == 0
    assert is_one_edit_distance("kitten", "kitten") is False


def test_classic_examples():
    assert levenshtein_distance("kitten", "sitting") == 3
    assert levenshtein_distance("flaw", "lawn") == 2
    assert levenshtein_distance("saturday", "sunday") == 3


def test_custom_operation_costs():
    # If substitution cost is higher than del + ins, del + ins should be chosen
    assert levenshtein_distance("a", "b", insertion_cost=2, deletion_cost=2, substitution_cost=5) == 4
    # Cheap substitution
    assert levenshtein_distance("a", "b", insertion_cost=5, deletion_cost=5, substitution_cost=1) == 1
    # Asymmetric costs
    assert levenshtein_distance("a", "", insertion_cost=1, deletion_cost=10) == 10
    assert levenshtein_distance("", "a", insertion_cost=10, deletion_cost=1) == 10


def test_validation():
    with pytest.raises(ValueError, match="operation costs must be non-negative"):
        levenshtein_distance("a", "b", insertion_cost=-1)
    with pytest.raises(ValueError, match="operation costs must be non-negative"):
        levenshtein_distance("a", "b", deletion_cost=-1)
    with pytest.raises(ValueError, match="operation costs must be non-negative"):
        levenshtein_distance("a", "b", substitution_cost=-1)


def test_non_string_sequences():
    seq1 = [1, 2, 3, 4]
    seq2 = [1, 2, 4]
    assert levenshtein_distance(seq1, seq2) == 1
    assert is_one_edit_distance(seq1, seq2) is True


def test_is_one_edit_distance():
    assert is_one_edit_distance("pale", "ple") is True
    assert is_one_edit_distance("pales", "pale") is True
    assert is_one_edit_distance("pale", "bale") is True
    assert is_one_edit_distance("pale", "bake") is False
    assert is_one_edit_distance("abc", "abcde") is False
    assert is_one_edit_distance([10, 20], [10, 30]) is True
