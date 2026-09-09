# -*- coding: utf-8 -*-
import os
import sys
import math
from collections import Counter, defaultdict

import django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from challenges.models import Task, TestCase, Tag
from challenges.services.runner import CodeRunnerService, parse_test_inputs
from django.db import transaction

ALL_TASKS = []

# ==================== TASKS 1 - 15 ====================

def solve_3sum(nums):
    nums = sorted(nums)
    res = []
    n = len(nums)
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        l, r = i + 1, n - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s < 0:
                l += 1
            elif s > 0:
                r -= 1
            else:
                res.append([nums[i], nums[l], nums[r]])
                while l < r and nums[l] == nums[l + 1]:
                    l += 1
                while l < r and nums[r] == nums[r - 1]:
                    r -= 1
                l += 1
                r -= 1
    return res

def solve_longest_palindrome(s):
    if not s: return ""
    start = end = 0
    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return l + 1, r - 1
    for i in range(len(s)):
        l1, r1 = expand(i, i)
        if r1 - l1 > end - start:
            start, end = l1, r1
        l2, r2 = expand(i, i + 1)
        if r2 - l2 > end - start:
            start, end = l2, r2
    return s[start:end + 1]

def solve_atoi(s):
    s = s.lstrip()
    if not s: return 0
    sign = 1
    idx = 0
    if s[0] == '-':
        sign = -1
        idx = 1
    elif s[0] == '+':
        idx = 1
    num = 0
    while idx < len(s) and s[idx].isdigit():
        num = num * 10 + int(s[idx])
        idx += 1
    num *= sign
    INT_MIN, INT_MAX = -2**31, 2**31 - 1
    if num < INT_MIN: return INT_MIN
    if num > INT_MAX: return INT_MAX
    return num

def solve_subarray_sum(nums, k):
    count = curr = 0
    prefix = {0: 1}
    for x in nums:
        curr += x
        count += prefix.get(curr - k, 0)
        prefix[curr] = prefix.get(curr, 0) + 1
    return count

def solve_product_except_self(nums):
    n = len(nums)
    res = [1] * n
    prefix = 1
    for i in range(n):
        res[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        res[i] *= suffix
        suffix *= nums[i]
    return res

def solve_group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        groups[tuple(sorted(s))].append(s)
    return sorted([sorted(g) for g in groups.values()])

def solve_top_k_frequent(nums, k):
    c = Counter(nums)
    top = sorted(c.keys(), key=lambda x: (-c[x], x))[:k]
    return sorted(top)

def solve_longest_consecutive(nums):
    s = set(nums)
    max_len = 0
    for x in s:
        if x - 1 not in s:
            curr = x
            cur_len = 1
            while curr + 1 in s:
                curr += 1
                cur_len += 1
            max_len = max(max_len, cur_len)
    return max_len

def solve_search_rotated(nums, target):
    l, r = 0, len(nums) - 1
    while l <= r:
        mid = (l + r) // 2
        if nums[mid] == target:
            return mid
        if nums[l] <= nums[mid]:
            if nums[l] <= target < nums[mid]:
                r = mid - 1
            else:
                l = mid + 1
        else:
            if nums[mid] < target <= nums[r]:
                l = mid + 1
            else:
                r = mid - 1
    return -1

def solve_find_min_rotated(nums):
    l, r = 0, len(nums) - 1
    while l < r:
        mid = (l + r) // 2
        if nums[mid] > nums[r]:
            l = mid + 1
        else:
            r = mid
    return nums[l]

def solve_find_peak(nums):
    l, r = 0, len(nums) - 1
    while l < r:
        mid = (l + r) // 2
        if nums[mid] > nums[mid + 1]:
            r = mid
        else:
            l = mid + 1
    return l

def solve_rotate_array(nums, k):
    n = len(nums)
    if n == 0: return []
    k = k % n
    return nums[-k:] + nums[:-k] if k > 0 else list(nums)

def solve_longest_substring(s):
    used = {}
    l = max_len = 0
    for r, ch in enumerate(s):
        if ch in used and used[ch] >= l:
            l = used[ch] + 1
        used[ch] = r
        max_len = max(max_len, r - l + 1)
    return max_len

def solve_container_water(height):
    l, r = 0, len(height) - 1
    ans = 0
    while l < r:
        ans = max(ans, min(height[l], height[r]) * (r - l))
        if height[l] < height[r]:
            l += 1
        else:
            r -= 1
    return ans

def solve_reverse_integer(x):
    sign = -1 if x < 0 else 1
    r = int(str(abs(x))[::-1]) * sign
    if -2**31 <= r <= 2**31 - 1:
        return r
    return 0


ALL_TASKS.extend([
    {
        "title": "Longest Substring Without Repeating Characters",
        "slug": "longest-substring-without-repeating-characters",
        "starter_code": "def solution(s: str) -> int:\n    pass\n",
        "description": """Дана строка `s`. Найдите длину самой длинной подстроки, не содержащей повторяющихся символов.

### Пример работы:
```python
solution("abcabcbb")  # Вернет: 3 (подстрока "abc")
```""",
        "tags": ["strings", "two-pointers"],
        "solver": solve_longest_substring,
        "inputs": [
            ['"abcabcbb"'], ['"bbbbb"'], ['"pwwkew"'], ['""'], ['" "'],
            ['"au"'], ['"dvdf"'], ['"anviaj"'], ['"tmmzuxt"'], ['"abcdefghijklmnopqrstuvwxyz"']
        ]
    },
    {
        "title": "Container With Most Water",
        "slug": "container-with-most-water",
        "starter_code": "def solution(height: list) -> int:\n    pass\n",
        "description": """Дан целочисленный массив `height` длины `n`. Найдите две вертикальные линии, которые вместе с осью X образуют контейнер, вмещающий максимальное количество воды. Верните максимальный объем воды.

### Пример работы:
```python
solution([1, 8, 6, 2, 5, 4, 8, 3, 7])  # Вернет: 49
```""",
        "tags": ["arrays", "two-pointers"],
        "solver": solve_container_water,
        "inputs": [
            ["[1, 8, 6, 2, 5, 4, 8, 3, 7]"], ["[1, 1]"], ["[4, 3, 2, 1, 4]"], ["[1, 2, 1]"],
            ["[2, 3, 4, 5, 18, 17, 6]"], ["[1, 8, 100, 2, 100, 4, 8, 3, 7]"],
            ["[10, 9, 8, 7, 6, 5, 4, 3, 2, 1]"], ["[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"],
            ["[5, 5, 5, 5, 5]"], ["[3, 9, 3, 4, 7, 2, 12, 6]"]
        ]
    },
    {
        "title": "3Sum",
        "slug": "three-sum",
        "starter_code": "def solution(nums: list) -> list:\n    pass\n",
        "description": """Дан целочисленный массив `nums`. Найдите все уникальные тройки элементов `[nums[i], nums[j], nums[k]]`, сумма которых равна `0`.

Каждая тройка и результирующий список отсортированы по возрастанию.

### Пример работы:
```python
solution([-1, 0, 1, 2, -1, -4])  # Вернет: [[-1, -1, 2], [-1, 0, 1]]
```""",
        "tags": ["arrays", "two-pointers"],
        "solver": solve_3sum,
        "inputs": [
            ["[-1, 0, 1, 2, -1, -4]"], ["[0, 1, 1]"], ["[0, 0, 0]"], ["[0, 0, 0, 0]"],
            ["[-2, 0, 1, 1, 2]"], ["[-1, 0, 1, 0]"],
            ["[-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6]"],
            ["[-2, 0, 0, 2, 2]"], ["[1, 2, -2, -1]"], ["[-1, -1, -1, 2]"]
        ]
    },
    {
        "title": "Longest Palindromic Substring",
        "slug": "longest-palindromic-substring",
        "starter_code": "def solution(s: str) -> str:\n    pass\n",
        "description": """Дана строка `s`. Найдите самую длинную подстроку в `s`, которая является палиндромом (читается одинаково слева направо и справа налево).

### Пример работы:
```python
solution("babad")  # Вернет: "bab" (или "aba")
```""",
        "tags": ["strings", "dynamic-programming"],
        "solver": solve_longest_palindrome,
        "inputs": [
            ['"babad"'], ['"cbbd"'], ['"a"'], ['"ac"'], ['"racecar"'],
            ['"noon"'], ['"abacdfgdcaba"'], ['"forgeeksskeegfor"'],
            ['"civilwartestingwhetherthatnaptownferriesacompaniessometimestwonightsrear"'],
            ['"bananas"']
        ]
    },
    {
        "title": "Reverse Integer",
        "slug": "reverse-integer",
        "starter_code": "def solution(x: int) -> int:\n    pass\n",
        "description": """Дано 32-битное знаковое целое число `x`. Разверните порядок его цифр. Если полученное число выходит за пределы 32-битного диапазона `[-2^31, 2^31 - 1]`, верните `0`.

### Пример работы:
```python
solution(-123)  # Вернет: -321
```""",
        "tags": ["math"],
        "solver": solve_reverse_integer,
        "inputs": [
            ["123"], ["-123"], ["120"], ["0"], ["1534236469"],
            ["-2147483648"], ["1"], ["-1"], ["1000000003"], ["8463847412"]
        ]
    },
    {
        "title": "String to Integer (atoi)",
        "slug": "string-to-integer-atoi",
        "starter_code": "def solution(s: str) -> int:\n    pass\n",
        "description": """Реализуйте функцию преобразования строки в 32-битное целое число. Пропустите пробелы в начале, определите знак числа (`+` или `-`), считайте последовательные цифры и примените ограничение диапазона `[-2^31, 2^31 - 1]`.

### Пример работы:
```python
solution("   -42")  # Вернет: -42
```""",
        "tags": ["strings"],
        "solver": solve_atoi,
        "inputs": [
            ['"42"'], ['"   -42"'], ['"1337c0d3"'], ['"0-1"'], ['"words and 987"'],
            ['"-91283472332"'], ['"+1"'], ['"+-12"'], ['""'], ['"  0000000000012345678"']
        ]
    },
    {
        "title": "Subarray Sum Equals K",
        "slug": "subarray-sum-equals-k",
        "starter_code": "def solution(nums: list, k: int) -> int:\n    pass\n",
        "description": """Дан массив целых чисел `nums` и целое число `k`. Найдите общее количество непрерывных подмассивов, сумма элементов которых равна `k`.

### Пример работы:
```python
solution([1, 1, 1], 2)  # Вернет: 2 (подмассивы с индексами [0..1] и [1..2])
```""",
        "tags": ["arrays", "prefix-sum"],
        "solver": solve_subarray_sum,
        "inputs": [
            ["[1, 1, 1], 2"], ["[1, 2, 3], 3"], ["[1, -1, 0], 0"], ["[1], 0"],
            ["[-1, -1, 1], 0"], ["[3, 4, 7, 2, -3, 1, 4, 2], 7"],
            ["[1, 2, 1, 2, 1], 3"], ["[0, 0, 0, 0, 0], 0"],
            ["[100, 1, 2, 3, 4], 6"], ["[-2, -1, 2, 1], 1"]
        ]
    },
    {
        "title": "Product of Array Except Self",
        "slug": "product-of-array-except-self",
        "starter_code": "def solution(nums: list) -> list:\n    pass\n",
        "description": """Дан массив целых чисел `nums`. Верните массив `answer`, где `answer[i]` равен произведению всех элементов `nums`, кроме `nums[i]`. Алгоритм должен работать за O(n) без операции деления.

### Пример работы:
```python
solution([1, 2, 3, 4])  # Вернет: [24, 12, 8, 6]
```""",
        "tags": ["arrays", "prefix-sum"],
        "solver": solve_product_except_self,
        "inputs": [
            ["[1, 2, 3, 4]"], ["[-1, 1, 0, -3, 3]"], ["[2, 3]"], ["[0, 0]"],
            ["[1, 0]"], ["[5, 2, 4, 3]"], ["[9, 0, -2]"], ["[1, 2, 3, 4, 5]"],
            ["[-2, -3, -4]"], ["[4, 5, 1, 8, 2]"]
        ]
    },
    {
        "title": "Group Anagrams",
        "slug": "group-anagrams",
        "starter_code": "def solution(strs: list) -> list:\n    pass\n",
        "description": """Дан массив строк `strs`. Сгруппируйте анаграммы вместе. Для стабильности проверки каждая группа отсортирована по алфавиту, а сам список групп отсортирован по первому элементу каждой группы.

### Пример работы:
```python
solution(["eat", "tea", "tan", "ate", "nat", "bat"])  # Вернет: [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
```""",
        "tags": ["strings", "hash-table"],
        "solver": solve_group_anagrams,
        "inputs": [
            ['["eat", "tea", "tan", "ate", "nat", "bat"]'], ['[""]'], ['["a"]'],
            ['["ab", "ba", "abc", "cba", "bca"]'], ['["hello", "world"]'],
            ['["listen", "silent", "enlist"]'], ['["rat", "tar", "art", "car"]'],
            ['["dormitory", "dirtyroom"]'], ['["cat", "dog", "god", "act"]'],
            ['["abc", "def", "ghi"]']
        ]
    },
    {
        "title": "Top K Frequent Elements",
        "slug": "top-k-frequent-elements",
        "starter_code": "def solution(nums: list, k: int) -> list:\n    pass\n",
        "description": """Дан целочисленный массив `nums` и число `k`. Найдите `k` наиболее часто встречающихся элементов. Верните результат, отсортированный по возрастанию.

### Пример работы:
```python
solution([1, 1, 1, 2, 2, 3], 2)  # Вернет: [1, 2]
```""",
        "tags": ["arrays", "heap"],
        "solver": solve_top_k_frequent,
        "inputs": [
            ["[1, 1, 1, 2, 2, 3], 2"], ["[1], 1"], ["[4, 1, -1, 2, -1, 2, 3], 2"],
            ["[1, 2, 2, 3, 3, 3], 1"], ["[5, 5, 5, 6, 6, 7], 2"], ["[10, 20, 30, 40], 2"],
            ["[-1, -1, -1, -2, -2, -3], 2"], ["[1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5], 1"],
            ["[7, 7, 8, 8, 8, 9, 9, 9, 9], 3"], ["[100, 200, 100, 300, 200, 100], 2"]
        ]
    },
    {
        "title": "Longest Consecutive Sequence",
        "slug": "longest-consecutive-sequence",
        "starter_code": "def solution(nums: list) -> int:\n    pass\n",
        "description": """Дан неотсортированный массив целых чисел `nums`. Найдите длину самой длинной последовательности последовательных чисел (`x, x+1, x+2...`). Алгоритм должен работать за O(n).

### Пример работы:
```python
solution([100, 4, 200, 1, 3, 2])  # Вернет: 4 (последовательность: [1, 2, 3, 4])
```""",
        "tags": ["arrays", "hash-table"],
        "solver": solve_longest_consecutive,
        "inputs": [
            ["[100, 4, 200, 1, 3, 2]"], ["[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]"],
            ["[]"], ["[9]"], ["[1, 2, 0, 1]"], ["[10, 5, 12, 3, 55, 30, 4, 11, 2]"],
            ["[-5, -4, -3, -2, -1, 0, 1]"], ["[1, 3, 5, 7, 9]"],
            ["[2, 2, 2, 2]"], ["[400, 4, 200, 1, 3, 2, 401, 402]"]
        ]
    },
    {
        "title": "Search in Rotated Sorted Array",
        "slug": "search-in-rotated-sorted-array",
        "starter_code": "def solution(nums: list, target: int) -> int:\n    pass\n",
        "description": """Дан массив уникальных чисел `nums`, отсортированный по возрастанию и циклически сдвинутый в неизвестной точке. Найдите индекс элемента `target` за O(log n) или верните `-1`, если элемент отсутствует.

### Пример работы:
```python
solution([4, 5, 6, 7, 0, 1, 2], 0)  # Вернет: 4
```""",
        "tags": ["arrays", "binary-search"],
        "solver": solve_search_rotated,
        "inputs": [
            ["[4, 5, 6, 7, 0, 1, 2], 0"], ["[4, 5, 6, 7, 0, 1, 2], 3"],
            ["[1], 0"], ["[1], 1"], ["[1, 3], 3"], ["[3, 1], 1"],
            ["[5, 1, 3], 5"], ["[4, 5, 6, 7, 8, 1, 2, 3], 8"],
            ["[6, 7, 1, 2, 3, 4, 5], 6"], ["[1, 2, 3, 4, 5, 6], 4"]
        ]
    },
    {
        "title": "Find Minimum in Rotated Sorted Array",
        "slug": "find-minimum-in-rotated-sorted-array",
        "starter_code": "def solution(nums: list) -> int:\n    pass\n",
        "description": """Дан массив уникальных чисел `nums`, отсортированный по возрастанию и циклически сдвинутый от 1 до n раз. Найдите минимальный элемент массива за время O(log n).

### Пример работы:
```python
solution([3, 4, 5, 1, 2])  # Вернет: 1
```""",
        "tags": ["arrays", "binary-search"],
        "solver": solve_find_min_rotated,
        "inputs": [
            ["[3, 4, 5, 1, 2]"], ["[4, 5, 6, 7, 0, 1, 2]"], ["[11, 13, 15, 17]"],
            ["[1]"], ["[2, 1]"], ["[3, 1, 2]"], ["[5, 1, 2, 3, 4]"],
            ["[2, 3, 4, 5, 6, 7, 8, 1]"], ["[10, 20, 30, 40, 50, 5]"], ["[1, 2, 3, 4, 5]"]
        ]
    },
    {
        "title": "Find Peak Element",
        "slug": "find-peak-element",
        "starter_code": "def solution(nums: list) -> int:\n    pass\n",
        "description": """Пиковым элементом называется элемент, который строго больше своих соседей. Найдите любой пиковый элемент и верните его индекс за O(log n).

### Пример работы:
```python
solution([1, 2, 3, 1])  # Вернет: 2 (число 3 больше 2 и 1)
```""",
        "tags": ["arrays", "binary-search"],
        "solver": solve_find_peak,
        "inputs": [
            ["[1, 2, 3, 1]"], ["[1, 2, 1, 3, 5, 6, 4]"], ["[1]"], ["[1, 2]"],
            ["[2, 1]"], ["[1, 2, 3, 4, 5]"], ["[5, 4, 3, 2, 1]"],
            ["[1, 3, 20, 4, 1, 0]"], ["[1, 5, 2, 1]"], ["[10, 20, 15, 2, 23, 90, 67]"]
        ]
    },
])

# ==================== TASKS 16 - 30 ====================

def solve_daily_temperatures(temperatures):
    n = len(temperatures)
    res = [0] * n
    stack = []
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            prev = stack.pop()
            res[prev] = i - prev
        stack.append(i)
    return res

def solve_coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for c in coins:
        for i in range(c, amount + 1):
            dp[i] = min(dp[i], dp[i - c] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1

def solve_house_robber(nums):
    prev1 = prev2 = 0
    for x in nums:
        curr = max(prev1, prev2 + x)
        prev2 = prev1
        prev1 = curr
    return prev1

def solve_house_robber_ii(nums):
    if len(nums) == 1: return nums[0]
    def rob_linear(h):
        p1 = p2 = 0
        for x in h:
            c = max(p1, p2 + x)
            p2 = p1
            p1 = c
        return p1
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))

def solve_jump_game(nums):
    reach = 0
    for i, x in enumerate(nums):
        if i > reach: return False
        reach = max(reach, i + x)
    return True

def solve_jump_game_ii(nums):
    jumps = 0
    curr_end = 0
    curr_farthest = 0
    for i in range(len(nums) - 1):
        curr_farthest = max(curr_farthest, i + nums[i])
        if i == curr_end:
            jumps += 1
            curr_end = curr_farthest
    return jumps

def solve_merge_intervals(intervals):
    if not intervals: return []
    intervals = sorted(intervals, key=lambda x: x[0])
    merged = [intervals[0]]
    for cur in intervals[1:]:
        last = merged[-1]
        if cur[0] <= last[1]:
            last[1] = max(last[1], cur[1])
        else:
            merged.append(cur)
    return merged

def solve_non_overlapping_intervals(intervals):
    if not intervals: return 0
    intervals = sorted(intervals, key=lambda x: x[1])
    count = 0
    end = intervals[0][1]
    for i in range(1, len(intervals)):
        if intervals[i][0] < end:
            count += 1
        else:
            end = intervals[i][1]
    return count

def solve_spiral_matrix(matrix):
    if not matrix: return []
    res = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            res.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):
            res.append(matrix[r][right])
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):
                res.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):
                res.append(matrix[r][left])
            left += 1
    return res

def solve_rotate_image(matrix):
    return [list(row) for row in zip(*matrix[::-1])]

def solve_set_matrix_zeroes(matrix):
    m, n = len(matrix), len(matrix[0])
    rows = set()
    cols = set()
    for r in range(m):
        for c in range(n):
            if matrix[r][c] == 0:
                rows.add(r)
                cols.add(c)
    res = [row[:] for row in matrix]
    for r in range(m):
        for c in range(n):
            if r in rows or c in cols:
                res[r][c] = 0
    return res

def solve_unique_paths(m, n):
    return math.comb(m + n - 2, m - 1)

def solve_min_path_sum(grid):
    m, n = len(grid), len(grid[0])
    dp = [row[:] for row in grid]
    for r in range(m):
        for c in range(n):
            if r == 0 and c == 0: continue
            elif r == 0: dp[r][c] += dp[r][c - 1]
            elif c == 0: dp[r][c] += dp[r - 1][c]
            else: dp[r][c] += min(dp[r - 1][c], dp[r][c - 1])
    return dp[m - 1][n - 1]

def solve_decode_ways(s):
    if not s or s[0] == '0': return 0
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = dp[1] = 1
    for i in range(2, n + 1):
        one = int(s[i - 1:i])
        two = int(s[i - 2:i])
        if 1 <= one <= 9: dp[i] += dp[i - 1]
        if 10 <= two <= 26: dp[i] += dp[i - 2]
    return dp[n]

def solve_word_break(s, wordDict):
    words = set(wordDict)
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    return dp[len(s)]


ALL_TASKS.extend([
    {
        "title": "Daily Temperatures",
        "slug": "daily-temperatures",
        "starter_code": "def solution(temperatures: list) -> list:\n    pass\n",
        "description": """Дан массив температур `temperatures`. Верните массив `answer`, где `answer[i]` — количество дней, которое нужно подождать до более теплой температуры. Если такого дня нет, запишите 0.

### Пример работы:
```python
solution([73, 74, 75, 71, 69, 72, 76, 73])  # Вернет: [1, 1, 4, 2, 1, 1, 0, 0]
```""",
        "tags": ["arrays", "stack"],
        "solver": solve_daily_temperatures,
        "inputs": [
            ["[73, 74, 75, 71, 69, 72, 76, 73]"], ["[30, 40, 50, 60]"],
            ["[30, 60, 90]"], ["[89, 62, 70, 58, 47, 47, 46, 76, 100, 70]"],
            ["[50]"], ["[55, 55, 55]"], ["[90, 80, 70, 60]"],
            ["[60, 70, 60, 70, 80]"], ["[45, 46, 47, 48, 49]"], ["[31, 32, 31, 32, 31, 32]"]
        ]
    },
    {
        "title": "Coin Change",
        "slug": "coin-change",
        "starter_code": "def solution(coins: list, amount: int) -> int:\n    pass\n",
        "description": """Дан массив монет разного номинала `coins` и общая сумма `amount`. Найдите наименьшее количество монет, необходимое для формирования этой суммы. Если сумму составить невозможно, верните -1.

### Пример работы:
```python
solution([1, 2, 5], 11)  # Вернет: 3 (5 + 5 + 1)
```""",
        "tags": ["dynamic-programming"],
        "solver": solve_coin_change,
        "inputs": [
            ["[1, 2, 5], 11"], ["[2], 3"], ["[1], 0"], ["[1], 1"], ["[1], 2"],
            ["[2, 5, 10, 1], 27"], ["[186, 419, 83, 408], 6249"],
            ["[3, 7, 405, 436], 8839"], ["[1, 3, 5], 8"], ["[5, 10, 25], 30"]
        ]
    },
    {
        "title": "House Robber",
        "slug": "house-robber",
        "starter_code": "def solution(nums: list) -> int:\n    pass\n",
        "description": """Вы профессиональный грабитель. Дома расположены вдоль улицы, и в каждом доме хранится сумма `nums[i]`. Соседние дома грабить нельзя (сработает сигнализация). Найдите максимальную сумму, которую можно украсть.

### Пример работы:
```python
solution([1, 2, 3, 1])  # Вернет: 4 (ограбить дом 1 и дом 3: 1 + 3 = 4)
```""",
        "tags": ["dynamic-programming"],
        "solver": solve_house_robber,
        "inputs": [
            ["[1, 2, 3, 1]"], ["[2, 7, 9, 3, 1]"], ["[2, 1, 1, 2]"],
            ["[0]"], ["[5]"], ["[1, 100, 1]"], ["[10, 2, 3, 20]"],
            ["[100, 1, 1, 100]"], ["[4, 1, 2, 7, 5, 3, 1]"], ["[5, 3, 4, 11, 2]"]
        ]
    },
    {
        "title": "House Robber II",
        "slug": "house-robber-ii",
        "starter_code": "def solution(nums: list) -> int:\n    pass\n",
        "description": """Дома расположены по кругу (первый и последний дома являются соседями). Соседние дома грабить нельзя. Найдите максимальную сумму, которую можно украсть.

### Пример работы:
```python
solution([2, 3, 2])  # Вернет: 3 (первый и третий дома соседствуют, грабим средний)
```""",
        "tags": ["dynamic-programming"],
        "solver": solve_house_robber_ii,
        "inputs": [
            ["[2, 3, 2]"], ["[1, 2, 3, 1]"], ["[1, 2, 3]"], ["[0]"],
            ["[5]"], ["[1, 3, 1, 3, 100]"], ["[20, 30, 40, 50, 60]"],
            ["[1, 2, 1, 1]"], ["[10, 1, 1, 10]"], ["[2, 7, 9, 3, 1]"]
        ]
    },
    {
        "title": "Jump Game",
        "slug": "jump-game",
        "starter_code": "def solution(nums: list) -> bool:\n    pass\n",
        "description": """Дан целочисленный массив `nums`. Начальная позиция — индекс 0. Значение `nums[i]` указывает максимальную длину прыжка из позиции `i`. Определите, можно ли достичь последнего индекса.

### Пример работы:
```python
solution([2, 3, 1, 1, 4])  # Вернет: True
```""",
        "tags": ["arrays", "greedy"],
        "solver": solve_jump_game,
        "inputs": [
            ["[2, 3, 1, 1, 4]"], ["[3, 2, 1, 0, 4]"], ["[0]"], ["[1]"],
            ["[2, 0]"], ["[1, 0, 1, 0]"], ["[2, 5, 0, 0]"],
            ["[1, 1, 1, 1]"], ["[0, 2, 3]"], ["[5, 9, 3, 2, 1, 0, 2, 3, 3, 1, 0, 0]"]
        ]
    },
    {
        "title": "Jump Game II",
        "slug": "jump-game-ii",
        "starter_code": "def solution(nums: list) -> int:\n    pass\n",
        "description": """Дан массив `nums`. Начиная с индекса 0, найдите минимальное количество прыжков, чтобы добраться до последнего индекса. Гарантируется, что достичь конца всегда возможно.

### Пример работы:
```python
solution([2, 3, 1, 1, 4])  # Вернет: 2 (прыжок на 1 шаг до индекса 1, затем на 3 шага до конца)
```""",
        "tags": ["arrays", "greedy"],
        "solver": solve_jump_game_ii,
        "inputs": [
            ["[2, 3, 1, 1, 4]"], ["[2, 3, 0, 1, 4]"], ["[1]"], ["[1, 2]"],
            ["[1, 2, 3]"], ["[2, 1]"], ["[3, 2, 1]"],
            ["[1, 1, 1, 1]"], ["[7, 0, 9, 6, 9, 6, 1, 7, 9, 0, 1, 2, 9, 0, 3]"],
            ["[10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 0]"]
        ]
    },
    {
        "title": "Merge Intervals",
        "slug": "merge-intervals",
        "starter_code": "def solution(intervals: list) -> list:\n    pass\n",
        "description": """Дан массив интервалов `intervals`, где `intervals[i] = [start, end]`. Объедините все перекрывающиеся интервалы и верните список неперекрывающихся интервалов.

### Пример работы:
```python
solution([[1, 3], [2, 6], [8, 10], [15, 18]])  # Вернет: [[1, 6], [8, 10], [15, 18]]
```""",
        "tags": ["arrays", "sorting"],
        "solver": solve_merge_intervals,
        "inputs": [
            ["[[1, 3], [2, 6], [8, 10], [15, 18]]"], ["[[1, 4], [4, 5]]"],
            ["[[1, 4], [0, 4]]"], ["[[1, 4], [2, 3]]"], ["[[1, 4]]"],
            ["[[1, 4], [0, 0]]"], ["[[2, 3], [4, 5], [6, 7], [8, 9], [1, 10]]"],
            ["[[1, 10], [2, 3], [4, 5], [6, 7]]"], ["[[1, 2], [3, 4], [5, 6]]"],
            ["[[1, 5], [2, 4], [3, 6], [8, 10]]"]
        ]
    },
    {
        "title": "Non-overlapping Intervals",
        "slug": "non-overlapping-intervals",
        "starter_code": "def solution(intervals: list) -> int:\n    pass\n",
        "description": """Дан массив интервалов `intervals`. Найдите минимальное количество интервалов, которые нужно удалить, чтобы остальные интервалы не перекрывались.

### Пример работы:
```python
solution([[1, 2], [2, 3], [3, 4], [1, 3]])  # Вернет: 1 (удалить [1, 3])
```""",
        "tags": ["arrays", "greedy"],
        "solver": solve_non_overlapping_intervals,
        "inputs": [
            ["[[1, 2], [2, 3], [3, 4], [1, 3]]"], ["[[1, 2], [1, 2], [1, 2]]"],
            ["[[1, 2], [2, 3]]"], ["[[1, 100], [11, 22], [1, 11], [2, 12]]"],
            ["[[0, 2], [1, 3], [2, 4], [3, 5], [4, 6]]"], ["[[1, 5], [2, 3], [3, 4]]"],
            ["[[-52, 31], [-73, -26], [82, 97], [-65, -11], [-62, -49]]"],
            ["[[1, 2]]"], ["[[1, 4], [2, 5], [3, 6]]"], ["[[1, 3], [2, 4], [3, 5], [4, 6]]"]
        ]
    },
    {
        "title": "Spiral Matrix",
        "slug": "spiral-matrix",
        "starter_code": "def solution(matrix: list) -> list:\n    pass\n",
        "description": """Дана матрица `matrix` размера `m x n`. Верните список всех элементов матрицы в порядке спирального обхода по часовой стрелке.

### Пример работы:
```python
solution([[1, 2, 3], [4, 5, 6], [7, 8, 9]])  # Вернет: [1, 2, 3, 6, 9, 8, 7, 4, 5]
```""",
        "tags": ["matrix"],
        "solver": solve_spiral_matrix,
        "inputs": [
            ["[[1, 2, 3], [4, 5, 6], [7, 8, 9]]"],
            ["[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]"],
            ["[[1]]"],
            ["[[1, 2, 3]]"],
            ["[[1], [2], [3]]"],
            ["[[1, 2], [3, 4]]"],
            ["[[2, 5, 8], [4, 0, -1]]"],
            ["[[1, 2, 3, 4, 5]]"],
            ["[[1], [2], [3], [4], [5]]"],
            ["[[1, 2], [3, 4], [5, 6], [7, 8]]"]
        ]
    },
    {
        "title": "Rotate Image",
        "slug": "rotate-image",
        "starter_code": "def solution(matrix: list) -> list:\n    pass\n",
        "description": """Дана квадратная матрица `matrix` размера `n x n`. Поверните изображение на 90 градусов по часовой стрелке и верните новую повернутую матрицу.

### Пример работы:
```python
solution([[1, 2, 3], [4, 5, 6], [7, 8, 9]])  # Вернет: [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
```""",
        "tags": ["matrix"],
        "solver": solve_rotate_image,
        "inputs": [
            ["[[1, 2, 3], [4, 5, 6], [7, 8, 9]]"],
            ["[[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]"],
            ["[[1]]"],
            ["[[1, 2], [3, 4]]"],
            ["[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]"],
            ["[[0, 1], [2, 3]]"],
            ["[[1, 0, 0], [0, 1, 0], [0, 0, 1]]"],
            ["[[9, 8, 7], [6, 5, 4], [3, 2, 1]]"],
            ["[[2, 4], [6, 8]]"],
            ["[[1, 5, 9], [2, 6, 10], [3, 7, 11]]"]
        ]
    },
    {
        "title": "Set Matrix Zeroes",
        "slug": "set-matrix-zeroes",
        "starter_code": "def solution(matrix: list) -> list:\n    pass\n",
        "description": """Дана матрица `matrix` размера `m x n`. Если какой-либо элемент равен 0, обнулите всю соответствующую строку и столбец. Верните измененную матрицу.

### Пример работы:
```python
solution([[1, 1, 1], [1, 0, 1], [1, 1, 1]])  # Вернет: [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
```""",
        "tags": ["matrix"],
        "solver": solve_set_matrix_zeroes,
        "inputs": [
            ["[[1, 1, 1], [1, 0, 1], [1, 1, 1]]"],
            ["[[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]"],
            ["[[1]]"],
            ["[[0]]"],
            ["[[1, 2], [3, 4]]"],
            ["[[1, 0], [3, 4]]"],
            ["[[1, 2, 3], [4, 5, 6], [7, 8, 0]]"],
            ["[[0, 0], [0, 0]]"],
            ["[[1, 2, 3, 4], [5, 0, 7, 8], [9, 10, 11, 12]]"],
            ["[[1, 1], [0, 1], [1, 1]]"]
        ]
    },
    {
        "title": "Unique Paths",
        "slug": "unique-paths",
        "starter_code": "def solution(m: int, n: int) -> int:\n    pass\n",
        "description": """Робот находится в левом верхнем углу сетки `m x n`. Он может двигаться только вправо или вниз. Найдите количество уникальных путей до правого нижнего угла.

### Пример работы:
```python
solution(3, 7)  # Вернет: 28
```""",
        "tags": ["dynamic-programming", "math"],
        "solver": solve_unique_paths,
        "inputs": [
            ["3, 7"], ["3, 2"], ["1, 1"], ["1, 10"], ["10, 1"],
            ["2, 2"], ["3, 3"], ["7, 3"], ["4, 4"], ["10, 10"]
        ]
    },
    {
        "title": "Minimum Path Sum",
        "slug": "minimum-path-sum",
        "starter_code": "def solution(grid: list) -> int:\n    pass\n",
        "description": """Дана сетка `grid` размера `m x n`, заполненная неотрицательными числами. Найдите путь из левого верхнего в правый нижний угол с минимальной суммой чисел вдоль пути (движение разрешено только вправо и вниз).

### Пример работы:
```python
solution([[1, 3, 1], [1, 5, 1], [4, 2, 1]])  # Вернет: 7 (путь 1 -> 3 -> 1 -> 1 -> 1)
```""",
        "tags": ["dynamic-programming", "matrix"],
        "solver": solve_min_path_sum,
        "inputs": [
            ["[[1, 3, 1], [1, 5, 1], [4, 2, 1]]"],
            ["[[1, 2, 3], [4, 5, 6]]"],
            ["[[5]]"],
            ["[[1, 2], [1, 1]]"],
            ["[[1, 2, 5], [3, 2, 1]]"],
            ["[[1, 100], [1, 1]]"],
            ["[[1, 2, 3, 4]]"],
            ["[[1], [2], [3], [4]]"],
            ["[[0, 0], [0, 0]]"],
            ["[[2, 1, 3], [6, 5, 4], [7, 8, 9]]"]
        ]
    },
    {
        "title": "Decode Ways",
        "slug": "decode-ways",
        "starter_code": "def solution(s: str) -> int:\n    pass\n",
        "description": """Секретное сообщение закодировано цифрами от '1' до '26' ('A' -> 1, 'B' -> 2, ..., 'Z' -> 26). Дана числовая строка `s`. Найдите количество способов расшифровать это сообщение.

### Пример работы:
```python
solution("12")  # Вернет: 2 ("AB" (1 2) или "L" (12))
```""",
        "tags": ["dynamic-programming", "strings"],
        "solver": solve_decode_ways,
        "inputs": [
            ['"12"'], ['"226"'], ['"06"'], ['"10"'], ['"27"'],
            ['"11106"'], ['"2101"'], ['"111111"'], ['"0"'], ['"2611055"']
        ]
    },
    {
        "title": "Word Break",
        "slug": "word-break",
        "starter_code": "def solution(s: str, wordDict: list) -> bool:\n    pass\n",
        "description": """Дана строка `s` и словарь слов `wordDict`. Определите, можно ли разбить строку `s` на последовательность из одного или нескольких слов из словаря. Одно и то же слово можно использовать повторно.

### Пример работы:
```python
solution("leetcode", ["leet", "code"])  # Вернет: True
```""",
        "tags": ["dynamic-programming", "strings"],
        "solver": solve_word_break,
        "inputs": [
            ['"leetcode", ["leet", "code"]'],
            ['"applepenapple", ["apple", "pen"]'],
            ['"catsandog", ["cats", "dog", "sand", "and", "cat"]'],
            ['"a", ["a"]'],
            ['"a", ["b"]'],
            ['"bb", ["a", "b", "bbb", "bbbb"]'],
            ['"cars", ["car", "ca", "rs"]'],
            ['"program", ["pro", "gram", "p"]'],
            ['"goalspecial", ["go", "goal", "special"]'],
            ['"abcd", ["a", "abc", "b", "cd"]']
        ]
    },
])

# ==================== TASKS 31 - 50 ====================
import bisect

def solve_lis(nums):
    sub = []
    for x in nums:
        idx = bisect.bisect_left(sub, x)
        if idx == len(sub):
            sub.append(x)
        else:
            sub[idx] = x
    return len(sub)

def solve_sort_colors(nums):
    return sorted(nums)

def solve_find_duplicate(nums):
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast: break
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow

def solve_find_all_duplicates(nums):
    c = Counter(nums)
    return sorted([k for k, v in c.items() if v > 1])

def solve_increasing_triplet(nums):
    first = second = float('inf')
    for x in nums:
        if x <= first:
            first = x
        elif x <= second:
            second = x
        else:
            return True
    return False

def solve_gas_station(gas, cost):
    if sum(gas) < sum(cost): return -1
    total = 0
    start = 0
    for i in range(len(gas)):
        total += gas[i] - cost[i]
        if total < 0:
            total = 0
            start = i + 1
    return start

def solve_partition_labels(s):
    last = {c: i for i, c in enumerate(s)}
    start = end = 0
    res = []
    for i, c in enumerate(s):
        end = max(end, last[c])
        if i == end:
            res.append(end - start + 1)
            start = i + 1
    return res

def solve_valid_sudoku(board):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    for r in range(9):
        for c in range(9):
            val = str(board[r][c])
            if val == '.' or val == '0': continue
            b = (r // 3) * 3 + (c // 3)
            if val in rows[r] or val in cols[c] or val in boxes[b]:
                return False
            rows[r].add(val)
            cols[c].add(val)
            boxes[b].add(val)
    return True

def solve_multiply_strings(num1, num2):
    return str(int(num1) * int(num2))

def solve_reverse_words(s):
    return " ".join(s.strip().split()[::-1])

def solve_sort_characters_by_frequency(s):
    c = Counter(s)
    return "".join(sorted(s, key=lambda ch: (-c[ch], ch)))

def solve_kth_largest(nums, k):
    return sorted(nums, reverse=True)[k - 1]

def solve_number_of_islands(grid):
    if not grid: return 0
    m, n = len(grid), len(grid[0])
    visited = [[False] * n for _ in range(m)]
    count = 0
    def dfs(r, c):
        if r < 0 or r >= m or c < 0 or c >= n or visited[r][c] or str(grid[r][c]) != '1':
            return
        visited[r][c] = True
        dfs(r + 1, c); dfs(r - 1, c); dfs(r, c + 1); dfs(r, c - 1)
    for r in range(m):
        for c in range(n):
            if not visited[r][c] and str(grid[r][c]) == '1':
                dfs(r, c)
                count += 1
    return count

def solve_max_area_of_island(grid):
    if not grid: return 0
    m, n = len(grid), len(grid[0])
    visited = [[False] * n for _ in range(m)]
    def dfs(r, c):
        if r < 0 or r >= m or c < 0 or c >= n or visited[r][c] or int(grid[r][c]) != 1:
            return 0
        visited[r][c] = True
        return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)
    max_area = 0
    for r in range(m):
        for c in range(n):
            if not visited[r][c] and int(grid[r][c]) == 1:
                max_area = max(max_area, dfs(r, c))
    return max_area

def solve_surrounded_regions(board):
    if not board: return []
    m, n = len(board), len(board[0])
    b = [list(row) for row in board]
    def dfs(r, c):
        if r < 0 or r >= m or c < 0 or c >= n or b[r][c] != 'O':
            return
        b[r][c] = 'E'
        dfs(r + 1, c); dfs(r - 1, c); dfs(r, c + 1); dfs(r, c - 1)
    for r in range(m):
        dfs(r, 0); dfs(r, n - 1)
    for c in range(n):
        dfs(0, c); dfs(m - 1, c)
    for r in range(m):
        for c in range(n):
            if b[r][c] == 'O': b[r][c] = 'X'
            elif b[r][c] == 'E': b[r][c] = 'O'
    return b

def solve_moving_zeros(lst):
    non_zeros = [x for x in lst if x != 0 or x is False]
    zeros = [x for x in lst if x == 0 and x is not False]
    return non_zeros + zeros

def solve_pig_latin(text):
    words = text.split(' ')
    res = []
    for w in words:
        if w.isalpha():
            res.append(w[1:] + w[0] + 'ay')
        else:
            res.append(w)
    return ' '.join(res)

def solve_human_readable_time(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def solve_valid_parentheses_string(s):
    low = high = 0
    for c in s:
        if c == '(':
            low += 1
            high += 1
        elif c == ')':
            low = max(0, low - 1)
            high -= 1
        elif c == '*':
            low = max(0, low - 1)
            high += 1
        if high < 0:
            return False
    return low == 0

def solve_rgb_to_hex(r, g, b):
    def clamp(x):
        return max(0, min(255, x))
    return f"{clamp(r):02X}{clamp(g):02X}{clamp(b):02X}"


ALL_TASKS.extend([
    {
        "title": "Longest Increasing Subsequence",
        "slug": "longest-increasing-subsequence",
        "starter_code": "def solution(nums: list) -> int:\n    pass\n",
        "description": """Дан целочисленный массив `nums`. Найдите длину самой длинной строго возрастающей подпоследовательности (элементы не обязательно должны идти подряд).

### Пример работы:
```python
solution([10, 9, 2, 5, 3, 7, 101, 18])  # Вернет: 4 (подпоследовательность [2, 3, 7, 101])
```""",
        "tags": ["arrays", "dynamic-programming"],
        "solver": solve_lis,
        "inputs": [
            ["[10, 9, 2, 5, 3, 7, 101, 18]"], ["[0, 1, 0, 3, 2, 3]"],
            ["[7, 7, 7, 7, 7, 7, 7]"], ["[1]"], ["[1, 3, 6, 7, 9, 4, 10, 5, 6]"],
            ["[4, 10, 4, 3, 8, 9]"], ["[2, 2]"], ["[1, 2, 3, 4, 5]"],
            ["[5, 4, 3, 2, 1]"], ["[3, 5, 6, 2, 5, 4, 19, 5, 6, 7, 12]"]
        ]
    },
    {
        "title": "Sort Colors",
        "slug": "sort-colors",
        "starter_code": "def solution(nums: list) -> list:\n    pass\n",
        "description": """Дан массив `nums` с объектами трех цветов: 0 (красный), 1 (белый) и 2 (синий). Отсортируйте массив по возрастанию цветов на месте за один проход с константной памятью и верните отсортированный массив.

### Пример работы:
```python
solution([2, 0, 2, 1, 1, 0])  # Вернет: [0, 0, 1, 1, 2, 2]
```""",
        "tags": ["arrays", "two-pointers"],
        "solver": solve_sort_colors,
        "inputs": [
            ["[2, 0, 2, 1, 1, 0]"], ["[2, 0, 1]"], ["[0]"], ["[1]"],
            ["[2]"], ["[1, 0]"], ["[2, 1, 0]"], ["[0, 0, 0]"],
            ["[2, 2, 2]"], ["[1, 2, 0, 1, 2, 0, 1, 2, 0]"]
        ]
    },
    {
        "title": "Find the Duplicate Number",
        "slug": "find-the-duplicate-number",
        "starter_code": "def solution(nums: list) -> int:\n    pass\n",
        "description": """Дан массив `nums`, содержащий `n + 1` целых чисел в диапазоне от 1 до n. В массиве гарантированно существует ровно одно повторяющееся число (оно может встречаться два или более раз). Найдите и верните это число, не изменяя массив и используя O(1) памяти.

### Пример работы:
```python
solution([1, 3, 4, 2, 2])  # Вернет: 2
```""",
        "tags": ["arrays", "two-pointers"],
        "solver": solve_find_duplicate,
        "inputs": [
            ["[1, 3, 4, 2, 2]"], ["[3, 1, 3, 4, 2]"], ["[3, 3, 3, 3, 3]"],
            ["[1, 1]"], ["[1, 1, 2]"], ["[2, 2, 2, 2, 2]"],
            ["[2, 5, 9, 6, 9, 3, 8, 9, 7, 1]"], ["[1, 4, 4, 2, 4]"],
            ["[1, 2, 3, 4, 4]"], ["[4, 3, 1, 4, 2]"]
        ]
    },
    {
        "title": "Find All Duplicates in an Array",
        "slug": "find-all-duplicates-in-an-array",
        "starter_code": "def solution(nums: list) -> list:\n    pass\n",
        "description": """Дан массив `nums` длины `n`, где каждое число находится в диапазоне `[1, n]`. Некоторые элементы появляются дважды, а остальные — один раз. Найдите все элементы, которые появляются дважды, и верните их список, отсортированный по возрастанию.

### Пример работы:
```python
solution([4, 3, 2, 7, 8, 2, 3, 1])  # Вернет: [2, 3]
```""",
        "tags": ["arrays"],
        "solver": solve_find_all_duplicates,
        "inputs": [
            ["[4, 3, 2, 7, 8, 2, 3, 1]"], ["[1, 1, 2]"], ["[1]"],
            ["[1, 2, 3, 4, 5]"], ["[2, 2, 1, 3, 4, 5, 3]"], ["[1, 2, 2, 3, 4, 4]"],
            ["[10, 2, 5, 10, 9, 1, 1, 4, 3, 7]"], ["[1, 2, 1, 2]"],
            ["[3, 1, 2]"], ["[5, 4, 6, 7, 9, 3, 10, 9, 5, 6]"]
        ]
    },
    {
        "title": "Increasing Triplet Subsequence",
        "slug": "increasing-triplet-subsequence",
        "starter_code": "def solution(nums: list) -> bool:\n    pass\n",
        "description": """Дан целочисленный массив `nums`. Определите, существуют ли три индекса `i < j < k`, такие что `nums[i] < nums[j] < nums[k]`. Решение должно работать за O(n) времени и O(1) памяти.

### Пример работы:
```python
solution([1, 2, 3, 4, 5])  # Вернет: True
```""",
        "tags": ["arrays", "greedy"],
        "solver": solve_increasing_triplet,
        "inputs": [
            ["[1, 2, 3, 4, 5]"], ["[5, 4, 3, 2, 1]"], ["[2, 1, 5, 0, 4, 6]"],
            ["[20, 100, 10, 12, 5, 13]"], ["[1, 1, 1, 1]"], ["[1, 2]"],
            ["[2, 4, -2, -3]"], ["[1, 5, 0, 4, 1, 3]"],
            ["[1, 2, 1, 2, 1, 2, 1, 2]"], ["[0, 4, 2, 1, 0, -1, -2, 5]"]
        ]
    },
    {
        "title": "Gas Station",
        "slug": "gas-station",
        "starter_code": "def solution(gas: list, cost: list) -> int:\n    pass\n",
        "description": """Вдоль кольцевого маршрута расположены `n` заправок. На станции `i` доступно `gas[i]` бензина, а для проезда до следующей станции требуется `cost[i]` бензина. Найдите начальную станцию, начав с которой можно совершить полный круг по часовой стрелке. Если маршрут невозможен, верните -1.

### Пример работы:
```python
solution([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])  # Вернет: 3 (старт со станции с индексом 3)
```""",
        "tags": ["arrays", "greedy"],
        "solver": solve_gas_station,
        "inputs": [
            ["[1, 2, 3, 4, 5], [3, 4, 5, 1, 2]"], ["[2, 3, 4], [3, 4, 3]"],
            ["[5, 1, 2, 3, 4], [4, 4, 1, 5, 1]"], ["[3, 1, 1], [1, 2, 2]"],
            ["[4, 5, 2, 6, 5, 3], [3, 2, 7, 3, 2, 9]"], ["[2], [2]"],
            ["[1], [2]"], ["[5, 8, 2, 8], [6, 5, 6, 6]"],
            ["[1, 2, 3, 4, 5, 5, 70], [2, 3, 4, 3, 9, 6, 2]"],
            ["[7, 1, 0, 11, 4], [5, 9, 1, 2, 5]"]
        ]
    },
    {
        "title": "Partition Labels",
        "slug": "partition-labels",
        "starter_code": "def solution(s: str) -> list:\n    pass\n",
        "description": """Дана строка `s`. Разбейте строку на как можно большее число частей так, чтобы каждая буква встречалась максимум в одной части. Верните список длин этих частей.

### Пример работы:
```python
solution("ababcbacadefegdehijhklij")  # Вернет: [9, 7, 8]
```""",
        "tags": ["strings", "greedy"],
        "solver": solve_partition_labels,
        "inputs": [
            ['"ababcbacadefegdehijhklij"'], ['"eccbbbbdec"'], ['"a"'],
            ['"abc"'], ['"caedbdedda"'], ['"defabc"'], ['"z"'],
            ['"abaccb"'], ['"qiejxqfnqcehy"'], ['"vhaflvvvkmqenvanvmqenk"']
        ]
    },
    {
        "title": "Valid Sudoku",
        "slug": "valid-sudoku",
        "starter_code": "def solution(board: list) -> bool:\n    pass\n",
        "description": """Определите, является ли поле судоку `9 x 9` допустимым. Каждая строка, каждый столбец и каждый из девяти квадратов `3 x 3` должны содержать цифры от 1 до 9 без повторений. Пустые клетки обозначены символом `.`

### Пример работы:
```python
solution([["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]])  # Вернет: True
```""",
        "tags": ["matrix", "hash-table"],
        "solver": solve_valid_sudoku,
        "inputs": [
            ['[["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]'],
            ['[["8","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]'],
            ['[[".",".",".",".","5",".",".","1","."],[".","4",".","3",".",".",".",".","."],[".",".",".",".",".","3",".",".","1"],["8",".",".",".",".",".",".","2","."],[".",".","2",".","7",".",".",".","."],[".","1","5",".",".",".",".",".","."],[".",".",".",".",".","2",".",".","."],[".","2",".","9",".",".",".",".","."],[".",".","4",".",".",".",".",".","."]]'],
            ['[["1","2","3","4","5","6","7","8","9"],["4","5","6","7","8","9","1","2","3"],["7","8","9","1","2","3","4","5","6"],["2","3","4","5","6","7","8","9","1"],["5","6","7","8","9","1","2","3","4"],["8","9","1","2","3","4","5","6","7"],["3","4","5","6","7","8","9","1","2"],["6","7","8","9","1","2","3","4","5"],["9","1","2","3","4","5","6","7","8"]]'],
            ['[["1","1",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."]]'],
            ['[[".",".",".",".",".",".",".",".","."],["1",".",".",".",".",".",".",".","."],["1",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."]]'],
            ['[[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."]]'],
            ['[["5",".",".",".",".",".",".",".","."],["5",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."]]'],
            ['[[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".","7",".",".",".",".","."],[".",".",".","7",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."]]'],
            ['[["3",".",".",".",".",".",".",".","."],["3",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."]]']
        ]
    },
    {
        "title": "Multiply Strings",
        "slug": "multiply-strings",
        "starter_code": "def solution(num1: str, num2: str) -> str:\n    pass\n",
        "description": """Даны две неотрицательные строки `num1` и `num2`, представляющие целые числа. Верните произведение `num1` и `num2`, также представленное в виде строки.

### Пример работы:
```python
solution("2", "3")  # Вернет: "6"
```""",
        "tags": ["strings", "math"],
        "solver": solve_multiply_strings,
        "inputs": [
            ['"2", "3"'], ['"123", "456"'], ['"0", "0"'], ['"9", "99"'],
            ['"10", "10"'], ['"100", "0"'], ['"498828660196", "840477629533"'],
            ['"1", "1"'], ['"12345", "6789"'], ['"99999", "99999"']
        ]
    },
    {
        "title": "Reverse Words in a String",
        "slug": "reverse-words-in-a-string",
        "starter_code": "def solution(s: str) -> str:\n    pass\n",
        "description": """Дана строка `s`. Разверните порядок слов в строке. Слова должны быть разделены одним пробелом, а начальные и конечные пробелы удалены.

### Пример работы:
```python
solution("the sky is blue")  # Вернет: "blue is sky the"
```""",
        "tags": ["strings", "two-pointers"],
        "solver": solve_reverse_words,
        "inputs": [
            ['"the sky is blue"'], ['"  hello world  "'], ['"a good   example"'],
            ['"word"'], ['"   "'], ['"Alice does not even like bob"'],
            ['"  Bob    Loves  Alice   "'], ['"1 2 3 4 5"'],
            ['"EPIC  WIN"'], ['"single"']
        ]
    },
    {
        "title": "Sort Characters By Frequency",
        "slug": "sort-characters-by-frequency",
        "starter_code": "def solution(s: str) -> str:\n    pass\n",
        "description": """Дана строка `s`. Отсортируйте её в порядке убывания частоты символов. При равной частоте символы упорядочиваются по алфавиту для стабильности проверки.

### Пример работы:
```python
solution("tree")  # Вернет: "eert" (буква 'e' встречается 2 раза, 'r' и 't' по 1 разу)
```""",
        "tags": ["strings", "hash-table"],
        "solver": solve_sort_characters_by_frequency,
        "inputs": [
            ['"tree"'], ['"cccaaa"'], ['"Aabb"'], ['"loveleetcode"'],
            ['"raeaforexamplerrr"'], ['"2a554442f544asfa"'], ['"a"'],
            ['""'], ['"abracadabra"'], ['"Mississippi"']
        ]
    },
    {
        "title": "Kth Largest Element in an Array",
        "slug": "kth-largest-element-in-an-array",
        "starter_code": "def solution(nums: list, k: int) -> int:\n    pass\n",
        "description": """Дан целочисленный массив `nums` и целое число `k`. Найдите `k`-й по величине элемент массива (с учетом дубликатов).

### Пример работы:
```python
solution([3, 2, 1, 5, 6, 4], 2)  # Вернет: 5
```""",
        "tags": ["arrays", "heap"],
        "solver": solve_kth_largest,
        "inputs": [
            ["[3, 2, 1, 5, 6, 4], 2"], ["[3, 2, 3, 1, 2, 4, 5, 5, 6], 4"],
            ["[1], 1"], ["[2, 1], 1"], ["[2, 1], 2"],
            ["[7, 6, 5, 4, 3, 2, 1], 5"], ["[100, 200, 300, 400], 1"],
            ["[-1, 2, 0], 2"], ["[5, 5, 5, 5], 3"], ["[99, 99], 1"]
        ]
    },
    {
        "title": "Number of Islands",
        "slug": "number-of-islands",
        "starter_code": "def solution(grid: list) -> int:\n    pass\n",
        "description": """Дана двумерная карта `grid`, состоящая из '1' (суша) и '0' (вода). Остров окружен водой и образуется соединением соседних по горизонтали или вертикали земель. Найдите количество островов.

### Пример работы:
```python
solution([["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]])  # Вернет: 1
```""",
        "tags": ["matrix", "depth-first-search"],
        "solver": solve_number_of_islands,
        "inputs": [
            ['[["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]'],
            ['[["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]'],
            ['[["1"]]'], ['[["0"]]'], ['[["1","0","1","0","1"]]'],
            ['[["1"],["0"],["1"],["0"],["1"]]'],
            ['[["0","0","0"],["0","0","0"],["0","0","0"]]'],
            ['[["1","1","1"],["0","1","0"],["1","1","1"]]'],
            ['[["1","0"],["0","1"]]'],
            ['[["1","1","0","0"],["0","0","1","1"],["1","1","0","0"],["0","0","1","1"]]']
        ]
    },
    {
        "title": "Max Area of Island",
        "slug": "max-area-of-island",
        "starter_code": "def solution(grid: list) -> int:\n    pass\n",
        "description": """Дана бинарная матрица `grid` размера `m x n`. Остров представляет собой группу соседних единиц (по вертикали или горизонтали). Площадь острова — это количество единиц в нем. Найдите максимальную площадь острова. Если островов нет, верните 0.

### Пример работы:
```python
solution([[0,0,1,0,0],[1,1,1,0,0],[0,0,0,1,1]])  # Вернет: 4
```""",
        "tags": ["matrix", "depth-first-search"],
        "solver": solve_max_area_of_island,
        "inputs": [
            ["[[0,0,1,0,0],[1,1,1,0,0],[0,0,0,1,1]]"],
            ["[[0,0,0,0,0,0,0,0]]"],
            ["[[1,1],[1,1]]"],
            ["[[1]]"],
            ["[[0]]"],
            ["[[1,0,1],[0,1,0],[1,0,1]]"],
            ["[[1,1,0,1],[1,1,0,1],[0,0,0,0],[1,1,1,1]]"],
            ["[[0,1],[1,0]]"],
            ["[[1,1,1,1,1]]"],
            ["[[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0]]"]
        ]
    },
    {
        "title": "Surrounded Regions",
        "slug": "surrounded-regions",
        "starter_code": "def solution(board: list) -> list:\n    pass\n",
        "description": """Дана матрица `board` размера `m x n`, содержащая символы 'X' и 'O'. Захватите все регионы, окруженные 'X', заменив в них 'O' на 'X'. Регион, соединенный с краем доски, захватить нельзя.

### Пример работы:
```python
solution([["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]])  # Вернет: [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]
```""",
        "tags": ["matrix", "breadth-first-search"],
        "solver": solve_surrounded_regions,
        "inputs": [
            ['[["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]'],
            ['[["X"]]'], ['[["O"]]'],
            ['[["O","O"],["O","O"]]'],
            ['[["X","X"],["X","X"]]'],
            ['[["X","O","X"],["X","O","X"],["X","O","X"]]'],
            ['[["O","X","O"],["X","O","X"],["O","X","O"]]'],
            ['[["X","X","X"],["X","O","X"],["X","X","X"]]'],
            ['[["X","X","X","X"],["X","O","X","X"],["X","X","O","X"],["X","X","X","X"]]'],
            ['[["O","X","X","X"],["X","O","O","X"],["X","X","X","X"]]']
        ]
    },
    {
        "title": "Moving Zeros To The End",
        "slug": "moving-zeros-to-the-end",
        "starter_code": "def solution(lst: list) -> list:\n    pass\n",
        "description": """Напишите функцию, которая принимает массив `lst` и перемещает все нули в конец, сохраняя исходный порядок всех остальных элементов. Значение `False` нулем не считается.

### Пример работы:
```python
solution([1, 2, 0, 1, 0, 1, 0, 3, 0, 1])  # Вернет: [1, 2, 1, 1, 3, 1, 0, 0, 0, 0]
```""",
        "tags": ["arrays"],
        "solver": solve_moving_zeros,
        "inputs": [
            ["[1, 2, 0, 1, 0, 1, 0, 3, 0, 1]"],
            ["[9, 0, 0, 9, 1, 2, 0, 1, 0, 1, 0, 3, 0, 1, 9, 0, 0, 0, 0, 9]"],
            ["[0, 0]"], ["[]"], ["[1, 2, 3]"],
            ["[False, 1, 0, 1, 2, 0, 1, 3, 'a']"],
            ["[0, 1, None, 2, False, 1, 0]"],
            ["[0, 0, 0, 1]"], ["[1, 0, 0, 0]"], ["[0, '0', 1, 0, 2]"]
        ]
    },
    {
        "title": "Simple Pig Latin",
        "slug": "simple-pig-latin",
        "starter_code": "def solution(text: str) -> str:\n    pass\n",
        "description": """Переместите первую букву каждого слова в конец слова и добавьте 'ay'. Знаки препинания должны остаться нетронутыми.

### Пример работы:
```python
solution("Pig latin is cool")  # Вернет: "igPay atinlay siay oolcay"
```""",
        "tags": ["strings"],
        "solver": solve_pig_latin,
        "inputs": [
            ['"Pig latin is cool"'], ['"This is my string"'],
            ['"Hello world !"'], ['"O tempora o mores !"'],
            ['"Quis custodiet ipsos custodes ?"'], ['"Acta est fabula"'],
            ['"Barba non facit philosophum"'], ['"De omnibus dubitandum"'],
            ['"In vino veritas"'], ['"Carpe diem !"']
        ]
    },
    {
        "title": "Human Readable Time",
        "slug": "human-readable-time",
        "starter_code": "def solution(seconds: int) -> str:\n    pass\n",
        "description": """Напишите функцию, которая принимает неотрицательное целое число (секунды) и возвращает время в удобочитаемом формате `HH:MM:SS`.

### Пример работы:
```python
solution(359999)  # Вернет: "99:59:59"
```""",
        "tags": ["math", "strings"],
        "solver": solve_human_readable_time,
        "inputs": [
            ["0"], ["59"], ["60"], ["3599"], ["3600"],
            ["45296"], ["86399"], ["86400"], ["359999"], ["12345"]
        ]
    },
    {
        "title": "Valid Parentheses String",
        "slug": "valid-parentheses-string",
        "starter_code": "def solution(s: str) -> bool:\n    pass\n",
        "description": """Дана строка `s`, содержащая только символы '(', ')' и '*'. Символ '*' может считаться как '(', так и ')', или пустой строкой. Определите, является ли скобочная последовательность допустимой.

### Пример работы:
```python
solution("(*))")  # Вернет: True
```""",
        "tags": ["strings", "greedy"],
        "solver": solve_valid_parentheses_string,
        "inputs": [
            ['"()"'], ['"(*)"'], ['"(*))"'], ['")("'], ['"(*()"'],
            ['"(((((*(()(((*((**(((()*****()()*)())()"'],
            ['"(((((*)))**"'], ['"***"'], ['""'], ['"(((((*"']
        ]
    },
    {
        "title": "RGB To Hex Conversion",
        "slug": "rgb-to-hex-conversion",
        "starter_code": "def solution(r: int, g: int, b: int) -> str:\n    pass\n",
        "description": """Реализуйте функцию, которая переводит десятичные значения RGB в шестнадцатеричный код цвета из 6 заглавных символов. Значения меньше 0 округляются до 0, а больше 255 — до 255.

### Пример работы:
```python
solution(255, 255, 300)  # Вернет: "FFFFFF"
```""",
        "tags": ["math", "strings"],
        "solver": solve_rgb_to_hex,
        "inputs": [
            ["0, 0, 0"], ["1, 2, 3"], ["255, 255, 255"], ["254, 253, 252"],
            ["-20, 275, 125"], ["255, 255, 300"], ["148, 0, 211"],
            ["173, 255, 47"], ["0, 0, -5"], ["300, 300, 300"]
        ]
    },
])

def solve_rot13(message):
    res = []
    for c in message:
        if 'a' <= c <= 'z':
            res.append(chr((ord(c) - ord('a') + 13) % 26 + ord('a')))
        elif 'A' <= c <= 'Z':
            res.append(chr((ord(c) - ord('A') + 13) % 26 + ord('A')))
        else:
            res.append(c)
    return ''.join(res)


ALL_TASKS.append({
    "title": "Rot13",
    "slug": "rot13",
    "starter_code": "def solution(message: str) -> str:\n    pass\n",
    "description": """Напишите функцию, которая принимает строку и возвращает зашифрованную строку с помощью шифра ROT13 (сдвиг каждой буквы на 13 позиций в алфавите с сохранением регистра). Символы, не являющиеся буквами, должны остаться без изменений.

### Пример работы:
```python
solution("test")  # Вернет: "grfg"
```""",
    "tags": ["strings", "ciphers"],
    "solver": solve_rot13,
    "inputs": [
        ['"test"'], ['"Test"'], ['"Ruby is cool!"'], ['"10+2 is twelve."'],
        ['"aA bB zZ"'], ['"Codewars"'], ['"grfg"'], ['"Hello, World!"'],
        ['"abcdefghijklmnopqrstuvwxyz"'],
        ['"The quick brown fox jumps over the lazy dog."']
    ]
})

print(f"Total tasks prepared: {len(ALL_TASKS)}")

# ==================== DATABASE SEEDING ====================

def run_seeder():
    created_count = 0
    updated_count = 0
    test_count = 0

    with transaction.atomic():
        for task_info in ALL_TASKS:
            task, created = Task.objects.update_or_create(
                slug=task_info["slug"],
                defaults={
                    "title": task_info["title"],
                    "description": task_info["description"],
                    "difficulty": Task.Difficulty.MEDIUM,
                    "starter_code": task_info["starter_code"],
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

            # Set tags
            tag_objs = []
            for tag_name in task_info.get("tags", []):
                tag_obj, _ = Tag.objects.get_or_create(
                    slug=tag_name,
                    defaults={"name": tag_name.replace('-', ' ').capitalize(), "color": "info"}
                )
                tag_objs.append(tag_obj)
            task.tags.set(tag_objs)

            # Recreate test cases
            task.test_cases.all().delete()
            solver = task_info["solver"]

            for inp_args in task_info["inputs"]:
                raw_input = inp_args[0]
                parsed_args = parse_test_inputs(raw_input)
                raw_output = solver(*parsed_args)
                expected_str = str(raw_output).strip()

                TestCase.objects.create(
                    task=task,
                    input_data=raw_input,
                    expected_output=expected_str,
                    is_hidden=False
                )
                test_count += 1

    print(f"Successfully seeded database! Created: {created_count}, Updated: {updated_count}, Total tests: {test_count}")

if __name__ == '__main__':
    run_seeder()

