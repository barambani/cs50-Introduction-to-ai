from hypothesis import strategies as str

def states(len, max_count) -> str.SearchStrategy[list[int]]:
    return str.lists(
        str.integers(0, max_count), min_size = 1, max_size = len
    ).filter(
        lambda xs: any([s for s in xs if s > 0])
    )