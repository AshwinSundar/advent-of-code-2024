from typing import List
from functools import reduce

def is_increasing(list: List[int]):
    pairs = zip(list, list[1:])
    return not any(a >= b for a, b in pairs)

def is_decreasing(list: List[int]):
    pairs = zip(list, list[1:])
    return not any(a <= b for a, b in pairs)

def slowly_changes(list: List[int]):
    pairs = zip(list, list[1:])
    return not any((abs(a-b) > 3) for a, b in pairs)


def count_safe_records(filename: str):
    def create_record(line: str):
        return list(map(int, line.strip().split(' ')))

    def check_original():
        with open(filename, 'r') as file:
            return reduce(
                lambda acc, record: acc+1 if slowly_changes(record) and (is_increasing(record) or is_decreasing(record)) else acc, 
                map(create_record, file), 
                0
            )

    def is_safe(record: List[int]) -> bool:
        return slowly_changes(record) and (is_increasing(record) or is_decreasing(record))

    def check_with_removals(record: List[int]) -> bool:
        # Check if already safe
        if is_safe(record):
            return True
        # Try removing each value
        return any(
            is_safe(record[:i] + record[i+1:])
            for i in range(len(record))
        )

    with open(filename, 'r') as file:
        return reduce(
            lambda acc, record: acc + (1 if check_with_removals(record) else 0),
            map(create_record, file),
            0
        )

print(count_safe_records("day2-input.txt"))
           
