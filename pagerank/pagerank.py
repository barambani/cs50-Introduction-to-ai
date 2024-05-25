import os
import random
import re
import sys
import math

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    result = dict()
    for corpus_page in corpus.keys():
        result[corpus_page] = 1 / len(corpus) * (1 - damping_factor)

        if len(corpus[page]) == 0:
            result[corpus_page] = 1 / len(corpus) * damping_factor + result[corpus_page]
        elif corpus_page in corpus[page]:
            result[corpus_page] = 1 / len(corpus[page]) * damping_factor + result[corpus_page]

    return dict(sorted(result.items()))


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    result = dict()
    next_sample = random.choice(list(corpus.keys()))
    result[next_sample] = 1
    for _ in range(1, n):
        next_ps = transition_model(corpus, next_sample, damping_factor)
        next_sample = random.choices(list(next_ps.keys()), list(next_ps.values()))[0]
        result[next_sample] = result[next_sample] + 1 if next_sample in result else 1

    for k, v in result.items():
        result[k] = v / n

    return dict(sorted(result.items()))


def get_linking_pages_corpus(corpus):
    """
    Returns a dictionary with the pages in the corpus in the key
    and a set with all the pages that link to the key in the value.
    """

    def add_to_linking_pages(key, new_value, corups_dict):
        if key in corups_dict:
            corups_dict[key].add(new_value)
        else:
            corups_dict[key] = { new_value }

    linking_pages = dict()
    for linking_page in corpus.keys():
        if len(corpus[linking_page]) == 0:
            for corpus_page in corpus.keys():
                add_to_linking_pages(corpus_page, linking_page, linking_pages)
        else:
            for linked_page in corpus[linking_page]:
                add_to_linking_pages(linked_page, linking_page, linking_pages)

    for missing in set(corpus.keys()) - set(linking_pages.keys()):
        linking_pages[missing] = {}

    return dict(sorted(linking_pages.items()))


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    accuracy = 0.001
    page_n = len(corpus)
    result = dict()
    linking_pages_corpus = get_linking_pages_corpus(corpus)

    for page in corpus.keys():
        result[page] = 1 / page_n

    while True:
        changed = False
        cycle_result = result.copy()

        for page in result.keys():
            current_rank = result[page]
            linking_pages = linking_pages_corpus[page]
            
            linking_pages_p = list(map(
                lambda x: result[x] / (len(corpus[x]) if len(corpus[x]) > 0 else len(corpus.keys())),
                linking_pages)
            )
            new_rank = round(((1 - damping_factor) / page_n) + damping_factor * sum(linking_pages_p), 12)

            if not math.isclose(new_rank, current_rank, abs_tol = accuracy):
                cycle_result[page] = new_rank
                changed = changed or True

        result = cycle_result
        if not changed:
            break

    return dict(sorted(result.items()))


if __name__ == "__main__":
    main()
