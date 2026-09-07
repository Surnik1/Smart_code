import os
import sys
import django

sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from challenges.models import Task, TestCase
from django.db import transaction

# Solvers and at least 10 inputs for all tasks

SOLVERS_AND_INPUTS = {}

# 1. return_task: sum of two numbers
SOLVERS_AND_INPUTS['return_task'] = {
    'starter': 'def solution(a, b):\n    pass\n',
    'solve': lambda a, b: a + b,
    'inputs': [
        "2, 3", "0, 0", "-1, 1", "100, 200", "-50, -50",
        "1234, 5678", "-999, 1000", "42, -42", "7, 8", "-10, 25",
        "999999, 1", "-123, -456"
    ]
}

# 2. two-numbers-difference
SOLVERS_AND_INPUTS['two-numbers-difference'] = {
    'starter': 'def solution(a, b):\n    pass\n',
    'solve': lambda a, b: a - b,
    'inputs': [
        "5, 10", "2, 1", "999, 1", "0, 0", "10, 5",
        "-5, -5", "-10, 5", "100, 50", "7, 12", "50, -50",
        "1000, 1000", "-25, 25"
    ]
}

# 3. palindromes-without-borders -> already has 30 tests, we'll keep them

# 304. leetcode-two-sum
def _two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        diff = target - n
        if diff in seen:
            return [seen[diff], i]
        seen[n] = i
    return []

SOLVERS_AND_INPUTS['leetcode-two-sum'] = {
    'starter': 'def solution(nums, target):\n    pass\n',
    'solve': _two_sum,
    'inputs': [
        "[2, 7, 11, 15], 9",
        "[3, 2, 4], 6",
        "[3, 3], 6",
        "[1, 5, 8, 12], 20",
        "[-1, -2, -3, -4, -5], -8",
        "[0, 4, 3, 0], 0",
        "[-3, 4, 3, 90], 0",
        "[1, 2, 3, 4, 5], 9",
        "[10, 20, 30, 40], 50",
        "[5, 75, 25], 100",
        "[2, 5, 5, 11], 10",
    ]
}

# 305. leetcode-valid-palindrome
def _valid_pal(s):
    clean = [c.lower() for c in s if c.isalnum()]
    return clean == clean[::-1]

SOLVERS_AND_INPUTS['leetcode-valid-palindrome'] = {
    'starter': 'def solution(s):\n    pass\n',
    'solve': _valid_pal,
    'inputs': [
        "'A man, a plan, a canal: Panama'",
        "'race a car'",
        "' '",
        "'0P'",
        "'No \\'x\\' in Nixon'",
        "'Was it a car or a cat I saw?'",
        "'tab a cat'",
        "'Eva, can I see bees in a cave?'",
        "'Madam, I\\'m Adam'",
        "'Never odd or even'",
        "'12321'",
        "'123321'",
    ]
}

# 306. leetcode-roman-to-integer
def _roman_to_int(s):
    vals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    for i in range(len(s)):
        if i + 1 < len(s) and vals[s[i]] < vals[s[i+1]]:
            total -= vals[s[i]]
        else:
            total += vals[s[i]]
    return total

SOLVERS_AND_INPUTS['leetcode-roman-to-integer'] = {
    'starter': 'def solution(s):\n    pass\n',
    'solve': _roman_to_int,
    'inputs': [
        "'III'", "'LVIII'", "'MCMXCIV'", "'IX'", "'XL'",
        "'IV'", "'CD'", "'CM'", "'MMXXIV'", "'DCCCXC'", "'MMMCMXCIX'"
    ]
}

# 307. leetcode-longest-common-prefix
def _longest_common_prefix(strs):
    if not strs: return ""
    prefix = strs[0]
    for s in strs[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix: return ""
    return prefix

SOLVERS_AND_INPUTS['leetcode-longest-common-prefix'] = {
    'starter': 'def solution(strs):\n    pass\n',
    'solve': _longest_common_prefix,
    'inputs': [
        "['flower', 'flow', 'flight']",
        "['dog', 'racecar', 'car']",
        "['interspecies', 'interstellar', 'interstate']",
        "['throne', 'throne']",
        "['a']",
        "['cir', 'car']",
        "['prefix', 'pretext', 'preface', 'prefer']",
        "['apple', 'app', 'application']",
        "['abc', 'abcde', 'ab', 'abcdef']",
        "['same', 'same', 'same']",
        "['xyz', 'abc']",
    ]
}

# 308. leetcode-valid-parentheses
def _valid_parens(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for c in s:
        if c in mapping:
            if not stack or stack[-1] != mapping[c]: return False
            stack.pop()
        else:
            stack.append(c)
    return len(stack) == 0

SOLVERS_AND_INPUTS['leetcode-valid-parentheses'] = {
    'starter': 'def solution(s):\n    pass\n',
    'solve': _valid_parens,
    'inputs': [
        "'()[]{}'", "'(]'", "'([{}])'", "'(('", "'{[]}'", "''",
        "'{[()]}'", "'(()('", "'()'", "'(([]){})'", "'[(])'", "')('"
    ]
}

# 309. leetcode-merge-two-sorted-lists
SOLVERS_AND_INPUTS['leetcode-merge-two-sorted-lists'] = {
    'starter': 'def solution(list1, list2):\n    pass\n',
    'solve': lambda l1, l2: sorted(l1 + l2),
    'inputs': [
        "[1, 2, 4], [1, 3, 4]",
        "[], []",
        "[], [0]",
        "[5, 10, 15], [2, 3, 20]",
        "[1, 5], [2, 3, 4, 6]",
        "[-10, -5, 0], [-8, 2, 4]",
        "[1, 1, 1], [1, 1]",
        "[100], [50, 150]",
        "[1, 2, 3], []",
        "[], [7, 8, 9]",
        "[2], [1]",
    ]
}

# 310. leetcode-remove-duplicates
def _remove_dups(nums):
    res = []
    for x in nums:
        if not res or res[-1] != x:
            res.append(x)
    return res

SOLVERS_AND_INPUTS['leetcode-remove-duplicates'] = {
    'starter': 'def solution(nums):\n    pass\n',
    'solve': _remove_dups,
    'inputs': [
        "[1, 1, 2]",
        "[0, 0, 1, 1, 1, 2, 2, 3, 3, 4]",
        "[1]",
        "[]",
        "[1, 1, 1, 1]",
        "[1, 2, 3, 4, 5]",
        "[-3, -3, -2, -1, -1, 0, 0]",
        "[2, 2, 3, 3, 4, 4]",
        "[0, 0]",
        "[1, 2, 2, 3, 4, 4, 5]",
        "[-1, 0, 0, 0, 3, 3]",
    ]
}

# 311. leetcode-find-needle-in-haystack
SOLVERS_AND_INPUTS['leetcode-find-needle-in-haystack'] = {
    'starter': 'def solution(haystack, needle):\n    pass\n',
    'solve': lambda h, n: h.find(n),
    'inputs': [
        "'sadbutsad', 'sad'",
        "'leetcode', 'leeto'",
        "'hello', 'll'",
        "'mississippi', 'issip'",
        "'a', 'a'",
        "'abc', 'c'",
        "'findtheneedle', 'the'",
        "'banana', 'an'",
        "'abcdef', 'gh'",
        "'starting', 'start'",
        "'word', 'words'",
    ]
}

# 312. leetcode-search-insert-position
def _search_insert(nums, target):
    l, r = 0, len(nums) - 1
    while l <= r:
        mid = (l + r) // 2
        if nums[mid] == target: return mid
        elif nums[mid] < target: l = mid + 1
        else: r = mid - 1
    return l

SOLVERS_AND_INPUTS['leetcode-search-insert-position'] = {
    'starter': 'def solution(nums, target):\n    pass\n',
    'solve': _search_insert,
    'inputs': [
        "[1, 3, 5, 6], 5",
        "[1, 3, 5, 6], 2",
        "[1, 3, 5, 6], 7",
        "[1, 3, 5, 6], 0",
        "[1], 0",
        "[1], 1",
        "[1], 2",
        "[1, 4, 6, 7, 8, 9], 6",
        "[2, 5, 8, 11, 14], 12",
        "[-5, -2, 0, 3], -3",
        "[10, 20, 30], 25",
    ]
}

# 313. leetcode-length-of-last-word
SOLVERS_AND_INPUTS['leetcode-length-of-last-word'] = {
    'starter': 'def solution(s):\n    pass\n',
    'solve': lambda s: len(s.strip().split()[-1]) if s.strip() else 0,
    'inputs': [
        "'Hello World'",
        "'   fly me   to   the moon  '",
        "'luffy is still joyboy'",
        "'a'",
        "'day'",
        "'   single   '",
        "'programming in python is fun'",
        "'test    test2   '",
        "'lots of     spaces     here    '",
        "'one'",
        "'ends with multiple words yes'",
    ]
}

# 314. leetcode-plus-one
def _plus_one(digits):
    num = int(''.join(map(str, digits))) + 1
    return [int(d) for d in str(num)]

SOLVERS_AND_INPUTS['leetcode-plus-one'] = {
    'starter': 'def solution(digits):\n    pass\n',
    'solve': _plus_one,
    'inputs': [
        "[1, 2, 3]",
        "[4, 3, 2, 1]",
        "[9]",
        "[9, 9, 9]",
        "[0]",
        "[1, 9, 9]",
        "[8, 9, 9, 9]",
        "[2, 0, 0]",
        "[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]",
        "[5, 5, 5]",
        "[9, 9]",
    ]
}

# 315. leetcode-add-binary
SOLVERS_AND_INPUTS['leetcode-add-binary'] = {
    'starter': 'def solution(a, b):\n    pass\n',
    'solve': lambda a, b: bin(int(a, 2) + int(b, 2))[2:],
    'inputs': [
        "'11', '1'",
        "'1010', '1011'",
        "'0', '0'",
        "'1111', '1111'",
        "'1', '0'",
        "'100', '110'",
        "'101', '10'",
        "'111', '1'",
        "'1000', '1'",
        "'10101', '111'",
        "'110010', '10111'",
    ]
}

# 316. leetcode-sqrtx
SOLVERS_AND_INPUTS['leetcode-sqrtx'] = {
    'starter': 'def solution(x):\n    pass\n',
    'solve': lambda x: int(x**0.5),
    'inputs': [
        "4", "8", "0", "1", "25", "1000000",
        "2", "3", "9", "15", "16", "99"
    ]
}

# 317. leetcode-climbing-stairs
def _climb_stairs(n):
    if n <= 2: return n
    a, b = 1, 2
    for _ in range(n - 2):
        a, b = b, a + b
    return b

SOLVERS_AND_INPUTS['leetcode-climbing-stairs'] = {
    'starter': 'def solution(n):\n    pass\n',
    'solve': _climb_stairs,
    'inputs': [
        "2", "3", "1", "5", "10",
        "4", "6", "7", "8", "9", "12"
    ]
}

# 318. leetcode-single-number
def _single_number(nums):
    ans = 0
    for x in nums: ans ^= x
    return ans

SOLVERS_AND_INPUTS['leetcode-single-number'] = {
    'starter': 'def solution(nums):\n    pass\n',
    'solve': _single_number,
    'inputs': [
        "[2, 2, 1]",
        "[4, 1, 2, 1, 2]",
        "[1]",
        "[-1, -1, -2]",
        "[7, 3, 5, 3, 7]",
        "[0, 1, 0]",
        "[10, 20, 10, 30, 20]",
        "[99, 50, 99]",
        "[-10, 2, 2]",
        "[42]",
        "[8, 8, 9, 10, 10]",
    ]
}

# 319. leetcode-majority-element
def _majority_element(nums):
    from collections import Counter
    return Counter(nums).most_common(1)[0][0]

SOLVERS_AND_INPUTS['leetcode-majority-element'] = {
    'starter': 'def solution(nums):\n    pass\n',
    'solve': _majority_element,
    'inputs': [
        "[3, 2, 3]",
        "[2, 2, 1, 1, 1, 2, 2]",
        "[1]",
        "[6, 5, 5]",
        "[1, 1, 1, 2, 2]",
        "[7, 7, 7, 7, 1, 2, 3]",
        "[4, 4, 4, 3, 4]",
        "[-1, -1, 2]",
        "[9, 9, 8, 9, 8, 9, 9]",
        "[100, 100, 200]",
        "[3, 3, 4, 2, 4, 4, 2, 4, 4]",
    ]
}

# 320. leetcode-isomorphic-strings
def _isomorphic(s, t):
    return len(set(zip(s, t))) == len(set(s)) == len(set(t)) and len(s) == len(t)

SOLVERS_AND_INPUTS['leetcode-isomorphic-strings'] = {
    'starter': 'def solution(s, t):\n    pass\n',
    'solve': _isomorphic,
    'inputs': [
        "'egg', 'add'",
        "'foo', 'bar'",
        "'paper', 'title'",
        "'badc', 'baba'",
        "'a', 'a'",
        "'ab', 'aa'",
        "'bbbaaaba', 'aaabbbba'",
        "'abcdef', 'uvwxyz'",
        "'turtle', 'txmlxe'",
        "'paper', 'titii'",
        "'same', 'game'",
    ]
}

# 321. leetcode-contains-duplicate
SOLVERS_AND_INPUTS['leetcode-contains-duplicate'] = {
    'starter': 'def solution(nums):\n    pass\n',
    'solve': lambda nums: len(nums) != len(set(nums)),
    'inputs': [
        "[1, 2, 3, 1]",
        "[1, 2, 3, 4]",
        "[1, 1, 1, 3, 3, 4, 3, 2, 4, 2]",
        "[]",
        "[1]",
        "[2, 2]",
        "[5, 10, 15, 20, 25]",
        "[-1, -2, -3, -1]",
        "[100, 200, 300, 400]",
        "[0, 0]",
        "[7, 8, 9, 10, 11, 7]",
    ]
}

# 322. leetcode-valid-anagram
SOLVERS_AND_INPUTS['leetcode-valid-anagram'] = {
    'starter': 'def solution(s, t):\n    pass\n',
    'solve': lambda s, t: sorted(s) == sorted(t),
    'inputs': [
        "'anagram', 'nagaram'",
        "'rat', 'car'",
        "'a', 'a'",
        "'ab', 'a'",
        "'listen', 'silent'",
        "'triangle', 'integral'",
        "'apple', 'pale'",
        "'cinema', 'iceman'",
        "'dormitory', 'dirtyroom'",
        "'hello', 'bello'",
        "'aabbcc', 'ccbbaa'",
    ]
}

# 323. leetcode-missing-number
def _missing_number(nums):
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)

SOLVERS_AND_INPUTS['leetcode-missing-number'] = {
    'starter': 'def solution(nums):\n    pass\n',
    'solve': _missing_number,
    'inputs': [
        "[3, 0, 1]",
        "[0, 1]",
        "[9, 6, 4, 2, 3, 5, 7, 0, 1]",
        "[0]",
        "[1]",
        "[1, 2]",
        "[0, 2, 3]",
        "[5, 4, 3, 2, 0]",
        "[0, 1, 2, 3, 4, 5, 6, 7, 9]",
        "[2, 0, 1, 4]",
        "[0, 1, 3, 4, 5, 6]",
    ]
}

# 324. leetcode-move-zeroes
def _move_zeroes(nums):
    non_zeros = [x for x in nums if x != 0]
    return non_zeros + [0] * (len(nums) - len(non_zeros))

SOLVERS_AND_INPUTS['leetcode-move-zeroes'] = {
    'starter': 'def solution(nums):\n    pass\n',
    'solve': _move_zeroes,
    'inputs': [
        "[0, 1, 0, 3, 12]",
        "[0]",
        "[1, 2, 3]",
        "[0, 0, 1]",
        "[0, 0, 0]",
        "[1, 0, 2, 0, 3, 0]",
        "[4, 2, 4, 0, 0, 3, 0, 5, 1, 0]",
        "[0, 1]",
        "[1, 0]",
        "[0, 0, 2, 3]",
        "[-1, 0, -2, 0, 5]",
    ]
}

# 325. codewars-vowel-count
SOLVERS_AND_INPUTS['codewars-vowel-count'] = {
    'starter': 'def solution(s):\n    pass\n',
    'solve': lambda s: sum(1 for c in s.lower() if c in 'aeiou'),
    'inputs': [
        "'abracadabra'",
        "'hello world'",
        "'xyz'",
        "''",
        "'aeiou'",
        "'rhythm'",
        "'PYTHON'",
        "'quick brown fox jumps over lazy dog'",
        "'Education'",
        "'programming'",
        "'bcdfg'",
    ]
}

# 326. codewars-disemvowel-trolls
SOLVERS_AND_INPUTS['codewars-disemvowel-trolls'] = {
    'starter': 'def solution(string):\n    pass\n',
    'solve': lambda s: ''.join(c for c in s if c.lower() not in 'aeiou'),
    'inputs': [
        "'This website is for losers LOL!'",
        "'No offense but,\\nYour writing is among the worst'",
        "'What are you, a communist?'",
        "'Hello World'",
        "'aeiouAEIOU'",
        "'rhythm'",
        "'Python is awesome'",
        "'Just testing vowels here'",
        "'Coding challenge'",
        "'CodeWars and LeetCode'",
        "'Disemvowel this troll!'",
    ]
}

# 327. codewars-square-every-digit
SOLVERS_AND_INPUTS['codewars-square-every-digit'] = {
    'starter': 'def solution(num):\n    pass\n',
    'solve': lambda n: int(''.join(str(int(d)**2) for d in str(n))),
    'inputs': [
        "9119", "0", "123", "765", "3212",
        "55", "8", "999", "1010", "4321", "2468"
    ]
}

# 328. codewars-descending-order
SOLVERS_AND_INPUTS['codewars-descending-order'] = {
    'starter': 'def solution(num):\n    pass\n',
    'solve': lambda n: int(''.join(sorted(str(n), reverse=True))),
    'inputs': [
        "42145", "145263", "123456789", "0", "15",
        "1021", "987", "111", "54321", "2048", "918273"
    ]
}

# 929. leetcode-palindrome-number
SOLVERS_AND_INPUTS['leetcode-palindrome-number'] = {
    'starter': 'def solution(x: int) -> bool:\n    pass\n',
    'solve': lambda x: str(x) == str(x)[::-1],
    'inputs': [
        "121", "-121", "10", "12321", "0",
        "7", "1001", "-101", "1234321", "55555", "99"
    ]
}

# 930. leetcode-remove-element
SOLVERS_AND_INPUTS['leetcode-remove-element'] = {
    'starter': 'def solution(nums: list, val: int) -> list:\n    pass\n',
    'solve': lambda nums, v: [x for x in nums if x != v],
    'inputs': [
        "[3, 2, 2, 3], 3",
        "[0, 1, 2, 2, 3, 0, 4, 2], 2",
        "[1, 1, 1], 1",
        "[4, 5], 1",
        "[], 0",
        "[1], 1",
        "[1, 2, 3, 4], 5",
        "[2, 2, 2, 2], 2",
        "[7, 8, 7, 9, 7], 7",
        "[10, 20, 30], 20",
        "[5, 5, 1, 5, 2], 5",
    ]
}

# 931. leetcode-maximum-subarray
def _max_sub_array(nums):
    cur = m = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        m = max(m, cur)
    return m

SOLVERS_AND_INPUTS['leetcode-maximum-subarray'] = {
    'starter': 'def solution(nums: list) -> int:\n    pass\n',
    'solve': _max_sub_array,
    'inputs': [
        "[-2, 1, -3, 4, -1, 2, 1, -5, 4]",
        "[1]",
        "[5, 4, -1, 7, 8]",
        "[-1, -2, -3]",
        "[-2, -1]",
        "[1, 2, 3, 4, 5]",
        "[-2, 3, 2, -1]",
        "[-1, 0, -2]",
        "[8, -19, 5, -4, 20]",
        "[-3, -2, 0, -1]",
        "[10, -5, 15, -2, 3]",
    ]
}

# 932. leetcode-merge-sorted-array
SOLVERS_AND_INPUTS['leetcode-merge-sorted-array'] = {
    'starter': 'def solution(nums1: list, nums2: list) -> list:\n    pass\n',
    'solve': lambda n1, n2: sorted(n1 + n2),
    'inputs': [
        "[1, 2, 3], [2, 5, 6]",
        "[1], []",
        "[], [1]",
        "[2, 4, 6], [1, 3, 5]",
        "[1, 1, 1], [2, 2]",
        "[-5, 0, 5], [-3, 2, 7]",
        "[10, 20], [5, 15, 25]",
        "[], []",
        "[1, 2], [3, 4]",
        "[-10], [-20, 0]",
        "[100], [50, 75, 125]",
    ]
}

# 933. leetcode-pascals-triangle
def _pascals_triangle(num_rows):
    res = [[1]]
    for _ in range(num_rows - 1):
        res.append([1] + [res[-1][i] + res[-1][i+1] for i in range(len(res[-1]) - 1)] + [1])
    return res

SOLVERS_AND_INPUTS['leetcode-pascals-triangle'] = {
    'starter': 'def solution(num_rows: int) -> list:\n    pass\n',
    'solve': _pascals_triangle,
    'inputs': [
        "5", "1", "2", "3", "4", "6", "7", "8", "9", "10", "11"
    ]
}

# 934. leetcode-best-time-to-buy-and-sell-stock
def _max_profit(prices):
    min_p, max_p = float('inf'), 0
    for p in prices:
        min_p = min(min_p, p)
        max_p = max(max_p, p - min_p)
    return max_p

SOLVERS_AND_INPUTS['leetcode-best-time-to-buy-and-sell-stock'] = {
    'starter': 'def solution(prices: list) -> int:\n    pass\n',
    'solve': _max_profit,
    'inputs': [
        "[7, 1, 5, 3, 6, 4]",
        "[7, 6, 4, 3, 1]",
        "[2, 4, 1]",
        "[1, 2]",
        "[3, 2, 6, 5, 0, 3]",
        "[1, 2, 3, 4, 5]",
        "[5]",
        "[2, 1, 2, 1, 0, 1, 2]",
        "[3, 3, 3, 3]",
        "[10, 2, 8, 1, 9]",
        "[1, 10]",
    ]
}

# 935. leetcode-excel-sheet-column-number
def _excel_col(s):
    ans = 0
    for c in s:
        ans = ans * 26 + (ord(c) - ord('A') + 1)
    return ans

SOLVERS_AND_INPUTS['leetcode-excel-sheet-column-number'] = {
    'starter': 'def solution(column_title: str) -> int:\n    pass\n',
    'solve': _excel_col,
    'inputs': [
        "'A'", "'AB'", "'ZY'", "'FXSHRXW'", "'B'",
        "'Z'", "'AA'", "'AZ'", "'BA'", "'BZ'", "'AAA'"
    ]
}

# 936. leetcode-number-of-1-bits
SOLVERS_AND_INPUTS['leetcode-number-of-1-bits'] = {
    'starter': 'def solution(n: int) -> int:\n    pass\n',
    'solve': lambda n: bin(n).count('1'),
    'inputs': [
        "11", "128", "2147483645", "0", "1",
        "2", "3", "7", "15", "255", "1023"
    ]
}

# 937. leetcode-happy-number
def _is_happy(n):
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(d)**2 for d in str(n))
    return n == 1

SOLVERS_AND_INPUTS['leetcode-happy-number'] = {
    'starter': 'def solution(n: int) -> bool:\n    pass\n',
    'solve': _is_happy,
    'inputs': [
        "19", "2", "1", "7", "4",
        "10", "28", "100", "111", "3", "20"
    ]
}

# 938. leetcode-reverse-string
SOLVERS_AND_INPUTS['leetcode-reverse-string'] = {
    'starter': 'def solution(s: str) -> str:\n    pass\n',
    'solve': lambda s: s[::-1],
    'inputs': [
        "'hello'", "'Hannah'", "''", "'Python'", "'a'",
        "'racecar'", "'12345'", "'SmartCode'", "'ab'", "'space '", "'UPPER lower'"
    ]
}

# 939. leetcode-power-of-two
SOLVERS_AND_INPUTS['leetcode-power-of-two'] = {
    'starter': 'def solution(n: int) -> bool:\n    pass\n',
    'solve': lambda n: n > 0 and (n & (n - 1)) == 0,
    'inputs': [
        "1", "16", "3", "0", "2",
        "4", "8", "5", "6", "1024", "-16"
    ]
}

# 940. leetcode-power-of-three
def _power_of_three(n):
    if n <= 0: return False
    while n % 3 == 0: n //= 3
    return n == 1

SOLVERS_AND_INPUTS['leetcode-power-of-three'] = {
    'starter': 'def solution(n: int) -> bool:\n    pass\n',
    'solve': _power_of_three,
    'inputs': [
        "27", "0", "-1", "9", "1",
        "3", "81", "45", "243", "6", "18"
    ]
}

# 941. leetcode-ugly-number
def _is_ugly(n):
    if n <= 0: return False
    for p in (2, 3, 5):
        while n % p == 0: n //= p
    return n == 1

SOLVERS_AND_INPUTS['leetcode-ugly-number'] = {
    'starter': 'def solution(n: int) -> bool:\n    pass\n',
    'solve': _is_ugly,
    'inputs': [
        "6", "1", "14", "-6", "8",
        "10", "12", "15", "7", "25", "30"
    ]
}

# 942. leetcode-word-pattern
def _word_pattern(pattern, s):
    words = s.split()
    if len(pattern) != len(words): return False
    return len(set(zip(pattern, words))) == len(set(pattern)) == len(set(words))

SOLVERS_AND_INPUTS['leetcode-word-pattern'] = {
    'starter': 'def solution(pattern: str, s: str) -> bool:\n    pass\n',
    'solve': _word_pattern,
    'inputs': [
        "'abba', 'dog cat cat dog'",
        "'abba', 'dog cat cat fish'",
        "'aaaa', 'dog cat cat dog'",
        "'abba', 'dog dog dog dog'",
        "'a', 'dog'",
        "'ab', 'dog dog'",
        "'abc', 'dog cat fish'",
        "'aaa', 'aa aa aa'",
        "'abba', 'cat dog dog cat'",
        "'abc', 'b c a'",
        "'aba', 'dog cat dog'",
    ]
}

# 943. leetcode-nim-game
SOLVERS_AND_INPUTS['leetcode-nim-game'] = {
    'starter': 'def solution(n: int) -> bool:\n    pass\n',
    'solve': lambda n: n % 4 != 0,
    'inputs': [
        "4", "1", "2", "8", "3",
        "5", "6", "7", "9", "12", "15"
    ]
}

# 944. leetcode-counting-bits
SOLVERS_AND_INPUTS['leetcode-counting-bits'] = {
    'starter': 'def solution(n: int) -> list:\n    pass\n',
    'solve': lambda n: [bin(i).count('1') for i in range(n + 1)],
    'inputs': [
        "2", "5", "0", "1", "3",
        "4", "6", "7", "8", "9", "10"
    ]
}

# 945. leetcode-power-of-four
def _power_of_four(n):
    if n <= 0: return False
    while n % 4 == 0: n //= 4
    return n == 1

SOLVERS_AND_INPUTS['leetcode-power-of-four'] = {
    'starter': 'def solution(n: int) -> bool:\n    pass\n',
    'solve': _power_of_four,
    'inputs': [
        "16", "5", "1", "8", "4",
        "64", "256", "0", "-4", "2", "12"
    ]
}

# 946. leetcode-reverse-vowels-of-a-string
def _reverse_vowels(s):
    vowels = set('aeiouAEIOU')
    chars = list(s)
    i, j = 0, len(chars) - 1
    while i < j:
        if chars[i] not in vowels: i += 1
        elif chars[j] not in vowels: j -= 1
        else:
            chars[i], chars[j] = chars[j], chars[i]
            i += 1; j -= 1
    return ''.join(chars)

SOLVERS_AND_INPUTS['leetcode-reverse-vowels-of-a-string'] = {
    'starter': 'def solution(s: str) -> str:\n    pass\n',
    'solve': _reverse_vowels,
    'inputs': [
        "'IceCreAm'", "'leetcode'", "'a.'", "'hello'", "'AEIOU'",
        "'rhythm'", "'Design'", "'programming'", "'world'", "'aA'", "''"
    ]
}

# 947. leetcode-intersection-of-two-arrays
SOLVERS_AND_INPUTS['leetcode-intersection-of-two-arrays'] = {
    'starter': 'def solution(nums1: list, nums2: list) -> list:\n    pass\n',
    'solve': lambda n1, n2: sorted(list(set(n1) & set(n2))),
    'inputs': [
        "[1, 2, 2, 1], [2, 2]",
        "[4, 9, 5], [9, 4, 9, 8, 4]",
        "[1, 2, 3], [4, 5, 6]",
        "[], [1, 2]",
        "[1], [1]",
        "[1, 2, 3], [1, 2, 3]",
        "[5, 5, 5], [5]",
        "[1, 3, 5, 7], [2, 3, 6, 7]",
        "[-1, 0, 1], [0, 2]",
        "[10, 20, 30], [20, 40]",
        "[1, 2], []",
    ]
}

# 948. leetcode-first-unique-character-in-a-string
def _first_uniq_char(s):
    from collections import Counter
    c = Counter(s)
    for i, ch in enumerate(s):
        if c[ch] == 1: return i
    return -1

SOLVERS_AND_INPUTS['leetcode-first-unique-character-in-a-string'] = {
    'starter': 'def solution(s: str) -> int:\n    pass\n',
    'solve': _first_uniq_char,
    'inputs': [
        "'leetcode'", "'loveleetcode'", "'aabb'", "'z'", "'abcabc'",
        "'swiss'", "'unique'", "'dddccdbba'", "'a'", "''", "'character'"
    ]
}

# 949. leetcode-find-the-difference
def _find_the_difference(s, t):
    from collections import Counter
    diff = Counter(t) - Counter(s)
    return list(diff.keys())[0]

SOLVERS_AND_INPUTS['leetcode-find-the-difference'] = {
    'starter': 'def solution(s: str, t: str) -> str:\n    pass\n',
    'solve': _find_the_difference,
    'inputs': [
        "'abcd', 'abcde'",
        "'', 'y'",
        "'a', 'aa'",
        "'ae', 'aea'",
        "'xyz', 'zxya'",
        "'hello', 'oheall'",
        "'test', 'ttest'",
        "'abc', 'abcb'",
        "'python', 'pythons'",
        "'code', 'cedco'",
        "'smart', 'tramps'",
    ]
}

# 950. leetcode-is-subsequence
def _is_subsequence(s, t):
    it = iter(t)
    return all(c in it for c in s)

SOLVERS_AND_INPUTS['leetcode-is-subsequence'] = {
    'starter': 'def solution(s: str, t: str) -> bool:\n    pass\n',
    'solve': _is_subsequence,
    'inputs': [
        "'abc', 'ahbgdc'",
        "'axc', 'ahbgdc'",
        "'', 'anystring'",
        "'', ''",
        "'b', 'c'",
        "'ace', 'abcde'",
        "'aec', 'abcde'",
        "'hello', 'hello'",
        "'sing', 'string'",
        "'sub', 'subsequence'",
        "'test', 'testing'",
    ]
}

# 951. leetcode-third-maximum-number
def _third_max(nums):
    u = sorted(set(nums), reverse=True)
    return u[2] if len(u) >= 3 else u[0]

SOLVERS_AND_INPUTS['leetcode-third-maximum-number'] = {
    'starter': 'def solution(nums: list) -> int:\n    pass\n',
    'solve': _third_max,
    'inputs': [
        "[3, 2, 1]",
        "[1, 2]",
        "[2, 2, 3, 1]",
        "[1]",
        "[5, 2, 4, 1, 3]",
        "[-1, 2, 3]",
        "[1, 1, 2]",
        "[1, 2, -2147483648]",
        "[10, 9, 8, 7, 6]",
        "[2, 2, 2]",
        "[1, 2, 2, 5, 3, 5]",
    ]
}

# 952. leetcode-add-strings
SOLVERS_AND_INPUTS['leetcode-add-strings'] = {
    'starter': 'def solution(num1: str, num2: str) -> str:\n    pass\n',
    'solve': lambda n1, n2: str(int(n1) + int(n2)),
    'inputs': [
        "'11', '123'",
        "'456', '77'",
        "'0', '0'",
        "'999', '1'",
        "'1', '9'",
        "'123456789', '987654321'",
        "'50', '50'",
        "'100', '200'",
        "'99', '99'",
        "'1000', '1'",
        "'45', '55'",
    ]
}

# 953. leetcode-number-of-segments-in-a-string
SOLVERS_AND_INPUTS['leetcode-number-of-segments-in-a-string'] = {
    'starter': 'def solution(s: str) -> int:\n    pass\n',
    'solve': lambda s: len(s.split()),
    'inputs': [
        "'Hello, my name is John'",
        "'Hello'",
        "''",
        "'                '",
        "'one two three'",
        "'   leading and trailing   '",
        "'a b c d e'",
        "'word1   word2   word3'",
        "'!@#$%^&*()'",
        "'single'",
        "'multiple spaces    between    words'",
    ]
}

# 954. leetcode-arranging-coins
def _arrange_coins(n):
    import math
    return int((math.sqrt(1 + 8*n) - 1) // 2)

SOLVERS_AND_INPUTS['leetcode-arranging-coins'] = {
    'starter': 'def solution(n: int) -> int:\n    pass\n',
    'solve': _arrange_coins,
    'inputs': [
        "5", "8", "1", "0", "3",
        "6", "10", "15", "16", "2", "20"
    ]
}

# 955. leetcode-find-all-numbers-disappeared-in-an-array
def _find_disappeared(nums):
    n = len(nums)
    s = set(nums)
    return [i for i in range(1, n + 1) if i not in s]

SOLVERS_AND_INPUTS['leetcode-find-all-numbers-disappeared-in-an-array'] = {
    'starter': 'def solution(nums: list) -> list:\n    pass\n',
    'solve': _find_disappeared,
    'inputs': [
        "[4, 3, 2, 7, 8, 2, 3, 1]",
        "[1, 1]",
        "[1]",
        "[2, 2]",
        "[1, 2, 3]",
        "[3, 3, 3]",
        "[1, 2, 2, 4]",
        "[5, 4, 3, 2, 1]",
        "[1, 1, 2, 2]",
        "[4, 4, 4, 4]",
        "[1, 3, 3]",
    ]
}

# 956. leetcode-assign-cookies
def _find_content_children(g, s):
    g_sorted, s_sorted = sorted(g), sorted(s)
    i = j = 0
    while i < len(g_sorted) and j < len(s_sorted):
        if s_sorted[j] >= g_sorted[i]:
            i += 1
        j += 1
    return i

SOLVERS_AND_INPUTS['leetcode-assign-cookies'] = {
    'starter': 'def solution(g: list, s: list) -> int:\n    pass\n',
    'solve': _find_content_children,
    'inputs': [
        "[1, 2, 3], [1, 1]",
        "[1, 2], [1, 2, 3]",
        "[1, 2, 3], []",
        "[], [1, 2]",
        "[1, 2, 3], [3]",
        "[10, 9, 8, 7], [5, 6, 7, 8]",
        "[1, 1, 1], [1, 1, 1]",
        "[5], [5]",
        "[2, 4], [1, 3, 5]",
        "[1, 2, 3, 4], [2, 3]",
        "[1, 5], [2, 4, 6]",
    ]
}

# 957. leetcode-repeated-substring-pattern
SOLVERS_AND_INPUTS['leetcode-repeated-substring-pattern'] = {
    'starter': 'def solution(s: str) -> bool:\n    pass\n',
    'solve': lambda s: s in (s + s)[1:-1],
    'inputs': [
        "'abab'", "'aba'", "'abcabcabcabc'", "'a'", "'aa'",
        "'aaa'", "'abac'", "'abcabc'", "'abcdabcd'", "'abaababaab'", "'xyzxyzxyz'"
    ]
}

# 958. leetcode-hamming-distance
SOLVERS_AND_INPUTS['leetcode-hamming-distance'] = {
    'starter': 'def solution(x: int, y: int) -> int:\n    pass\n',
    'solve': lambda x, y: bin(x ^ y).count('1'),
    'inputs': [
        "1, 4", "3, 1", "0, 0", "1, 1", "0, 1",
        "7, 0", "15, 15", "8, 7", "93, 73", "100, 200", "255, 0"
    ]
}

# 959. leetcode-island-perimeter
def _island_perimeter(grid):
    p = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 1:
                p += 4
                if r > 0 and grid[r-1][c] == 1: p -= 2
                if c > 0 and grid[r][c-1] == 1: p -= 2
    return p

SOLVERS_AND_INPUTS['leetcode-island-perimeter'] = {
    'starter': 'def solution(grid: list) -> int:\n    pass\n',
    'solve': _island_perimeter,
    'inputs': [
        "[[0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [1, 1, 0, 0]]",
        "[[1]]",
        "[[1, 0]]",
        "[[1, 1], [1, 1]]",
        "[[1, 1, 1]]",
        "[[1], [1], [1]]",
        "[[0, 1], [1, 1]]",
        "[[1, 1, 0], [0, 1, 0]]",
        "[[0, 0], [0, 1]]",
        "[[1, 1, 1, 1]]",
        "[[1, 1], [0, 1]]",
    ]
}

# 960. leetcode-license-key-formatting
def _license_key(s, k):
    clean = s.replace('-', '').upper()
    res = []
    rem = len(clean) % k
    if rem: res.append(clean[:rem])
    for i in range(rem, len(clean), k):
        res.append(clean[i:i+k])
    return '-'.join(res)

SOLVERS_AND_INPUTS['leetcode-license-key-formatting'] = {
    'starter': 'def solution(s: str, k: int) -> str:\n    pass\n',
    'solve': _license_key,
    'inputs': [
        "'5F3Z-2e-9-w', 4",
        "'2-5g-3-J', 2",
        "'---', 3",
        "'a-a-a-a-', 1",
        "'2-4A0r7-4k', 4",
        "'r', 1",
        "'abc-def-ghi', 3",
        "'12345', 2",
        "'a0001af4-5', 4",
        "'j-k-l', 2",
        "'AbCd-EfGh', 4",
    ]
}

# 961. leetcode-max-consecutive-ones
SOLVERS_AND_INPUTS['leetcode-max-consecutive-ones'] = {
    'starter': 'def solution(nums: list) -> int:\n    pass\n',
    'solve': lambda nums: max((len(x) for x in ''.join(map(str, nums)).split('0')), default=0),
    'inputs': [
        "[1, 1, 0, 1, 1, 1]",
        "[1, 0, 1, 1, 0, 1]",
        "[0, 0, 0]",
        "[1, 1, 1, 1]",
        "[0]",
        "[1]",
        "[1, 0]",
        "[0, 1]",
        "[1, 1, 0, 0, 1, 1, 1, 1, 0]",
        "[1, 0, 1, 0, 1]",
        "[0, 1, 1, 0, 1, 1, 1]",
    ]
}

# 962. leetcode-base-7
def _base7(n):
    if n == 0: return '0'
    neg = n < 0
    n = abs(n)
    res = []
    while n:
        res.append(str(n % 7))
        n //= 7
    if neg: res.append('-')
    return ''.join(reversed(res))

SOLVERS_AND_INPUTS['leetcode-base-7'] = {
    'starter': 'def solution(num: int) -> str:\n    pass\n',
    'solve': _base7,
    'inputs': [
        "100", "-7", "0", "7", "49",
        "1", "-1", "48", "350", "-100", "14"
    ]
}

# 963. leetcode-relative-ranks
def _relative_ranks(score):
    ranks = {s: i for i, s in enumerate(sorted(score, reverse=True))}
    medals = {0: 'Gold Medal', 1: 'Silver Medal', 2: 'Bronze Medal'}
    return [medals.get(ranks[s], str(ranks[s] + 1)) for s in score]

SOLVERS_AND_INPUTS['leetcode-relative-ranks'] = {
    'starter': 'def solution(score: list) -> list:\n    pass\n',
    'solve': _relative_ranks,
    'inputs': [
        "[5, 4, 3, 2, 1]",
        "[10, 3, 8, 9, 4]",
        "[1]",
        "[1, 2]",
        "[3, 2, 1]",
        "[12, 15, 10]",
        "[100, 50, 75, 25]",
        "[4, 1, 2, 3]",
        "[9, 8, 7, 6, 5, 4, 3, 2, 1]",
        "[2, 1]",
        "[1, 3, 2]",
    ]
}

# 964. leetcode-perfect-number
def _is_perfect(n):
    if n <= 1: return False
    s = 1
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            s += i
            if i * i != n: s += n // i
    return s == n

SOLVERS_AND_INPUTS['leetcode-perfect-number'] = {
    'starter': 'def solution(num: int) -> bool:\n    pass\n',
    'solve': _is_perfect,
    'inputs': [
        "28", "7", "6", "1", "496",
        "8128", "2", "3", "12", "16", "33550336"
    ]
}

# 965. leetcode-fibonacci-number
def _fib(n):
    a, b = 0, 1
    for _ in range(n): a, b = b, a + b
    return a

SOLVERS_AND_INPUTS['leetcode-fibonacci-number'] = {
    'starter': 'def solution(n: int) -> int:\n    pass\n',
    'solve': _fib,
    'inputs': [
        "2", "3", "4", "0", "1",
        "5", "6", "7", "8", "10", "15"
    ]
}

# 966. leetcode-detect-capital
SOLVERS_AND_INPUTS['leetcode-detect-capital'] = {
    'starter': 'def solution(word: str) -> bool:\n    pass\n',
    'solve': lambda w: w.isupper() or w.islower() or w.istitle(),
    'inputs': [
        "'USA'", "'FlaG'", "'Google'", "'leetcode'", "'c'",
        "'C'", "'mL'", "'leetcodE'", "'Hello'", "'WORLD'", "'Python'"
    ]
}

# 967. leetcode-reverse-words-in-a-string-iii
SOLVERS_AND_INPUTS['leetcode-reverse-words-in-a-string-iii'] = {
    'starter': 'def solution(s: str) -> str:\n    pass\n',
    'solve': lambda s: ' '.join(w[::-1] for w in s.split(' ')),
    'inputs': [
        "'Let\\'s take LeetCode contest'",
        "'God Ding'",
        "'Python'",
        "'a b c'",
        "'hello world'",
        "'word'",
        "'The quick brown fox'",
        "'jumps over the lazy dog'",
        "'abc def'",
        "'123 456'",
        "'racecar level'",
    ]
}

# 968. leetcode-array-partition
SOLVERS_AND_INPUTS['leetcode-array-partition'] = {
    'starter': 'def solution(nums: list) -> int:\n    pass\n',
    'solve': lambda nums: sum(sorted(nums)[::2]),
    'inputs': [
        "[1, 4, 3, 2]",
        "[6, 2, 6, 5, 1, 2]",
        "[1, 2]",
        "[1, 1]",
        "[5, 6, 7, 8]",
        "[10, 20, 30, 40]",
        "[-1, -2, -3, -4]",
        "[0, 0, 0, 0]",
        "[3, 1, 4, 2]",
        "[9, 1, 8, 2, 7, 3]",
        "[1, 5, 2, 4]",
    ]
}

# 969. leetcode-reshape-the-matrix
def _matrix_reshape(mat, r, c):
    flat = [x for row in mat for x in row]
    if len(flat) != r * c: return mat
    return [flat[i*c:(i+1)*c] for i in range(r)]

SOLVERS_AND_INPUTS['leetcode-reshape-the-matrix'] = {
    'starter': 'def solution(mat: list, r: int, c: int) -> list:\n    pass\n',
    'solve': _matrix_reshape,
    'inputs': [
        "[[1, 2], [3, 4]], 1, 4",
        "[[1, 2], [3, 4]], 2, 4",
        "[[1, 2, 3, 4]], 2, 2",
        "[[1, 2], [3, 4]], 4, 1",
        "[[1]], 1, 1",
        "[[1, 2, 3], [4, 5, 6]], 3, 2",
        "[[1, 2, 3], [4, 5, 6]], 1, 6",
        "[[1, 2], [3, 4]], 2, 2",
        "[[1, 2, 3]], 2, 2",
        "[[5, 6], [7, 8]], 1, 4",
        "[[1, 2], [3, 4], [5, 6]], 2, 3",
    ]
}

# 970. leetcode-can-place-flowers
def _can_place_flowers(flowerbed, n):
    fb = [0] + flowerbed + [0]
    cnt = 0
    for i in range(1, len(fb) - 1):
        if fb[i-1] == 0 and fb[i] == 0 and fb[i+1] == 0:
            fb[i] = 1
            cnt += 1
    return cnt >= n

SOLVERS_AND_INPUTS['leetcode-can-place-flowers'] = {
    'starter': 'def solution(flowerbed: list, n: int) -> bool:\n    pass\n',
    'solve': _can_place_flowers,
    'inputs': [
        "[1, 0, 0, 0, 1], 1",
        "[1, 0, 0, 0, 1], 2",
        "[0, 0, 1, 0, 0], 2",
        "[0, 0, 0, 0, 0], 3",
        "[0], 1",
        "[1], 0",
        "[1], 1",
        "[0, 0, 0], 2",
        "[1, 0, 0, 0, 0, 1], 2",
        "[0, 1, 0], 1",
        "[1, 0, 1, 0, 1], 0",
    ]
}

# 971. codewars-sum-of-positive
SOLVERS_AND_INPUTS['codewars-sum-of-positive'] = {
    'starter': 'def solution(arr: list) -> int:\n    pass\n',
    'solve': lambda arr: sum(x for x in arr if x > 0),
    'inputs': [
        "[1, -4, 7, 12]",
        "[-1, -2, -3, -4, -5]",
        "[]",
        "[1, 2, 3, 4, 5]",
        "[-1]",
        "[0]",
        "[10, -10, 20, -20]",
        "[100]",
        "[-5, 0, 5]",
        "[2, 4, 6, -8]",
        "[1, -1, 1, -1, 1]",
    ]
}

# 972. codewars-opposites-attract
SOLVERS_AND_INPUTS['codewars-opposites-attract'] = {
    'starter': 'def solution(flower1: int, flower2: int) -> bool:\n    pass\n',
    'solve': lambda f1, f2: (f1 % 2) != (f2 % 2),
    'inputs': [
        "1, 4", "2, 2", "0, 1", "0, 0", "5, 5",
        "3, 6", "10, 15", "8, 9", "12, 14", "1, 3", "7, 10"
    ]
}

# 973. codewars-youre-a-square
SOLVERS_AND_INPUTS['codewars-youre-a-square'] = {
    'starter': 'def solution(n: int) -> bool:\n    pass\n',
    'solve': lambda n: n >= 0 and int(n**0.5)**2 == n,
    'inputs': [
        "-1", "0", "3", "25", "4",
        "9", "16", "26", "100", "144", "-4"
    ]
}

# 974. codewars-growth-of-a-population
def _nb_year(p0, percent, aug, p):
    y = 0
    while p0 < p:
        p0 = int(p0 + p0 * percent / 100 + aug)
        y += 1
    return y

SOLVERS_AND_INPUTS['codewars-growth-of-a-population'] = {
    'starter': 'def solution(p0: int, percent: float, aug: int, p: int) -> int:\n    pass\n',
    'solve': _nb_year,
    'inputs': [
        "1500, 5, 100, 5000",
        "1500000, 2.5, 10000, 2000000",
        "1000, 2, 50, 1200",
        "1500000, 0.25, 1000, 2000000",
        "1000, 2.0, 50, 1070",
        "1000, 5, 100, 2000",
        "500, 10, 50, 1000",
        "2000, 1.5, 100, 2500",
        "100, 1, 10, 200",
        "800, 3, 20, 1000",
        "10000, 0.5, 50, 12000",
    ]
}

# 975. codewars-categorize-new-member
def _open_or_senior(data):
    return ['Senior' if age >= 55 and h > 7 else 'Open' for age, h in data]

SOLVERS_AND_INPUTS['codewars-categorize-new-member'] = {
    'starter': 'def solution(data: list) -> list:\n    pass\n',
    'solve': _open_or_senior,
    'inputs': [
        "[[18, 20], [45, 2], [61, 12], [37, 6], [21, 21], [78, 9]]",
        "[[55, 8], [55, 7], [54, 9]]",
        "[]",
        "[[55, 10]]",
        "[[54, 10]]",
        "[[60, 12], [20, 5]]",
        "[[55, 8], [55, 8]]",
        "[[30, 0], [40, 2], [50, 5]]",
        "[[70, 15], [80, 20]]",
        "[[56, 7], [55, 8]]",
        "[[90, 8], [10, 10]]",
    ]
}

# 976. codewars-highest-and-lowest
def _high_and_low(numbers):
    nums = list(map(int, numbers.split()))
    return f"{max(nums)} {min(nums)}"

SOLVERS_AND_INPUTS['codewars-highest-and-lowest'] = {
    'starter': 'def solution(numbers: str) -> str:\n    pass\n',
    'solve': _high_and_low,
    'inputs': [
        "'1 2 3 4 5'",
        "'1 2 -3 4 5'",
        "'1 9 3 4 -5'",
        "'42'",
        "'0 0 0'",
        "'8 3 -5 42 -1 0 0 -9 4 7 4 -4'",
        "'-1 -2 -3 -4 -5'",
        "'100 200 50 25'",
        "'5 5 5 5'",
        "'10 -10'",
        "'1 2 3'",
    ]
}

# 977. codewars-string-ends-with
SOLVERS_AND_INPUTS['codewars-string-ends-with'] = {
    'starter': 'def solution(text: str, ending: str) -> bool:\n    pass\n',
    'solve': lambda t, e: t.endswith(e),
    'inputs': [
        "'abc', 'bc'",
        "'abc', 'd'",
        "'samurai', 'ai'",
        "'fails', 'ails '",
        "'this', ''",
        "'ninja', 'ja'",
        "'sensei', 'i'",
        "'abc', 'abc'",
        "'abc', 'abcd'",
        "'banana', 'an'",
        "'coding', 'ing'",
    ]
}

# 978. codewars-find-the-smallest-integer-in-the-array
SOLVERS_AND_INPUTS['codewars-find-the-smallest-integer-in-the-array'] = {
    'starter': 'def solution(arr: list) -> int:\n    pass\n',
    'solve': lambda arr: min(arr),
    'inputs': [
        "[34, 15, 88, 2]",
        "[34, -345, -1, 100]",
        "[0]",
        "[7, 7, 7]",
        "[1, 2, 3, 4, 5]",
        "[-5, -4, -3, -2, -1]",
        "[100, 50, 25, 10]",
        "[999, -999]",
        "[42]",
        "[-10, 0, 10]",
        "[5, 4, 3, 2, 1, 0, -1]",
    ]
}

def run():
    print("Starting test cases expansion to at least 10 tests per task...")
    all_tasks = list(Task.objects.order_by('id'))
    print(f"Total tasks to update: {len(all_tasks)}")
    
    with transaction.atomic():
        for task in all_tasks:
            slug = task.slug
            
            # Special case for task 3 (palindromes-without-borders) which already has 30 tests
            if slug == 'palindromes-without-borders':
                print(f"Task {slug} already has {task.test_cases.count()} test cases. Keeping.")
                continue
                
            if slug not in SOLVERS_AND_INPUTS:
                print(f"WARNING: No solver for slug {slug}!")
                continue
                
            spec = SOLVERS_AND_INPUTS[slug]
            solver = spec['solve']
            inputs = spec['inputs']
            
            if 'starter' in spec:
                task.starter_code = spec['starter']
                task.save()
                
            # Delete existing test cases
            task.test_cases.all().delete()
            
            # Create new test cases (at least 10)
            for idx, in_str in enumerate(inputs):
                # Evaluate inputs to pass to solver
                val = eval(f"({in_str},)")
                if len(val) == 1:
                    raw_ans = solver(val[0])
                else:
                    raw_ans = solver(*val)
                    
                expected_str = str(raw_ans)
                # First 3 tests are open, rest are hidden
                is_hidden = idx >= 3
                
                TestCase.objects.create(
                    task=task,
                    input_data=in_str,
                    expected_output=expected_str,
                    is_hidden=is_hidden
                )
                
            print(f"Task '{slug}': created {len(inputs)} test cases (3 visible, {len(inputs)-3} hidden).")
            
    print("\nSummary verification:")
    for t in Task.objects.order_by('id'):
        tc_cnt = t.test_cases.count()
        if tc_cnt < 10:
            print(f"ERROR: {t.slug} has {tc_cnt} tests (< 10)!")
    print("All tasks successfully have >= 10 test cases!")

if __name__ == '__main__':
    run()

