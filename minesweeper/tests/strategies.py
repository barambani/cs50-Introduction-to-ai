from hypothesis import strategies as str


def cells(height, width) -> str.SearchStrategy[set[tuple[int, int]]]:
    return str.sets(str.tuples(str.integers(0, height - 1), str.integers(0, width - 1)))