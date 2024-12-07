from dataclasses import dataclass
from datetime import datetime
import random
import string


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


"""
Remaining functions taken from https://www.kaggle.com/datasets/thedevastator/python-code-instruction-dataset
"""


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
            if len(permutation) > 0 and myString[i] == permutation[0]:  # Fixed bug on this line
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


def infix_to_postfix(infix_expr: str):
    prec = {}
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    opStack = []
    postfixList = []
    tokenList = infix_expr.split()

    for token in tokenList:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "0123456789":
            postfixList.append(token)
        elif token == "(":
            opStack.append(token)
        elif token == ")":
            topToken = opStack.pop()
            while topToken != "(":
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (len(opStack) != 0) and (prec[opStack[-1]] >= prec[token]):
                postfixList.append(opStack.pop())
            opStack.append(token)

    while len(opStack) != 0:
        postfixList.append(opStack.pop())
    return " ".join(postfixList)


def is_prime(num: int):
    for i in range(2, num):
        if num % i == 0:
            return False
    return True


def median(nums: list[int]):
    nums.sort()
    length = len(nums)
    is_even = length % 2 == 0
    if is_even:
        mid = length // 2
        return (nums[mid] + nums[mid - 1]) / 2
    else:
        return nums[length // 2]


def insertionSort(array: list[float]):
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and key < array[j]:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key


def find_common_elements(set1: list[int], set2: list[int]):
    common_elements = []
    for item in set1:
        if item in set2 and item not in common_elements:
            common_elements.append(item)
    return common_elements


def difference(list1: list[int], list2: list[int]):
    difference_list = []
    for num1 in list1:
        if num1 not in list2:
            difference_list.append(num1)
    for num2 in list2:
        if num2 not in list1:
            difference_list.append(num2)
    return difference_list


def is_palindrome(s: str):
    rev_s = s[::-1]

    if s == rev_s:
        return True
    else:
        return False


def primeSum(lower: int, upper: int):
    sum = 0
    for num in range(lower, upper + 1):
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else:
                sum += num

    return sum


def check_leap_year(year: int):
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                print("{0} is a leap year".format(year))
            else:
                print("{0} is not a leap year".format(year))
        else:
            print("{0} is a leap year".format(year))
    else:
        print("{0} is not a leap year".format(year))


def selection_sort(arr: list[int]):
    for i in range(0, len(arr) - 1):
        min = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min]:
                min = j
        arr[i], arr[min] = arr[min], arr[i]


def is_anagram(s1: str, s2: str):
    s1_list = list(s1)
    s1_list.sort()
    s2_list = list(s2)
    s2_list.sort()

    if s1_list == s2_list:
        return True
    else:
        return False


def extract_domain_name(url: str):
    split_url = url.split("//")
    if len(split_url) == 2:
        domain_name = split_url[1]
    else:
        domain_name = split_url[0]

    split_domain_name = domain_name.split("/")
    return split_domain_name[0]


def is_unique(string: str):
    characters = set()
    for char in string:
        if char in characters:
            return False
        characters.add(char)
    return True


def group_by_department(employees: list[dict[str, str]]):
    result = {}
    for emp in employees:
        if emp["department"] in result:
            result[emp["department"]].append(emp)
        else:
            result[emp["department"]] = [emp]
    return result


def search(list: list[str], query: str):
    found_indices = []
    for i in range(len(list)):
        if list[i] == query:
            found_indices.append(i)
    return found_indices


def bot_responses(input_message: str):

    # Responses when the user is asking to book an appointment
    if input_message.lower() == "i want to book an appointment":  # Edited: FIXED BUG
        return "OK, please provide the following details: date, time, name, and the doctor you would like to visit."

    # Responses when the user is providing the required details
    elif (
        "date" in input_message.lower()
        and "time" in input_message.lower()
        and "name" in input_message.lower()
        and "doctor" in input_message.lower()
    ):
        return "Your appointment has been booked. Please arrive 15 minutes before your appointment time."

    # Random response to other messages
    else:
        responses = ["I'm sorry, I don't understand.", "Can you please rephrase that?", "What do you mean?"]
        return random.choice(responses)


def form_subarrays(array: list[int], k: int):
    # Edited: add check to prevent infinite loop
    if k <= 0:
        raise Exception("Invalid length")

    subarrays = []
    start = 0
    end = k

    # loop until all of the elements are placed in
    # subarrays
    while start < len(array):
        subarrays.append(array[start:end])
        start += k
        end += k

    return subarrays


def get_probability_of_equal(arr: list[int]):
    # Get the number of elements in the array
    n = len(arr)

    # Get the number of occurrences of the values
    count = [0] * n
    for i in range(n):
        count[arr[i] - 1] += 1

    # Calculate the probability
    probability = 1.0
    for i in range(n):
        probability *= count[i] / n

    return probability


def bubble_sort(items: list[int]):
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(items) - 1):
            if items[i] > items[i + 1]:
                items[i], items[i + 1] = items[i + 1], items[i]
                swapped = True
    return items


def order_without_nlogn(arr: list[float]):
    n = len(arr)

    # Traverse through all array elements
    for i in range(n):

        # Last i elements are already in place
        for j in range(0, n - i - 1):

            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


def move_items(list1: list[int], list2: list[int]):
    for item in list1:
        list2.append(item)
    for i in range(len(list1)):
        list1.pop()


def array_sum(arr: list[float]):
    sum_arr = 0
    for _ in range(len(arr)):
        sum_arr += arr[_]
    return sum_arr


def find_max(arr: list[int]):
    max_num = arr[0]
    for num in arr:
        if num > max_num:
            max_num = num
    return max_num


def remove_vowels(s: str):
    vowels = ("a", "e", "i", "o", "u")
    for x in s:
        if x in vowels:
            s = s.replace(x, "")
    return s


def sum_natural_numbers(n: int):
    if n < 1:
        return 0
    else:
        return n + sum_natural_numbers(n - 1)


def common_substring(str1: str, str2: str):
    longest = ""
    for i in range(len(str1)):
        for j in range(len(str2)):
            pos = 0
            while str1[i + pos] == str2[j + pos]:
                pos += 1
                if (i + pos >= len(str1)) or (j + pos >= len(str2)):
                    break
            if pos > len(longest):
                longest = str1[i : i + pos]
    return longest


def find_max_min(lst: list[float]):
    if len(lst) == 1:
        return lst[0], lst[0]

    elif len(lst) == 2:
        return max(lst), min(lst)

    mid = len(lst) // 2
    left_max, left_min = find_max_min(lst[:mid])
    right_max, right_min = find_max_min(lst[mid:])

    return max(left_max, right_max), min(left_min, right_min)


def countVowels(string: str):

    vowels = "aeiouAEIOU"
    count = 0

    for char in string:
        if char in vowels:
            count += 1

    return count


def max_int(a: int, b: int):
    if a > b:
        return a
    else:
        return b


def classify(salary: float):
    if salary <= 10000:
        return "low"
    elif salary <= 30000:
        return "medium"
    else:
        return "high"


def most_frequent(list: list[int]):
    counter = 0
    num = list[0]

    for i in list:
        curr_frequency = list.count(i)
        if curr_frequency > counter:
            counter = curr_frequency
            num = i

    return num


def hammingDistance(string1: str, string2: str):
    if len(string1) != len(string2):
        raise ValueError("Strings must be of equal length.")

    distance = 0

    for c1, c2 in zip(string1, string2):
        if c1 != c2:
            distance += 1

    return distance


def find_two_add_up_to_target(nums: list[int], target: int):
    for num1 in nums:
        for num2 in nums:
            if num1 + num2 == target:
                return True
    return False


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
    # all_palindromic_permutations, # Excluded due to infinite loop
    celsius_to_fahrenheit,
    character_count,
    lcs,
    infix_to_postfix,
    is_prime,
    median,
    insertionSort,
    find_common_elements,
    difference,
    is_palindrome,
    # primeSum, # Excluded due to exection time
    check_leap_year,
    selection_sort,
    is_anagram,
    extract_domain_name,
    group_by_department,  # Needs dictionary support
    search,
    bot_responses,
    form_subarrays,
    get_probability_of_equal,
    bubble_sort,
    order_without_nlogn,
    move_items,
    array_sum,
    find_max,
    remove_vowels,
    sum_natural_numbers,
    common_substring,
    find_max_min,
    countVowels,
    max_int,
    classify,
    most_frequent,
    hammingDistance,
    find_two_add_up_to_target,
]


def probability_of_heads(n: int):
    total_outcomes = 2**n
    heads_outcomes = total_outcomes / 2

    probability_of_heads = heads_outcomes / total_outcomes

    return probability_of_heads


def getRandomName(names: list[str]):
    randomIndex = random.randint(0, len(names) - 1)
    return names[randomIndex]


def replace_whitespaces(string: str, character: str):
    return string.replace(" ", character)


def generate_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    size = 10
    return "".join(random.choice(chars) for x in range(size, 20))


def normalize(data: list[float]):
    """Performs standard normalization of a given data"""
    mean = sum(data) / len(data)
    std_dev = (sum([(x - mean) ** 2 for x in data]) / len(data)) ** 0.5
    return [(x - mean) / std_dev for x in data]


def joinStrings(s1: str, s2: str):
    return s1 + s2


def to_lower(arr: list[str]):
    return [item.lower() for item in arr]


def remove_duplicates(lst: list[int]):
    return list(dict.fromkeys(lst))


def generate_html_doc(solution: str):
    html = "<html>\n<head>\n<title>Python Documentation</title>\n</head>\n<body>\n\n<h1>Solution</h1>\n<pre>\n"
    html += solution + "\n</pre>\n\n</body>\n</html>"
    return html


non_path_test_funcs = [
    probability_of_heads,
    getRandomName,
    replace_whitespaces,
    generate_password,
    normalize,
    joinStrings,
    to_lower,
    remove_duplicates,
    generate_html_doc,
]
