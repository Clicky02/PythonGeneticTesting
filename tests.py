from dataclasses import dataclass
from datetime import datetime


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


MY_CONST = 7.0


def testable_float(a: float, b: float):
    if a < 3.0:
        return 5
    pass
    pass
    pass
    if b != MY_CONST:
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


def third_largest(lst: list[int]):
    if len(lst) < 3:
        return
    distinct = []
    for i in lst:
        if i not in distinct:
            distinct.append(i)
    distinct.sort(reverse=True)
    return distinct[2]


def contains_words(input_string: str, words: list[str]):
    for word in words:
        if word not in input_string:
            return False
    return True


def find_numbers_divisible_by(m: int, n: int, divisor: int):
    divisible_numbers = []
    for i in range(m, n + 1):
        if i % divisor == 0:
            divisible_numbers.append(i)
    return divisible_numbers


def check_contains(query: str, word: str):
    if query.find(word) != -1:
        return True
    return False


def factorial(n: int):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def fibonacci(n: int):
    a = 0
    b = 1
    if n < 0:
        print("Incorrect input")
    elif n == 0:
        return a
    elif n == 1:
        return b
    else:
        for i in range(2, n):
            c = a + b
            a = b
            b = c
        return b


def sum_digits(num: int):
    total = 0
    while num > 0:
        digit = num % 10
        total += digit
        num = num // 10
    return total


def sort_by_length(strings: list[str]):
    for i in range(len(strings) - 1):
        for j in range(i + 1, len(strings)):
            if len(strings[i]) > len(strings[j]):
                strings[i], strings[j] = strings[j], strings[i]
    return strings


def get_max_min(lst: list[int]):
    min_value = lst[0]
    max_value = lst[0]

    for i in range(1, len(lst)):
        if lst[i] > max_value:
            max_value = lst[i]
        if lst[i] < min_value:
            min_value = lst[i]

    return (min_value, max_value)


def merge_sort(A: list[int], B: list[int]):
    result = []
    i, j = 0, 0

    # Compare elements and add lower one to result
    while i < len(A) and j < len(B):
        if A[i] < B[j]:
            result.append(A[i])
            i += 1
        else:
            result.append(B[j])
            j += 1

        # Add remaining elements
        result += A[i:]
        result += B[j:]

    return result


def is_in_rectangle(x: float, y: float, bx: float, by: float, tx: float, ty: float):
    """
    Check if a given data point is inside a given
    rectangle shaped area.
    """

    # Check if (x,y) is inside the rectangle
    if bx <= x <= tx and by <= y <= ty:
        return True
    else:
        return False


def linear_search(list: list[int], x: int):
    for i in range(len(list)):
        if list[i] == x:
            return i
    return -1


def hours_difference(time1: str, time2: str):
    """
    This program takes two times and calculates the number of hours between them
    """
    time_format = "%I:%M%p"  # 12-hour clock AM/PM
    datetime1 = datetime.strptime(time1, time_format)
    datetime2 = datetime.strptime(time2, time_format)
    difference = datetime2 - datetime1
    return difference.seconds / 3600


def code_generator(code_base: str):
    updated_code = []
    lines = code_base.splitlines()
    for line in lines:
        # Tokenize the line
        tokens = line.split(" ")

        # Find the tokens that need to be updated
        modified_tokens = [token for token in tokens if token.startswith("[") and token.endswith("]")]

        # Replace the tokens with new ones
        for token in modified_tokens:
            new_token = token.replace("[", "")
            new_token = new_token.replace("]", "")
            new_token = "<generated-token>"
            line = line.replace(token, new_token)

        updated_code.append(line)
    return "\n".join(updated_code)


def find_second_largest_number(input_list: list[float]):
    """Finds the second largest number in a given list."""
    first = float("-infinity")
    second = float("-infinity")

    for num in input_list:
        if num > first:
            second = first
            first = num
        elif num > second and num != first:
            second = num

    return second


def find_all_indices(list: list[str], item: str):
    result = []
    for index, i in enumerate(list):
        if i == item:
            result.append(index)
    return result


def all_palindromic_permutations(myString: str):
    if len(myString) == 0:
        return [""]

    permutationList = []
    for i in range(len(myString)):
        subString = myString[:i] + myString[i + 1 :]
        partList = all_palindromic_permutations(subString)

        for permutation in partList:
            if myString[i] == permutation[0]:
                permutationList.append(myString[i] + permutation + myString[i])
            else:
                permutationList.append(permutation + myString[i])

    return list(set(permutationList))


def celsius_to_fahrenheit(temp_celsius: float):
    temp_fahrenheit = (temp_celsius * 9 / 5) + 32
    return temp_fahrenheit


def character_count(str: str):
    d = dict()
    for c in str:
        if c in d:
            d[c] += 1
        else:
            d[c] = 1
    return d


def lcs(string1: str, string2: str):
    n = len(string1)
    m = len(string2)

    dp = [[0 for x in range(m + 1)] for x in range(n + 1)]

    # fill dp table in bottom up manner
    for i in range(n + 1):
        for j in range(m + 1):
            if i == 0 or j == 0:
                dp[i][j] = 0
            elif string1[i - 1] == string2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    index = dp[n][m]

    # Create an array of size of lcs
    longest_common_subsequence = [""] * (index + 1)
    longest_common_subsequence[index] = ""

    # Start from the right-most-bottom-most corner and
    # one by one store characters in lcs[]
    i = n
    j = m
    while i > 0 and j > 0:

        # If current character in X[] and Y are same, then
        # current character is part of LCS
        if string1[i - 1] == string2[j - 1]:
            longest_common_subsequence[index - 1] = string1[i - 1]
            i -= 1
            j -= 1
            index -= 1

        # If not same, then find the larger of two and
        # go in the direction of larger value
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return "".join(longest_common_subsequence)


test_funcs = [
    testable_int,
    testable_float,
    testable_str,
    longest_consecutive_subsequence,
    third_largest,
    contains_words,
    find_numbers_divisible_by,
    check_contains,
    factorial,
    fibonacci,
    sum_digits,
    sort_by_length,
    get_max_min,
    merge_sort,
    is_in_rectangle,
    linear_search,
    hours_difference,
    code_generator,
    find_second_largest_number,
    find_all_indices,
    all_palindromic_permutations,
    celsius_to_fahrenheit,
    character_count,
    lcs,
]
