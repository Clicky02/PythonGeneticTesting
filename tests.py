from dataclasses import dataclass


@dataclass
class A:
    a: int
    b: float
    c: str


JOHN = "ASA"


def testable_int(a: int, b: int):
    if a < 0:  # 2
        return 5
    pass
    pass
    if b < 10:  # 3
        pass
        if a > 6:  # 4
            pass
        else:
            pass
            pass
    pass
    g = A(a, 0.0, JOHN)
    return 3


def testable_float(a: float, b: float):
    if a < 3.0:
        return 5
    pass
    pass
    pass
    if b != 7.0:
        return 5
    pass
    if a > b:
        return 3
    else:
        return 5


def testable_str(a: str, b: str):
    if "x" in a:
        return 1
    pass
    pass
    if b in a:
        return 2
    pass
    if "a" in b or "b" in b or "c" in b:
        return 5


def longest_consecutive_subsequence(nums: list[int]):
    """
    Finds the length of the longest subsequence of consecutive integers in an unsorted list.

    Args:
        nums (list): A list of integers.

    Returns:
        int: Length of the longest subsequence of consecutive integers.
    """
    if not nums:
        return 0

    # Sort the numbers
    nums = sorted(nums)

    # Initialize variables
    max_length = 1
    current_length = 1

    # Iterate through the sorted list
    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1] + 1:
            # Increment current sequence length
            current_length += 1
        elif nums[i] != nums[i - 1]:
            # Reset current sequence length
            max_length = max(max_length, current_length)
            current_length = 1

    # Check final sequence
    max_length = max(max_length, current_length)

    return max_length
