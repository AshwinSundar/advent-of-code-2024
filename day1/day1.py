from functools import reduce
from typing import List

def split_lists(filename):
    col1 = []
    col2 = []

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split('   ')
            if len(parts) >= 2:
                col1.append(int(parts[0]))
                col2.append(int(parts[1]))
                
    return col1, col2

filename = "day1-input.txt"
list1, list2 = split_lists(filename)

sorted_list1 = sorted(list1)
sorted_list2 = sorted(list2)

def pairwise_diff(list1, list2):
    return reduce(lambda l1, l2: l1+l2, [abs(list1[i] - list2[i]) for i in range(len(list1))])

def similarity_score(list1, list2):
    def inner_compare(val, lst: List[int]):
        return reduce(lambda acc, l: acc+val if l == val else acc, lst, 0)

    return reduce(lambda acc, innerRes: acc+innerRes, [inner_compare(list1[i], list2) for i in range(len(list1))], 0)

print(similarity_score(sorted_list1, sorted_list2))
# print(pairwise_diff(sorted_list1, sorted_list2))
