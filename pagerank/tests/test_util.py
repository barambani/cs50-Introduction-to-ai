import math

def are_page_ranks_close(dict_a, dict_b, tol = 0.002):
    result = True

    if len(dict_a) != len(dict_b):
        return False

    for k, v in dict_a.items():
        result = result and math.isclose(v, dict_b[k], abs_tol = tol)
    return result