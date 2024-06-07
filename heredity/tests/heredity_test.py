import math

from heredity.heredity import *


def whole_family_info_test_1():
    people = {
        "Harry": { "name": "Harry", "mother": "Lily", "father": "James", "trait": None },
        "James": { "name": "James", "mother": None, "father": None, "trait": True },
        "Lily": { "name": "Lily", "mother": None, "father": None, "trait": False }
    }
    one_gene = { "Harry" }
    two_genes = { "James" }
    have_trait = { "James" }
    result = whole_family_info(people, one_gene, two_genes, have_trait)
    expected = {
        "Harry": {
            "genes": 1,
            "trait": False,
            "parents_genes": {
                "mother": 0,
                "father": 2
            }
        },
        "James": {
            "genes": 2,
            "trait": True,
            "parents_genes": None
        },
        "Lily": {
            "genes": 0,
            "trait": False,
            "parents_genes": None
        }
    }
    assert result == expected, f'Found: {result}. Should be {expected}'


def joint_probability_test_1():
    people = {
        "Harry": { "name": "Harry", "mother": "Lily", "father": "James", "trait": None },
        "James": { "name": "James", "mother": None, "father": None, "trait": True },
        "Lily": { "name": "Lily", "mother": None, "father": None, "trait": False }
    }
    one_gene = { "Harry" }
    two_genes = { "James" }
    have_trait = { "James" }
    result = joint_probability(people, one_gene, two_genes, have_trait)
    expected = 0.9504 * 0.0065 * 0.431288
    assert  math.isclose(result, expected, abs_tol = 0.000000001), f'Found: {result}. Should be {expected}'


def joint_probability_test_2():
    people = {
        "Harry": { "name": "Harry", "mother": "Lily", "father": "James", "trait": None },
        "James": { "name": "James", "mother": None, "father": None, "trait": None },
        "Lily": { "name": "Lily", "mother": None, "father": None, "trait": None }
    }
    one_gene = {}
    two_genes = {}
    have_trait = {}
    result = joint_probability(people, one_gene, two_genes, have_trait)
    expected = 0.87643242998784
    assert  math.isclose(result, expected, abs_tol = 0.000000001), f'Found: {result}. Should be {expected}'


def update_test_1():
    probabilities = {
        "Harry": { "gene": { 2: 0, 1: 0, 0: 0 }, "trait": { True: 0, False: 0 } },
        "James": { "gene": { 2: 0, 1: 0, 0: 0 }, "trait": { True: 0, False: 0 } },
        "Lily": { "gene": { 2: 0, 1: 0, 0: 0 }, "trait": { True: 0, False: 0 } },
    }
    one_gene = { "Harry" }
    two_genes = { "James" }
    have_trait = { "James" }
    p = 0.0026643247488
    update(probabilities, one_gene, two_genes, have_trait, p)
    expected = {
        "Harry": { "gene": { 2: 0, 1: 0.0026643247488, 0: 0 }, "trait": { True: 0, False: 0.0026643247488 } },
        "James": { "gene": { 2: 0.0026643247488, 1: 0, 0: 0 }, "trait": { True: 0.0026643247488, False: 0 } },
        "Lily": { "gene": { 2: 0, 1: 0, 0: 0.0026643247488 }, "trait": { True: 0, False: 0.0026643247488 } },
    }
    assert  probabilities == expected, f'Found: {probabilities}. Should be {expected}'


def normalize_test_1():
    probabilities = {
        "Harry": { "gene": { 2: 0, 1: 0.0026643247488, 0: 0 }, "trait": { True: 0, False: 0.0026643247488 } },
        "James": { "gene": { 2: 0.0026643247488, 1: 0, 0: 0 }, "trait": { True: 0.0026643247488, False: 0 } },
        "Lily": { "gene": { 2: 0, 1: 0, 0: 0.0026643247488 }, "trait": { True: 0, False: 0.0026643247488 } },
    }
    normalize(probabilities)
    expected = {
        "Harry": { "gene": { 2: 0, 1: 1, 0: 0 }, "trait": { True: 0, False: 1 } },
        "James": { "gene": { 2: 1, 1: 0, 0: 0 }, "trait": { True: 1, False: 0 } },
        "Lily": { "gene": { 2: 0, 1: 0, 0: 1 }, "trait": { True: 0, False: 1 } },
    }
    assert  probabilities == expected, f'Found: {probabilities}. Should be {expected}'