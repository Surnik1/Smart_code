# -*- coding: utf-8 -*-
"""
Добавление 25 классических задач уровня Easy из LeetCode и Codewars в базу данных Smart Code.
"""
import os
import sys
import django

sys.path.append('d:/Smart_code')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import transaction
from challenges.models import Task, Tag, TestCase
from challenges.services.runner import parse_test_inputs, CodeRunnerService

# Чистые функции решения для каждой задачи
def fn_two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        diff = target - x
        if diff in seen:
            return [seen[diff], i]
        seen[x] = i
    return []

def fn_valid_palindrome(s):
    clean = [c.lower() for c in s if c.isalnum()]
    return clean == clean[::-1]

def fn_roman_to_int(s):
    vals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    prev = 0
    for c in reversed(s):
        curr = vals.get(c, 0)
        if curr >= prev:
            total += curr
        else:
            total -= curr
        prev = curr
    return total

def fn_longest_common_prefix(strs):
    if not strs:
        return ""
    prefix = strs[0]
    for s in strs[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix

def fn_valid_parentheses(s):
    m = {')': '(', '}': '{', ']': '['}
    stack = []
    for c in s:
        if c in m.values():
            stack.append(c)
        elif c in m:
            if not stack or stack.pop() != m[c]:
                return False
    return len(stack) == 0

def fn_merge_sorted_lists(l1, l2):
    return sorted(l1 + l2)

def fn_remove_duplicates(nums):
    return sorted(list(set(nums)))

def fn_str_str(h, n):
    return h.find(n)

def fn_search_insert(nums, target):
    import bisect
    return bisect.bisect_left(nums, target)

def fn_length_last_word(s):
    words = s.split()
    return len(words[-1]) if words else 0

def fn_plus_one(digits):
    num = int(''.join(map(str, digits))) + 1
    return [int(d) for d in str(num)]

def fn_add_binary(a, b):
    return bin(int(a, 2) + int(b, 2))[2:]

def fn_sqrtx(x):
    return int(x ** 0.5)

def fn_climbing_stairs(n):
    if n <= 1:
        return 1
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

def fn_single_number(nums):
    res = 0
    for x in nums:
        res ^= x
    return res

def fn_majority_element(nums):
    return sorted(nums)[len(nums) // 2]

def fn_isomorphic(s, t):
    return len(set(zip(s, t))) == len(set(s)) == len(set(t)) and len(s) == len(t)

def fn_contains_duplicate(nums):
    return len(nums) != len(set(nums))

def fn_valid_anagram(s, t):
    return sorted(s) == sorted(t)

def fn_missing_number(nums):
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)

def fn_move_zeroes(nums):
    non_zeros = [x for x in nums if x != 0]
    return non_zeros + [0] * (len(nums) - len(non_zeros))

def fn_vowel_count(s):
    return sum(1 for c in s.lower() if c in 'aeiou')

def fn_disemvowel(s):
    return ''.join(c for c in s if c not in 'aeiouAEIOU')

def fn_square_digits(num):
    return int(''.join(str(int(d)**2) for d in str(num)))

def fn_descending_order(num):
    return int(''.join(sorted(str(num), reverse=True)))


# 25 задач
TASKS_25 = [
    # 1. Two Sum (LeetCode #1)
    {
        'slug': 'leetcode-two-sum',
        'title': 'Two Sum (LeetCode #1)',
        'desc': (
            "### Условие задачи (LeetCode #1 — Two Sum)\n\n"
            "Дан список целых чисел `nums` и целое число `target`. Найдите **индексы** двух чисел таких, "
            "что их сумма равна `target`.\n\n"
            "Гарантируется, что существует ровно одно решение. Нельзя использовать один и тот же элемент дважды.\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: nums = [2, 7, 11, 15], target = 9\n"
            "Выход: [0, 1] # так как nums[0] + nums[1] == 2 + 7 == 9\n"
            "```\n\n"
            "### Пример 2:\n"
            "```python\n"
            "Вход: nums = [3, 2, 4], target = 6\n"
            "Выход: [1, 2]\n"
            "```"
        ),
        'starter': "def solution(nums, target):\n    # Верните список из двух индексов\n    pass",
        'tags': ['arrays', 'search'],
        'fn': fn_two_sum,
        'tests': [
            ([2, 7, 11, 15], 9),
            ([3, 2, 4], 6),
            ([3, 3], 6),
            ([1, 5, 8, 12], 20),
            ([-1, -2, -3, -4, -5], -8),
        ]
    },

    # 2. Valid Palindrome (LeetCode #125)
    {
        'slug': 'leetcode-valid-palindrome',
        'title': 'Valid Palindrome (LeetCode #125)',
        'desc': (
            "### Условие задачи (LeetCode #125 — Valid Palindrome)\n\n"
            "Фраза является палиндромом, если после преобразования всех заглавных букв в строчные и "
            "удаления всех не буквенно-цифровых символов она читается одинаково вперед и назад.\n\n"
            "Напишите функцию `solution(s)`, возвращающую `True`, если строка является палиндромом, и `False` иначе.\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: s = \"A man, a plan, a canal: Panama\"\n"
            "Выход: True # \"amanaplanacanalpanama\"\n"
            "```"
        ),
        'starter': "def solution(s):\n    pass",
        'tags': ['strings'],
        'fn': fn_valid_palindrome,
        'tests': [
            ("A man, a plan, a canal: Panama",),
            ("race a car",),
            (" ",),
            ("0P",),
            ("No 'x' in Nixon",),
        ]
    },

    # 3. Roman to Integer (LeetCode #13)
    {
        'slug': 'leetcode-roman-to-integer',
        'title': 'Roman to Integer (LeetCode #13)',
        'desc': (
            "### Условие задачи (LeetCode #13 — Roman to Integer)\n\n"
            "Римские цифры обозначаются символами: `I` (1), `V` (5), `X` (10), `L` (50), `C` (100), `D` (500), `M` (1000).\n\n"
            "Переведите переданную римскую запись `s` в арабское число (`int`).\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: s = \"III\" ➔ Выход: 3\n"
            "Вход: s = \"LVIII\" ➔ Выход: 58\n"
            "Вход: s = \"MCMXCIV\" ➔ Выход: 1994\n"
            "```"
        ),
        'starter': "def solution(s):\n    pass",
        'tags': ['math', 'strings'],
        'fn': fn_roman_to_int,
        'tests': [
            ("III",),
            ("LVIII",),
            ("MCMXCIV",),
            ("IX",),
            ("XL",),
        ]
    },

    # 4. Longest Common Prefix (LeetCode #14)
    {
        'slug': 'leetcode-longest-common-prefix',
        'title': 'Longest Common Prefix (LeetCode #14)',
        'desc': (
            "### Условие задачи (LeetCode #14 — Longest Common Prefix)\n\n"
            "Напишите функцию `solution(strs)`, находящую самый длинный общий префикс среди массива строк.\n"
            "Если общего префикса нет, верните пустую строку `\"\"`.\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: strs = [\"flower\",\"flow\",\"flight\"]\n"
            "Выход: \"fl\"\n"
            "```"
        ),
        'starter': "def solution(strs):\n    pass",
        'tags': ['strings'],
        'fn': fn_longest_common_prefix,
        'tests': [
            (["flower", "flow", "flight"],),
            (["dog", "racecar", "car"],),
            (["interspecies", "interstellar", "interstate"],),
            (["throne", "throne"],),
            (["a"],),
        ]
    },

    # 5. Valid Parentheses (LeetCode #20)
    {
        'slug': 'leetcode-valid-parentheses',
        'title': 'Valid Parentheses (LeetCode #20)',
        'desc': (
            "### Условие задачи (LeetCode #20 — Valid Parentheses)\n\n"
            "Дана строка `s`, содержащая скобки `'('`, `')'`, `'{'`, `'}'`, `'['` и `']'`.\n"
            "Определите, является ли входная строка правильной:\n"
            "1. Открытые скобки должны закрываться скобками того же типа.\n"
            "2. Скобки должны закрываться в правильном порядке.\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: s = \"()[]{}\" ➔ Выход: True\n"
            "Вход: s = \"(]\" ➔ Выход: False\n"
            "Вход: s = \"([{}])\" ➔ Выход: True\n"
            "```"
        ),
        'starter': "def solution(s):\n    pass",
        'tags': ['strings'],
        'fn': fn_valid_parentheses,
        'tests': [
            ("()[]{}",),
            ("(]",),
            ("([{}])",),
            ("((",),
            ("{[]}",),
            ("",),
        ]
    },

    # 6. Merge Two Sorted Lists (LeetCode #21)
    {
        'slug': 'leetcode-merge-two-sorted-lists',
        'title': 'Merge Two Sorted Lists (LeetCode #21)',
        'desc': (
            "### Условие задачи (LeetCode #21 — Merge Two Sorted Lists)\n\n"
            "Вам даны два отсортированных по возрастанию списка чисел `list1` и `list2`.\n"
            "Объедините их в один отсортированный список и верните его.\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: list1 = [1, 2, 4], list2 = [1, 3, 4]\n"
            "Выход: [1, 1, 2, 3, 4, 4]\n"
            "```"
        ),
        'starter': "def solution(list1, list2):\n    pass",
        'tags': ['arrays', 'basics'],
        'fn': fn_merge_sorted_lists,
        'tests': [
            ([1, 2, 4], [1, 3, 4]),
            ([], []),
            ([], [0]),
            ([5, 10, 15], [2, 3, 20]),
        ]
    },

    # 7. Remove Duplicates from Sorted Array (LeetCode #26)
    {
        'slug': 'leetcode-remove-duplicates',
        'title': 'Remove Duplicates from Sorted Array (LeetCode #26)',
        'desc': (
            "### Условие задачи (LeetCode #26 — Remove Duplicates)\n\n"
            "Дан отсортированный массив `nums`. Удалите дубликаты так, чтобы каждый уникальный элемент "
            "появлялся только один раз. Верните новый отсортированный список уникальных элементов.\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: nums = [1, 1, 2]\n"
            "Выход: [1, 2]\n"
            "Вход: nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]\n"
            "Выход: [0, 1, 2, 3, 4]\n"
            "```"
        ),
        'starter': "def solution(nums):\n    pass",
        'tags': ['arrays'],
        'fn': fn_remove_duplicates,
        'tests': [
            ([1, 1, 2],),
            ([0, 0, 1, 1, 1, 2, 2, 3, 3, 4],),
            ([1],),
            ([],),
        ]
    },

    # 8. Find the Index of the First Occurrence (LeetCode #28 - strStr)
    {
        'slug': 'leetcode-find-needle-in-haystack',
        'title': 'Find the Index of the First Occurrence (LeetCode #28)',
        'desc': (
            "### Условие задачи (LeetCode #28 — strStr)\n\n"
            "Даны две строки `haystack` и `needle`. Верните индекс первого вхождения строки `needle` "
            "в `haystack`, или `-1`, если `needle` не является частью `haystack`.\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: haystack = \"sadbutsad\", needle = \"sad\"\n"
            "Выход: 0\n"
            "```"
        ),
        'starter': "def solution(haystack, needle):\n    pass",
        'tags': ['strings', 'search'],
        'fn': fn_str_str,
        'tests': [
            ("sadbutsad", "sad"),
            ("leetcode", "leeto"),
            ("hello", "ll"),
            ("mississippi", "issip"),
        ]
    },

    # 9. Search Insert Position (LeetCode #35)
    {
        'slug': 'leetcode-search-insert-position',
        'title': 'Search Insert Position (LeetCode #35)',
        'desc': (
            "### Условие задачи (LeetCode #35 — Search Insert Position)\n\n"
            "Дан отсортированный массив различных целых чисел `nums` и число `target`.\n"
            "Верните индекс `target`, если он найден. Если нет, верните индекс, на котором он должен был бы "
            "находиться при упорядоченной вставке.\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: nums = [1, 3, 5, 6], target = 5 ➔ Выход: 2\n"
            "Вход: nums = [1, 3, 5, 6], target = 2 ➔ Выход: 1\n"
            "Вход: nums = [1, 3, 5, 6], target = 7 ➔ Выход: 4\n"
            "```"
        ),
        'starter': "def solution(nums, target):\n    pass",
        'tags': ['arrays', 'search'],
        'fn': fn_search_insert,
        'tests': [
            ([1, 3, 5, 6], 5),
            ([1, 3, 5, 6], 2),
            ([1, 3, 5, 6], 7),
            ([1, 3, 5, 6], 0),
        ]
    },

    # 10. Length of Last Word (LeetCode #58)
    {
        'slug': 'leetcode-length-of-last-word',
        'title': 'Length of Last Word (LeetCode #58)',
        'desc': (
            "### Условие задачи (LeetCode #58 — Length of Last Word)\n\n"
            "Дана строка `s`, состоящая из слов и пробелов. Верните длину последнего слова в строке.\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: s = \"Hello World\" ➔ Выход: 5\n"
            "Вход: s = \"   fly me   to   the moon  \" ➔ Выход: 4\n"
            "Вход: s = \"luffy is still joyboy\" ➔ Выход: 6\n"
            "```"
        ),
        'starter': "def solution(s):\n    pass",
        'tags': ['strings'],
        'fn': fn_length_last_word,
        'tests': [
            ("Hello World",),
            ("   fly me   to   the moon  ",),
            ("luffy is still joyboy",),
            ("a",),
        ]
    },

    # 11. Plus One (LeetCode #66)
    {
        'slug': 'leetcode-plus-one',
        'title': 'Plus One (LeetCode #66)',
        'desc': (
            "### Условие задачи (LeetCode #66 — Plus One)\n\n"
            "Вам дано большое целое неотрицательное число, представленное списком его цифр `digits`.\n"
            "Прибавьте к этому числу `1` и верните результирующий список цифр.\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: digits = [1, 2, 3] ➔ Выход: [1, 2, 4] # (123 + 1 = 124)\n"
            "Вход: digits = [9] ➔ Выход: [1, 0] # (9 + 1 = 10)\n"
            "```"
        ),
        'starter': "def solution(digits):\n    pass",
        'tags': ['arrays', 'math'],
        'fn': fn_plus_one,
        'tests': [
            ([1, 2, 3],),
            ([4, 3, 2, 1],),
            ([9],),
            ([9, 9, 9],),
        ]
    },

    # 12. Add Binary (LeetCode #67)
    {
        'slug': 'leetcode-add-binary',
        'title': 'Add Binary (LeetCode #67)',
        'desc': (
            "### Условие задачи (LeetCode #67 — Add Binary)\n\n"
            "Даны две двоичные строки `a` и `b`. Верните их сумму также в виде двоичной строки.\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: a = \"11\", b = \"1\" ➔ Выход: \"100\"\n"
            "Вход: a = \"1010\", b = \"1011\" ➔ Выход: \"10101\"\n"
            "```"
        ),
        'starter': "def solution(a, b):\n    pass",
        'tags': ['math', 'strings'],
        'fn': fn_add_binary,
        'tests': [
            ("11", "1"),
            ("1010", "1011"),
            ("0", "0"),
            ("1111", "1111"),
        ]
    },

    # 13. Sqrt(x) (LeetCode #69)
    {
        'slug': 'leetcode-sqrtx',
        'title': 'Sqrt(x) (LeetCode #69)',
        'desc': (
            "### Условие задачи (LeetCode #69 — Sqrt(x))\n\n"
            "Дано неотрицательное целое число `x`. Вычислите и верните целочисленный квадратный корень из `x` "
            "(дробная часть отбрасывается).\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: x = 4 ➔ Выход: 2\n"
            "Вход: x = 8 ➔ Выход: 2 # (sqrt(8) ≈ 2.82842...)\n"
            "```"
        ),
        'starter': "def solution(x):\n    pass",
        'tags': ['math'],
        'fn': fn_sqrtx,
        'tests': [
            (4,),
            (8,),
            (0,),
            (1,),
            (25,),
            (1000000,),
        ]
    },

    # 14. Climbing Stairs (LeetCode #70)
    {
        'slug': 'leetcode-climbing-stairs',
        'title': 'Climbing Stairs (LeetCode #70)',
        'desc': (
            "### Условие задачи (LeetCode #70 — Climbing Stairs)\n\n"
            "Вы поднимаетесь по лестнице из `n` ступенек. Каждый раз вы можете подняться на `1` или на `2` ступеньки.\n"
            "Сколькими различными способами вы можете подняться на вершину?\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: n = 2 ➔ Выход: 2 (1+1 или 2)\n"
            "Вход: n = 3 ➔ Выход: 3 (1+1+1, 1+2, 2+1)\n"
            "```"
        ),
        'starter': "def solution(n):\n    pass",
        'tags': ['math', 'dp'],
        'fn': fn_climbing_stairs,
        'tests': [
            (2,),
            (3,),
            (1,),
            (5,),
            (10,),
        ]
    },

    # 15. Single Number (LeetCode #136)
    {
        'slug': 'leetcode-single-number',
        'title': 'Single Number (LeetCode #136)',
        'desc': (
            "### Условие задачи (LeetCode #136 — Single Number)\n\n"
            "Дан непустой массив целых чисел `nums`. Каждый элемент повторяется дважды, кроме одного.\n"
            "Найдите этот единственный неповторяющийся элемент.\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: nums = [2, 2, 1] ➔ Выход: 1\n"
            "Вход: nums = [4, 1, 2, 1, 2] ➔ Выход: 4\n"
            "```"
        ),
        'starter': "def solution(nums):\n    pass",
        'tags': ['arrays'],
        'fn': fn_single_number,
        'tests': [
            ([2, 2, 1],),
            ([4, 1, 2, 1, 2],),
            ([1],),
            ([-1, -1, -2],),
        ]
    },

    # 16. Majority Element (LeetCode #169)
    {
        'slug': 'leetcode-majority-element',
        'title': 'Majority Element (LeetCode #169)',
        'desc': (
            "### Условие задачи (LeetCode #169 — Majority Element)\n\n"
            "Дан массив `nums` размера `n`. Найдите мажоритарный элемент — элемент, который встречается "
            "строго более чем `⌊n / 2⌋` раз. Гарантируется, что такой элемент всегда существует.\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: nums = [3, 2, 3] ➔ Выход: 3\n"
            "Вход: nums = [2, 2, 1, 1, 1, 2, 2] ➔ Выход: 2\n"
            "```"
        ),
        'starter': "def solution(nums):\n    pass",
        'tags': ['arrays'],
        'fn': fn_majority_element,
        'tests': [
            ([3, 2, 3],),
            ([2, 2, 1, 1, 1, 2, 2],),
            ([1],),
            ([6, 5, 5],),
        ]
    },

    # 17. Isomorphic Strings (LeetCode #205)
    {
        'slug': 'leetcode-isomorphic-strings',
        'title': 'Isomorphic Strings (LeetCode #205)',
        'desc': (
            "### Условие задачи (LeetCode #205 — Isomorphic Strings)\n\n"
            "Две строки `s` и `t` изоморфны, если символы в `s` можно заменить для получения `t`.\n"
            "Все вхождения одного символа должны заменяться на другой символ с сохранением порядка.\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: s = \"egg\", t = \"add\" ➔ Выход: True\n"
            "Вход: s = \"foo\", t = \"bar\" ➔ Выход: False\n"
            "Вход: s = \"paper\", t = \"title\" ➔ Выход: True\n"
            "```"
        ),
        'starter': "def solution(s, t):\n    pass",
        'tags': ['strings', 'dicts'],
        'fn': fn_isomorphic,
        'tests': [
            ("egg", "add"),
            ("foo", "bar"),
            ("paper", "title"),
            ("badc", "baba"),
        ]
    },

    # 18. Contains Duplicate (LeetCode #217)
    {
        'slug': 'leetcode-contains-duplicate',
        'title': 'Contains Duplicate (LeetCode #217)',
        'desc': (
            "### Условие задачи (LeetCode #217 — Contains Duplicate)\n\n"
            "Дан целочисленный список `nums`. Верните `True`, если хотя бы одно значение встречается "
            "в массиве минимум два раза, и `False`, если все элементы уникальны.\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: nums = [1, 2, 3, 1] ➔ Выход: True\n"
            "Вход: nums = [1, 2, 3, 4] ➔ Выход: False\n"
            "```"
        ),
        'starter': "def solution(nums):\n    pass",
        'tags': ['arrays', 'dicts'],
        'fn': fn_contains_duplicate,
        'tests': [
            ([1, 2, 3, 1],),
            ([1, 2, 3, 4],),
            ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2],),
            ([],),
        ]
    },

    # 19. Valid Anagram (LeetCode #242)
    {
        'slug': 'leetcode-valid-anagram',
        'title': 'Valid Anagram (LeetCode #242)',
        'desc': (
            "### Условие задачи (LeetCode #242 — Valid Anagram)\n\n"
            "Анаграмма — это слово, полученное перестановкой букв другого слова.\n"
            "Напишите функцию `solution(s, t)`, возвращающую `True`, если строка `t` является анаграммой строки `s`.\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: s = \"anagram\", t = \"nagaram\" ➔ Выход: True\n"
            "Вход: s = \"rat\", t = \"car\" ➔ Выход: False\n"
            "```"
        ),
        'starter': "def solution(s, t):\n    pass",
        'tags': ['strings', 'dicts'],
        'fn': fn_valid_anagram,
        'tests': [
            ("anagram", "nagaram"),
            ("rat", "car"),
            ("a", "a"),
            ("ab", "a"),
        ]
    },

    # 20. Missing Number (LeetCode #268)
    {
        'slug': 'leetcode-missing-number',
        'title': 'Missing Number (LeetCode #268)',
        'desc': (
            "### Условие задачи (LeetCode #268 — Missing Number)\n\n"
            "Дан массив `nums`, содержащий `n` уникальных чисел из диапазона `[0, n]`.\n"
            "Найдите единственное число из этого диапазона, которого нет в массиве.\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: nums = [3, 0, 1] ➔ Выход: 2 (n = 3, диапазон [0, 3])\n"
            "Вход: nums = [0, 1] ➔ Выход: 2\n"
            "```"
        ),
        'starter': "def solution(nums):\n    pass",
        'tags': ['arrays', 'math'],
        'fn': fn_missing_number,
        'tests': [
            ([3, 0, 1],),
            ([0, 1],),
            ([9, 6, 4, 2, 3, 5, 7, 0, 1],),
            ([0],),
        ]
    },

    # 21. Move Zeroes (LeetCode #283)
    {
        'slug': 'leetcode-move-zeroes',
        'title': 'Move Zeroes (LeetCode #283)',
        'desc': (
            "### Условие задачи (LeetCode #283 — Move Zeroes)\n\n"
            "Дан массив чисел `nums`. Переместите все нули в конец массива, сохраняя относительный порядок "
            "ненулевых элементов. Верните измененный список.\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: nums = [0, 1, 0, 3, 12]\n"
            "Выход: [1, 3, 12, 0, 0]\n"
            "```"
        ),
        'starter': "def solution(nums):\n    pass",
        'tags': ['arrays'],
        'fn': fn_move_zeroes,
        'tests': [
            ([0, 1, 0, 3, 12],),
            ([0],),
            ([1, 2, 3],),
            ([0, 0, 1],),
        ]
    },

    # 22. Vowel Count (Codewars 7 kyu)
    {
        'slug': 'codewars-vowel-count',
        'title': 'Vowel Count (Codewars 7 kyu)',
        'desc': (
            "### Условие задачи (Codewars 7 kyu — Vowel Count)\n\n"
            "Верните количество (число) гласных английских букв (`a, e, i, o, u`) в заданной строке.\n"
            "Входная строка состоит только из строчных букв и пробелов.\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: s = \"abracadabra\" ➔ Выход: 5\n"
            "```"
        ),
        'starter': "def solution(s):\n    pass",
        'tags': ['strings'],
        'fn': fn_vowel_count,
        'tests': [
            ("abracadabra",),
            ("hello world",),
            ("xyz",),
            ("",),
        ]
    },

    # 23. Disemvowel Trolls (Codewars 7 kyu)
    {
        'slug': 'codewars-disemvowel-trolls',
        'title': 'Disemvowel Trolls (Codewars 7 kyu)',
        'desc': (
            "### Условие задачи (Codewars 7 kyu — Disemvowel Trolls)\n\n"
            "Тролли атакуют ваш сайт в комментариях! Напишите функцию `solution(string)`, "
            "которая удаляет все гласные буквы (`a, e, i, o, u`, как строчные, так и прописные) из строки комментария.\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: \"This website is for losers LOL!\"\n"
            "Выход: \"Ths wbst s fr lsrs LL!\"\n"
            "```"
        ),
        'starter': "def solution(string):\n    pass",
        'tags': ['strings'],
        'fn': fn_disemvowel,
        'tests': [
            ("This website is for losers LOL!",),
            ("No offense but,\nYour writing is among the worst",),
            ("What are you, a communist?",),
        ]
    },

    # 24. Square Every Digit (Codewars 7 kyu)
    {
        'slug': 'codewars-square-every-digit',
        'title': 'Square Every Digit (Codewars 7 kyu)',
        'desc': (
            "### Условие задачи (Codewars 7 kyu — Square Every Digit)\n\n"
            "Напишите функцию `solution(num)`, которая возводит в квадрат каждую цифру переданного целого числа "
            "и склеивает их в одно результирующее число (`int`).\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: num = 9119 ➔ Выход: 811181 (так как 9^2 = 81, 1^2 = 1, 1^2 = 1, 9^2 = 81)\n"
            "```"
        ),
        'starter': "def solution(num):\n    pass",
        'tags': ['math'],
        'fn': fn_square_digits,
        'tests': [
            (9119,),
            (0,),
            (123,),
            (765,),
        ]
    },

    # 25. Descending Order (Codewars 7 kyu)
    {
        'slug': 'codewars-descending-order',
        'title': 'Descending Order (Codewars 7 kyu)',
        'desc': (
            "### Условие задачи (Codewars 7 kyu — Descending Order)\n\n"
            "Напишите функцию `solution(num)`, которая принимает неотрицательное целое число и возвращает "
            "число, составленное из его цифр, отсортированных по убыванию.\n\n"
            "### Пример 1:\n"
            "```python\n"
            "Вход: num = 42145 ➔ Выход: 54421\n"
            "Вход: num = 145263 ➔ Выход: 654321\n"
            "Вход: num = 123456789 ➔ Выход: 987654321\n"
            "```"
        ),
        'starter': "def solution(num):\n    pass",
        'tags': ['math', 'basics'],
        'fn': fn_descending_order,
        'tests': [
            (42145,),
            (145263,),
            (123456789,),
            (0,),
        ]
    },
]

def add_tasks():
    print(f"Запуск добавления {len(TASKS_25)} классических задач LeetCode & Codewars...")
    
    # 1. Проверяем наличие необходимых тегов
    tag_map = {}
    for t in Tag.objects.all():
        tag_map[t.slug] = t

    added_count = 0
    with transaction.atomic():
        for task_info in TASKS_25:
            slug = task_info['slug']
            title = task_info['title']
            desc = task_info['desc']
            starter = task_info['starter']
            tags_slugs = task_info['tags']
            fn = task_info['fn']
            tests = task_info['tests']

            # Создаем или обновляем задачу
            task, created = Task.objects.update_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'description': desc,
                    'difficulty': Task.Difficulty.EASY,
                    'starter_code': starter,
                }
            )

            # Привязываем теги
            assigned_tags = [tag_map[ts] for ts in tags_slugs if ts in tag_map]
            if assigned_tags:
                task.tags.set(assigned_tags)

            # Обновляем тесты
            task.test_cases.all().delete()
            num_tests = len(tests)
            for i, args in enumerate(tests, start=1):
                input_str = repr(args[0]) if len(args) == 1 else ", ".join(repr(x) for x in args)
                result = fn(*args)
                expected_str = repr(result) if not isinstance(result, str) else result
                is_hidden = (i == num_tests) and (num_tests > 1)

                TestCase.objects.create(
                    task=task,
                    input_data=input_str,
                    expected_output=expected_str,
                    is_hidden=is_hidden,
                )
            
            added_count += 1
            print(f"[{added_count}/{len(TASKS_25)}] Добавлена: {title} ({len(tests)} тестов)")

    print(f"\nГотово! Всего задач в базе: {Task.objects.count()}")

if __name__ == '__main__':
    add_tasks()

