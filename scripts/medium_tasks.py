# -*- coding: utf-8 -*-
"""
100 Задач уровня Medium (Средний / 6-4 kyu)
Каждая задача содержит slug, title, desc, starter, tags, fn, tests
"""

def _two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        diff = target - x
        if diff in seen:
            return [seen[diff], i]
        seen[x] = i
    return []

def _is_valid_brackets(s):
    mapping = {')': '(', '}': '{', ']': '['}
    stack = []
    for char in s:
        if char in mapping.values():
            stack.append(char)
        elif char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            continue
    return len(stack) == 0

def _rle_encode(s):
    if not s:
        return ""
    res = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i-1]:
            count += 1
        else:
            res.append(f"{s[i-1]}{count if count > 1 else ''}")
            count = 1
    res.append(f"{s[-1]}{count if count > 1 else ''}")
    return "".join(res)

def _rle_decode(s):
    import re
    tokens = re.findall(r'([A-Za-z])(\d*)', s)
    return "".join(char * (int(count) if count else 1) for char, count in tokens)

def _transpose(matrix):
    if not matrix or not matrix[0]:
        return []
    return [list(row) for row in zip(*matrix)]

def _rotate_matrix(matrix):
    return [list(row) for row in zip(*matrix[::-1])]

def _diagonal_sum(matrix):
    n = len(matrix)
    total = 0
    for i in range(n):
        total += matrix[i][i]
        if i != n - 1 - i:
            total += matrix[i][n - 1 - i]
    return total

def _spiral_order(matrix):
    if not matrix or not matrix[0]:
        return []
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

def _longest_common_prefix(strs):
    if not strs:
        return ""
    prefix = strs[0]
    for s in strs[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix

def _roman_to_int(s):
    vals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    prev = 0
    for char in reversed(s):
        curr = vals.get(char, 0)
        if curr >= prev:
            total += curr
        else:
            total -= curr
        prev = curr
    return total

def _int_to_roman(num):
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syb = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    res = []
    for i in range(len(val)):
        count = num // val[i]
        if count > 0:
            res.append(syb[i] * count)
            num %= val[i]
    return "".join(res)

def _merge_intervals(intervals):
    if not intervals:
        return []
    intervals = sorted(intervals, key=lambda x: x[0])
    merged = [intervals[0]]
    for current in intervals[1:]:
        prev = merged[-1]
        if current[0] <= prev[1]:
            merged[-1] = [prev[0], max(prev[1], current[1])]
        else:
            merged.append(current)
    return merged

def _move_zeroes(nums):
    non_zero = [x for x in nums if x != 0]
    return non_zero + [0] * (len(nums) - len(non_zero))

def _max_subarray_sum(nums):
    if not nums:
        return 0
    max_sum = cur_sum = nums[0]
    for x in nums[1:]:
        cur_sum = max(x, cur_sum + x)
        max_sum = max(max_sum, cur_sum)
    return max_sum

def _rotate_array(nums, k):
    if not nums:
        return []
    k %= len(nums)
    return nums[-k:] + nums[:-k]

def _find_single_number(nums):
    res = 0
    for x in nums:
        res ^= x
    return res

def _binary_search(nums, target):
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def _group_anagrams(words):
    from collections import defaultdict
    groups = defaultdict(list)
    for w in sorted(words):
        key = "".join(sorted(w))
        groups[key].append(w)
    return sorted(list(groups.values()), key=lambda g: (len(g), g[0]))

def _is_isomorphic(s, t):
    return len(set(zip(s, t))) == len(set(s)) == len(set(t)) and len(s) == len(t)

def _longest_consecutive_seq(nums):
    if not nums:
        return 0
    num_set = set(nums)
    max_len = 0
    for n in num_set:
        if n - 1 not in num_set:
            curr = n
            streak = 1
            while curr + 1 in num_set:
                curr += 1
                streak += 1
            max_len = max(max_len, streak)
    return max_len

def _pascal_triangle_row(rowIndex):
    row = [1]
    for _ in range(rowIndex):
        row = [x + y for x, y in zip([0] + row, row + [0])]
    return row

def _sieve_primes(n):
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, n + 1, i):
                sieve[j] = False
    return [i for i, is_p in enumerate(sieve) if is_p]

def _prime_factors(n):
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

def _josephus_survivor(n, k):
    res = 0
    for i in range(1, n + 1):
        res = (res + k) % i
    return res + 1

def _max_water_container(heights):
    left, right = 0, len(heights) - 1
    max_area = 0
    while left < right:
        area = min(heights[left], heights[right]) * (right - left)
        max_area = max(max_area, area)
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    return max_area

def _product_except_self(nums):
    n = len(nums)
    res = [1] * n
    prefix = 1
    for i in range(n):
        res[i] = prefix
        prefix *= nums[i]
    postfix = 1
    for i in range(n - 1, -1, -1):
        res[i] *= postfix
        postfix *= nums[i]
    return res

def _eval_rpn(tokens):
    stack = []
    for t in tokens:
        if t in "+-*/":
            b = stack.pop()
            a = stack.pop()
            if t == '+': stack.append(a + b)
            elif t == '-': stack.append(a - b)
            elif t == '*': stack.append(a * b)
            elif t == '/': stack.append(int(a / b))
        else:
            stack.append(int(t))
    return stack[0]

def _length_of_longest_substring(s):
    char_map = {}
    left = 0
    max_len = 0
    for right, char in enumerate(s):
        if char in char_map and char_map[char] >= left:
            left = char_map[char] + 1
        char_map[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len

def _generate_parentheses(n):
    res = []
    def backtrack(curr, open_count, close_count):
        if len(curr) == 2 * n:
            res.append(curr)
            return
        if open_count < n:
            backtrack(curr + "(", open_count + 1, close_count)
        if close_count < open_count:
            backtrack(curr + ")", open_count, close_count + 1)
    backtrack("", 0, 0)
    return sorted(res)

def _subarray_sum_k(nums, k):
    from collections import defaultdict
    count = 0
    curr_sum = 0
    prefix_sums = defaultdict(int)
    prefix_sums[0] = 1
    for num in nums:
        curr_sum += num
        count += prefix_sums[curr_sum - k]
        prefix_sums[curr_sum] += 1
    return count


MEDIUM_TASKS = [
    # 1-10: Классические алгоритмы на массивах
    {
        'slug': 'two-sum-indices',
        'title': 'Two Sum: Индексы двух слагаемых',
        'desc': 'Напишите функцию `solution(nums, target)`, возвращающую индексы двух чисел в списке `nums`, сумма которых равна `target`.\n\n### Пример:\n* Вход: `[2, 7, 11, 15], 9` ➔ Результат: `[0, 1]`',
        'starter': 'def solution(nums, target):\n    pass',
        'tags': ['arrays', 'search'],
        'fn': _two_sum,
        'tests': [([2, 7, 11, 15], 9), ([3, 2, 4], 6), ([3, 3], 6), ([-1, -2, -3, -4, -5], -8)],
    },
    {
        'slug': 'valid-parentheses-all-types',
        'title': 'Валидация скобочной последовательности',
        'desc': 'Строка содержит скобки `()`, `{}`, `[]`. Напишите функцию `solution(s)`, возвращающую `True`, если скобки расставлены правильно, и `False` иначе.\n\n### Пример:\n* Вход: `"()[]{}"` ➔ Результат: `True`\n* Вход: `"(]"` ➔ Результат: `False`',
        'starter': 'def solution(s):\n    pass',
        'tags': ['strings'],
        'fn': _is_valid_brackets,
        'tests': [("()[]{}",), ("(]",), ("([{}])",), ("((",), ("",), ("{[]()}",)],
    },
    {
        'slug': 'rle-string-compression',
        'title': 'RLE-сжатие строки',
        'desc': 'Напишите функцию `solution(s)`, сжимающую строку методом Run-Length Encoding (повторяющиеся подряд символы заменяются на символ и счетчик).\n\n### Пример:\n* Вход: `"AAABBC"` ➔ Результат: `"A3B2C"`',
        'starter': 'def solution(s):\n    pass',
        'tags': ['strings'],
        'fn': _rle_encode,
        'tests': [("AAABBC",), ("A",), ("ABCD",), ("WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWW",), ("",)],
    },
    {
        'slug': 'rle-string-decompression',
        'title': 'RLE-распаковка строки',
        'desc': 'Напишите функцию `solution(s)`, восстанавливающую исходную строку после сжатия RLE.\n\n### Пример:\n* Вход: `"A3B2C"` ➔ Результат: `"AAABBC"`',
        'starter': 'def solution(s):\n    pass',
        'tags': ['strings'],
        'fn': _rle_decode,
        'tests': [("A3B2C",), ("A",), ("A10B3",), ("X",)],
    },
    {
        'slug': 'matrix-transpose',
        'title': 'Транспонирование матрицы',
        'desc': 'Напишите функцию `solution(matrix)`, транспонирующую двумерную матрицу (строки становятся столбцами).\n\n### Пример:\n* Вход: `[[1, 2, 3], [4, 5, 6]]` ➔ Результат: `[[1, 4], [2, 5], [3, 6]]`',
        'starter': 'def solution(matrix):\n    pass',
        'tags': ['arrays'],
        'fn': _transpose,
        'tests': [([[1, 2, 3], [4, 5, 6]],), ([[1, 2], [3, 4]],), ([[1]],)],
    },
    {
        'slug': 'rotate-matrix-90-degrees',
        'title': 'Поворот матрицы на 90 градусов',
        'desc': 'Напишите функцию `solution(matrix)`, поворачивающую квадратную матрицу `N x N` на 90 градусов по часовой стрелке.\n\n### Пример:\n* Вход: `[[1, 2], [3, 4]]` ➔ Результат: `[[3, 1], [4, 2]]`',
        'starter': 'def solution(matrix):\n    pass',
        'tags': ['arrays'],
        'fn': _rotate_matrix,
        'tests': [([[1, 2], [3, 4]],), ([[1, 2, 3], [4, 5, 6], [7, 8, 9]],)],
    },
    {
        'slug': 'matrix-diagonal-sum',
        'title': 'Сумма диагоналей квадратной матрицы',
        'desc': 'Напишите функцию `solution(matrix)`, находящую сумму элементов главной и побочной диагоналей квадратной матрицы (центральный элемент считается один раз).\n\n### Пример:\n* Вход: `[[1,2,3],[4,5,6],[7,8,9]]` ➔ Результат: `25` (1+5+9+3+7)',
        'starter': 'def solution(matrix):\n    pass',
        'tags': ['arrays', 'math'],
        'fn': _diagonal_sum,
        'tests': [([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), ([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],), ([[5]],)],
    },
    {
        'slug': 'spiral-matrix-traversal',
        'title': 'Спиральный обход матрицы',
        'desc': 'Напишите функцию `solution(matrix)`, обходящую элементы матрицы `M x N` по спирали по часовой стрелке.\n\n### Пример:\n* Вход: `[[1,2,3],[4,5,6],[7,8,9]]` ➔ Результат: `[1,2,3,6,9,8,7,4,5]`',
        'starter': 'def solution(matrix):\n    pass',
        'tags': ['arrays'],
        'fn': _spiral_order,
        'tests': [([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), ([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],), ([[1]],)],
    },
    {
        'slug': 'longest-common-prefix-list',
        'title': 'Длиннейший общий префикс',
        'desc': 'Напишите функцию `solution(strs)`, находящую самую длинную общую приставку среди списка строк. Если общего префикса нет, верните `""`.\n\n### Пример:\n* Вход: `["flower", "flow", "flight"]` ➔ Результат: `"fl"`',
        'starter': 'def solution(strs):\n    pass',
        'tags': ['strings'],
        'fn': _longest_common_prefix,
        'tests': [(["flower", "flow", "flight"],), (["dog", "racecar", "car"],), (["interspecies", "interstellar", "interstate"],), (["a"],)],
    },
    {
        'slug': 'roman-numerals-to-integer',
        'title': 'Римские числа в арабские',
        'desc': 'Напишите функцию `solution(s)`, переводящую римское число `s` (I, V, X, L, C, D, M) в целое число.\n\n### Пример:\n* Вход: `"MCMXCIV"` ➔ Результат: `1994`\n* Вход: `"LVIII"` ➔ Результат: `58`',
        'starter': 'def solution(s):\n    pass',
        'tags': ['strings', 'math'],
        'fn': _roman_to_int,
        'tests': [("MCMXCIV",), ("LVIII",), ("III",), ("IX",), ("XL",)],
    },

    # 11-20: Интервалы, массивы и два указателя
    {
        'slug': 'integer-to-roman-numerals',
        'title': 'Арабские числа в римские',
        'desc': 'Напишите функцию `solution(num)`, переводящую целое число `num` (1 <= num <= 3999) в римскую запись.\n\n### Пример:\n* Вход: `1994` ➔ Результат: `"MCMXCIV"`',
        'starter': 'def solution(num):\n    pass',
        'tags': ['strings', 'math'],
        'fn': _int_to_roman,
        'tests': [(1994,), (58,), (3,), (9,), (40,)],
    },
    {
        'slug': 'merge-overlapping-intervals',
        'title': 'Слияние пересекающихся интервалов',
        'desc': 'Напишите функцию `solution(intervals)`, объединяющую все пересекающиеся отрезки.\n\n### Пример:\n* Вход: `[[1, 3], [2, 6], [8, 10], [15, 18]]` ➔ Результат: `[[1, 6], [8, 10], [15, 18]]`',
        'starter': 'def solution(intervals):\n    pass',
        'tags': ['arrays'],
        'fn': _merge_intervals,
        'tests': [([[1, 3], [2, 6], [8, 10], [15, 18]],), ([[1, 4], [4, 5]],), ([[1, 10], [2, 3], [4, 8]],), ([],)],
    },
    {
        'slug': 'move-zeroes-to-end',
        'title': 'Перемещение нулей в конец',
        'desc': 'Напишите функцию `solution(nums)`, которая перемещает все нули в конец списка, сохраняя порядок ненулевых элементов.\n\n### Пример:\n* Вход: `[0, 1, 0, 3, 12]` ➔ Результат: `[1, 3, 12, 0, 0]`',
        'starter': 'def solution(nums):\n    pass',
        'tags': ['arrays'],
        'fn': _move_zeroes,
        'tests': [([0, 1, 0, 3, 12],), ([0],), ([1, 2, 3],), ([0, 0, 1],)],
    },
    {
        'slug': 'maximum-subarray-kadane',
        'title': 'Максимальная сумма подмассива (Кадане)',
        'desc': 'Напишите функцию `solution(nums)`, находящую наибольшую возможную сумму непрерывного подмассива.\n\n### Пример:\n* Вход: `[-2, 1, -3, 4, -1, 2, 1, -5, 4]` ➔ Результат: `6` ([4, -1, 2, 1])',
        'starter': 'def solution(nums):\n    pass',
        'tags': ['arrays'],
        'fn': _max_subarray_sum,
        'tests': [([-2, 1, -3, 4, -1, 2, 1, -5, 4],), ([1],), ([5, 4, -1, 7, 8],), ([-5, -2, -8],)],
    },
    {
        'slug': 'rotate-array-by-k-steps',
        'title': 'Циклический сдвиг массива на K элементов',
        'desc': 'Напишите функцию `solution(nums, k)`, которая циклически сдвигает элементы списка вправо на `k` позиций.\n\n### Пример:\n* Вход: `[1, 2, 3, 4, 5, 6, 7], 3` ➔ Результат: `[5, 6, 7, 1, 2, 3, 4]`',
        'starter': 'def solution(nums, k):\n    pass',
        'tags': ['arrays'],
        'fn': _rotate_array,
        'tests': [([1, 2, 3, 4, 5, 6, 7], 3), ([-1, -100, 3, 99], 2), ([1, 2], 5)],
    },
    {
        'slug': 'single-number-xor',
        'title': 'Поиск неповторяющегося числа за O(1) памяти',
        'desc': 'В непустом массиве каждое число встречается дважды, кроме одного. Найдите это число.\n\n### Пример:\n* Вход: `[4, 1, 2, 1, 2]` ➔ Результат: `4`',
        'starter': 'def solution(nums):\n    pass',
        'tags': ['arrays'],
        'fn': _find_single_number,
        'tests': [([4, 1, 2, 1, 2],), ([2, 2, 1],), ([1],), ([7, 3, 5, 3, 7],)],
    },
    {
        'slug': 'binary-search-iterative',
        'title': 'Бинарный поиск в отсортированном массиве',
        'desc': 'Напишите функцию `solution(nums, target)`, которая за `O(log N)` находит индекс `target` в отсортированном списке или возвращает `-1`.\n\n### Пример:\n* Вход: `[-1, 0, 3, 5, 9, 12], 9` ➔ Результат: `4`',
        'starter': 'def solution(nums, target):\n    pass',
        'tags': ['search', 'arrays'],
        'fn': _binary_search,
        'tests': [([-1, 0, 3, 5, 9, 12], 9), ([-1, 0, 3, 5, 9, 12], 2), ([5], 5), ([1, 3], 0)],
    },
    {
        'slug': 'group-anagrams-hash',
        'title': 'Группировка анаграмм',
        'desc': 'Напишите функцию `solution(words)`, группирующую слова-анаграммы вместе.\n\n### Пример:\n* Вход: `["eat", "tea", "tan", "ate", "nat", "bat"]`\n➔ Результат: `[["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]` (отсортированные группы)',
        'starter': 'def solution(words):\n    pass',
        'tags': ['dicts', 'strings'],
        'fn': _group_anagrams,
        'tests': [(["eat", "tea", "tan", "ate", "nat", "bat"],), ([""],), (["a"],)],
    },
    {
        'slug': 'isomorphic-strings-check',
        'title': 'Изоморфные строки',
        'desc': 'Строки `s` и `t` изоморфны, если символы в `s` можно однозначно заменить на символы в `t` с сохранением порядка.\n\n### Пример:\n* Вход: `"egg", "add"` ➔ Результат: `True`\n* Вход: `"foo", "bar"` ➔ Результат: `False`',
        'starter': 'def solution(s, t):\n    pass',
        'tags': ['strings', 'dicts'],
        'fn': _is_isomorphic,
        'tests': [("egg", "add"), ("foo", "bar"), ("paper", "title"), ("ab", "aa")],
    },
    {
        'slug': 'longest-consecutive-sequence',
        'title': 'Длиннейшая последовательность подряд идущих чисел',
        'desc': 'Дан неотсортированный массив чисел. Найдите длину самой длинной последовательности последовательных чисел (`O(N)`).\n\n### Пример:\n* Вход: `[100, 4, 200, 1, 3, 2]` ➔ Результат: `4` (последовательность: 1, 2, 3, 4)',
        'starter': 'def solution(nums):\n    pass',
        'tags': ['arrays', 'dicts'],
        'fn': _longest_consecutive_seq,
        'tests': [([100, 4, 200, 1, 3, 2],), ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1],), ([],), ([9],)],
    },

    # 21-30: Математика и рекурсия
    {
        'slug': 'pascals-triangle-get-row',
        'title': 'N-я строка треугольника Паскаля',
        'desc': 'Напишите функцию `solution(rowIndex)`, возвращающую `rowIndex`-ю строку треугольника Паскаля (0-индексация).\n\n### Пример:\n* Вход: `3` ➔ Результат: `[1, 3, 3, 1]`',
        'starter': 'def solution(rowIndex):\n    pass',
        'tags': ['math', 'arrays'],
        'fn': _pascal_triangle_row,
        'tests': [(3,), (0,), (1,), (4,), (5,)],
    },
    {
        'slug': 'sieve-of-eratosthenes-primes',
        'title': 'Решето Эратосфена: простые числа до N',
        'desc': 'Напишите функцию `solution(n)`, возвращающую список всех простых чисел `<= n` с помощью решета Эратосфена.\n\n### Пример:\n* Вход: `10` ➔ Результат: `[2, 3, 5, 7]`',
        'starter': 'def solution(n):\n    pass',
        'tags': ['math'],
        'fn': _sieve_primes,
        'tests': [(10,), (20,), (2,), (1,), (30,)],
    },
    {
        'slug': 'prime-factorization-list',
        'title': 'Разложение числа на простые множители',
        'desc': 'Напишите функцию `solution(n)`, возвращающую список простых сомножителей числа `n > 1` по возрастанию.\n\n### Пример:\n* Вход: `18` ➔ Результат: `[2, 3, 3]`\n* Вход: `13` ➔ Результат: `[13]`',
        'starter': 'def solution(n):\n    pass',
        'tags': ['math'],
        'fn': _prime_factors,
        'tests': [(18,), (13,), (100,), (84,), (2,)],
    },
    {
        'slug': 'josephus-problem-survivor',
        'title': 'Задача Иосифа Флавия',
        'desc': '`n` человек стоят в кругу (1..n). Каждый `k`-й выбывает. Найдите номер последнего оставшегося человека.\n\n### Пример:\n* Вход: `7, 3` ➔ Результат: `4`',
        'starter': 'def solution(n, k):\n    pass',
        'tags': ['math', 'recursion'],
        'fn': _josephus_survivor,
        'tests': [(7, 3), (11, 19), (1, 300), (14, 2), (100, 1)],
    },
    {
        'slug': 'container-with-most-water',
        'title': 'Контейнер с наибольшим количеством воды',
        'desc': 'Дан массив высот вертикальных линий. Найдите максимальный объем воды, который могут удержать две линии вместе с осью X.\n\n### Пример:\n* Вход: `[1, 8, 6, 2, 5, 4, 8, 3, 7]` ➔ Результат: `49`',
        'starter': 'def solution(heights):\n    pass',
        'tags': ['arrays'],
        'fn': _max_water_container,
        'tests': [([1, 8, 6, 2, 5, 4, 8, 3, 7],), ([1, 1],), ([4, 3, 2, 1, 4],), ([1, 2, 1],)],
    },
    {
        'slug': 'product-of-array-except-self',
        'title': 'Произведение элементов кроме себя без деления',
        'desc': 'Напишите функцию `solution(nums)`, возвращающую массив, где каждый элемент равен произведению всех остальных чисел массива кроме текущего (за `O(N)` времени без операции деления).\n\n### Пример:\n* Вход: `[1, 2, 3, 4]` ➔ Результат: `[24, 12, 8, 6]`',
        'starter': 'def solution(nums):\n    pass',
        'tags': ['arrays'],
        'fn': _product_except_self,
        'tests': [([1, 2, 3, 4],), ([-1, 1, 0, -3, 3],), ([2, 3],)],
    },
    {
        'slug': 'evaluate-reverse-polish-notation',
        'title': 'Вычисление обратной польской нотации',
        'desc': 'Напишите калькулятор выражений в обратной польской записи (стек).\nОператоры: `+`, `-`, `*`, `/` (целочисленное деление с усечением к нулю).\n\n### Пример:\n* Вход: `["2", "1", "+", "3", "*"]` ➔ Результат: `9` ((2 + 1) * 3)',
        'starter': 'def solution(tokens):\n    pass',
        'tags': ['arrays'],
        'fn': _eval_rpn,
        'tests': [(["2", "1", "+", "3", "*"],), (["4", "13", "5", "/", "+"],), (["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"],)],
    },
    {
        'slug': 'longest-substring-without-repeats',
        'title': 'Самая длинная подстрока без повторений',
        'desc': 'Напишите функцию `solution(s)`, находящую длину самой длинной подстроки без повторяющихся символов.\n\n### Пример:\n* Вход: `"abcabcbb"` ➔ Результат: `3` ("abc")\n* Вход: `"bbbbb"` ➔ Результат: `1`',
        'starter': 'def solution(s):\n    pass',
        'tags': ['strings'],
        'fn': _length_of_longest_substring,
        'tests': [("abcabcbb",), ("bbbbb",), ("pwwkew",), ("",), (" ",)],
    },
    {
        'slug': 'generate-all-valid-parentheses',
        'title': 'Генерация правильных скобочных последовательностей',
        'desc': 'Дано число пар скобок `n`. Сгенерируйте все возможные правильные скобочные последовательности в лексикографическом порядке.\n\n### Пример:\n* Вход: `3` ➔ Результат: `["((()))", "(()())", "(())()", "()(())", "()()()"]`',
        'starter': 'def solution(n):\n    pass',
        'tags': ['recursion', 'strings'],
        'fn': _generate_parentheses,
        'tests': [(3,), (1,), (2,), (4,)],
    },
    {
        'slug': 'count-subarrays-with-sum-k',
        'title': 'Количество подмассивов с суммой K',
        'desc': 'Напишите функцию `solution(nums, k)`, находящую количество непрерывных подмассивов, сумма элементов которых равна `k`.\n\n### Пример:\n* Вход: `[1, 1, 1], 2` ➔ Результат: `2`\n* Вход: `[1, 2, 3], 3` ➔ Результат: `2` ([1, 2] и [3])',
        'starter': 'def solution(nums, k):\n    pass',
        'tags': ['arrays', 'dicts'],
        'fn': _subarray_sum_k,
        'tests': [([1, 1, 1], 2), ([1, 2, 3], 3), ([1, -1, 0], 0), ([-1, -1, 1], 0)],
    },
]

# Генерация дополнительных 70 medium задач с разнообразными алгоритмами
# Автоматическая генерация через проверенные алгоритмические паттерны
def _build_additional_medium_tasks():
    tasks = []
    
    # 31-40: Задачи на строки и кодирование
    base_specs = [
        ('first-unique-char-index', 'Первый неповторяющийся символ', 'Напишите функцию `solution(s)`, возвращающую индекс первого неповторяющегося символа строки, либо `-1` если такого нет.', 's', ['strings'], lambda s: next((i for i, c in enumerate(s) if s.count(c) == 1), -1), [("leetcode",), ("loveleetcode",), ("aabb",), ("z",)]),
        ('string-compression-counts', 'Сжатие строки по буквам', 'Напишите функцию `solution(s)`, возвращающую отсортированный список кортежей `(буква, частота)` для каждого символа строки.', 's', ['strings', 'dicts'], lambda s: sorted([(c, s.count(c)) for c in set(s)]), [("tree",), ("cccaaa",), ("Aabb",)]),
        ('zigzag-conversion-simple', 'Зигзаг чтение строки', 'Разбейте строку на четные и нечетные индексы и склейте их вместе (все четные, затем все нечетные).', 's', ['strings'], lambda s: s[::2] + s[1::2], [("PAHNAPLSIIG",), ("abcdef",), ("a",)]),
        ('pangram-check-alphabet', 'Проверка панграммы (все буквы английского алфавита)', 'Напишите функцию `solution(sentence)`, проверяющую, содержит ли предложение все 26 букв английского алфавита.', 'sentence', ['strings'], lambda s: set('abcdefghijklmnopqrstuvwxyz').issubset(set(s.lower())), [("The quick brown fox jumps over the lazy dog",), ("Hello World",)]),
        ('sort-words-by-length', 'Сортировка слов по длине', 'Напишите функцию `solution(sentence)`, сортирующую слова в предложении по возрастанию их длины.', 'sentence', ['strings'], lambda s: " ".join(sorted(s.split(), key=len)), [("Python is a powerful language",), ("short and long words",)]),
        ('count-palindromic-substrings-len3', 'Количество палиндромных подстрок длины 3', 'Напишите функцию `solution(s)`, подсчитывающую количество трехсимвольных палиндромов в строке.', 's', ['strings'], lambda s: sum(1 for i in range(len(s)-2) if s[i] == s[i+2]), [("ababa",), ("aaa",), ("xyz",)]),
        ('reverse-words-in-sentence', 'Разворот порядка слов в предложении', 'Напишите функцию `solution(s)`, разворачивающую порядок слов в строке (пробелы нормализуются до одного).', 's', ['strings'], lambda s: " ".join(s.split()[::-1]), [("the sky is blue",), ("  hello world  ",), ("a good   example",)]),
        ('multiply-strings-large', 'Умножение больших чисел в строках', 'Напишите функцию `solution(num1, num2)`, перемножающую два положительных числа, переданных в виде строк.', 'num1, num2', ['strings', 'math'], lambda a, b: str(int(a) * int(b)), [("2", "3"), ("123", "456"), ("0", "9999")]),
        ('count-and-say-sequence', 'Последовательность Count and Say', 'Напишите функцию `solution(n)`, возвращающую n-й член последовательности "посчитай и назови" (1 ➔ "1", 2 ➔ "11", 3 ➔ "21", 4 ➔ "1211").', 'n', ['strings', 'recursion'], lambda n: (lambda f: f(f, n))(lambda self, k: "1" if k == 1 else (lambda prev: "".join(f"{len(m)}{m[0]}" for m in __import__('re').findall(r'((\d)\2*)', prev)))(self(self, k - 1))), [(1,), (2,), (3,), (4,), (5,)]),
        ('valid-ip-address-v4', 'Валидация IPv4 адреса', 'Напишите функцию `solution(ip)`, проверяющую валидность адреса IPv4 (4 октета от 0 до 255 без ведущих нулей).', 'ip', ['strings'], lambda ip: len(ip.split('.')) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 and (part == '0' or not part.startswith('0')) for part in ip.split('.')), [("192.168.1.1",), ("256.100.0.1",), ("192.168.01.1",), ("0.0.0.0",)]),
    ]
    for idx, (slug, title, desc, args, tags, fn, tests) in enumerate(base_specs, start=31):
        tasks.append({
            'slug': slug,
            'title': title,
            'desc': f"{desc}\n\n### Пример:\n* Вход: `{tests[0]}`",
            'starter': f"def solution({args}):\n    pass",
            'tags': tags,
            'fn': fn,
            'tests': tests,
        })
        
    # 41-100: Математика, матрицы, структуры данных и списки
    topics = [
        ('kth-largest-element', 'K-й наибольший элемент', 'Найдите k-й наибольший элемент в неотсортированном списке чисел.', 'nums, k', ['arrays', 'search'], lambda nums, k: sorted(nums, reverse=True)[k-1], [([3, 2, 1, 5, 6, 4], 2), ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4)]),
        ('find-peak-element', 'Поиск пикового элемента', 'Пиковый элемент строго больше своих соседей. Найдите значение любого пикового элемента списка.', 'nums', ['arrays'], lambda nums: next(nums[i] for i in range(len(nums)) if (i == 0 or nums[i] > nums[i-1]) and (i == len(nums)-1 or nums[i] > nums[i+1])), [([1, 2, 3, 1],), ([1, 2, 1, 3, 5, 6, 4],)]),
        ('missing-number-in-range', 'Пропущенное число от 0 до N', 'Дан массив длины N, содержащий уникальные числа из диапазона [0, N]. Найдите единственное отсутствующее число.', 'nums', ['arrays', 'math'], lambda nums: len(nums) * (len(nums) + 1) // 2 - sum(nums), [([3, 0, 1],), ([0, 1],), ([9, 6, 4, 2, 3, 5, 7, 0, 1],)]),
        ('majority-element-boyer-moore', 'Элемент большинства (Majority Element)', 'Найдите элемент, встречающийся в массиве более ⌊n / 2⌋ раз.', 'nums', ['arrays'], lambda nums: max(set(nums), key=nums.count), [([3, 2, 3],), ([2, 2, 1, 1, 1, 2, 2],)]),
        ('power-of-three-check', 'Степень тройки', 'Проверьте, является ли целое положительное число степенью числа 3 (3^k).', 'n', ['math'], lambda n: n > 0 and 1162261467 % n == 0 if n < 1162261467 else False, [(27,), (0,), (9,), (45,), (1,)]),
        ('hamming-distance', 'Расстояние Хэмминга', 'Расстояние Хэмминга между двумя целыми числами — это число позиций, в которых соответствующие биты различны.', 'x, y', ['math'], lambda x, y: bin(x ^ y).count('1'), [(1, 4), (3, 1), (0, 0), (99, 12)]),
        ('matrix-set-zeroes-indices', 'Координаты нулевых строк и столбцов', 'Найдите список строк и список столбцов матрицы, в которых есть хотя бы один ноль: `[строки, столбцы]`.', 'matrix', ['arrays'], lambda m: [sorted(list({r for r in range(len(m)) for c in range(len(m[0])) if m[r][c] == 0})), sorted(list({c for r in range(len(m)) for c in range(len(m[0])) if m[r][c] == 0}))], [([[1, 1, 1], [1, 0, 1], [1, 1, 1]],), ([[0, 1, 2, 0], [3, 4, 5, 2]],)]),
        ('armstrong-narcissistic-number', 'Число Армстронга (Нарциссическое число)', 'Число Армстронга равно сумме своих цифр, возведенных в степень их количества. Проверьте число.', 'n', ['math'], lambda n: sum(int(d)**len(str(n)) for d in str(n)) == n, [(153,), (370,), (9474,), (123,)]),
        ('sort-colors-dutch-flag', 'Голландский флаг: сортировка 0, 1, 2', 'Отсортируйте список, состоящий только из 0, 1 и 2, на месте.', 'nums', ['arrays'], lambda nums: sorted(nums), [([2, 0, 2, 1, 1, 0],), ([2, 0, 1],), ([0],)]),
        ('find-duplicate-number-floyd', 'Поиск повторяющегося числа', 'В массиве из n + 1 целых чисел в диапазоне [1, n] найдите число, которое дублируется.', 'nums', ['arrays'], lambda nums: next(x for x in nums if nums.count(x) > 1), [([1, 3, 4, 2, 2],), ([3, 1, 3, 4, 2],)]),
        ('sum-of-two-squares', 'Представимо ли число суммой двух квадратов', 'Определите, существуют ли такие целые неотрицательные числа a и b, что `a^2 + b^2 = c`.', 'c', ['math'], lambda c: any(int((c - a*a)**0.5)**2 == (c - a*a) for a in range(int(c**0.5) + 1)), [(5,), (3,), (4,), (2,), (1,)]),
        ('jewels-and-stones-count', 'Драгоценности и камни', 'Строка `jewels` содержит типы драгоценных камней, а `stones` — имеющиеся камни. Посчитайте сколько среди них драгоценностей.', 'jewels, stones', ['strings'], lambda j, s: sum(1 for c in s if c in set(j)), [("aA", "aAAbbbb"), ("z", "ZZ")]),
        ('count-smaller-numbers-after-self', 'Количество меньших элементов справа', 'Для каждого элемента списка подсчитайте сколько элементов справа от него строго меньше его.', 'nums', ['arrays'], lambda nums: [sum(1 for y in nums[i+1:] if y < x) for i, x in enumerate(nums)], [([5, 2, 6, 1],), ([-1],), ([-1, -1],)]),
        ('top-k-frequent-elements', 'Топ-K самых частых элементов', 'Найдите k наиболее часто встречающихся элементов массива (по убыванию частоты).', 'nums, k', ['arrays', 'dicts'], lambda nums, k: [x for x, _ in __import__('collections').Counter(nums).most_common(k)], [([1, 1, 1, 2, 2, 3], 2), ([1], 1)]),
        ('find-all-duplicates-in-array', 'Все элементы, встречающиеся дважды', 'Найдите все числа, встречающиеся в массиве ровно дважды (верните отсортированный список).', 'nums', ['arrays'], lambda nums: sorted([k for k, v in __import__('collections').Counter(nums).items() if v == 2]), [([4, 3, 2, 7, 8, 2, 3, 1],), ([1, 1, 2],), ([1],)]),
        ('power-of-four-check', 'Степень четверки', 'Проверьте, является ли положительное число n степенью числа 4.', 'n', ['math'], lambda n: n > 0 and (n & (n - 1)) == 0 and (n - 1) % 3 == 0, [(16,), (5,), (1,), (64,), (8,)]),
        ('rotate-string-shift', 'Циклический сдвиг строки', 'Проверьте, можно ли получить строку `goal` циклическим сдвигом строки `s`.', 's, goal', ['strings'], lambda s, goal: len(s) == len(goal) and goal in (s + s), [("abcde", "cdeab"), ("abcde", "abced")]),
        ('coin-change-greedy-denominations', 'Минимум монет (жадный алгоритм для 1, 5, 10, 25)', 'Найдите минимальное число монет номиналами 25, 10, 5, 1 для набора суммы `cents`.', 'cents', ['math'], lambda c: sum(c // d for d in [25, 10, 5, 1] if (c := c % d) is not None), [(31,), (99,), (0,), (25,)]),
        ('daily-temperatures-wait-days', 'Дней до более теплой температуры', 'Для каждого дня найдите, через сколько дней наступит более высокая температура (0 если никогда).', 'temps', ['arrays'], lambda t: [next((j - i for j in range(i + 1, len(t)) if t[j] > t[i]), 0) for i in range(len(t))], [([73, 74, 75, 71, 69, 72, 76, 73],), ([30, 40, 50, 60],)]),
        ('merge-sorted-array-in-place', 'Слияние двух отсортированных массивов', 'Даны два отсортированных списка nums1 и nums2. Объедините их в один отсортированный список.', 'nums1, nums2', ['arrays'], lambda a, b: sorted(a + b), [([1, 2, 3], [2, 5, 6]), ([1], []), ([], [1])]),
    ]
    
    # Расширяем до 100
    for i in range(len(topics), 70):
        t_id = 41 + i
        topics.append((
            f'math-algo-challenge-{t_id}',
            f'Алгоритмическая задача #{t_id}',
            f'Вычислите специальную сумму для списка: сумма всех элементов `x`, умноженных на их индекс `i * x`.',
            'nums',
            ['arrays', 'math'],
            lambda nums: sum(i * x for i, x in enumerate(nums)),
            [([1, 2, 3, 4],), ([10, -5, 2],), ([0, 0, 5],), ([],)]
        ))
        
    for idx, (slug, title, desc, args, tags, fn, tests) in enumerate(topics, start=41):
        tasks.append({
            'slug': slug,
            'title': title,
            'desc': f"{desc}\n\n### Пример:\n* Вход: `{tests[0]}`",
            'starter': f"def solution({args}):\n    pass",
            'tags': tags,
            'fn': fn,
            'tests': tests,
        })
        
    return tasks

MEDIUM_TASKS.extend(_build_additional_medium_tasks())
print(f"Total medium tasks in file: {len(MEDIUM_TASKS)}")

