""" 
File Name: tags.py
Creator: Ghazanfar Shahbaz
Creaetd: 08/05/2023
Last Updated: 08/05/2023
Description: Provides functionality for linking tags to links and database tables
Edit Log:
08/05/2023
- Moved over file from leetcode bot
"""

from typing import Dict, Tuple, Final

TAGS: Final[Dict[str, str]] = {
    "Arrays": "https://leetcode.com/problemset/all/?topicSlugs=array",
    "Hash Table": "https://leetcode.com/problemset/all/?topicSlugs=hash-table",
    "Linked Lists": "https://leetcode.com/problemset/all/?topicSlugs=linked-list",
    "Math": "https://leetcode.com/problemset/all/?topicSlugs=math",
    "Two Pointers": "https://leetcode.com/problemset/all/?topicSlugs=two-pointers",
    "String": "https://leetcode.com/problemset/all/?topicSlugs=string",
    "Binary Search": "https://leetcode.com/problemset/all/?topicSlugs=binary-search",
    "Divide and Conquer": "https://leetcode.com/problemset/all/?topicSlugs=divide-and-conquer",
    "Dynamic Programming": "https://leetcode.com/problemset/all/?topicSlugs=dynamic-programming",
    "Backtracking": "https://leetcode.com/problemset/all/?topicSlugs=backtracking",
    "Stack": "https://leetcode.com/problemset/all/?topicSlugs=stack",
    "Heap": "https://leetcode.com/problemset/all/?topicSlugs=heap",
    "Greedy": "https://leetcode.com/problemset/all/?topicSlugs=greedy",
    "Sort": "https://leetcode.com/problemset/all/?topicSlugs=sort",
    "Bit Manipulation": "https://leetcode.com/problemset/all/?topicSlugs=bit-manipulation",
    "Tree": "https://leetcode.com/problemset/all/?topicSlugs=tree",
    "Depth First Search": "https://leetcode.com/problemset/all/?topicSlugs=depth-first-search",
    "Breadth First Search": "https://leetcode.com/problemset/all/?topicSlugs=breadth-first-search",
    "Union Find": "https://leetcode.com/problemset/all/?topicSlugs=union-find",
    "Graph": "https://leetcode.com/problemset/all/?topicSlugs=graph",
    "Design": "https://leetcode.com/problemset/all/?topicSlugs=design",
    "Topological Sort": "https://leetcode.com/problemset/all/?topicSlugs=topological-sort",
    "Trie": "https://leetcode.com/problemset/all/?topicSlugs=trie",
    "Binary Indexed Tree": "https://leetcode.com/problemset/all/?topicSlugs=binary-indexed-tree",
    "Segment Tree": "https://leetcode.com/problemset/all/?topicSlugs=segment-tree",
    "Binary Search Tree": "https://leetcode.com/problemset/all/?topicSlugs=binary-search-tree",
    "Recursion": "https://leetcode.com/problemset/all/?topicSlugs=recursion",
    "Brain Teaser": "https://leetcode.com/problemset/all/?topicSlugs=brainteaser",
    "Memoization": "https://leetcode.com/problemset/all/?topicSlugs=memoization",
    "Queue": "https://leetcode.com/problemset/all/?topicSlugs=queue",
    "Minimax": "https://leetcode.com/problemset/all/?topicSlugs=minimax",
    "Reservoir Sampling": "https://leetcode.com/problemset/all/?topicSlugs=reservoir-sampling",
    "Ordered Map": "https://leetcode.com/problemset/all/?topicSlugs=ordered-map",
    "Geometry": "https://leetcode.com/problemset/all/?topicSlugs=geometry",
    "Random": "https://leetcode.com/problemset/all/?topicSlugs=random",
    "Rejection Sampling": "https://leetcode.com/problemset/all/?topicSlugs=rejection-sampling",
    "Sliding Window": "https://leetcode.com/problemset/all/?topicSlugs=sliding-window",
    "Line Sweep": "https://leetcode.com/problemset/concurrency/?topicSlugs=line-sweep",
    "Rolling Hash": "https://leetcode.com/problemset/concurrency/?topicSlugs=rolling-hash",
    "Suffix Array": "https://leetcode.com/problemset/concurrency/?topicSlugs=suffix-array",
}

TAG_CORR: Final[Dict[str, str]] = {
    "Arrays": "arrays",
    "Backtracking": "backtracking",
    "Binary Indexed Tree": "binary_indexed_tree",
    "Binary Search": "binary_search",
    "Binary Search Tree": "binary_search_tree",
    "Bit Manipulation": "bit_manipulation",
    "Brain Teaser": "brain_teaser",
    "Breadth First Search": "breadth_first_search",
    "Depth First Search": "depth_first_search",
    "Design": "design",
    "Divide and Conquer": "divide_and_conquer",
    "Dynamic Programming": "dynamic_programming",
    "Geometry": "geometry",
    "Graph": "graph",
    "Greedy": "greedy",
    "Hash Table": "hash_table",
    "Heap": "heap",
    "Line Sweep": "line_sweep",
    "Linked Lists": "linked_lists",
    "Math": "math",
    "Memoization": "memoization",
    "Minimax": "minimax",
    "Ordered Map": "ordered_map",
    "Queue": "queue",
    "Random": "random",
    "Recursion": "recursion",
    "Rejection Sampling": "rejection_sampling",
    "Reservoir Sampling": "reservoir_sampling",
    "Rolling Hash": "rolling_hash",
    "Segment Tree": "segment_tree",
    "Sliding Window": "sliding_window",
    "Sort": "sort",
    "Stack": "stack",
    "String": "string",
    "Suffix Array": "suffix_array",
    "Topological Sort": "topological_sort",
    "Tree": "tree",
    "Trie": "trie",
    "Two Pointers": "two_pointers",
    "Union Find": "union_find",
}


def get_tags() -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Returns a tuple containing a list of all available tags and a dictionary mapping
    tags to their full names.

    Returns:
        Tuple[List[str], Dict[str, str]]: A tuple containing a list of all available tags
                                          and a dictionary mapping tags to their full names.
    """
    return TAGS, TAG_CORR
