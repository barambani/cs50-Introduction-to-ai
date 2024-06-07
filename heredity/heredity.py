import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def genes_of_person(person, one_gene, two_genes):
    """
    Returns the genes of a person depending on which group is in
    """
    return 0 if person not in one_gene and person not in two_genes else 1 if person in one_gene else 2


def whole_family_info(people, one_gene, two_genes, have_trait):
    """
    Returns a structure containing all the people with the inf needed for the joint probability calculation 
    """
    return {
        person: {
            "genes": genes_of_person(person, one_gene, two_genes),
            "trait": person in have_trait,
            "parents_genes": {
                "mother": genes_of_person(people[person]["mother"], one_gene, two_genes),
                "father": genes_of_person(people[person]["father"], one_gene, two_genes)
            } if people[person]["mother"] and people[person]["father"] else None
        }
        for person in people
    }


def prob_0_genes_not_from_p1_nor_from_p2(g_parent1, g_parent2):
    """
    Returns the probability the gene is not taken from parent1 nor from parent2, given their gene's counts
    """
    res_a = 0
    res_b = 0

    # prob. the gene is taken from parent 1
    if g_parent1 == 0:
        res_a = 1 - PROBS["mutation"]
    elif g_parent1 == 1:
        res_a = 0.5
    elif g_parent1 == 2:
        res_a = PROBS["mutation"]

    # prob. the gene is not taken from parent 2
    if g_parent2 == 0:
        res_b = 1 - PROBS["mutation"]
    elif g_parent2 == 1:
        res_b = 0.5
    elif g_parent2 == 2:
        res_b = PROBS["mutation"]
    
    return res_a * res_b


def prob_1_gene_from_p1_and_not_from_p2(g_parent1, g_parent2):
    """
    Returns the probability the gene is taken either from parent1 or from parent2, given their gene's counts
    """
    res_a = 0
    res_b = 0

    # prob. the gene is taken from parent 1
    if g_parent1 == 0:
        res_a = PROBS["mutation"]
    elif g_parent1 == 1:
        res_a = 0.5
    elif g_parent1 == 2:
        res_a = 1 - PROBS["mutation"]
    
    # prob. the gene is not taken from parent 2
    if g_parent2 == 0:
        res_b = 1 - PROBS["mutation"]
    elif g_parent2 == 1:
        res_b = 0.5
    elif g_parent2 == 2:
        res_b = PROBS["mutation"]

    return res_a * res_b


def prob_2_genes_from_p1_and_from_p2(g_parent1, g_parent2):
    """
    Returns the probability the gene is taken both from parent1 and from parent2, given their gene's counts
    """
    res_a = 0
    res_b = 0

    # prob. the genes is taken from parent 1
    if g_parent1 == 0:
        res_a = PROBS["mutation"]
    elif g_parent1 == 1:
        res_a = 0.5
    elif g_parent1 == 2:
        res_a = 1 - PROBS["mutation"]
    
    # prob. the gene is not taken from parent 2
    if g_parent2 == 0:
        res_b = PROBS["mutation"]
    elif g_parent2 == 1:
        res_b = 0.5
    elif g_parent2 == 2:
        res_b = 1 - PROBS["mutation"]

    return res_a * res_b


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    families = whole_family_info(people, one_gene, two_genes, have_trait)
    joint_p = 1
    for person in families.values():
        if person["parents_genes"] is None:
            person_genes = person["genes"]
            p_gene = PROBS["gene"][person_genes]
            p_trait = PROBS["trait"][person_genes][person["trait"]]
            joint_p = joint_p * p_gene * p_trait
        else:
            parents_g = person["parents_genes"]
            if person["genes"] == 0:
                p_gene = prob_0_genes_not_from_p1_nor_from_p2(parents_g["mother"], parents_g["father"])
            elif person["genes"] == 1:
                p_gene = prob_1_gene_from_p1_and_not_from_p2(parents_g["mother"], parents_g["father"]) \
                    + prob_1_gene_from_p1_and_not_from_p2(parents_g["father"], parents_g["mother"])
            elif person["genes"] == 2:
                p_gene = prob_2_genes_from_p1_and_from_p2(parents_g["mother"], parents_g["father"])

            p_trait = PROBS["trait"][person["genes"]][person["trait"]]
            joint_p = joint_p * p_gene * p_trait

    return joint_p


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities.keys():
        probabilities[person]["gene"][genes_of_person(person, one_gene, two_genes)] += p
        probabilities[person]["trait"][person in have_trait] += p
    return


def normalize_distribution(person_distribution):
    factor = 0
    for p_key in person_distribution.values():
        factor += p_key

    factor = 1 / factor
    for key, p_key in person_distribution.items():
        person_distribution[key] = p_key * factor
    return


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities.keys():
        normalize_distribution(probabilities[person]["gene"])
        normalize_distribution(probabilities[person]["trait"])
    return


if __name__ == "__main__":
    main()
