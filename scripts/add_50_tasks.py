import os
import sys
import django

# Setup django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from challenges.models import Task, TestCase, Tag
from django.db import transaction

tasks_data = [
    # 1. Palindrome Number (LeetCode #9)
    {
        "title": "Palindrome Number (LeetCode #9)",
        "slug": "leetcode-palindrome-number",
        "description": "Определите, является ли целое число `x` палиндромом. Отрицательные числа не являются палиндромами.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def is_palindrome_number(x: int) -> bool:\n    pass\n",
        "tags": ["math"],
        "tests": [
            ("121", "True", False),
            ("-121", "False", False),
            ("10", "False", True),
            ("12321", "True", True),
        ]
    },
    # 2. Remove Element (LeetCode #27)
    {
        "title": "Remove Element (LeetCode #27)",
        "slug": "leetcode-remove-element",
        "description": "Дан массив `nums` и число `val`. Верните новый список, содержащий все элементы `nums`, не равные `val` (с сохранением исходного порядка).",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def remove_element(nums: list, val: int) -> list:\n    pass\n",
        "tags": ["arrays", "two-pointers"],
        "tests": [
            ("[3, 2, 2, 3], 3", "[2, 2]", False),
            ("[0, 1, 2, 2, 3, 0, 4, 2], 2", "[0, 1, 3, 0, 4]", False),
            ("[1, 1, 1], 1", "[]", True),
            ("[4, 5], 1", "[4, 5]", True),
        ]
    },
    # 3. Maximum Subarray (LeetCode #53)
    {
        "title": "Maximum Subarray (LeetCode #53)",
        "slug": "leetcode-maximum-subarray",
        "description": "Найдите непрерывный подмассив с наибольшей суммой элементов и верните эту сумму.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def max_sub_array(nums: list) -> int:\n    pass\n",
        "tags": ["arrays", "dynamic-programming"],
        "tests": [
            ("[-2, 1, -3, 4, -1, 2, 1, -5, 4]", "6", False),
            ("[1]", "1", False),
            ("[5, 4, -1, 7, 8]", "23", True),
            ("[-1, -2, -3]", "-1", True),
        ]
    },
    # 4. Merge Sorted Array (LeetCode #88)
    {
        "title": "Merge Sorted Array (LeetCode #88)",
        "slug": "leetcode-merge-sorted-array",
        "description": "Даны два отсортированных списка `nums1` и `nums2`. Объедините их в один отсортированный список и верните его.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def merge_sorted_arrays(nums1: list, nums2: list) -> list:\n    pass\n",
        "tags": ["arrays", "two-pointers", "sorting"],
        "tests": [
            ("[1, 2, 3], [2, 5, 6]", "[1, 2, 2, 3, 5, 6]", False),
            ("[1], []", "[1]", False),
            ("[], [1]", "[1]", True),
            ("[2, 4, 6], [1, 3, 5]", "[1, 2, 3, 4, 5, 6]", True),
        ]
    },
    # 5. Pascal's Triangle (LeetCode #118)
    {
        "title": "Pascal's Triangle (LeetCode #118)",
        "slug": "leetcode-pascals-triangle",
        "description": "Дано целое число `num_rows`. Верните первые `num_rows` строк треугольника Паскаля в виде списка списков.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def generate_pascals_triangle(num_rows: int) -> list:\n    pass\n",
        "tags": ["arrays", "dynamic-programming"],
        "tests": [
            ("5", "[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]", False),
            ("1", "[[1]]", False),
            ("2", "[[1], [1, 1]]", True),
        ]
    },
    # 6. Best Time to Buy and Sell Stock (LeetCode #121)
    {
        "title": "Best Time to Buy and Sell Stock (LeetCode #121)",
        "slug": "leetcode-best-time-to-buy-and-sell-stock",
        "description": "Дан массив `prices`, где `prices[i]` — цена акции в $i$-й день. Найдите максимальную прибыль от одной покупки и последующей продажи. Если прибыль получить нельзя, верните 0.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def max_profit(prices: list) -> int:\n    pass\n",
        "tags": ["arrays", "dynamic-programming"],
        "tests": [
            ("[7, 1, 5, 3, 6, 4]", "5", False),
            ("[7, 6, 4, 3, 1]", "0", False),
            ("[2, 4, 1]", "2", True),
        ]
    },
    # 7. Excel Sheet Column Number (LeetCode #171)
    {
        "title": "Excel Sheet Column Number (LeetCode #171)",
        "slug": "leetcode-excel-sheet-column-number",
        "description": "Дана строка с названием колонки Excel (напр. 'A', 'B', 'Z', 'AA', 'AB'). Верните её порядковый номер.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def title_to_number(column_title: str) -> int:\n    pass\n",
        "tags": ["math", "strings"],
        "tests": [
            ("'A'", "1", False),
            ("'AB'", "28", False),
            ("'ZY'", "701", True),
            ("'FXSHRXW'", "2147483647", True),
        ]
    },
    # 8. Number of 1 Bits (LeetCode #191)
    {
        "title": "Number of 1 Bits (LeetCode #191)",
        "slug": "leetcode-number-of-1-bits",
        "description": "Дано неотрицательное целое число `n`. Верните количество единичных битов (вес Хэмминга) в его двоичном представлении.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def hamming_weight(n: int) -> int:\n    pass\n",
        "tags": ["bit-manipulation"],
        "tests": [
            ("11", "3", False),
            ("128", "1", False),
            ("2147483645", "30", True),
            ("0", "0", True),
        ]
    },
    # 9. Happy Number (LeetCode #202)
    {
        "title": "Happy Number (LeetCode #202)",
        "slug": "leetcode-happy-number",
        "description": "Счастливое число — число, которое в процессе последовательной замены на сумму квадратов своих цифр в итоге сходится к 1. Если процесс зацикливается без 1 — число несчастливое. Верните `True`, если `n` счастливое, иначе `False`.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def is_happy(n: int) -> bool:\n    pass\n",
        "tags": ["math", "hash-table"],
        "tests": [
            ("19", "True", False),
            ("2", "False", False),
            ("1", "True", True),
            ("7", "True", True),
        ]
    },
    # 10. Reverse String (LeetCode #344)
    {
        "title": "Reverse String (LeetCode #344)",
        "slug": "leetcode-reverse-string",
        "description": "Напишите функцию, которая принимает строку `s` и возвращает строку, записанную задом наперёд.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def reverse_string(s: str) -> str:\n    pass\n",
        "tags": ["strings", "two-pointers"],
        "tests": [
            ("'hello'", "olleh", False),
            ("'Hannah'", "hannaH", False),
            ("''", "", True),
            ("'Python'", "nohtyP", True),
        ]
    },
    # 11. Power of Two (LeetCode #231)
    {
        "title": "Power of Two (LeetCode #231)",
        "slug": "leetcode-power-of-two",
        "description": "Определите, является ли целое число `n` степенью двойки ($n = 2^x$).",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def is_power_of_two(n: int) -> bool:\n    pass\n",
        "tags": ["math", "bit-manipulation"],
        "tests": [
            ("1", "True", False),
            ("16", "True", False),
            ("3", "False", True),
            ("0", "False", True),
        ]
    },
    # 12. Power of Three (LeetCode #326)
    {
        "title": "Power of Three (LeetCode #326)",
        "slug": "leetcode-power-of-three",
        "description": "Определите, является ли целое число `n` степенью тройки ($n = 3^x$).",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def is_power_of_three(n: int) -> bool:\n    pass\n",
        "tags": ["math"],
        "tests": [
            ("27", "True", False),
            ("0", "False", False),
            ("-1", "False", True),
            ("9", "True", True),
        ]
    },
    # 13. Ugly Number (LeetCode #263)
    {
        "title": "Ugly Number (LeetCode #263)",
        "slug": "leetcode-ugly-number",
        "description": "Уродливое число — положительное целое число, простые делители которого ограничены 2, 3 и 5. Верните `True`, если `n` уродливое, иначе `False`.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def is_ugly(n: int) -> bool:\n    pass\n",
        "tags": ["math"],
        "tests": [
            ("6", "True", False),
            ("1", "True", False),
            ("14", "False", True),
            ("-6", "False", True),
        ]
    },
    # 14. Word Pattern (LeetCode #290)
    {
        "title": "Word Pattern (LeetCode #290)",
        "slug": "leetcode-word-pattern",
        "description": "Даны шаблон `pattern` и строка слов `s`. Проверьте, следует ли строка `s` шаблону `pattern` (биективное соответствие символов и слов).",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def word_pattern(pattern: str, s: str) -> bool:\n    pass\n",
        "tags": ["hash-table", "strings"],
        "tests": [
            ("'abba', 'dog cat cat dog'", "True", False),
            ("'abba', 'dog cat cat fish'", "False", False),
            ("'aaaa', 'dog cat cat dog'", "False", True),
            ("'abba', 'dog dog dog dog'", "False", True),
        ]
    },
    # 15. Nim Game (LeetCode #292)
    {
        "title": "Nim Game (LeetCode #292)",
        "slug": "leetcode-nim-game",
        "description": "Вы играете в игру Ним с кучкой из `n` камней. Вы ходите первым. Каждый ход можно взять от 1 до 3 камней. Побеждает тот, кто берет последний камень. Верните `True`, если вы можете гарантированно победить при оптимальной игре обоих участников.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def can_win_nim(n: int) -> bool:\n    pass\n",
        "tags": ["math", "brainteaser"],
        "tests": [
            ("4", "False", False),
            ("1", "True", False),
            ("2", "True", True),
            ("8", "False", True),
        ]
    },
    # 16. Counting Bits (LeetCode #338)
    {
        "title": "Counting Bits (LeetCode #338)",
        "slug": "leetcode-counting-bits",
        "description": "Дано целое число `n`. Верните массив длины `n + 1`, где `ans[i]` — количество единиц в двоичной записи числа `i`.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def count_bits(n: int) -> list:\n    pass\n",
        "tags": ["bit-manipulation", "dynamic-programming"],
        "tests": [
            ("2", "[0, 1, 1]", False),
            ("5", "[0, 1, 1, 2, 1, 2]", False),
            ("0", "[0]", True),
        ]
    },
    # 17. Power of Four (LeetCode #342)
    {
        "title": "Power of Four (LeetCode #342)",
        "slug": "leetcode-power-of-four",
        "description": "Определите, является ли целое число `n` степенью четверки ($n = 4^x$).",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def is_power_of_four(n: int) -> bool:\n    pass\n",
        "tags": ["math", "bit-manipulation"],
        "tests": [
            ("16", "True", False),
            ("5", "False", False),
            ("1", "True", True),
            ("8", "False", True),
        ]
    },
    # 18. Reverse Vowels of a String (LeetCode #345)
    {
        "title": "Reverse Vowels of a String (LeetCode #345)",
        "slug": "leetcode-reverse-vowels-of-a-string",
        "description": "Дана строка `s`. Разверните только гласные буквы (a, e, i, o, u в любом регистре) и верните полученную строку.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def reverse_vowels(s: str) -> str:\n    pass\n",
        "tags": ["strings", "two-pointers"],
        "tests": [
            ("'IceCreAm'", "AceCreIm", False),
            ("'leetcode'", "leotcede", False),
            ("'a.'", "a.", True),
        ]
    },
    # 19. Intersection of Two Arrays (LeetCode #349)
    {
        "title": "Intersection of Two Arrays (LeetCode #349)",
        "slug": "leetcode-intersection-of-two-arrays",
        "description": "Даны два массива `nums1` и `nums2`. Верните отсортированный массив их уникального пересечения.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def intersection(nums1: list, nums2: list) -> list:\n    pass\n",
        "tags": ["arrays", "hash-table"],
        "tests": [
            ("[1, 2, 2, 1], [2, 2]", "[2]", False),
            ("[4, 9, 5], [9, 4, 9, 8, 4]", "[4, 9]", False),
            ("[1, 2, 3], [4, 5, 6]", "[]", True),
        ]
    },
    # 20. First Unique Character in a String (LeetCode #387)
    {
        "title": "First Unique Character in a String (LeetCode #387)",
        "slug": "leetcode-first-unique-character-in-a-string",
        "description": "Найдите первый неповторяющийся символ в строке `s` и верните его индекс. Если такого символа нет, верните -1.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def first_uniq_char(s: str) -> int:\n    pass\n",
        "tags": ["strings", "hash-table"],
        "tests": [
            ("'leetcode'", "0", False),
            ("'loveleetcode'", "2", False),
            ("'aabb'", "-1", True),
        ]
    },
    # 21. Find the Difference (LeetCode #389)
    {
        "title": "Find the Difference (LeetCode #389)",
        "slug": "leetcode-find-the-difference",
        "description": "Строка `t` получена перемешиванием строки `s` и добавлением одной случайной буквы. Найдите и верните добавленную букву.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def find_the_difference(s: str, t: str) -> str:\n    pass\n",
        "tags": ["strings", "hash-table", "bit-manipulation"],
        "tests": [
            ("'abcd', 'abcde'", "e", False),
            ("'', 'y'", "y", False),
            ("'a', 'aa'", "a", True),
        ]
    },
    # 22. Is Subsequence (LeetCode #392)
    {
        "title": "Is Subsequence (LeetCode #392)",
        "slug": "leetcode-is-subsequence",
        "description": "Даны две строки `s` и `t`. Проверьте, является ли `s` подпоследовательностью `t`.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def is_subsequence(s: str, t: str) -> bool:\n    pass\n",
        "tags": ["strings", "two-pointers", "dynamic-programming"],
        "tests": [
            ("'abc', 'ahbgdc'", "True", False),
            ("'axc', 'ahbgdc'", "False", False),
            ("'', 'anystring'", "True", True),
        ]
    },
    # 23. Third Maximum Number (LeetCode #414)
    {
        "title": "Third Maximum Number (LeetCode #414)",
        "slug": "leetcode-third-maximum-number",
        "description": "Дан целочисленный массив `nums`. Верните третье по величине уникальное число. Если третьего максимума нет, верните максимальное число.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def third_max(nums: list) -> int:\n    pass\n",
        "tags": ["arrays", "sorting"],
        "tests": [
            ("[3, 2, 1]", "1", False),
            ("[1, 2]", "2", False),
            ("[2, 2, 3, 1]", "1", True),
        ]
    },
    # 24. Add Strings (LeetCode #415)
    {
        "title": "Add Strings (LeetCode #415)",
        "slug": "leetcode-add-strings",
        "description": "Даны два неотрицательных числа в виде строк `num1` и `num2`. Сложите их и верните результат в виде строки (без прямого преобразования всей строки через int()).",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def add_strings(num1: str, num2: str) -> str:\n    pass\n",
        "tags": ["math", "strings"],
        "tests": [
            ("'11', '123'", "134", False),
            ("'456', '77'", "533", False),
            ("'0', '0'", "0", True),
        ]
    },
    # 25. Number of Segments in a String (LeetCode #434)
    {
        "title": "Number of Segments in a String (LeetCode #434)",
        "slug": "leetcode-number-of-segments-in-a-string",
        "description": "Дана строка `s`. Верните количество сегментов (последовательностей непробельных символов).",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def count_segments(s: str) -> int:\n    pass\n",
        "tags": ["strings"],
        "tests": [
            ("'Hello, my name is John'", "5", False),
            ("'Hello'", "1", False),
            ("''", "0", True),
            ("'                '", "0", True),
        ]
    },
    # 26. Arranging Coins (LeetCode #441)
    {
        "title": "Arranging Coins (LeetCode #441)",
        "slug": "leetcode-arranging-coins",
        "description": "У вас есть `n` монет, и вы строите лестницу, где на $k$-й ступени должно быть ровно $k$ монет. Верните количество полностью заполненных рядов.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def arrange_coins(n: int) -> int:\n    pass\n",
        "tags": ["math", "binary-search"],
        "tests": [
            ("5", "2", False),
            ("8", "3", False),
            ("1", "1", True),
            ("0", "0", True),
        ]
    },
    # 27. Find All Numbers Disappeared in an Array (LeetCode #448)
    {
        "title": "Find All Numbers Disappeared in an Array (LeetCode #448)",
        "slug": "leetcode-find-all-numbers-disappeared-in-an-array",
        "description": "Дан массив `nums` из $n$ чисел, где каждое число находится в диапазоне $[1, n]$. Верните отсортированный список всех чисел из диапазона $[1, n]$, которых нет в `nums`.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def find_disappeared_numbers(nums: list) -> list:\n    pass\n",
        "tags": ["arrays", "hash-table"],
        "tests": [
            ("[4, 3, 2, 7, 8, 2, 3, 1]", "[5, 6]", False),
            ("[1, 1]", "[2]", False),
            ("[1]", "[]", True),
        ]
    },
    # 28. Assign Cookies (LeetCode #455)
    {
        "title": "Assign Cookies (LeetCode #455)",
        "slug": "leetcode-assign-cookies",
        "description": "Каждому ребенку $i$ требуется печенье размером не менее $g[i]$. У вас есть печенья с размерами $s$. Каждому ребенку можно дать максимум одно печенье. Максимизируйте количество довольных детей.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def find_content_children(g: list, s: list) -> int:\n    pass\n",
        "tags": ["arrays", "greedy", "sorting"],
        "tests": [
            ("[1, 2, 3], [1, 1]", "1", False),
            ("[1, 2], [1, 2, 3]", "2", False),
            ("[1, 2, 3], []", "0", True),
        ]
    },
    # 29. Repeated Substring Pattern (LeetCode #459)
    {
        "title": "Repeated Substring Pattern (LeetCode #459)",
        "slug": "leetcode-repeated-substring-pattern",
        "description": "Проверьте, можно ли составить непустую строку `s`, повторив одну из её подстрок два или более раз.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def repeated_substring_pattern(s: str) -> bool:\n    pass\n",
        "tags": ["strings", "string-matching"],
        "tests": [
            ("'abab'", "True", False),
            ("'aba'", "False", False),
            ("'abcabcabcabc'", "True", True),
        ]
    },
    # 30. Hamming Distance (LeetCode #461)
    {
        "title": "Hamming Distance (LeetCode #461)",
        "slug": "leetcode-hamming-distance",
        "description": "Расстояние Хэмминга между двумя целыми числами — это количество позиций, в которых соответствующие биты различаются. Вычислите это расстояние для `x` и `y`.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def hamming_distance(x: int, y: int) -> int:\n    pass\n",
        "tags": ["bit-manipulation"],
        "tests": [
            ("1, 4", "2", False),
            ("3, 1", "1", False),
            ("0, 0", "0", True),
        ]
    },
    # 31. Island Perimeter (LeetCode #463)
    {
        "title": "Island Perimeter (LeetCode #463)",
        "slug": "leetcode-island-perimeter",
        "description": "Дана сетка `grid` размера $row \\times col$, где 1 представляет сушу, а 0 — воду. Остров ровно один и не имеет озер. Вычислите его периметр.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def island_perimeter(grid: list) -> int:\n    pass\n",
        "tags": ["arrays", "matrix"],
        "tests": [
            ("[[0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [1, 1, 0, 0]]", "16", False),
            ("[[1]]", "4", False),
            ("[[1, 0]]", "4", True),
        ]
    },
    # 32. License Key Formatting (LeetCode #482)
    {
        "title": "License Key Formatting (LeetCode #482)",
        "slug": "leetcode-license-key-formatting",
        "description": "Дан лицензионный ключ `s` и число `k`. Отформатируйте строку так, чтобы каждая группа содержала ровно `k` символов в верхнем регистре, разделённых дефисом (кроме первой группы, которая может быть короче).",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def license_key_formatting(s: str, k: int) -> str:\n    pass\n",
        "tags": ["strings"],
        "tests": [
            ("'5F3Z-2e-9-w', 4", "5F3Z-2E9W", False),
            ("'2-5g-3-J', 2", "2-5G-3J", False),
            ("'---', 3", "", True),
        ]
    },
    # 33. Max Consecutive Ones (LeetCode #485)
    {
        "title": "Max Consecutive Ones (LeetCode #485)",
        "slug": "leetcode-max-consecutive-ones",
        "description": "Дан двоичный массив `nums`. Найдите максимальное количество последовательных единиц в массиве.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def find_max_consecutive_ones(nums: list) -> int:\n    pass\n",
        "tags": ["arrays"],
        "tests": [
            ("[1, 1, 0, 1, 1, 1]", "3", False),
            ("[1, 0, 1, 1, 0, 1]", "2", False),
            ("[0, 0, 0]", "0", True),
        ]
    },
    # 34. Base 7 (LeetCode #504)
    {
        "title": "Base 7 (LeetCode #504)",
        "slug": "leetcode-base-7",
        "description": "Дано целое число `num`. Верните его строковое представление в семеричной системе счисления (по основанию 7).",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def convert_to_base7(num: int) -> str:\n    pass\n",
        "tags": ["math"],
        "tests": [
            ("100", "202", False),
            ("-7", "-10", False),
            ("0", "0", True),
        ]
    },
    # 35. Relative Ranks (LeetCode #506)
    {
        "title": "Relative Ranks (LeetCode #506)",
        "slug": "leetcode-relative-ranks",
        "description": "Дан массив `score` с баллами спортсменов. Присвойте им ранги: 1-е место — 'Gold Medal', 2-е — 'Silver Medal', 3-е — 'Bronze Medal', а остальным — их порядковый номер в виде строки.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def find_relative_ranks(score: list) -> list:\n    pass\n",
        "tags": ["arrays", "sorting"],
        "tests": [
            ("[5, 4, 3, 2, 1]", "['Gold Medal', 'Silver Medal', 'Bronze Medal', '4', '5']", False),
            ("[10, 3, 8, 9, 4]", "['Gold Medal', '5', 'Bronze Medal', 'Silver Medal', '4']", False),
            ("[1]", "['Gold Medal']", True),
        ]
    },
    # 36. Perfect Number (LeetCode #507)
    {
        "title": "Perfect Number (LeetCode #507)",
        "slug": "leetcode-perfect-number",
        "description": "Совершенное число — это положительное целое число, равное сумме всех своих собственных положительных делителей (исключая само число). Верните `True`, если `num` совершенно, иначе `False`.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def check_perfect_number(num: int) -> bool:\n    pass\n",
        "tags": ["math"],
        "tests": [
            ("28", "True", False),
            ("7", "False", False),
            ("6", "True", True),
            ("1", "False", True),
        ]
    },
    # 37. Fibonacci Number (LeetCode #509)
    {
        "title": "Fibonacci Number (LeetCode #509)",
        "slug": "leetcode-fibonacci-number",
        "description": "Вычислите $n$-е число Фибоначчи: $F(0) = 0, F(1) = 1, F(n) = F(n - 1) + F(n - 2)$.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def fib(n: int) -> int:\n    pass\n",
        "tags": ["math", "dynamic-programming"],
        "tests": [
            ("2", "1", False),
            ("3", "2", False),
            ("4", "3", True),
            ("0", "0", True),
        ]
    },
    # 38. Detect Capital (LeetCode #520)
    {
        "title": "Detect Capital (LeetCode #520)",
        "slug": "leetcode-detect-capital",
        "description": "Проверьте правильность использования заглавных букв в слове: все заглавные ('USA'), все строчные ('leetcode') или только первая заглавная ('Google').",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def detect_capital_use(word: str) -> bool:\n    pass\n",
        "tags": ["strings"],
        "tests": [
            ("'USA'", "True", False),
            ("'FlaG'", "False", False),
            ("'Google'", "True", True),
            ("'leetcode'", "True", True),
        ]
    },
    # 39. Reverse Words in a String III (LeetCode #557)
    {
        "title": "Reverse Words in a String III (LeetCode #557)",
        "slug": "leetcode-reverse-words-in-a-string-iii",
        "description": "Дана строка `s`. Разверните порядок символов в каждом слове, сохраняя пробелы и начальный порядок слов.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def reverse_words(s: str) -> str:\n    pass\n",
        "tags": ["strings", "two-pointers"],
        "tests": [
            ("'Let\\'s take LeetCode contest'", "s'teL ekat edoCteeL tsetnoc", False),
            ("'God Ding'", "doG gniD", False),
            ("'Python'", "nohtyP", True),
        ]
    },
    # 40. Array Partition (LeetCode #561)
    {
        "title": "Array Partition (LeetCode #561)",
        "slug": "leetcode-array-partition",
        "description": "Дан целочисленный массив `nums` из $2n$ элементов. Сгруппируйте эти элементы в пары $(a_i, b_i)$ так, чтобы сумма $\\min(a_i, b_i)$ была максимально возможной. Верните эту сумму.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def array_pair_sum(nums: list) -> int:\n    pass\n",
        "tags": ["arrays", "greedy", "sorting"],
        "tests": [
            ("[1, 4, 3, 2]", "4", False),
            ("[6, 2, 6, 5, 1, 2]", "9", False),
            ("[1, 2]", "1", True),
        ]
    },
    # 41. Reshape the Matrix (LeetCode #566)
    {
        "title": "Reshape the Matrix (LeetCode #566)",
        "slug": "leetcode-reshape-the-matrix",
        "description": "Дана матрица `mat` размера $m \\times n$ и два числа $r$ и $c$. Преобразуйте матрицу в размер $r \\times c$, сохраняя построчный порядок обхода. Если преобразование невозможно, верните исходную матрицу.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def matrix_reshape(mat: list, r: int, c: int) -> list:\n    pass\n",
        "tags": ["arrays", "matrix"],
        "tests": [
            ("[[1, 2], [3, 4]], 1, 4", "[[1, 2, 3, 4]]", False),
            ("[[1, 2], [3, 4]], 2, 4", "[[1, 2], [3, 4]]", False),
            ("[[1, 2, 3, 4]], 2, 2", "[[1, 2], [3, 4]]", True),
        ]
    },
    # 42. Can Place Flowers (LeetCode #605)
    {
        "title": "Can Place Flowers (LeetCode #605)",
        "slug": "leetcode-can-place-flowers",
        "description": "Дан массив `flowerbed` из 0 и 1, где цветы не могут быть посажены на соседних участках. Определите, можно ли посадить `n` новых цветов, не нарушая правила.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def can_place_flowers(flowerbed: list, n: int) -> bool:\n    pass\n",
        "tags": ["arrays", "greedy"],
        "tests": [
            ("[1, 0, 0, 0, 1], 1", "True", False),
            ("[1, 0, 0, 0, 1], 2", "False", False),
            ("[0, 0, 1, 0, 0], 2", "True", True),
            ("[0, 0, 0, 0, 0], 3", "True", True),
        ]
    },
    # 43. Sum of Positive (Codewars 8 kyu)
    {
        "title": "Sum of Positive (Codewars 8 kyu)",
        "slug": "codewars-sum-of-positive",
        "description": "Дан массив чисел. Верните сумму всех положительных чисел. Если положительных чисел нет, верните 0.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def positive_sum(arr: list) -> int:\n    pass\n",
        "tags": ["arrays"],
        "tests": [
            ("[1, -4, 7, 12]", "20", False),
            ("[-1, -2, -3, -4, -5]", "0", False),
            ("[]", "0", True),
            ("[1, 2, 3, 4, 5]", "15", True),
        ]
    },
    # 44. Opposites Attract (Codewars 8 kyu)
    {
        "title": "Opposites Attract (Codewars 8 kyu)",
        "slug": "codewars-opposites-attract",
        "description": "Тимми и Сара влюблены, если у одного из них количество лепестков на цветке чётное, а у другого — нечётное. Верните `True`, если они влюблены, и `False`, если нет.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def lovefunc(flower1: int, flower2: int) -> bool:\n    pass\n",
        "tags": ["math"],
        "tests": [
            ("1, 4", "True", False),
            ("2, 2", "False", False),
            ("0, 1", "True", True),
            ("0, 0", "False", True),
        ]
    },
    # 45. You're a Square! (Codewars 7 kyu)
    {
        "title": "You're a Square! (Codewars 7 kyu)",
        "slug": "codewars-youre-a-square",
        "description": "Дано целое число `n`. Определите, является ли оно точным квадратом некоторого целого числа ($n = k^2$). Отрицательные числа квадратами целых чисел быть не могут.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def is_square(n: int) -> bool:\n    pass\n",
        "tags": ["math"],
        "tests": [
            ("-1", "False", False),
            ("0", "True", False),
            ("3", "False", True),
            ("25", "True", True),
        ]
    },
    # 46. Growth of a Population (Codewars 7 kyu)
    {
        "title": "Growth of a Population (Codewars 7 kyu)",
        "slug": "codewars-growth-of-a-population",
        "description": "В городе население $p_0$. Каждый год оно увеличивается на $percent$ процентов, и еще прибывает $aug$ жителей. Верните количество полных лет, необходимых для достижения населения не менее $p$.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def nb_year(p0: int, percent: float, aug: int, p: int) -> int:\n    pass\n",
        "tags": ["math"],
        "tests": [
            ("1500, 5, 100, 5000", "15", False),
            ("1500000, 2.5, 10000, 2000000", "10", False),
            ("1000, 2, 50, 1200", "3", True),
        ]
    },
    # 47. Categorize New Member (Codewars 7 kyu)
    {
        "title": "Categorize New Member (Codewars 7 kyu)",
        "slug": "codewars-categorize-new-member",
        "description": "Клуб принимает участников в категории 'Senior' и 'Open'. Участник становится 'Senior', если ему не менее 55 лет и его гандикап строго больше 7. Иначе он 'Open'. Дан список пар `[age, handicap]`, верните список категорий.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def open_or_senior(data: list) -> list:\n    pass\n",
        "tags": ["arrays"],
        "tests": [
            ("[[18, 20], [45, 2], [61, 12], [37, 6], [21, 21], [78, 9]]", "['Open', 'Open', 'Senior', 'Open', 'Open', 'Senior']", False),
            ("[[55, 8], [55, 7], [54, 9]]", "['Senior', 'Open', 'Open']", False),
            ("[]", "[]", True),
        ]
    },
    # 48. Highest and Lowest (Codewars 7 kyu)
    {
        "title": "Highest and Lowest (Codewars 7 kyu)",
        "slug": "codewars-highest-and-lowest",
        "description": "Дана строка чисел, разделённых пробелами. Верните строку с наибольшим и наименьшим числом через пробел (в формате 'max min').",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def high_and_low(numbers: str) -> str:\n    pass\n",
        "tags": ["strings", "sorting"],
        "tests": [
            ("'1 2 3 4 5'", "5 1", False),
            ("'1 2 -3 4 5'", "5 -3", False),
            ("'1 9 3 4 -5'", "9 -5", True),
            ("'42'", "42 42", True),
        ]
    },
    # 49. String Ends With? (Codewars 7 kyu)
    {
        "title": "String Ends With? (Codewars 7 kyu)",
        "slug": "codewars-string-ends-with",
        "description": "Определите, заканчивается ли первая строка `text` второй строкой `ending`.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def solution(text: str, ending: str) -> bool:\n    pass\n",
        "tags": ["strings"],
        "tests": [
            ("'abc', 'bc'", "True", False),
            ("'abc', 'd'", "False", False),
            ("'samurai', 'ai'", "True", True),
            ("'fails', 'ails '", "False", True),
        ]
    },
    # 50. Find the Smallest Integer in the Array (Codewars 8 kyu)
    {
        "title": "Find the Smallest Integer in the Array (Codewars 8 kyu)",
        "slug": "codewars-find-the-smallest-integer-in-the-array",
        "description": "Дан непустой массив целых чисел `arr`. Найдите и верните наименьшее число.",
        "difficulty": Task.Difficulty.EASY,
        "points": 100,
        "starter_code": "def find_smallest_int(arr: list) -> int:\n    pass\n",
        "tags": ["arrays"],
        "tests": [
            ("[34, 15, 88, 2]", "2", False),
            ("[34, -345, -1, 100]", "-345", False),
            ("[0]", "0", True),
            ("[7, 7, 7]", "7", True),
        ]
    },
]

def run():
    print(f"Adding {len(tasks_data)} curated Easy tasks...")
    tag_cache = {}
    
    with transaction.atomic():
        for item in tasks_data:
            # Check slug doesn't exist
            if Task.objects.filter(slug=item["slug"]).exists():
                print(f"Skipping existing: {item['slug']}")
                continue
                
            task = Task.objects.create(
                title=item["title"],
                slug=item["slug"],
                description=item["description"],
                difficulty=item["difficulty"],
                starter_code=item["starter_code"],
            )
            
            for tag_name in item["tags"]:
                if tag_name not in tag_cache:
                    tag_obj = Tag.objects.filter(slug=tag_name).first()
                    if not tag_obj:
                        tag_obj = Tag.objects.filter(name__iexact=tag_name).first()
                    if not tag_obj:
                        tag_obj = Tag.objects.create(
                            name=tag_name.replace('-', ' ').title(),
                            slug=tag_name,
                            color="primary"
                        )
                    tag_cache[tag_name] = tag_obj
                task.tags.add(tag_cache[tag_name])
                
            for in_data, exp_data, hidden in item["tests"]:
                TestCase.objects.create(
                    task=task,
                    input_data=in_data,
                    expected_output=exp_data,
                    is_hidden=hidden,
                )
                
    print(f"Successfully added {len(tasks_data)} tasks!")
    print(f"Total tasks now: {Task.objects.count()}")

if __name__ == "__main__":
    run()
