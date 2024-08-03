from shopping.shopping import *


def parse_data_test_1():
    evidence, labels = load_data("./shopping.csv")
    evidence, labels = [evidence[0], evidence[76]], [labels[0], labels[76]]
    expected_evidence = [
        [0,0,0,0,1,0,0.2,0.2,0,0,1,1,1,1,1,1,0],
        [10, 1005.666667, 0, 0, 36,2111.341667, 0.004347826, 0.014492754, 11.43941195, 0, 1, 2, 6, 1, 2, 1, 0],
    ]
    expecte_labels = [0, 1]
    assert evidence == expected_evidence, f'Evidences - Found: {evidence}. Should be {expected_evidence}'
    assert labels == expecte_labels, f'Labels - Found: {labels}. Should be {expecte_labels}'