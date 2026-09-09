# -*- coding: utf-8 -*-
"""
Unified Database Seeder for SmartCode.
Seeds all 129 tasks, tags, test cases (>= 10 per task),
reference solutions with explanations, achievements, and superuser.
"""
import os
import sys
import django

# Setup Django if run as standalone script
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()
else:
    try:
        from django.conf import settings
        _ = settings.DATABASES
    except Exception:
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
        django.setup()

from django.db import transaction
from django.contrib.auth import get_user_model
from challenges.models import Task, TestCase, Tag
from challenges.services.gamification_service import GamificationService

# ==============================================================================
# TASKS DATA (129 tasks with >= 10 tests each, starter code, and reference solutions)
# ==============================================================================

TASKS_DATA = [{'slug': 'return_task',
  'title': 'return_task',
  'difficulty': 'easy',
  'description': 'Даны два числа `a` и `b`. Напишите функцию `solution(a, b)`, которая возвращает их сумму.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(2, 3)  # Вернет: 5 (так как 2 + 3 = 5)\n'
                 '```',
  'starter_code': 'def solution(a, b):\n    pass\n',
  'reference_solution': 'def solution(a, b):\n    return a + b,',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': [],
  'tests': [('2, 3', '5', False),
            ('0, 0', '0', False),
            ('-1, 1', '0', False),
            ('100, 200', '300', False),
            ('-50, -50', '-100', False),
            ('1234, 5678', '6912', False),
            ('-999, 1000', '1', False),
            ('42, -42', '0', False),
            ('7, 8', '15', False),
            ('-10, 25', '15', False),
            ('999999, 1', '1000000', False),
            ('-123, -456', '-579', False)]},
 {'slug': 'two-numbers-difference',
  'title': 'Разница двух чисел',
  'difficulty': 'easy',
  'description': 'Даны два числа `a` и `b`. Напишите функцию `solution(a, b)`, которая возвращает разность чисел (`a - '
                 'b`).\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(5, 10)  # Вернет: -5 (так как 5 - 10 = -5)\n'
                 '```',
  'starter_code': 'def solution(a, b):\n    pass\n',
  'reference_solution': 'def solution(a, b):\n    return a - b,',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': [],
  'tests': [('5, 10', '-5', False),
            ('2, 1', '1', False),
            ('999, 1', '998', False),
            ('0, 0', '0', False),
            ('10, 5', '5', False),
            ('-5, -5', '0', False),
            ('-10, 5', '-15', False),
            ('100, 50', '50', False),
            ('7, 12', '-5', False),
            ('50, -50', '100', False),
            ('1000, 1000', '0', False),
            ('-25, 25', '-50', False)]},
 {'slug': 'palindromes-without-borders',
  'title': 'Палиндромы без границ',
  'difficulty': 'easy',
  'description': 'Проверьте, является ли строка `s` палиндромом (читается одинаково слева направо и справа налево). '
                 'Регистр букв и пробелы при проверке игнорируются.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("А роза упала на лапу Азора")  # Вернет: True\n'
                 '```',
  'starter_code': 'def solution(s: str) -> bool:\r\n    # Ваш код здесь\r\n    pass',
  'reference_solution': 'def solution(s: str) -> bool:\n'
                        "    cleaned = ''.join(c.lower() for c in s if c.isalnum())\n"
                        '    return cleaned == cleaned[::-1]',
  'reference_solution_explanation': 'Приводим строку к нижнему регистру, фильтруем только буквенно-цифровые символы и '
                                    'сравниваем со срезом в обратном порядке.',
  'tags': ['search', 'strings'],
  'tests': [('"А роза упала на лапу Азора"', 'True', False),
            ('"Привет мир"', 'False', False),
            ('""', 'True', False),
            ('"   "', 'True', False),
            ('"a"', 'True', False),
            ('"A"', 'True', False),
            ('"racecar"', 'True', False),
            ('"RaceCar"', 'True', False),
            ('"race car"', 'True', False),
            ('"not a palindrome"', 'False', False),
            ('"Madam"', 'True', False),
            ('"Аргентина манит негра"', 'True', False),
            ('"Аргентинаманитнегра"', 'True', False),
            ('"Аргентина  манит   негра"', 'True', False),
            ('"Абба"', 'True', False),
            ('"abba"', 'True', False),
            ('"abb c"', 'False', False),
            ('"a b c b a"', 'True', False),
            ('"abcba"', 'True', False),
            ('"abccba"', 'True', False),
            ('"abc dcba"', 'True', False),
            ('"Python"', 'False', False),
            ('"no lemon no melon"', 'True', False),
            ('"Was it a car or a cat I saw"', 'True', False),
            ('"Step on no pets"', 'True', False),
            ('"Top spot"', 'True', False),
            ('"My gym"', 'True', False),
            ('"Don nod"', 'True', False),
            ('"notapalindrome"', 'False', False),
            ('"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"', 'True', False)]},
 {'slug': 'leetcode-two-sum',
  'title': 'Two Sum',
  'difficulty': 'easy',
  'description': 'Дан массив целых чисел `nums` и целое число `target`. Найдите и верните индексы двух элементов '
                 'массива, сумма которых равна `target`.\n'
                 '\n'
                 'Каждый вход имеет ровно одно решение. Один и тот же элемент нельзя использовать дважды. Порядок '
                 'индексов в ответе может быть любым.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([2, 7, 11, 15], 9)  # Вернет: [0, 1] (так как nums[0] + nums[1] == 2 + 7 == 9)\n'
                 '```',
  'starter_code': 'def solution(nums, target):\n    pass\n',
  'reference_solution': 'def solution(nums, target):\n'
                        '    seen = {}\n'
                        '    for i, n in enumerate(nums):\n'
                        '        diff = target - n\n'
                        '        if diff in seen:\n'
                        '            return [seen[diff], i]\n'
                        '        seen[n] = i\n'
                        '    return []',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['search', 'arrays'],
  'tests': [('[2, 7, 11, 15], 9', '[0, 1]', False),
            ('[3, 2, 4], 6', '[1, 2]', False),
            ('[3, 3], 6', '[0, 1]', False),
            ('[1, 5, 8, 12], 20', '[2, 3]', False),
            ('[-1, -2, -3, -4, -5], -8', '[2, 4]', False),
            ('[0, 4, 3, 0], 0', '[0, 3]', False),
            ('[-3, 4, 3, 90], 0', '[0, 2]', False),
            ('[1, 2, 3, 4, 5], 9', '[3, 4]', False),
            ('[10, 20, 30, 40], 50', '[1, 2]', False),
            ('[5, 75, 25], 100', '[1, 2]', False),
            ('[2, 5, 5, 11], 10', '[1, 2]', False)]},
 {'slug': 'leetcode-valid-palindrome',
  'title': 'Valid Palindrome',
  'difficulty': 'easy',
  'description': 'Строка является палиндромом, если после приведения всех букв к нижнему регистру и удаления всех не '
                 'буквенно-цифровых символов она читается одинаково слева направо и справа налево.\n'
                 '\n'
                 'Верните `True`, если строка `s` является палиндромом, иначе `False`.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("A man, a plan, a canal: Panama")  # Вернет: True ("amanaplanacanalpanama")\n'
                 '```',
  'starter_code': 'def solution(s):\n    pass\n',
  'reference_solution': 'def solution(s):\n'
                        '    clean = [c.lower() for c in s if c.isalnum()]\n'
                        '    return clean == clean[::-1]',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['strings'],
  'tests': [("'A man, a plan, a canal: Panama'", 'True', False),
            ("'race a car'", 'False', False),
            ("' '", 'True', False),
            ("'0P'", 'False', False),
            ("'No \\'x\\' in Nixon'", 'True', False),
            ("'Was it a car or a cat I saw?'", 'True', False),
            ("'tab a cat'", 'False', False),
            ("'Eva, can I see bees in a cave?'", 'True', False),
            ("'Madam, I\\'m Adam'", 'True', False),
            ("'Never odd or even'", 'True', False),
            ("'12321'", 'True', False),
            ("'123321'", 'True', False)]},
 {'slug': 'leetcode-roman-to-integer',
  'title': 'Roman to Integer',
  'difficulty': 'easy',
  'description': 'Римские цифры представлены семью символами: `I` (1), `V` (5), `X` (10), `L` (50), `C` (100), `D` '
                 '(500), `M` (1000).\n'
                 '\n'
                 'Дана строка `s`, содержащая римское число. Переведите его в стандартное целое число (`int`).\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("MCMXCIV")  # Вернет: 1994 (M=1000, CM=900, XC=90, IV=4)\n'
                 '```',
  'starter_code': 'def solution(s):\n    pass\n',
  'reference_solution': 'def solution(s):\n'
                        "    vals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}\n"
                        '    total = 0\n'
                        '    for i in range(len(s)):\n'
                        '        if i + 1 < len(s) and vals[s[i]] < vals[s[i+1]]:\n'
                        '            total -= vals[s[i]]\n'
                        '        else:\n'
                        '            total += vals[s[i]]\n'
                        '    return total',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['math', 'strings'],
  'tests': [("'III'", '3', False),
            ("'LVIII'", '58', False),
            ("'MCMXCIV'", '1994', False),
            ("'IX'", '9', False),
            ("'XL'", '40', False),
            ("'IV'", '4', False),
            ("'CD'", '400', False),
            ("'CM'", '900', False),
            ("'MMXXIV'", '2024', False),
            ("'DCCCXC'", '890', False),
            ("'MMMCMXCIX'", '3999', False)]},
 {'slug': 'leetcode-longest-common-prefix',
  'title': 'Longest Common Prefix',
  'difficulty': 'easy',
  'description': 'Напишите функцию, которая находит самый длинный общий префикс среди массива строк `strs`.\n'
                 '\n'
                 'Если общего префикса нет, верните пустую строку `""`.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(["flower", "flow", "flight"])  # Вернет: "fl"\n'
                 '```',
  'starter_code': 'def solution(strs):\n    pass\n',
  'reference_solution': 'def solution(strs):\n'
                        '    if not strs: return ""\n'
                        '    prefix = strs[0]\n'
                        '    for s in strs[1:]:\n'
                        '        while not s.startswith(prefix):\n'
                        '            prefix = prefix[:-1]\n'
                        '            if not prefix: return ""\n'
                        '    return prefix',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['strings'],
  'tests': [("['flower', 'flow', 'flight']", 'fl', False),
            ("['dog', 'racecar', 'car']", '', False),
            ("['interspecies', 'interstellar', 'interstate']", 'inters', False),
            ("['throne', 'throne']", 'throne', False),
            ("['a']", 'a', False),
            ("['cir', 'car']", 'c', False),
            ("['prefix', 'pretext', 'preface', 'prefer']", 'pre', False),
            ("['apple', 'app', 'application']", 'app', False),
            ("['abc', 'abcde', 'ab', 'abcdef']", 'ab', False),
            ("['same', 'same', 'same']", 'same', False),
            ("['xyz', 'abc']", '', False)]},
 {'slug': 'leetcode-valid-parentheses',
  'title': 'Valid Parentheses',
  'difficulty': 'easy',
  'description': "Дана строка `s`, состоящая только из скобок `'('`, `')'`, `'{'`, `'}'`, `'['` и `']'`. Определите, "
                 'является ли входная строка валидной.\n'
                 '\n'
                 'Строка валидна, если:\n'
                 '1. Открытые скобки закрываются скобками того же типа.\n'
                 '2. Открытые скобки закрываются в правильном порядке.\n'
                 '3. Каждая закрывающая скобка имеет соответствующую открытую скобку.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("()[]{}")  # Вернет: True\n'
                 '```',
  'starter_code': 'def solution(s):\n    pass\n',
  'reference_solution': 'def solution(s):\n'
                        '    stack = []\n'
                        "    mapping = {')': '(', '}': '{', ']': '['}\n"
                        '    for c in s:\n'
                        '        if c in mapping:\n'
                        '            if not stack or stack[-1] != mapping[c]: return False\n'
                        '            stack.pop()\n'
                        '        else:\n'
                        '            stack.append(c)\n'
                        '    return len(stack) == 0',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['strings'],
  'tests': [("'()[]{}'", 'True', False),
            ("'(]'", 'False', False),
            ("'([{}])'", 'True', False),
            ("'(('", 'False', False),
            ("'{[]}'", 'True', False),
            ("''", 'True', False),
            ("'{[()]}'", 'True', False),
            ("'(()('", 'False', False),
            ("'()'", 'True', False),
            ("'(([]){})'", 'True', False),
            ("'[(])'", 'False', False),
            ("')('", 'False', False)]},
 {'slug': 'leetcode-merge-two-sorted-lists',
  'title': 'Merge Two Sorted Lists',
  'difficulty': 'easy',
  'description': 'Даны два отсортированных по возрастанию списка чисел `list1` и `list2`.\n'
                 '\n'
                 'Объедините их в один отсортированный по возрастанию список.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([1, 2, 4], [1, 3, 4])  # Вернет: [1, 1, 2, 3, 4, 4]\n'
                 '```',
  'starter_code': 'def solution(list1, list2):\n    pass\n',
  'reference_solution': 'def solution(list1, list2):\n    return sorted(l1 + l2),',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['arrays', 'basics'],
  'tests': [('[1, 2, 4], [1, 3, 4]', '[1, 1, 2, 3, 4, 4]', False),
            ('[], []', '[]', False),
            ('[], [0]', '[0]', False),
            ('[5, 10, 15], [2, 3, 20]', '[2, 3, 5, 10, 15, 20]', False),
            ('[1, 5], [2, 3, 4, 6]', '[1, 2, 3, 4, 5, 6]', False),
            ('[-10, -5, 0], [-8, 2, 4]', '[-10, -8, -5, 0, 2, 4]', False),
            ('[1, 1, 1], [1, 1]', '[1, 1, 1, 1, 1]', False),
            ('[100], [50, 150]', '[50, 100, 150]', False),
            ('[1, 2, 3], []', '[1, 2, 3]', False),
            ('[], [7, 8, 9]', '[7, 8, 9]', False),
            ('[2], [1]', '[1, 2]', False)]},
 {'slug': 'leetcode-remove-duplicates',
  'title': 'Remove Duplicates from Sorted Array',
  'difficulty': 'easy',
  'description': 'Дан отсортированный по возрастанию массив чисел `nums`.\n'
                 '\n'
                 'Удалите дубликаты так, чтобы каждый уникальный элемент встречался только один раз, сохранив исходный '
                 'относительный порядок элементов.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([1, 1, 2])  # Вернет: [1, 2]\n'
                 '```',
  'starter_code': 'def solution(nums):\n    pass\n',
  'reference_solution': 'def solution(nums):\n'
                        '    res = []\n'
                        '    for x in nums:\n'
                        '        if not res or res[-1] != x:\n'
                        '            res.append(x)\n'
                        '    return res',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['arrays'],
  'tests': [('[1, 1, 2]', '[1, 2]', False),
            ('[0, 0, 1, 1, 1, 2, 2, 3, 3, 4]', '[0, 1, 2, 3, 4]', False),
            ('[1]', '[1]', False),
            ('[]', '[]', False),
            ('[1, 1, 1, 1]', '[1]', False),
            ('[1, 2, 3, 4, 5]', '[1, 2, 3, 4, 5]', False),
            ('[-3, -3, -2, -1, -1, 0, 0]', '[-3, -2, -1, 0]', False),
            ('[2, 2, 3, 3, 4, 4]', '[2, 3, 4]', False),
            ('[0, 0]', '[0]', False),
            ('[1, 2, 2, 3, 4, 4, 5]', '[1, 2, 3, 4, 5]', False),
            ('[-1, 0, 0, 0, 3, 3]', '[-1, 0, 3]', False)]},
 {'slug': 'leetcode-find-needle-in-haystack',
  'title': 'Find the Index of the First Occurrence',
  'difficulty': 'easy',
  'description': 'Даны две строки: `haystack` и `needle`.\n'
                 '\n'
                 'Верните индекс первого вхождения подстроки `needle` в строку `haystack`, либо `-1`, если `needle` не '
                 'входит в состав `haystack`.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("sadbutsad", "sad")  # Вернет: 0 (первое вхождение на индексе 0)\n'
                 '```',
  'starter_code': 'def solution(haystack, needle):\n    pass\n',
  'reference_solution': 'def solution(haystack, needle):\n    return h.find(n),',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['search', 'strings'],
  'tests': [("'sadbutsad', 'sad'", '0', False),
            ("'leetcode', 'leeto'", '-1', False),
            ("'hello', 'll'", '2', False),
            ("'mississippi', 'issip'", '4', False),
            ("'a', 'a'", '0', False),
            ("'abc', 'c'", '2', False),
            ("'findtheneedle', 'the'", '4', False),
            ("'banana', 'an'", '1', False),
            ("'abcdef', 'gh'", '-1', False),
            ("'starting', 'start'", '0', False),
            ("'word', 'words'", '-1', False)]},
 {'slug': 'leetcode-search-insert-position',
  'title': 'Search Insert Position',
  'difficulty': 'easy',
  'description': 'Дан отсортированный массив уникальных целых чисел `nums` и целевое значение `target`.\n'
                 '\n'
                 'Если `target` присутствует в массиве, верните его индекс. Если нет — верните индекс, куда он должен '
                 'быть вставлен с сохранением порядка сортировки.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([1, 3, 5, 6], 5)  # Вернет: 2\n'
                 '```',
  'starter_code': 'def solution(nums, target):\n    pass\n',
  'reference_solution': 'def solution(nums, target):\n'
                        '    l, r = 0, len(nums) - 1\n'
                        '    while l <= r:\n'
                        '        mid = (l + r) // 2\n'
                        '        if nums[mid] == target: return mid\n'
                        '        elif nums[mid] < target: l = mid + 1\n'
                        '        else: r = mid - 1\n'
                        '    return l',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['search', 'arrays'],
  'tests': [('[1, 3, 5, 6], 5', '2', False),
            ('[1, 3, 5, 6], 2', '1', False),
            ('[1, 3, 5, 6], 7', '4', False),
            ('[1, 3, 5, 6], 0', '0', False),
            ('[1], 0', '0', False),
            ('[1], 1', '0', False),
            ('[1], 2', '1', False),
            ('[1, 4, 6, 7, 8, 9], 6', '2', False),
            ('[2, 5, 8, 11, 14], 12', '4', False),
            ('[-5, -2, 0, 3], -3', '1', False),
            ('[10, 20, 30], 25', '2', False)]},
 {'slug': 'leetcode-length-of-last-word',
  'title': 'Length of Last Word',
  'difficulty': 'easy',
  'description': 'Дана строка `s`, состоящая из слов и пробелов.\n'
                 '\n'
                 'Верните длину последнего слова в строке (слово — максимальная подстрока из непробельных символов).\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("Hello World")  # Вернет: 5 (длина слова "World")\n'
                 '```',
  'starter_code': 'def solution(s):\n    pass\n',
  'reference_solution': 'def solution(s):\n    return len(s.strip().split()[-1]) if s.strip() else 0,',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['strings'],
  'tests': [("'Hello World'", '5', False),
            ("'   fly me   to   the moon  '", '4', False),
            ("'luffy is still joyboy'", '6', False),
            ("'a'", '1', False),
            ("'day'", '3', False),
            ("'   single   '", '6', False),
            ("'programming in python is fun'", '3', False),
            ("'test    test2   '", '5', False),
            ("'lots of     spaces     here    '", '4', False),
            ("'one'", '3', False),
            ("'ends with multiple words yes'", '3', False)]},
 {'slug': 'leetcode-plus-one',
  'title': 'Plus One',
  'difficulty': 'easy',
  'description': 'Дано большое целое число, представленное в виде массива цифр `digits` (где `digits[0]` — старший '
                 'разряд).\n'
                 '\n'
                 'Прибавьте к этому числу `1` и верните получившийся массив цифр.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([1, 2, 3])  # Вернет: [1, 2, 4] (123 + 1 = 124)\n'
                 '```',
  'starter_code': 'def solution(digits):\n    pass\n',
  'reference_solution': 'def solution(digits):\n'
                        "    num = int(''.join(map(str, digits))) + 1\n"
                        '    return [int(d) for d in str(num)]',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['math', 'arrays'],
  'tests': [('[1, 2, 3]', '[1, 2, 4]', False),
            ('[4, 3, 2, 1]', '[4, 3, 2, 2]', False),
            ('[9]', '[1, 0]', False),
            ('[9, 9, 9]', '[1, 0, 0, 0]', False),
            ('[0]', '[1]', False),
            ('[1, 9, 9]', '[2, 0, 0]', False),
            ('[8, 9, 9, 9]', '[9, 0, 0, 0]', False),
            ('[2, 0, 0]', '[2, 0, 1]', False),
            ('[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]', '[9, 8, 7, 6, 5, 4, 3, 2, 1, 1]', False),
            ('[5, 5, 5]', '[5, 5, 6]', False),
            ('[9, 9]', '[1, 0, 0]', False)]},
 {'slug': 'leetcode-add-binary',
  'title': 'Add Binary',
  'difficulty': 'easy',
  'description': 'Даны две двоичные строки `a` и `b`.\n'
                 '\n'
                 'Сложите их и верните их сумму в виде двоичной строки.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("11", "1")  # Вернет: "100" (3 + 1 = 4 в двоичной системе)\n'
                 '```',
  'starter_code': 'def solution(a, b):\n    pass\n',
  'reference_solution': 'def solution(a, b):\n    return bin(int(a, 2) + int(b, 2))[2:],',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['math', 'strings'],
  'tests': [("'11', '1'", '100', False),
            ("'1010', '1011'", '10101', False),
            ("'0', '0'", '0', False),
            ("'1111', '1111'", '11110', False),
            ("'1', '0'", '1', False),
            ("'100', '110'", '1010', False),
            ("'101', '10'", '111', False),
            ("'111', '1'", '1000', False),
            ("'1000', '1'", '1001', False),
            ("'10101', '111'", '11100', False),
            ("'110010', '10111'", '1001001', False)]},
 {'slug': 'leetcode-sqrtx',
  'title': 'Sqrt(x)',
  'difficulty': 'easy',
  'description': 'Дано неотрицательное целое число `x`.\n'
                 '\n'
                 'Вычислите и верните целочисленный квадратный корень из `x` (округленный вниз до ближайшего целого '
                 'числа).\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(8)  # Вернет: 2 (квадратный корень из 8 равен 2.828..., округляем вниз)\n'
                 '```',
  'starter_code': 'def solution(x):\n    pass\n',
  'reference_solution': 'def solution(x):\n    return int(x**0.5),',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['math'],
  'tests': [('4', '2', False),
            ('8', '2', False),
            ('0', '0', False),
            ('1', '1', False),
            ('25', '5', False),
            ('1000000', '1000', False),
            ('2', '1', False),
            ('3', '1', False),
            ('9', '3', False),
            ('15', '3', False),
            ('16', '4', False),
            ('99', '9', False)]},
 {'slug': 'leetcode-climbing-stairs',
  'title': 'Climbing Stairs',
  'difficulty': 'easy',
  'description': 'Вы поднимаетесь по лестнице из `n` ступеней. За один шаг можно подняться на `1` или на `2` ступени.\n'
                 '\n'
                 'Сколькими различными способами можно подняться на вершину?\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(3)  # Вернет: 3 (способы: 1+1+1, 1+2, 2+1)\n'
                 '```',
  'starter_code': 'def solution(n):\n    pass\n',
  'reference_solution': 'def solution(n):\n'
                        '    if n <= 2: return n\n'
                        '    a, b = 1, 2\n'
                        '    for _ in range(n - 2):\n'
                        '        a, b = b, a + b\n'
                        '    return b',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['dp', 'math'],
  'tests': [('2', '2', False),
            ('3', '3', False),
            ('1', '1', False),
            ('5', '8', False),
            ('10', '89', False),
            ('4', '5', False),
            ('6', '13', False),
            ('7', '21', False),
            ('8', '34', False),
            ('9', '55', False),
            ('12', '233', False)]},
 {'slug': 'leetcode-single-number',
  'title': 'Single Number',
  'difficulty': 'easy',
  'description': 'Дан непустой массив целых чисел `nums`. Каждый элемент в нем встречается дважды, за исключением '
                 'одного.\n'
                 '\n'
                 'Найдите и верните этот единственный элемент.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([4, 1, 2, 1, 2])  # Вернет: 4\n'
                 '```',
  'starter_code': 'def solution(nums):\n    pass\n',
  'reference_solution': 'def solution(nums):\n    ans = 0\n    for x in nums: ans ^= x\n    return ans',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['arrays'],
  'tests': [('[2, 2, 1]', '1', False),
            ('[4, 1, 2, 1, 2]', '4', False),
            ('[1]', '1', False),
            ('[-1, -1, -2]', '-2', False),
            ('[7, 3, 5, 3, 7]', '5', False),
            ('[0, 1, 0]', '1', False),
            ('[10, 20, 10, 30, 20]', '30', False),
            ('[99, 50, 99]', '50', False),
            ('[-10, 2, 2]', '-10', False),
            ('[42]', '42', False),
            ('[8, 8, 9, 10, 10]', '9', False)]},
 {'slug': 'leetcode-majority-element',
  'title': 'Majority Element',
  'difficulty': 'easy',
  'description': 'Дан массив `nums` размера `n`. Найдите мажоритарный элемент.\n'
                 '\n'
                 'Мажоритарный элемент — это элемент, который появляется в массиве более чем `n // 2` раз. '
                 'Гарантируется, что такой элемент всегда существует.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([2, 2, 1, 1, 1, 2, 2])  # Вернет: 2\n'
                 '```',
  'starter_code': 'def solution(nums):\n    pass\n',
  'reference_solution': 'def solution(nums):\n'
                        '    from collections import Counter\n'
                        '    return Counter(nums).most_common(1)[0][0]',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['arrays'],
  'tests': [('[3, 2, 3]', '3', False),
            ('[2, 2, 1, 1, 1, 2, 2]', '2', False),
            ('[1]', '1', False),
            ('[6, 5, 5]', '5', False),
            ('[1, 1, 1, 2, 2]', '1', False),
            ('[7, 7, 7, 7, 1, 2, 3]', '7', False),
            ('[4, 4, 4, 3, 4]', '4', False),
            ('[-1, -1, 2]', '-1', False),
            ('[9, 9, 8, 9, 8, 9, 9]', '9', False),
            ('[100, 100, 200]', '100', False),
            ('[3, 3, 4, 2, 4, 4, 2, 4, 4]', '4', False)]},
 {'slug': 'leetcode-isomorphic-strings',
  'title': 'Isomorphic Strings',
  'difficulty': 'easy',
  'description': 'Даны две строки `s` и `t`. Определите, являются ли они изоморфными.\n'
                 '\n'
                 'Две строки изоморфны, если символы в `s` можно заменить так, чтобы получить `t`, сохраняя порядок '
                 'символов и однозначное соответствие между буквами.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("egg", "add")  # Вернет: True (e -> a, g -> d)\n'
                 '```',
  'starter_code': 'def solution(s, t):\n    pass\n',
  'reference_solution': 'def solution(s, t):\n'
                        '    return len(set(zip(s, t))) == len(set(s)) == len(set(t)) and len(s) == len(t)',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['dicts', 'strings'],
  'tests': [("'egg', 'add'", 'True', False),
            ("'foo', 'bar'", 'False', False),
            ("'paper', 'title'", 'True', False),
            ("'badc', 'baba'", 'False', False),
            ("'a', 'a'", 'True', False),
            ("'ab', 'aa'", 'False', False),
            ("'bbbaaaba', 'aaabbbba'", 'False', False),
            ("'abcdef', 'uvwxyz'", 'True', False),
            ("'turtle', 'txmlxe'", 'False', False),
            ("'paper', 'titii'", 'False', False),
            ("'same', 'game'", 'True', False)]},
 {'slug': 'leetcode-contains-duplicate',
  'title': 'Contains Duplicate',
  'difficulty': 'easy',
  'description': 'Дан массив целых чисел `nums`.\n'
                 '\n'
                 'Верните `True`, если хотя бы одно значение встречается в массиве минимум два раза, и `False`, если '
                 'все элементы в массиве уникальны.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([1, 2, 3, 1])  # Вернет: True\n'
                 '```',
  'starter_code': 'def solution(nums):\n    pass\n',
  'reference_solution': 'def solution(nums):\n    return len(nums) != len(set(nums)),',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['dicts', 'arrays'],
  'tests': [('[1, 2, 3, 1]', 'True', False),
            ('[1, 2, 3, 4]', 'False', False),
            ('[1, 1, 1, 3, 3, 4, 3, 2, 4, 2]', 'True', False),
            ('[]', 'False', False),
            ('[1]', 'False', False),
            ('[2, 2]', 'True', False),
            ('[5, 10, 15, 20, 25]', 'False', False),
            ('[-1, -2, -3, -1]', 'True', False),
            ('[100, 200, 300, 400]', 'False', False),
            ('[0, 0]', 'True', False),
            ('[7, 8, 9, 10, 11, 7]', 'True', False)]},
 {'slug': 'leetcode-valid-anagram',
  'title': 'Valid Anagram',
  'difficulty': 'easy',
  'description': 'Даны две строки `s` и `t`.\n'
                 '\n'
                 'Верните `True`, если строка `t` является анаграммой строки `s` (содержит точно такие же буквы с '
                 'такой же частотой), и `False` в противном случае.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("anagram", "nagaram")  # Вернет: True\n'
                 '```',
  'starter_code': 'def solution(s, t):\n    pass\n',
  'reference_solution': 'def solution(s, t):\n    return sorted(s) == sorted(t),',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['dicts', 'strings'],
  'tests': [("'anagram', 'nagaram'", 'True', False),
            ("'rat', 'car'", 'False', False),
            ("'a', 'a'", 'True', False),
            ("'ab', 'a'", 'False', False),
            ("'listen', 'silent'", 'True', False),
            ("'triangle', 'integral'", 'True', False),
            ("'apple', 'pale'", 'False', False),
            ("'cinema', 'iceman'", 'True', False),
            ("'dormitory', 'dirtyroom'", 'True', False),
            ("'hello', 'bello'", 'False', False),
            ("'aabbcc', 'ccbbaa'", 'True', False)]},
 {'slug': 'leetcode-missing-number',
  'title': 'Missing Number',
  'difficulty': 'easy',
  'description': 'Дан массив `nums`, содержащий `n` уникальных чисел из диапазона `[0, n]`.\n'
                 '\n'
                 'Найдите единственное число из диапазона, которое отсутствует в массиве.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([3, 0, 1])  # Вернет: 2 (в диапазоне [0, 3] отсутствует число 2)\n'
                 '```',
  'starter_code': 'def solution(nums):\n    pass\n',
  'reference_solution': 'def solution(nums):\n    n = len(nums)\n    return n * (n + 1) // 2 - sum(nums)',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['math', 'arrays'],
  'tests': [('[3, 0, 1]', '2', False),
            ('[0, 1]', '2', False),
            ('[9, 6, 4, 2, 3, 5, 7, 0, 1]', '8', False),
            ('[0]', '1', False),
            ('[1]', '0', False),
            ('[1, 2]', '0', False),
            ('[0, 2, 3]', '1', False),
            ('[5, 4, 3, 2, 0]', '1', False),
            ('[0, 1, 2, 3, 4, 5, 6, 7, 9]', '8', False),
            ('[2, 0, 1, 4]', '3', False),
            ('[0, 1, 3, 4, 5, 6]', '2', False)]},
 {'slug': 'leetcode-move-zeroes',
  'title': 'Move Zeroes',
  'difficulty': 'easy',
  'description': 'Дан целочисленный массив `nums`.\n'
                 '\n'
                 'Переместите все нули в конец массива, сохранив относительный порядок всех ненулевых элементов.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([0, 1, 0, 3, 12])  # Вернет: [1, 3, 12, 0, 0]\n'
                 '```',
  'starter_code': 'def solution(nums):\n    pass\n',
  'reference_solution': 'def solution(nums):\n'
                        '    non_zeros = [x for x in nums if x != 0]\n'
                        '    return non_zeros + [0] * (len(nums) - len(non_zeros))',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['arrays'],
  'tests': [('[0, 1, 0, 3, 12]', '[1, 3, 12, 0, 0]', False),
            ('[0]', '[0]', False),
            ('[1, 2, 3]', '[1, 2, 3]', False),
            ('[0, 0, 1]', '[1, 0, 0]', False),
            ('[0, 0, 0]', '[0, 0, 0]', False),
            ('[1, 0, 2, 0, 3, 0]', '[1, 2, 3, 0, 0, 0]', False),
            ('[4, 2, 4, 0, 0, 3, 0, 5, 1, 0]', '[4, 2, 4, 3, 5, 1, 0, 0, 0, 0]', False),
            ('[0, 1]', '[1, 0]', False),
            ('[1, 0]', '[1, 0]', False),
            ('[0, 0, 2, 3]', '[2, 3, 0, 0]', False),
            ('[-1, 0, -2, 0, 5]', '[-1, -2, 5, 0, 0]', False)]},
 {'slug': 'codewars-vowel-count',
  'title': 'Vowel Count',
  'difficulty': 'easy',
  'description': 'Напишите функцию, которая возвращает общее количество гласных букв (`a`, `e`, `i`, `o`, `u`) в '
                 'переданной строке `s`.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("abracadabra")  # Вернет: 5\n'
                 '```',
  'starter_code': 'def solution(s):\n    pass\n',
  'reference_solution': "def solution(s):\n    return sum(1 for c in s.lower() if c in 'aeiou'),",
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['strings'],
  'tests': [("'abracadabra'", '5', False),
            ("'hello world'", '3', False),
            ("'xyz'", '0', False),
            ("''", '0', False),
            ("'aeiou'", '5', False),
            ("'rhythm'", '0', False),
            ("'PYTHON'", '1', False),
            ("'quick brown fox jumps over lazy dog'", '9', False),
            ("'Education'", '5', False),
            ("'programming'", '3', False),
            ("'bcdfg'", '0', False)]},
 {'slug': 'codewars-disemvowel-trolls',
  'title': 'Disemvowel Trolls',
  'difficulty': 'easy',
  'description': 'Напишите функцию, которая принимает строку и возвращает новую строку, из которой удалены все гласные '
                 'буквы (`a`, `e`, `i`, `o`, `u` в верхнем и нижнем регистрах).\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("This website is for losers LOL!")  # Вернет: "Ths wbst s fr lsrs LL!"\n'
                 '```',
  'starter_code': 'def solution(string):\n    pass\n',
  'reference_solution': "def solution(string):\n    return ''.join(c for c in s if c.lower() not in 'aeiou'),",
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['strings'],
  'tests': [("'This website is for losers LOL!'", 'Ths wbst s fr lsrs LL!', False),
            ("'No offense but,\\nYour writing is among the worst'", 'N ffns bt,\nYr wrtng s mng th wrst', False),
            ("'What are you, a communist?'", 'Wht r y,  cmmnst?', False),
            ("'Hello World'", 'Hll Wrld', False),
            ("'aeiouAEIOU'", '', False),
            ("'rhythm'", 'rhythm', False),
            ("'Python is awesome'", 'Pythn s wsm', False),
            ("'Just testing vowels here'", 'Jst tstng vwls hr', False),
            ("'Coding challenge'", 'Cdng chllng', False),
            ("'CodeWars and LeetCode'", 'CdWrs nd LtCd', False),
            ("'Disemvowel this troll!'", 'Dsmvwl ths trll!', False)]},
 {'slug': 'codewars-square-every-digit',
  'title': 'Square Every Digit',
  'difficulty': 'easy',
  'description': 'Возведите каждую цифру переданного целого числа `num` в квадрат и объедините их в одно число.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(9119)  # Вернет: 811181 (так как 9^2=81, 1^2=1, 1^2=1, 9^2=81)\n'
                 '```',
  'starter_code': 'def solution(num):\n    pass\n',
  'reference_solution': "def solution(num):\n    return int(''.join(str(int(d)**2) for d in str(n))),",
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['math'],
  'tests': [('9119', '811181', False),
            ('0', '0', False),
            ('123', '149', False),
            ('765', '493625', False),
            ('3212', '9414', False),
            ('55', '2525', False),
            ('8', '64', False),
            ('999', '818181', False),
            ('1010', '1010', False),
            ('4321', '16941', False),
            ('2468', '4163664', False)]},
 {'slug': 'codewars-descending-order',
  'title': 'Descending Order',
  'difficulty': 'easy',
  'description': 'Напишите функцию, которая принимает неотрицательное целое число `num` и возвращает число, '
                 'составленное из его цифр в порядке убывания.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(42145)  # Вернет: 54421\n'
                 '```',
  'starter_code': 'def solution(num):\n    pass\n',
  'reference_solution': "def solution(num):\n    return int(''.join(sorted(str(n), reverse=True))),",
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['math', 'basics'],
  'tests': [('42145', '54421', False),
            ('145263', '654321', False),
            ('123456789', '987654321', False),
            ('0', '0', False),
            ('15', '51', False),
            ('1021', '2110', False),
            ('987', '987', False),
            ('111', '111', False),
            ('54321', '54321', False),
            ('2048', '8420', False),
            ('918273', '987321', False)]},
 {'slug': 'leetcode-palindrome-number',
  'title': 'Palindrome Number',
  'difficulty': 'easy',
  'description': 'Определите, является ли целое число `x` палиндромом (читается одинаково слева направо и справа '
                 'налево). Отрицательные числа палиндромами не являются.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(121)  # Вернет: True\n'
                 '```',
  'starter_code': 'def solution(x: int) -> bool:\n    pass\n',
  'reference_solution': 'def solution(x):\n    return str(x) == str(x)[::-1],',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['math'],
  'tests': [('121', 'True', False),
            ('-121', 'False', False),
            ('10', 'False', False),
            ('12321', 'True', False),
            ('0', 'True', False),
            ('7', 'True', False),
            ('1001', 'True', False),
            ('-101', 'False', False),
            ('1234321', 'True', False),
            ('55555', 'True', False),
            ('99', 'True', False)]},
 {'slug': 'leetcode-remove-element',
  'title': 'Remove Element',
  'difficulty': 'easy',
  'description': 'Дан массив `nums` и число `val`. Верните новый список, содержащий все элементы `nums`, не равные '
                 '`val`, сохранив их исходный порядок.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([3, 2, 2, 3], 3)  # Вернет: [2, 2]\n'
                 '```',
  'starter_code': 'def solution(nums: list, val: int) -> list:\n    pass\n',
  'reference_solution': 'def solution(x):\n    return [x for x in nums if x != v],',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['two-pointers', 'arrays'],
  'tests': [('[3, 2, 2, 3], 3', '[2, 2]', False),
            ('[0, 1, 2, 2, 3, 0, 4, 2], 2', '[0, 1, 3, 0, 4]', False),
            ('[1, 1, 1], 1', '[]', False),
            ('[4, 5], 1', '[4, 5]', False),
            ('[], 0', '[]', False),
            ('[1], 1', '[]', False),
            ('[1, 2, 3, 4], 5', '[1, 2, 3, 4]', False),
            ('[2, 2, 2, 2], 2', '[]', False),
            ('[7, 8, 7, 9, 7], 7', '[8, 9]', False),
            ('[10, 20, 30], 20', '[10, 30]', False),
            ('[5, 5, 1, 5, 2], 5', '[1, 2]', False)]},
 {'slug': 'leetcode-maximum-subarray',
  'title': 'Maximum Subarray',
  'difficulty': 'easy',
  'description': 'Найдите в массиве `nums` непрерывный подмассив с наибольшей суммой элементов и верните эту сумму.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([-2, 1, -3, 4, -1, 2, 1, -5, 4])  # Вернет: 6 (подмассив [4, -1, 2, 1])\n'
                 '```',
  'starter_code': 'def solution(nums: list) -> int:\n    pass\n',
  'reference_solution': 'def solution(nums):\n'
                        '    cur = m = nums[0]\n'
                        '    for x in nums[1:]:\n'
                        '        cur = max(x, cur + x)\n'
                        '        m = max(m, cur)\n'
                        '    return m',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['dynamic-programming', 'arrays'],
  'tests': [('[-2, 1, -3, 4, -1, 2, 1, -5, 4]', '6', False),
            ('[1]', '1', False),
            ('[5, 4, -1, 7, 8]', '23', False),
            ('[-1, -2, -3]', '-1', False),
            ('[-2, -1]', '-1', False),
            ('[1, 2, 3, 4, 5]', '15', False),
            ('[-2, 3, 2, -1]', '5', False),
            ('[-1, 0, -2]', '0', False),
            ('[8, -19, 5, -4, 20]', '21', False),
            ('[-3, -2, 0, -1]', '0', False),
            ('[10, -5, 15, -2, 3]', '21', False)]},
 {'slug': 'leetcode-merge-sorted-array',
  'title': 'Merge Sorted Array',
  'difficulty': 'easy',
  'description': 'Даны два отсортированных списка `nums1` и `nums2`. Объедините их в один общий отсортированный '
                 'список.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([1, 2, 3], [2, 5, 6])  # Вернет: [1, 2, 2, 3, 5, 6]\n'
                 '```',
  'starter_code': 'def solution(nums1: list, nums2: list) -> list:\n    pass\n',
  'reference_solution': 'def solution(x):\n    return sorted(n1 + n2),',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['sorting', 'two-pointers', 'arrays'],
  'tests': [('[1, 2, 3], [2, 5, 6]', '[1, 2, 2, 3, 5, 6]', False),
            ('[1], []', '[1]', False),
            ('[], [1]', '[1]', False),
            ('[2, 4, 6], [1, 3, 5]', '[1, 2, 3, 4, 5, 6]', False),
            ('[1, 1, 1], [2, 2]', '[1, 1, 1, 2, 2]', False),
            ('[-5, 0, 5], [-3, 2, 7]', '[-5, -3, 0, 2, 5, 7]', False),
            ('[10, 20], [5, 15, 25]', '[5, 10, 15, 20, 25]', False),
            ('[], []', '[]', False),
            ('[1, 2], [3, 4]', '[1, 2, 3, 4]', False),
            ('[-10], [-20, 0]', '[-20, -10, 0]', False),
            ('[100], [50, 75, 125]', '[50, 75, 100, 125]', False)]},
 {'slug': 'leetcode-pascals-triangle',
  'title': "Pascal's Triangle",
  'difficulty': 'easy',
  'description': 'Дано целое число `num_rows`. Верните первые `num_rows` строк треугольника Паскаля в виде списка '
                 'списков.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(5)  # Вернет: [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]\n'
                 '```',
  'starter_code': 'def solution(num_rows: int) -> list:\n    pass\n',
  'reference_solution': 'def solution(num_rows):\n'
                        '    res = [[1]]\n'
                        '    for _ in range(num_rows - 1):\n'
                        '        res.append([1] + [res[-1][i] + res[-1][i+1] for i in range(len(res[-1]) - 1)] + [1])\n'
                        '    return res',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['dynamic-programming', 'arrays'],
  'tests': [('5', '[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]', False),
            ('1', '[[1]]', False),
            ('2', '[[1], [1, 1]]', False),
            ('3', '[[1], [1, 1], [1, 2, 1]]', False),
            ('4', '[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1]]', False),
            ('6', '[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1], [1, 5, 10, 10, 5, 1]]', False),
            ('7',
             '[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1], [1, 5, 10, 10, 5, 1], [1, 6, 15, 20, 15, 6, 1]]',
             False),
            ('8',
             '[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1], [1, 5, 10, 10, 5, 1], [1, 6, 15, 20, 15, 6, 1], '
             '[1, 7, 21, 35, 35, 21, 7, 1]]',
             False),
            ('9',
             '[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1], [1, 5, 10, 10, 5, 1], [1, 6, 15, 20, 15, 6, 1], '
             '[1, 7, 21, 35, 35, 21, 7, 1], [1, 8, 28, 56, 70, 56, 28, 8, 1]]',
             False),
            ('10',
             '[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1], [1, 5, 10, 10, 5, 1], [1, 6, 15, 20, 15, 6, 1], '
             '[1, 7, 21, 35, 35, 21, 7, 1], [1, 8, 28, 56, 70, 56, 28, 8, 1], [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]]',
             False),
            ('11',
             '[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1], [1, 5, 10, 10, 5, 1], [1, 6, 15, 20, 15, 6, 1], '
             '[1, 7, 21, 35, 35, 21, 7, 1], [1, 8, 28, 56, 70, 56, 28, 8, 1], [1, 9, 36, 84, 126, 126, 84, 36, 9, 1], '
             '[1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]]',
             False)]},
 {'slug': 'leetcode-best-time-to-buy-and-sell-stock',
  'title': 'Best Time to Buy and Sell Stock',
  'difficulty': 'easy',
  'description': 'Дан массив цен акций `prices`, где `prices[i]` — цена в i-й день. Найдите максимальную прибыль от '
                 'одной сделки (покупка и последующая продажа). Если прибыль получить нельзя, верните 0.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([7, 1, 5, 3, 6, 4])  # Вернет: 5 (покупка по цене 1, продажа по цене 6)\n'
                 '```',
  'starter_code': 'def solution(prices: list) -> int:\n    pass\n',
  'reference_solution': 'def solution(prices):\n'
                        "    min_p, max_p = float('inf'), 0\n"
                        '    for p in prices:\n'
                        '        min_p = min(min_p, p)\n'
                        '        max_p = max(max_p, p - min_p)\n'
                        '    return max_p',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['dynamic-programming', 'arrays'],
  'tests': [('[7, 1, 5, 3, 6, 4]', '5', False),
            ('[7, 6, 4, 3, 1]', '0', False),
            ('[2, 4, 1]', '2', False),
            ('[1, 2]', '1', False),
            ('[3, 2, 6, 5, 0, 3]', '4', False),
            ('[1, 2, 3, 4, 5]', '4', False),
            ('[5]', '0', False),
            ('[2, 1, 2, 1, 0, 1, 2]', '2', False),
            ('[3, 3, 3, 3]', '0', False),
            ('[10, 2, 8, 1, 9]', '8', False),
            ('[1, 10]', '9', False)]},
 {'slug': 'leetcode-excel-sheet-column-number',
  'title': 'Excel Sheet Column Number',
  'difficulty': 'easy',
  'description': "Дана строка с названием колонки таблицы Excel (например, 'A', 'B', 'Z', 'AA', 'AB'). Верните её "
                 'соответствующий порядковый номер.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("AB")  # Вернет: 28 (A=1, ..., Z=26, AA=27, AB=28)\n'
                 '```',
  'starter_code': 'def solution(column_title: str) -> int:\n    pass\n',
  'reference_solution': 'def solution(s):\n'
                        '    ans = 0\n'
                        '    for c in s:\n'
                        "        ans = ans * 26 + (ord(c) - ord('A') + 1)\n"
                        '    return ans',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['math', 'strings'],
  'tests': [("'A'", '1', False),
            ("'AB'", '28', False),
            ("'ZY'", '701', False),
            ("'FXSHRXW'", '2147483647', False),
            ("'B'", '2', False),
            ("'Z'", '26', False),
            ("'AA'", '27', False),
            ("'AZ'", '52', False),
            ("'BA'", '53', False),
            ("'BZ'", '78', False),
            ("'AAA'", '703', False)]},
 {'slug': 'leetcode-number-of-1-bits',
  'title': 'Number of 1 Bits',
  'difficulty': 'easy',
  'description': 'Дано неотрицательное целое число `n`. Верните количество единичных битов (вес Хэмминга) в его '
                 'двоичном представлении.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(11)  # Вернет: 3 (в двоичной записи 11 это 1011)\n'
                 '```',
  'starter_code': 'def solution(n: int) -> int:\n    pass\n',
  'reference_solution': "def solution(x):\n    return bin(n).count('1'),",
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['bit-manipulation'],
  'tests': [('11', '3', False),
            ('128', '1', False),
            ('2147483645', '30', False),
            ('0', '0', False),
            ('1', '1', False),
            ('2', '1', False),
            ('3', '2', False),
            ('7', '3', False),
            ('15', '4', False),
            ('255', '8', False),
            ('1023', '10', False)]},
 {'slug': 'leetcode-happy-number',
  'title': 'Happy Number',
  'difficulty': 'easy',
  'description': 'Счастливое число — число, которое в процессе последовательной замены на сумму квадратов своих цифр в '
                 'итоге сходится к 1. Если процесс зацикливается без 1 — число несчастливое. Верните `True`, если `n` '
                 'счастливое, иначе `False`.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(19)  # Вернет: True (1^2 + 9^2 = 82 -> 8^2 + 2^2 = 68 -> ... -> 1)\n'
                 '```',
  'starter_code': 'def solution(n: int) -> bool:\n    pass\n',
  'reference_solution': 'def solution(n):\n'
                        '    seen = set()\n'
                        '    while n != 1 and n not in seen:\n'
                        '        seen.add(n)\n'
                        '        n = sum(int(d)**2 for d in str(n))\n'
                        '    return n == 1',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['hash-table', 'math'],
  'tests': [('19', 'True', False),
            ('2', 'False', False),
            ('1', 'True', False),
            ('7', 'True', False),
            ('4', 'False', False),
            ('10', 'True', False),
            ('28', 'True', False),
            ('100', 'True', False),
            ('111', 'False', False),
            ('3', 'False', False),
            ('20', 'False', False)]},
 {'slug': 'leetcode-reverse-string',
  'title': 'Reverse String',
  'difficulty': 'easy',
  'description': 'Напишите функцию, которая принимает строку `s` и возвращает строку, записанную задом наперед.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("hello")  # Вернет: "olleh"\n'
                 '```',
  'starter_code': 'def solution(s: str) -> str:\n    pass\n',
  'reference_solution': 'def solution(x):\n    return s[::-1],',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['two-pointers', 'strings'],
  'tests': [("'hello'", 'olleh', False),
            ("'Hannah'", 'hannaH', False),
            ("''", '', False),
            ("'Python'", 'nohtyP', False),
            ("'a'", 'a', False),
            ("'racecar'", 'racecar', False),
            ("'12345'", '54321', False),
            ("'SmartCode'", 'edoCtramS', False),
            ("'ab'", 'ba', False),
            ("'space '", ' ecaps', False),
            ("'UPPER lower'", 'rewol REPPU', False)]},
 {'slug': 'leetcode-power-of-two',
  'title': 'Power of Two',
  'difficulty': 'easy',
  'description': 'Определите, является ли целое число `n` степенью двойки (n = 2^x).\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(16)  # Вернет: True (так как 2^4 = 16)\n'
                 '```',
  'starter_code': 'def solution(n: int) -> bool:\n    pass\n',
  'reference_solution': 'def solution(x):\n    return n > 0 and (n & (n - 1)) == 0,',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['bit-manipulation', 'math'],
  'tests': [('1', 'True', False),
            ('16', 'True', False),
            ('3', 'False', False),
            ('0', 'False', False),
            ('2', 'True', False),
            ('4', 'True', False),
            ('8', 'True', False),
            ('5', 'False', False),
            ('6', 'False', False),
            ('1024', 'True', False),
            ('-16', 'False', False)]},
 {'slug': 'leetcode-power-of-three',
  'title': 'Power of Three',
  'difficulty': 'easy',
  'description': 'Определите, является ли целое число `n` степенью тройки (n = 3^x).\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(27)  # Вернет: True (так как 3^3 = 27)\n'
                 '```',
  'starter_code': 'def solution(n: int) -> bool:\n    pass\n',
  'reference_solution': 'def solution(n):\n'
                        '    if n <= 0: return False\n'
                        '    while n % 3 == 0: n //= 3\n'
                        '    return n == 1',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['math'],
  'tests': [('27', 'True', False),
            ('0', 'False', False),
            ('-1', 'False', False),
            ('9', 'True', False),
            ('1', 'True', False),
            ('3', 'True', False),
            ('81', 'True', False),
            ('45', 'False', False),
            ('243', 'True', False),
            ('6', 'False', False),
            ('18', 'False', False)]},
 {'slug': 'leetcode-ugly-number',
  'title': 'Ugly Number',
  'difficulty': 'easy',
  'description': 'Уродливое число — положительное число, простые делители которого ограничены числами 2, 3 и 5. '
                 'Верните `True`, если `n` уродливое, иначе `False`.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(6)  # Вернет: True (делители 2 и 3)\n'
                 '```',
  'starter_code': 'def solution(n: int) -> bool:\n    pass\n',
  'reference_solution': 'def solution(n):\n'
                        '    if n <= 0: return False\n'
                        '    for p in (2, 3, 5):\n'
                        '        while n % p == 0: n //= p\n'
                        '    return n == 1',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['math'],
  'tests': [('6', 'True', False),
            ('1', 'True', False),
            ('14', 'False', False),
            ('-6', 'False', False),
            ('8', 'True', False),
            ('10', 'True', False),
            ('12', 'True', False),
            ('15', 'True', False),
            ('7', 'False', False),
            ('25', 'True', False),
            ('30', 'True', False)]},
 {'slug': 'leetcode-word-pattern',
  'title': 'Word Pattern',
  'difficulty': 'easy',
  'description': 'Даны шаблон `pattern` и строка слов `s`. Проверьте, соответствует ли строка `s` шаблону `pattern` '
                 '(биективное соответствие символов и слов).\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("abba", "dog cat cat dog")  # Вернет: True\n'
                 '```',
  'starter_code': 'def solution(pattern: str, s: str) -> bool:\n    pass\n',
  'reference_solution': 'def solution(pattern, s):\n'
                        '    words = s.split()\n'
                        '    if len(pattern) != len(words): return False\n'
                        '    return len(set(zip(pattern, words))) == len(set(pattern)) == len(set(words))',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['hash-table', 'strings'],
  'tests': [("'abba', 'dog cat cat dog'", 'True', False),
            ("'abba', 'dog cat cat fish'", 'False', False),
            ("'aaaa', 'dog cat cat dog'", 'False', False),
            ("'abba', 'dog dog dog dog'", 'False', False),
            ("'a', 'dog'", 'True', False),
            ("'ab', 'dog dog'", 'False', False),
            ("'abc', 'dog cat fish'", 'True', False),
            ("'aaa', 'aa aa aa'", 'True', False),
            ("'abba', 'cat dog dog cat'", 'True', False),
            ("'abc', 'b c a'", 'True', False),
            ("'aba', 'dog cat dog'", 'True', False)]},
 {'slug': 'leetcode-nim-game',
  'title': 'Nim Game',
  'difficulty': 'easy',
  'description': 'Вы играете в игру Ним с кучкой из `n` камней. Вы ходите первым. Каждый ход можно взять от 1 до 3 '
                 'камней. Побеждает взявший последний камень. Верните `True`, если вы можете гарантированно победить '
                 'при оптимальной игре обоих участников.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(4)  # Вернет: False\n'
                 '```',
  'starter_code': 'def solution(n: int) -> bool:\n    pass\n',
  'reference_solution': 'def solution(x):\n    return n % 4 != 0,',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['brainteaser', 'math'],
  'tests': [('4', 'False', False),
            ('1', 'True', False),
            ('2', 'True', False),
            ('8', 'False', False),
            ('3', 'True', False),
            ('5', 'True', False),
            ('6', 'True', False),
            ('7', 'True', False),
            ('9', 'True', False),
            ('12', 'False', False),
            ('15', 'True', False)]},
 {'slug': 'leetcode-counting-bits',
  'title': 'Counting Bits',
  'difficulty': 'easy',
  'description': 'Дано целое число `n`. Верните массив длины `n + 1`, где `ans[i]` — количество единиц в двоичной '
                 'записи числа `i`.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(5)  # Вернет: [0, 1, 1, 2, 1, 2]\n'
                 '```',
  'starter_code': 'def solution(n: int) -> list:\n    pass\n',
  'reference_solution': "def solution(x):\n    return [bin(i).count('1') for i in range(n + 1)],",
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['bit-manipulation', 'dynamic-programming'],
  'tests': [('2', '[0, 1, 1]', False),
            ('5', '[0, 1, 1, 2, 1, 2]', False),
            ('0', '[0]', False),
            ('1', '[0, 1]', False),
            ('3', '[0, 1, 1, 2]', False),
            ('4', '[0, 1, 1, 2, 1]', False),
            ('6', '[0, 1, 1, 2, 1, 2, 2]', False),
            ('7', '[0, 1, 1, 2, 1, 2, 2, 3]', False),
            ('8', '[0, 1, 1, 2, 1, 2, 2, 3, 1]', False),
            ('9', '[0, 1, 1, 2, 1, 2, 2, 3, 1, 2]', False),
            ('10', '[0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2]', False)]},
 {'slug': 'leetcode-power-of-four',
  'title': 'Power of Four',
  'difficulty': 'easy',
  'description': 'Определите, является ли целое число `n` степенью четверки (n = 4^x).\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(16)  # Вернет: True (так как 4^2 = 16)\n'
                 '```',
  'starter_code': 'def solution(n: int) -> bool:\n    pass\n',
  'reference_solution': 'def solution(n):\n'
                        '    if n <= 0: return False\n'
                        '    while n % 4 == 0: n //= 4\n'
                        '    return n == 1',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['bit-manipulation', 'math'],
  'tests': [('16', 'True', False),
            ('5', 'False', False),
            ('1', 'True', False),
            ('8', 'False', False),
            ('4', 'True', False),
            ('64', 'True', False),
            ('256', 'True', False),
            ('0', 'False', False),
            ('-4', 'False', False),
            ('2', 'False', False),
            ('12', 'False', False)]},
 {'slug': 'leetcode-reverse-vowels-of-a-string',
  'title': 'Reverse Vowels of a String',
  'difficulty': 'easy',
  'description': 'Дана строка `s`. Разверните только гласные буквы (`a, e, i, o, u` в любом регистре), сохранив '
                 'позиции согласных.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("IceCreAm")  # Вернет: "AceCreIm"\n'
                 '```',
  'starter_code': 'def solution(s: str) -> str:\n    pass\n',
  'reference_solution': 'def solution(s):\n'
                        "    vowels = set('aeiouAEIOU')\n"
                        '    chars = list(s)\n'
                        '    i, j = 0, len(chars) - 1\n'
                        '    while i < j:\n'
                        '        if chars[i] not in vowels: i += 1\n'
                        '        elif chars[j] not in vowels: j -= 1\n'
                        '        else:\n'
                        '            chars[i], chars[j] = chars[j], chars[i]\n'
                        '            i += 1; j -= 1\n'
                        "    return ''.join(chars)",
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['two-pointers', 'strings'],
  'tests': [("'IceCreAm'", 'AceCreIm', False),
            ("'leetcode'", 'leotcede', False),
            ("'a.'", 'a.', False),
            ("'hello'", 'holle', False),
            ("'AEIOU'", 'UOIEA', False),
            ("'rhythm'", 'rhythm', False),
            ("'Design'", 'Disegn', False),
            ("'programming'", 'prigrammong', False),
            ("'world'", 'world', False),
            ("'aA'", 'Aa', False),
            ("''", '', False)]},
 {'slug': 'leetcode-intersection-of-two-arrays',
  'title': 'Intersection of Two Arrays',
  'difficulty': 'easy',
  'description': 'Даны два массива `nums1` и `nums2`. Верните отсортированный по возрастанию массив их уникального '
                 'пересечения.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([1, 2, 2, 1], [2, 2])  # Вернет: [2]\n'
                 '```',
  'starter_code': 'def solution(nums1: list, nums2: list) -> list:\n    pass\n',
  'reference_solution': 'def solution(x):\n    return sorted(list(set(n1) & set(n2))),',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['hash-table', 'arrays'],
  'tests': [('[1, 2, 2, 1], [2, 2]', '[2]', False),
            ('[4, 9, 5], [9, 4, 9, 8, 4]', '[4, 9]', False),
            ('[1, 2, 3], [4, 5, 6]', '[]', False),
            ('[], [1, 2]', '[]', False),
            ('[1], [1]', '[1]', False),
            ('[1, 2, 3], [1, 2, 3]', '[1, 2, 3]', False),
            ('[5, 5, 5], [5]', '[5]', False),
            ('[1, 3, 5, 7], [2, 3, 6, 7]', '[3, 7]', False),
            ('[-1, 0, 1], [0, 2]', '[0]', False),
            ('[10, 20, 30], [20, 40]', '[20]', False),
            ('[1, 2], []', '[]', False)]},
 {'slug': 'leetcode-first-unique-character-in-a-string',
  'title': 'First Unique Character in a String',
  'difficulty': 'easy',
  'description': 'Найдите первый неповторяющийся символ в строке `s` и верните его индекс. Если такого символа нет, '
                 'верните `-1`.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("leetcode")  # Вернет: 0 (буква \'l\' встречается один раз)\n'
                 '```',
  'starter_code': 'def solution(s: str) -> int:\n    pass\n',
  'reference_solution': 'def solution(s):\n'
                        '    from collections import Counter\n'
                        '    c = Counter(s)\n'
                        '    for i, ch in enumerate(s):\n'
                        '        if c[ch] == 1: return i\n'
                        '    return -1',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['hash-table', 'strings'],
  'tests': [("'leetcode'", '0', False),
            ("'loveleetcode'", '2', False),
            ("'aabb'", '-1', False),
            ("'z'", '0', False),
            ("'abcabc'", '-1', False),
            ("'swiss'", '1', False),
            ("'unique'", '1', False),
            ("'dddccdbba'", '8', False),
            ("'a'", '0', False),
            ("''", '-1', False),
            ("'character'", '1', False)]},
 {'slug': 'leetcode-find-the-difference',
  'title': 'Find the Difference',
  'difficulty': 'easy',
  'description': 'Строка `t` получена перемешиванием строки `s` и добавлением одной случайной буквы. Найдите и верните '
                 'добавленную букву.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("abcd", "abcde")  # Вернет: "e"\n'
                 '```',
  'starter_code': 'def solution(s: str, t: str) -> str:\n    pass\n',
  'reference_solution': 'def solution(s, t):\n'
                        '    from collections import Counter\n'
                        '    diff = Counter(t) - Counter(s)\n'
                        '    return list(diff.keys())[0]',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['bit-manipulation', 'hash-table', 'strings'],
  'tests': [("'abcd', 'abcde'", 'e', False),
            ("'', 'y'", 'y', False),
            ("'a', 'aa'", 'a', False),
            ("'ae', 'aea'", 'a', False),
            ("'xyz', 'zxya'", 'a', False),
            ("'hello', 'oheall'", 'a', False),
            ("'test', 'ttest'", 't', False),
            ("'abc', 'abcb'", 'b', False),
            ("'python', 'pythons'", 's', False),
            ("'code', 'cedco'", 'c', False),
            ("'smart', 'tramps'", 'p', False)]},
 {'slug': 'leetcode-is-subsequence',
  'title': 'Is Subsequence',
  'difficulty': 'easy',
  'description': 'Даны две строки `s` и `t`. Проверьте, является ли `s` подпоследовательностью `t`.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("abc", "ahbgdc")  # Вернет: True\n'
                 '```',
  'starter_code': 'def solution(s: str, t: str) -> bool:\n    pass\n',
  'reference_solution': 'def solution(s, t):\n    it = iter(t)\n    return all(c in it for c in s)',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['dynamic-programming', 'two-pointers', 'strings'],
  'tests': [("'abc', 'ahbgdc'", 'True', False),
            ("'axc', 'ahbgdc'", 'False', False),
            ("'', 'anystring'", 'True', False),
            ("'', ''", 'True', False),
            ("'b', 'c'", 'False', False),
            ("'ace', 'abcde'", 'True', False),
            ("'aec', 'abcde'", 'False', False),
            ("'hello', 'hello'", 'True', False),
            ("'sing', 'string'", 'True', False),
            ("'sub', 'subsequence'", 'True', False),
            ("'test', 'testing'", 'True', False)]},
 {'slug': 'leetcode-third-maximum-number',
  'title': 'Third Maximum Number',
  'difficulty': 'easy',
  'description': 'Дан целочисленный массив `nums`. Верните третье по величине уникальное число. Если третьего '
                 'максимума нет, верните максимальное число.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([3, 2, 1])  # Вернет: 1\n'
                 '```',
  'starter_code': 'def solution(nums: list) -> int:\n    pass\n',
  'reference_solution': 'def solution(nums):\n'
                        '    u = sorted(set(nums), reverse=True)\n'
                        '    return u[2] if len(u) >= 3 else u[0]',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['sorting', 'arrays'],
  'tests': [('[3, 2, 1]', '1', False),
            ('[1, 2]', '2', False),
            ('[2, 2, 3, 1]', '1', False),
            ('[1]', '1', False),
            ('[5, 2, 4, 1, 3]', '3', False),
            ('[-1, 2, 3]', '-1', False),
            ('[1, 1, 2]', '2', False),
            ('[1, 2, -2147483648]', '-2147483648', False),
            ('[10, 9, 8, 7, 6]', '8', False),
            ('[2, 2, 2]', '2', False),
            ('[1, 2, 2, 5, 3, 5]', '2', False)]},
 {'slug': 'leetcode-add-strings',
  'title': 'Add Strings',
  'difficulty': 'easy',
  'description': 'Даны два неотрицательных числа в виде строк `num1` и `num2`. Сложите их и верните результат в виде '
                 'строки.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("11", "123")  # Вернет: "134"\n'
                 '```',
  'starter_code': 'def solution(num1: str, num2: str) -> str:\n    pass\n',
  'reference_solution': 'def solution(x):\n    return str(int(n1) + int(n2)),',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['math', 'strings'],
  'tests': [("'11', '123'", '134', False),
            ("'456', '77'", '533', False),
            ("'0', '0'", '0', False),
            ("'999', '1'", '1000', False),
            ("'1', '9'", '10', False),
            ("'123456789', '987654321'", '1111111110', False),
            ("'50', '50'", '100', False),
            ("'100', '200'", '300', False),
            ("'99', '99'", '198', False),
            ("'1000', '1'", '1001', False),
            ("'45', '55'", '100', False)]},
 {'slug': 'leetcode-number-of-segments-in-a-string',
  'title': 'Number of Segments in a String',
  'difficulty': 'easy',
  'description': 'Дана строка `s`. Верните количество сегментов (последовательностей непробельных символов).\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("Hello, my name is John")  # Вернет: 5\n'
                 '```',
  'starter_code': 'def solution(s: str) -> int:\n    pass\n',
  'reference_solution': 'def solution(x):\n    return len(s.split()),',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['strings'],
  'tests': [("'Hello, my name is John'", '5', False),
            ("'Hello'", '1', False),
            ("''", '0', False),
            ("'                '", '0', False),
            ("'one two three'", '3', False),
            ("'   leading and trailing   '", '3', False),
            ("'a b c d e'", '5', False),
            ("'word1   word2   word3'", '3', False),
            ("'!@#$%^&*()'", '1', False),
            ("'single'", '1', False),
            ("'multiple spaces    between    words'", '4', False)]},
 {'slug': 'leetcode-arranging-coins',
  'title': 'Arranging Coins',
  'difficulty': 'easy',
  'description': 'У вас есть `n` монет для постройки лестницы, где на k-й ступени должно быть ровно k монет. Верните '
                 'количество полностью заполненных рядов.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(5)  # Вернет: 2 (ряды: 1 монета, 2 монеты; на 3-й ряд из 3 монет не хватает)\n'
                 '```',
  'starter_code': 'def solution(n: int) -> int:\n    pass\n',
  'reference_solution': 'def solution(n):\n    import math\n    return int((math.sqrt(1 + 8*n) - 1) // 2)',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['binary-search', 'math'],
  'tests': [('5', '2', False),
            ('8', '3', False),
            ('1', '1', False),
            ('0', '0', False),
            ('3', '2', False),
            ('6', '3', False),
            ('10', '4', False),
            ('15', '5', False),
            ('16', '5', False),
            ('2', '1', False),
            ('20', '5', False)]},
 {'slug': 'leetcode-find-all-numbers-disappeared-in-an-array',
  'title': 'Find All Numbers Disappeared in an Array',
  'difficulty': 'easy',
  'description': 'Дан массив `nums` из n чисел, где каждое число находится в диапазоне [1, n]. Верните отсортированный '
                 'список всех чисел от 1 до n, отсутствующих в `nums`.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([4, 3, 2, 7, 8, 2, 3, 1])  # Вернет: [5, 6]\n'
                 '```',
  'starter_code': 'def solution(nums: list) -> list:\n    pass\n',
  'reference_solution': 'def solution(nums):\n'
                        '    n = len(nums)\n'
                        '    s = set(nums)\n'
                        '    return [i for i in range(1, n + 1) if i not in s]',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['hash-table', 'arrays'],
  'tests': [('[4, 3, 2, 7, 8, 2, 3, 1]', '[5, 6]', False),
            ('[1, 1]', '[2]', False),
            ('[1]', '[]', False),
            ('[2, 2]', '[1]', False),
            ('[1, 2, 3]', '[]', False),
            ('[3, 3, 3]', '[1, 2]', False),
            ('[1, 2, 2, 4]', '[3]', False),
            ('[5, 4, 3, 2, 1]', '[]', False),
            ('[1, 1, 2, 2]', '[3, 4]', False),
            ('[4, 4, 4, 4]', '[1, 2, 3]', False),
            ('[1, 3, 3]', '[2]', False)]},
 {'slug': 'leetcode-assign-cookies',
  'title': 'Assign Cookies',
  'difficulty': 'easy',
  'description': 'Каждому ребенку i требуется печенье размером не менее g[i]. У вас есть печенья с размерами s. '
                 'Каждому ребенку можно дать максимум одно печенье. Максимизируйте количество довольных детей.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([1, 2, 3], [1, 1])  # Вернет: 1\n'
                 '```',
  'starter_code': 'def solution(g: list, s: list) -> int:\n    pass\n',
  'reference_solution': 'def solution(g, s):\n'
                        '    g_sorted, s_sorted = sorted(g), sorted(s)\n'
                        '    i = j = 0\n'
                        '    while i < len(g_sorted) and j < len(s_sorted):\n'
                        '        if s_sorted[j] >= g_sorted[i]:\n'
                        '            i += 1\n'
                        '        j += 1\n'
                        '    return i',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['greedy', 'sorting', 'arrays'],
  'tests': [('[1, 2, 3], [1, 1]', '1', False),
            ('[1, 2], [1, 2, 3]', '2', False),
            ('[1, 2, 3], []', '0', False),
            ('[], [1, 2]', '0', False),
            ('[1, 2, 3], [3]', '1', False),
            ('[10, 9, 8, 7], [5, 6, 7, 8]', '2', False),
            ('[1, 1, 1], [1, 1, 1]', '3', False),
            ('[5], [5]', '1', False),
            ('[2, 4], [1, 3, 5]', '2', False),
            ('[1, 2, 3, 4], [2, 3]', '2', False),
            ('[1, 5], [2, 4, 6]', '2', False)]},
 {'slug': 'leetcode-repeated-substring-pattern',
  'title': 'Repeated Substring Pattern',
  'difficulty': 'easy',
  'description': 'Проверьте, можно ли составить непустую строку `s`, повторив одну из её подстрок два или более раз.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("abab")  # Вернет: True (подстрока "ab" повторена 2 раза)\n'
                 '```',
  'starter_code': 'def solution(s: str) -> bool:\n    pass\n',
  'reference_solution': 'def solution(x):\n    return s in (s + s)[1:-1],',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['string-matching', 'strings'],
  'tests': [("'abab'", 'True', False),
            ("'aba'", 'False', False),
            ("'abcabcabcabc'", 'True', False),
            ("'a'", 'False', False),
            ("'aa'", 'True', False),
            ("'aaa'", 'True', False),
            ("'abac'", 'False', False),
            ("'abcabc'", 'True', False),
            ("'abcdabcd'", 'True', False),
            ("'abaababaab'", 'True', False),
            ("'xyzxyzxyz'", 'True', False)]},
 {'slug': 'leetcode-hamming-distance',
  'title': 'Hamming Distance',
  'difficulty': 'easy',
  'description': 'Расстояние Хэмминга между двумя целыми числами — это количество позиций, в которых соответствующие '
                 'биты различаются. Вычислите это расстояние для `x` и `y`.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(1, 4)  # Вернет: 2 (1 = 001_2, 4 = 100_2, различаются 2 бита)\n'
                 '```',
  'starter_code': 'def solution(x: int, y: int) -> int:\n    pass\n',
  'reference_solution': "def solution(x):\n    return bin(x ^ y).count('1'),",
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['bit-manipulation'],
  'tests': [('1, 4', '2', False),
            ('3, 1', '1', False),
            ('0, 0', '0', False),
            ('1, 1', '0', False),
            ('0, 1', '1', False),
            ('7, 0', '3', False),
            ('15, 15', '0', False),
            ('8, 7', '4', False),
            ('93, 73', '2', False),
            ('100, 200', '4', False),
            ('255, 0', '8', False)]},
 {'slug': 'leetcode-island-perimeter',
  'title': 'Island Perimeter',
  'difficulty': 'easy',
  'description': 'Дана сетка `grid`, где 1 представляет сушу, а 0 — воду. Остров ровно один и не имеет внутренних '
                 'озер. Вычислите его периметр.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([[0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [1, 1, 0, 0]])  # Вернет: 16\n'
                 '```',
  'starter_code': 'def solution(grid: list) -> int:\n    pass\n',
  'reference_solution': 'def solution(grid):\n'
                        '    p = 0\n'
                        '    for r in range(len(grid)):\n'
                        '        for c in range(len(grid[0])):\n'
                        '            if grid[r][c] == 1:\n'
                        '                p += 4\n'
                        '                if r > 0 and grid[r-1][c] == 1: p -= 2\n'
                        '                if c > 0 and grid[r][c-1] == 1: p -= 2\n'
                        '    return p',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['matrix', 'arrays'],
  'tests': [('[[0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [1, 1, 0, 0]]', '16', False),
            ('[[1]]', '4', False),
            ('[[1, 0]]', '4', False),
            ('[[1, 1], [1, 1]]', '8', False),
            ('[[1, 1, 1]]', '8', False),
            ('[[1], [1], [1]]', '8', False),
            ('[[0, 1], [1, 1]]', '8', False),
            ('[[1, 1, 0], [0, 1, 0]]', '8', False),
            ('[[0, 0], [0, 1]]', '4', False),
            ('[[1, 1, 1, 1]]', '10', False),
            ('[[1, 1], [0, 1]]', '8', False)]},
 {'slug': 'leetcode-license-key-formatting',
  'title': 'License Key Formatting',
  'difficulty': 'easy',
  'description': 'Дан лицензионный ключ `s` и число `k`. Отформатируйте строку так, чтобы каждая группа содержала '
                 'ровно `k` символов в верхнем регистре, разделённых дефисом (кроме первой группы, которая может быть '
                 'короче).\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("5F3Z-2e-9-w", 4)  # Вернет: "5F3Z-2E9W"\n'
                 '```',
  'starter_code': 'def solution(s: str, k: int) -> str:\n    pass\n',
  'reference_solution': 'def solution(s, k):\n'
                        "    clean = s.replace('-', '').upper()\n"
                        '    res = []\n'
                        '    rem = len(clean) % k\n'
                        '    if rem: res.append(clean[:rem])\n'
                        '    for i in range(rem, len(clean), k):\n'
                        '        res.append(clean[i:i+k])\n'
                        "    return '-'.join(res)",
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['strings'],
  'tests': [("'5F3Z-2e-9-w', 4", '5F3Z-2E9W', False),
            ("'2-5g-3-J', 2", '2-5G-3J', False),
            ("'---', 3", '', False),
            ("'a-a-a-a-', 1", 'A-A-A-A', False),
            ("'2-4A0r7-4k', 4", '24A0-R74K', False),
            ("'r', 1", 'R', False),
            ("'abc-def-ghi', 3", 'ABC-DEF-GHI', False),
            ("'12345', 2", '1-23-45', False),
            ("'a0001af4-5', 4", 'A-0001-AF45', False),
            ("'j-k-l', 2", 'J-KL', False),
            ("'AbCd-EfGh', 4", 'ABCD-EFGH', False)]},
 {'slug': 'leetcode-max-consecutive-ones',
  'title': 'Max Consecutive Ones',
  'difficulty': 'easy',
  'description': 'Дан двоичный массив `nums`. Найдите максимальное количество последовательных единиц в массиве.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([1, 1, 0, 1, 1, 1])  # Вернет: 3\n'
                 '```',
  'starter_code': 'def solution(nums: list) -> int:\n    pass\n',
  'reference_solution': 'def solution(x):\n'
                        "    return max((len(x) for x in ''.join(map(str, nums)).split('0')), default=0),",
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['arrays'],
  'tests': [('[1, 1, 0, 1, 1, 1]', '3', False),
            ('[1, 0, 1, 1, 0, 1]', '2', False),
            ('[0, 0, 0]', '0', False),
            ('[1, 1, 1, 1]', '4', False),
            ('[0]', '0', False),
            ('[1]', '1', False),
            ('[1, 0]', '1', False),
            ('[0, 1]', '1', False),
            ('[1, 1, 0, 0, 1, 1, 1, 1, 0]', '4', False),
            ('[1, 0, 1, 0, 1]', '1', False),
            ('[0, 1, 1, 0, 1, 1, 1]', '3', False)]},
 {'slug': 'leetcode-base-7',
  'title': 'Base 7',
  'difficulty': 'easy',
  'description': 'Дано целое число `num`. Верните его строковое представление в семеричной системе счисления (по '
                 'основанию 7).\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(100)  # Вернет: "202" (2*49 + 0*7 + 2 = 100)\n'
                 '```',
  'starter_code': 'def solution(num: int) -> str:\n    pass\n',
  'reference_solution': 'def solution(n):\n'
                        "    if n == 0: return '0'\n"
                        '    neg = n < 0\n'
                        '    n = abs(n)\n'
                        '    res = []\n'
                        '    while n:\n'
                        '        res.append(str(n % 7))\n'
                        '        n //= 7\n'
                        "    if neg: res.append('-')\n"
                        "    return ''.join(reversed(res))",
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['math'],
  'tests': [('100', '202', False),
            ('-7', '-10', False),
            ('0', '0', False),
            ('7', '10', False),
            ('49', '100', False),
            ('1', '1', False),
            ('-1', '-1', False),
            ('48', '66', False),
            ('350', '1010', False),
            ('-100', '-202', False),
            ('14', '20', False)]},
 {'slug': 'leetcode-relative-ranks',
  'title': 'Relative Ranks',
  'difficulty': 'easy',
  'description': "Дан массив `score` с баллами спортсменов. Присвойте им ранги: 1-е место — 'Gold Medal', 2-е — "
                 "'Silver Medal', 3-е — 'Bronze Medal', а остальным — их порядковый номер в виде строки.\n"
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([5, 4, 3, 2, 1])  # Вернет: ["Gold Medal", "Silver Medal", "Bronze Medal", "4", "5"]\n'
                 '```',
  'starter_code': 'def solution(score: list) -> list:\n    pass\n',
  'reference_solution': 'def solution(score):\n'
                        '    ranks = {s: i for i, s in enumerate(sorted(score, reverse=True))}\n'
                        "    medals = {0: 'Gold Medal', 1: 'Silver Medal', 2: 'Bronze Medal'}\n"
                        '    return [medals.get(ranks[s], str(ranks[s] + 1)) for s in score]',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['sorting', 'arrays'],
  'tests': [('[5, 4, 3, 2, 1]', "['Gold Medal', 'Silver Medal', 'Bronze Medal', '4', '5']", False),
            ('[10, 3, 8, 9, 4]', "['Gold Medal', '5', 'Bronze Medal', 'Silver Medal', '4']", False),
            ('[1]', "['Gold Medal']", False),
            ('[1, 2]', "['Silver Medal', 'Gold Medal']", False),
            ('[3, 2, 1]', "['Gold Medal', 'Silver Medal', 'Bronze Medal']", False),
            ('[12, 15, 10]', "['Silver Medal', 'Gold Medal', 'Bronze Medal']", False),
            ('[100, 50, 75, 25]', "['Gold Medal', 'Bronze Medal', 'Silver Medal', '4']", False),
            ('[4, 1, 2, 3]', "['Gold Medal', '4', 'Bronze Medal', 'Silver Medal']", False),
            ('[9, 8, 7, 6, 5, 4, 3, 2, 1]',
             "['Gold Medal', 'Silver Medal', 'Bronze Medal', '4', '5', '6', '7', '8', '9']",
             False),
            ('[2, 1]', "['Gold Medal', 'Silver Medal']", False),
            ('[1, 3, 2]', "['Bronze Medal', 'Gold Medal', 'Silver Medal']", False)]},
 {'slug': 'leetcode-perfect-number',
  'title': 'Perfect Number',
  'difficulty': 'easy',
  'description': 'Совершенное число — положительное целое число, равное сумме всех своих собственных положительных '
                 'делителей (исключая само число). Верните `True`, если `num` совершенно, иначе `False`.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(28)  # Вернет: True (1 + 2 + 4 + 7 + 14 = 28)\n'
                 '```',
  'starter_code': 'def solution(num: int) -> bool:\n    pass\n',
  'reference_solution': 'def solution(n):\n'
                        '    if n <= 1: return False\n'
                        '    s = 1\n'
                        '    for i in range(2, int(n**0.5) + 1):\n'
                        '        if n % i == 0:\n'
                        '            s += i\n'
                        '            if i * i != n: s += n // i\n'
                        '    return s == n',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['math'],
  'tests': [('28', 'True', False),
            ('7', 'False', False),
            ('6', 'True', False),
            ('1', 'False', False),
            ('496', 'True', False),
            ('8128', 'True', False),
            ('2', 'False', False),
            ('3', 'False', False),
            ('12', 'False', False),
            ('16', 'False', False),
            ('33550336', 'True', False)]},
 {'slug': 'leetcode-fibonacci-number',
  'title': 'Fibonacci Number',
  'difficulty': 'easy',
  'description': 'Вычислите n-е число Фибоначчи: F(0) = 0, F(1) = 1, F(n) = F(n - 1) + F(n - 2).\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(4)  # Вернет: 3 (F(0)=0, F(1)=1, F(2)=1, F(3)=2, F(4)=3)\n'
                 '```',
  'starter_code': 'def solution(n: int) -> int:\n    pass\n',
  'reference_solution': 'def solution(n):\n    a, b = 0, 1\n    for _ in range(n): a, b = b, a + b\n    return a',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['dynamic-programming', 'math'],
  'tests': [('2', '1', False),
            ('3', '2', False),
            ('4', '3', False),
            ('0', '0', False),
            ('1', '1', False),
            ('5', '5', False),
            ('6', '8', False),
            ('7', '13', False),
            ('8', '21', False),
            ('10', '55', False),
            ('15', '610', False)]},
 {'slug': 'leetcode-detect-capital',
  'title': 'Detect Capital',
  'difficulty': 'easy',
  'description': "Проверьте правильность использования заглавных букв в слове `word`: все заглавные ('USA'), все "
                 "строчные ('leetcode') или только первая заглавная ('Google').\n"
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("USA")  # Вернет: True\n'
                 '```',
  'starter_code': 'def solution(word: str) -> bool:\n    pass\n',
  'reference_solution': 'def solution(x):\n    return w.isupper() or w.islower() or w.istitle(),',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['strings'],
  'tests': [("'USA'", 'True', False),
            ("'FlaG'", 'False', False),
            ("'Google'", 'True', False),
            ("'leetcode'", 'True', False),
            ("'c'", 'True', False),
            ("'C'", 'True', False),
            ("'mL'", 'False', False),
            ("'leetcodE'", 'False', False),
            ("'Hello'", 'True', False),
            ("'WORLD'", 'True', False),
            ("'Python'", 'True', False)]},
 {'slug': 'leetcode-reverse-words-in-a-string-iii',
  'title': 'Reverse Words in a String III',
  'difficulty': 'easy',
  'description': 'Дана строка `s`. Разверните порядок символов в каждом слове, сохраняя пробелы и начальный порядок '
                 'слов.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("Let\'s take LeetCode contest")  # Вернет: "s\'teL ekat edoCteeL tsetnoc"\n'
                 '```',
  'starter_code': 'def solution(s: str) -> str:\n    pass\n',
  'reference_solution': "def solution(x):\n    return ' '.join(w[::-1] for w in s.split(' ')),",
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['two-pointers', 'strings'],
  'tests': [("'Let\\'s take LeetCode contest'", "s'teL ekat edoCteeL tsetnoc", False),
            ("'God Ding'", 'doG gniD', False),
            ("'Python'", 'nohtyP', False),
            ("'a b c'", 'a b c', False),
            ("'hello world'", 'olleh dlrow', False),
            ("'word'", 'drow', False),
            ("'The quick brown fox'", 'ehT kciuq nworb xof', False),
            ("'jumps over the lazy dog'", 'spmuj revo eht yzal god', False),
            ("'abc def'", 'cba fed', False),
            ("'123 456'", '321 654', False),
            ("'racecar level'", 'racecar level', False)]},
 {'slug': 'leetcode-array-partition',
  'title': 'Array Partition',
  'difficulty': 'easy',
  'description': 'Дан целочисленный массив `nums` из 2n элементов. Сгруппируйте их в пары (a_i, b_i) так, чтобы сумма '
                 'min(a_i, b_i) была максимально возможной. Верните эту сумму.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([1, 4, 3, 2])  # Вернет: 4 (пары: (1, 2) и (3, 4), сумма min: 1 + 3 = 4)\n'
                 '```',
  'starter_code': 'def solution(nums: list) -> int:\n    pass\n',
  'reference_solution': 'def solution(x):\n    return sum(sorted(nums)[::2]),',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['greedy', 'sorting', 'arrays'],
  'tests': [('[1, 4, 3, 2]', '4', False),
            ('[6, 2, 6, 5, 1, 2]', '9', False),
            ('[1, 2]', '1', False),
            ('[1, 1]', '1', False),
            ('[5, 6, 7, 8]', '12', False),
            ('[10, 20, 30, 40]', '40', False),
            ('[-1, -2, -3, -4]', '-6', False),
            ('[0, 0, 0, 0]', '0', False),
            ('[3, 1, 4, 2]', '4', False),
            ('[9, 1, 8, 2, 7, 3]', '12', False),
            ('[1, 5, 2, 4]', '5', False)]},
 {'slug': 'leetcode-reshape-the-matrix',
  'title': 'Reshape the Matrix',
  'difficulty': 'easy',
  'description': 'Дана матрица `mat` размера m x n и два числа r и c. Преобразуйте матрицу в размер r x c, сохраняя '
                 'построчный порядок обхода. Если преобразование невозможно, верните исходную матрицу.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([[1, 2], [3, 4]], 1, 4)  # Вернет: [[1, 2, 3, 4]]\n'
                 '```',
  'starter_code': 'def solution(mat: list, r: int, c: int) -> list:\n    pass\n',
  'reference_solution': 'def solution(mat, r, c):\n'
                        '    flat = [x for row in mat for x in row]\n'
                        '    if len(flat) != r * c: return mat\n'
                        '    return [flat[i*c:(i+1)*c] for i in range(r)]',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['matrix', 'arrays'],
  'tests': [('[[1, 2], [3, 4]], 1, 4', '[[1, 2, 3, 4]]', False),
            ('[[1, 2], [3, 4]], 2, 4', '[[1, 2], [3, 4]]', False),
            ('[[1, 2, 3, 4]], 2, 2', '[[1, 2], [3, 4]]', False),
            ('[[1, 2], [3, 4]], 4, 1', '[[1], [2], [3], [4]]', False),
            ('[[1]], 1, 1', '[[1]]', False),
            ('[[1, 2, 3], [4, 5, 6]], 3, 2', '[[1, 2], [3, 4], [5, 6]]', False),
            ('[[1, 2, 3], [4, 5, 6]], 1, 6', '[[1, 2, 3, 4, 5, 6]]', False),
            ('[[1, 2], [3, 4]], 2, 2', '[[1, 2], [3, 4]]', False),
            ('[[1, 2, 3]], 2, 2', '[[1, 2, 3]]', False),
            ('[[5, 6], [7, 8]], 1, 4', '[[5, 6, 7, 8]]', False),
            ('[[1, 2], [3, 4], [5, 6]], 2, 3', '[[1, 2, 3], [4, 5, 6]]', False)]},
 {'slug': 'leetcode-can-place-flowers',
  'title': 'Can Place Flowers',
  'difficulty': 'easy',
  'description': 'Дан массив `flowerbed` из 0 и 1, где цветы не могут расти на соседних участках. Определите, можно ли '
                 'посадить `n` новых цветов, не нарушая правила.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([1, 0, 0, 0, 1], 1)  # Вернет: True\n'
                 '```',
  'starter_code': 'def solution(flowerbed: list, n: int) -> bool:\n    pass\n',
  'reference_solution': 'def solution(flowerbed, n):\n'
                        '    fb = [0] + flowerbed + [0]\n'
                        '    cnt = 0\n'
                        '    for i in range(1, len(fb) - 1):\n'
                        '        if fb[i-1] == 0 and fb[i] == 0 and fb[i+1] == 0:\n'
                        '            fb[i] = 1\n'
                        '            cnt += 1\n'
                        '    return cnt >= n',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['greedy', 'arrays'],
  'tests': [('[1, 0, 0, 0, 1], 1', 'True', False),
            ('[1, 0, 0, 0, 1], 2', 'False', False),
            ('[0, 0, 1, 0, 0], 2', 'True', False),
            ('[0, 0, 0, 0, 0], 3', 'True', False),
            ('[0], 1', 'True', False),
            ('[1], 0', 'True', False),
            ('[1], 1', 'False', False),
            ('[0, 0, 0], 2', 'True', False),
            ('[1, 0, 0, 0, 0, 1], 2', 'False', False),
            ('[0, 1, 0], 1', 'False', False),
            ('[1, 0, 1, 0, 1], 0', 'True', False)]},
 {'slug': 'codewars-sum-of-positive',
  'title': 'Sum of Positive',
  'difficulty': 'easy',
  'description': 'Дан массив чисел `arr`. Верните сумму всех положительных чисел. Если положительных чисел нет, '
                 'верните 0.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([1, -4, 7, 12])  # Вернет: 20 (1 + 7 + 12 = 20)\n'
                 '```',
  'starter_code': 'def solution(arr: list) -> int:\n    pass\n',
  'reference_solution': 'def solution(x):\n    return sum(x for x in arr if x > 0),',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['arrays'],
  'tests': [('[1, -4, 7, 12]', '20', False),
            ('[-1, -2, -3, -4, -5]', '0', False),
            ('[]', '0', False),
            ('[1, 2, 3, 4, 5]', '15', False),
            ('[-1]', '0', False),
            ('[0]', '0', False),
            ('[10, -10, 20, -20]', '30', False),
            ('[100]', '100', False),
            ('[-5, 0, 5]', '5', False),
            ('[2, 4, 6, -8]', '12', False),
            ('[1, -1, 1, -1, 1]', '3', False)]},
 {'slug': 'codewars-opposites-attract',
  'title': 'Opposites Attract',
  'difficulty': 'easy',
  'description': 'Тимми и Сара влюблены, если у одного из них количество лепестков на цветке чётное, а у другого — '
                 'нечётное. Верните `True`, если они влюблены, и `False`, если нет.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(1, 4)  # Вернет: True\n'
                 '```',
  'starter_code': 'def solution(flower1: int, flower2: int) -> bool:\n    pass\n',
  'reference_solution': 'def solution(x):\n    return (f1 % 2) != (f2 % 2),',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['math'],
  'tests': [('1, 4', 'True', False),
            ('2, 2', 'False', False),
            ('0, 1', 'True', False),
            ('0, 0', 'False', False),
            ('5, 5', 'False', False),
            ('3, 6', 'True', False),
            ('10, 15', 'True', False),
            ('8, 9', 'True', False),
            ('12, 14', 'False', False),
            ('1, 3', 'False', False),
            ('7, 10', 'True', False)]},
 {'slug': 'codewars-youre-a-square',
  'title': "You're a Square!",
  'difficulty': 'easy',
  'description': 'Дано целое число `n`. Определите, является ли оно точным квадратом некоторого целого числа (n = '
                 'k^2). Отрицательные числа квадратами быть не могут.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(25)  # Вернет: True (5 * 5 = 25)\n'
                 '```',
  'starter_code': 'def solution(n: int) -> bool:\n    pass\n',
  'reference_solution': 'def solution(x):\n    return n >= 0 and int(n**0.5)**2 == n,',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['math'],
  'tests': [('-1', 'False', False),
            ('0', 'True', False),
            ('3', 'False', False),
            ('25', 'True', False),
            ('4', 'True', False),
            ('9', 'True', False),
            ('16', 'True', False),
            ('26', 'False', False),
            ('100', 'True', False),
            ('144', 'True', False),
            ('-4', 'False', False)]},
 {'slug': 'codewars-growth-of-a-population',
  'title': 'Growth of a Population',
  'difficulty': 'easy',
  'description': 'В городе население p_0. Каждый год оно увеличивается на percent процентов, и еще прибывает aug '
                 'жителей. Верните количество полных лет, необходимых для достижения населения не менее p.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(1500, 5, 100, 5000)  # Вернет: 15\n'
                 '```',
  'starter_code': 'def solution(p0: int, percent: float, aug: int, p: int) -> int:\n    pass\n',
  'reference_solution': 'def solution(p0, percent, aug, p):\n'
                        '    y = 0\n'
                        '    while p0 < p:\n'
                        '        p0 = int(p0 + p0 * percent / 100 + aug)\n'
                        '        y += 1\n'
                        '    return y',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['math'],
  'tests': [('1500, 5, 100, 5000', '15', False),
            ('1500000, 2.5, 10000, 2000000', '10', False),
            ('1000, 2, 50, 1200', '3', False),
            ('1500000, 0.25, 1000, 2000000', '94', False),
            ('1000, 2.0, 50, 1070', '1', False),
            ('1000, 5, 100, 2000', '6', False),
            ('500, 10, 50, 1000', '5', False),
            ('2000, 1.5, 100, 2500', '4', False),
            ('100, 1, 10, 200', '10', False),
            ('800, 3, 20, 1000', '5', False),
            ('10000, 0.5, 50, 12000', '20', False)]},
 {'slug': 'codewars-categorize-new-member',
  'title': 'Categorize New Member',
  'difficulty': 'easy',
  'description': "Клуб принимает участников в категории 'Senior' и 'Open'. Участник становится 'Senior', если ему не "
                 "менее 55 лет и его гандикап строго больше 7. Иначе он 'Open'. Дан список пар `[age, handicap]`, "
                 'верните список категорий.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([[18, 20], [45, 2], [61, 12], [37, 6]])  # Вернет: ["Open", "Open", "Senior", "Open"]\n'
                 '```',
  'starter_code': 'def solution(data: list) -> list:\n    pass\n',
  'reference_solution': 'def solution(data):\n'
                        "    return ['Senior' if age >= 55 and h > 7 else 'Open' for age, h in data]",
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['arrays'],
  'tests': [('[[18, 20], [45, 2], [61, 12], [37, 6], [21, 21], [78, 9]]',
             "['Open', 'Open', 'Senior', 'Open', 'Open', 'Senior']",
             False),
            ('[[55, 8], [55, 7], [54, 9]]', "['Senior', 'Open', 'Open']", False),
            ('[]', '[]', False),
            ('[[55, 10]]', "['Senior']", False),
            ('[[54, 10]]', "['Open']", False),
            ('[[60, 12], [20, 5]]', "['Senior', 'Open']", False),
            ('[[55, 8], [55, 8]]', "['Senior', 'Senior']", False),
            ('[[30, 0], [40, 2], [50, 5]]', "['Open', 'Open', 'Open']", False),
            ('[[70, 15], [80, 20]]', "['Senior', 'Senior']", False),
            ('[[56, 7], [55, 8]]', "['Open', 'Senior']", False),
            ('[[90, 8], [10, 10]]', "['Senior', 'Open']", False)]},
 {'slug': 'codewars-highest-and-lowest',
  'title': 'Highest and Lowest',
  'difficulty': 'easy',
  'description': 'Дана строка чисел, разделённых пробелами. Верните строку с наибольшим и наименьшим числом через '
                 "пробел (в формате 'max min').\n"
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("1 2 3 4 5")  # Вернет: "5 1"\n'
                 '```',
  'starter_code': 'def solution(numbers: str) -> str:\n    pass\n',
  'reference_solution': 'def solution(numbers):\n'
                        '    nums = list(map(int, numbers.split()))\n'
                        '    return f"{max(nums)} {min(nums)}"',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['sorting', 'strings'],
  'tests': [("'1 2 3 4 5'", '5 1', False),
            ("'1 2 -3 4 5'", '5 -3', False),
            ("'1 9 3 4 -5'", '9 -5', False),
            ("'42'", '42 42', False),
            ("'0 0 0'", '0 0', False),
            ("'8 3 -5 42 -1 0 0 -9 4 7 4 -4'", '42 -9', False),
            ("'-1 -2 -3 -4 -5'", '-1 -5', False),
            ("'100 200 50 25'", '200 25', False),
            ("'5 5 5 5'", '5 5', False),
            ("'10 -10'", '10 -10', False),
            ("'1 2 3'", '3 1', False)]},
 {'slug': 'codewars-string-ends-with',
  'title': 'String Ends With?',
  'difficulty': 'easy',
  'description': 'Определите, заканчивается ли первая строка `text` второй строкой `ending`.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("abc", "bc")  # Вернет: True\n'
                 '```',
  'starter_code': 'def solution(text: str, ending: str) -> bool:\n    pass\n',
  'reference_solution': 'def solution(x):\n    return t.endswith(e),',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['strings'],
  'tests': [("'abc', 'bc'", 'True', False),
            ("'abc', 'd'", 'False', False),
            ("'samurai', 'ai'", 'True', False),
            ("'fails', 'ails '", 'False', False),
            ("'this', ''", 'True', False),
            ("'ninja', 'ja'", 'True', False),
            ("'sensei', 'i'", 'True', False),
            ("'abc', 'abc'", 'True', False),
            ("'abc', 'abcd'", 'False', False),
            ("'banana', 'an'", 'False', False),
            ("'coding', 'ing'", 'True', False)]},
 {'slug': 'codewars-find-the-smallest-integer-in-the-array',
  'title': 'Find the Smallest Integer in the Array',
  'difficulty': 'easy',
  'description': 'Дан непустой массив целых чисел `arr`. Найдите и верните наименьшее число.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([34, 15, 88, 2])  # Вернет: 2\n'
                 '```',
  'starter_code': 'def solution(arr: list) -> int:\n    pass\n',
  'reference_solution': 'def solution(x):\n    return min(arr),',
  'reference_solution_explanation': 'Эталонное решение задачи на Python.',
  'tags': ['arrays'],
  'tests': [('[34, 15, 88, 2]', '2', False),
            ('[34, -345, -1, 100]', '-345', False),
            ('[0]', '0', False),
            ('[7, 7, 7]', '7', False),
            ('[1, 2, 3, 4, 5]', '1', False),
            ('[-5, -4, -3, -2, -1]', '-5', False),
            ('[100, 50, 25, 10]', '10', False),
            ('[999, -999]', '-999', False),
            ('[42]', '42', False),
            ('[-10, 0, 10]', '-10', False),
            ('[5, 4, 3, 2, 1, 0, -1]', '-1', False)]},
 {'slug': 'longest-substring-without-repeating-characters',
  'title': 'Longest Substring Without Repeating Characters',
  'difficulty': 'medium',
  'description': 'Дана строка `s`. Найдите длину самой длинной подстроки, не содержащей повторяющихся символов.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("abcabcbb")  # Вернет: 3 (подстрока "abc")\n'
                 '```',
  'starter_code': 'def solution(s: str) -> int:\n    pass\n',
  'reference_solution': 'def solution(s):\n'
                        '    used = {}\n'
                        '    l = max_len = 0\n'
                        '    for r, ch in enumerate(s):\n'
                        '        if ch in used and used[ch] >= l:\n'
                        '            l = used[ch] + 1\n'
                        '        used[ch] = r\n'
                        '        max_len = max(max_len, r - l + 1)\n'
                        '    return max_len',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['two-pointers', 'strings'],
  'tests': [('"abcabcbb"', '3', False),
            ('"bbbbb"', '1', False),
            ('"pwwkew"', '3', False),
            ('""', '0', False),
            ('" "', '1', False),
            ('"au"', '2', False),
            ('"dvdf"', '3', False),
            ('"anviaj"', '5', False),
            ('"tmmzuxt"', '5', False),
            ('"abcdefghijklmnopqrstuvwxyz"', '26', False)]},
 {'slug': 'container-with-most-water',
  'title': 'Container With Most Water',
  'difficulty': 'medium',
  'description': 'Дан целочисленный массив `height` длины `n`. Найдите две вертикальные линии, которые вместе с осью X '
                 'образуют контейнер, вмещающий максимальное количество воды. Верните максимальный объем воды.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([1, 8, 6, 2, 5, 4, 8, 3, 7])  # Вернет: 49\n'
                 '```',
  'starter_code': 'def solution(height: list) -> int:\n    pass\n',
  'reference_solution': 'def solution(height):\n'
                        '    l, r = 0, len(height) - 1\n'
                        '    ans = 0\n'
                        '    while l < r:\n'
                        '        ans = max(ans, min(height[l], height[r]) * (r - l))\n'
                        '        if height[l] < height[r]:\n'
                        '            l += 1\n'
                        '        else:\n'
                        '            r -= 1\n'
                        '    return ans',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['two-pointers', 'arrays'],
  'tests': [('[1, 8, 6, 2, 5, 4, 8, 3, 7]', '49', False),
            ('[1, 1]', '1', False),
            ('[4, 3, 2, 1, 4]', '16', False),
            ('[1, 2, 1]', '2', False),
            ('[2, 3, 4, 5, 18, 17, 6]', '17', False),
            ('[1, 8, 100, 2, 100, 4, 8, 3, 7]', '200', False),
            ('[10, 9, 8, 7, 6, 5, 4, 3, 2, 1]', '25', False),
            ('[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]', '25', False),
            ('[5, 5, 5, 5, 5]', '20', False),
            ('[3, 9, 3, 4, 7, 2, 12, 6]', '45', False)]},
 {'slug': 'three-sum',
  'title': '3Sum',
  'difficulty': 'medium',
  'description': 'Дан целочисленный массив `nums`. Найдите все уникальные тройки элементов `[nums[i], nums[j], '
                 'nums[k]]`, сумма которых равна `0`.\n'
                 '\n'
                 'Каждая тройка и результирующий список отсортированы по возрастанию.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([-1, 0, 1, 2, -1, -4])  # Вернет: [[-1, -1, 2], [-1, 0, 1]]\n'
                 '```',
  'starter_code': 'def solution(nums: list) -> list:\n    pass\n',
  'reference_solution': 'def solution(nums):\n'
                        '    nums = sorted(nums)\n'
                        '    res = []\n'
                        '    n = len(nums)\n'
                        '    for i in range(n - 2):\n'
                        '        if i > 0 and nums[i] == nums[i - 1]:\n'
                        '            continue\n'
                        '        l, r = i + 1, n - 1\n'
                        '        while l < r:\n'
                        '            s = nums[i] + nums[l] + nums[r]\n'
                        '            if s < 0:\n'
                        '                l += 1\n'
                        '            elif s > 0:\n'
                        '                r -= 1\n'
                        '            else:\n'
                        '                res.append([nums[i], nums[l], nums[r]])\n'
                        '                while l < r and nums[l] == nums[l + 1]:\n'
                        '                    l += 1\n'
                        '                while l < r and nums[r] == nums[r - 1]:\n'
                        '                    r -= 1\n'
                        '                l += 1\n'
                        '                r -= 1\n'
                        '    return res',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['two-pointers', 'arrays'],
  'tests': [('[-1, 0, 1, 2, -1, -4]', '[[-1, -1, 2], [-1, 0, 1]]', False),
            ('[0, 1, 1]', '[]', False),
            ('[0, 0, 0]', '[[0, 0, 0]]', False),
            ('[0, 0, 0, 0]', '[[0, 0, 0]]', False),
            ('[-2, 0, 1, 1, 2]', '[[-2, 0, 2], [-2, 1, 1]]', False),
            ('[-1, 0, 1, 0]', '[[-1, 0, 1]]', False),
            ('[-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6]',
             '[[-4, -2, 6], [-4, 0, 4], [-4, 1, 3], [-4, 2, 2], [-2, -2, 4], [-2, 0, 2]]',
             False),
            ('[-2, 0, 0, 2, 2]', '[[-2, 0, 2]]', False),
            ('[1, 2, -2, -1]', '[]', False),
            ('[-1, -1, -1, 2]', '[[-1, -1, 2]]', False)]},
 {'slug': 'longest-palindromic-substring',
  'title': 'Longest Palindromic Substring',
  'difficulty': 'medium',
  'description': 'Дана строка `s`. Найдите самую длинную подстроку в `s`, которая является палиндромом (читается '
                 'одинаково слева направо и справа налево).\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("babad")  # Вернет: "bab" (или "aba")\n'
                 '```',
  'starter_code': 'def solution(s: str) -> str:\n    pass\n',
  'reference_solution': 'def solution(s):\n'
                        '    if not s: return ""\n'
                        '    start = end = 0\n'
                        '    def expand(l, r):\n'
                        '        while l >= 0 and r < len(s) and s[l] == s[r]:\n'
                        '            l -= 1\n'
                        '            r += 1\n'
                        '        return l + 1, r - 1\n'
                        '    for i in range(len(s)):\n'
                        '        l1, r1 = expand(i, i)\n'
                        '        if r1 - l1 > end - start:\n'
                        '            start, end = l1, r1\n'
                        '        l2, r2 = expand(i, i + 1)\n'
                        '        if r2 - l2 > end - start:\n'
                        '            start, end = l2, r2\n'
                        '    return s[start:end + 1]',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['dynamic-programming', 'strings'],
  'tests': [('"babad"', 'bab', False),
            ('"cbbd"', 'bb', False),
            ('"a"', 'a', False),
            ('"ac"', 'a', False),
            ('"racecar"', 'racecar', False),
            ('"noon"', 'noon', False),
            ('"abacdfgdcaba"', 'aba', False),
            ('"forgeeksskeegfor"', 'geeksskeeg', False),
            ('"civilwartestingwhetherthatnaptownferriesacompaniessometimestwonightsrear"', 'ivi', False),
            ('"bananas"', 'anana', False)]},
 {'slug': 'reverse-integer',
  'title': 'Reverse Integer',
  'difficulty': 'medium',
  'description': 'Дано 32-битное знаковое целое число `x`. Разверните порядок его цифр. Если полученное число выходит '
                 'за пределы 32-битного диапазона `[-2^31, 2^31 - 1]`, верните `0`.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(-123)  # Вернет: -321\n'
                 '```',
  'starter_code': 'def solution(x: int) -> int:\n    pass\n',
  'reference_solution': 'def solution(x):\n'
                        '    sign = -1 if x < 0 else 1\n'
                        '    r = int(str(abs(x))[::-1]) * sign\n'
                        '    if -2**31 <= r <= 2**31 - 1:\n'
                        '        return r\n'
                        '    return 0',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['math'],
  'tests': [('123', '321', False),
            ('-123', '-321', False),
            ('120', '21', False),
            ('0', '0', False),
            ('1534236469', '0', False),
            ('-2147483648', '0', False),
            ('1', '1', False),
            ('-1', '-1', False),
            ('1000000003', '0', False),
            ('8463847412', '0', False)]},
 {'slug': 'string-to-integer-atoi',
  'title': 'String to Integer (atoi)',
  'difficulty': 'medium',
  'description': 'Реализуйте функцию преобразования строки в 32-битное целое число. Пропустите пробелы в начале, '
                 'определите знак числа (`+` или `-`), считайте последовательные цифры и примените ограничение '
                 'диапазона `[-2^31, 2^31 - 1]`.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("   -42")  # Вернет: -42\n'
                 '```',
  'starter_code': 'def solution(s: str) -> int:\n    pass\n',
  'reference_solution': 'def solution(s):\n'
                        '    s = s.lstrip()\n'
                        '    if not s: return 0\n'
                        '    sign = 1\n'
                        '    idx = 0\n'
                        "    if s[0] == '-':\n"
                        '        sign = -1\n'
                        '        idx = 1\n'
                        "    elif s[0] == '+':\n"
                        '        idx = 1\n'
                        '    num = 0\n'
                        '    while idx < len(s) and s[idx].isdigit():\n'
                        '        num = num * 10 + int(s[idx])\n'
                        '        idx += 1\n'
                        '    num *= sign\n'
                        '    INT_MIN, INT_MAX = -2**31, 2**31 - 1\n'
                        '    if num < INT_MIN: return INT_MIN\n'
                        '    if num > INT_MAX: return INT_MAX\n'
                        '    return num',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['strings'],
  'tests': [('"42"', '42', False),
            ('"   -42"', '-42', False),
            ('"1337c0d3"', '1337', False),
            ('"0-1"', '0', False),
            ('"words and 987"', '0', False),
            ('"-91283472332"', '-2147483648', False),
            ('"+1"', '1', False),
            ('"+-12"', '0', False),
            ('""', '0', False),
            ('"  0000000000012345678"', '12345678', False)]},
 {'slug': 'subarray-sum-equals-k',
  'title': 'Subarray Sum Equals K',
  'difficulty': 'medium',
  'description': 'Дан массив целых чисел `nums` и целое число `k`. Найдите общее количество непрерывных подмассивов, '
                 'сумма элементов которых равна `k`.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([1, 1, 1], 2)  # Вернет: 2 (подмассивы с индексами [0..1] и [1..2])\n'
                 '```',
  'starter_code': 'def solution(nums: list, k: int) -> int:\n    pass\n',
  'reference_solution': 'def solution(nums, k):\n'
                        '    count = curr = 0\n'
                        '    prefix = {0: 1}\n'
                        '    for x in nums:\n'
                        '        curr += x\n'
                        '        count += prefix.get(curr - k, 0)\n'
                        '        prefix[curr] = prefix.get(curr, 0) + 1\n'
                        '    return count',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['prefix-sum', 'arrays'],
  'tests': [('[1, 1, 1], 2', '2', False),
            ('[1, 2, 3], 3', '2', False),
            ('[1, -1, 0], 0', '3', False),
            ('[1], 0', '0', False),
            ('[-1, -1, 1], 0', '1', False),
            ('[3, 4, 7, 2, -3, 1, 4, 2], 7', '4', False),
            ('[1, 2, 1, 2, 1], 3', '4', False),
            ('[0, 0, 0, 0, 0], 0', '15', False),
            ('[100, 1, 2, 3, 4], 6', '1', False),
            ('[-2, -1, 2, 1], 1', '2', False)]},
 {'slug': 'product-of-array-except-self',
  'title': 'Product of Array Except Self',
  'difficulty': 'medium',
  'description': 'Дан массив целых чисел `nums`. Верните массив `answer`, где `answer[i]` равен произведению всех '
                 'элементов `nums`, кроме `nums[i]`. Алгоритм должен работать за O(n) без операции деления.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([1, 2, 3, 4])  # Вернет: [24, 12, 8, 6]\n'
                 '```',
  'starter_code': 'def solution(nums: list) -> list:\n    pass\n',
  'reference_solution': 'def solution(nums):\n'
                        '    n = len(nums)\n'
                        '    res = [1] * n\n'
                        '    prefix = 1\n'
                        '    for i in range(n):\n'
                        '        res[i] = prefix\n'
                        '        prefix *= nums[i]\n'
                        '    suffix = 1\n'
                        '    for i in range(n - 1, -1, -1):\n'
                        '        res[i] *= suffix\n'
                        '        suffix *= nums[i]\n'
                        '    return res',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['prefix-sum', 'arrays'],
  'tests': [('[1, 2, 3, 4]', '[24, 12, 8, 6]', False),
            ('[-1, 1, 0, -3, 3]', '[0, 0, 9, 0, 0]', False),
            ('[2, 3]', '[3, 2]', False),
            ('[0, 0]', '[0, 0]', False),
            ('[1, 0]', '[0, 1]', False),
            ('[5, 2, 4, 3]', '[24, 60, 30, 40]', False),
            ('[9, 0, -2]', '[0, -18, 0]', False),
            ('[1, 2, 3, 4, 5]', '[120, 60, 40, 30, 24]', False),
            ('[-2, -3, -4]', '[12, 8, 6]', False),
            ('[4, 5, 1, 8, 2]', '[80, 64, 320, 40, 160]', False)]},
 {'slug': 'group-anagrams',
  'title': 'Group Anagrams',
  'difficulty': 'medium',
  'description': 'Дан массив строк `strs`. Сгруппируйте анаграммы вместе. Для стабильности проверки каждая группа '
                 'отсортирована по алфавиту, а сам список групп отсортирован по первому элементу каждой группы.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(["eat", "tea", "tan", "ate", "nat", "bat"])  # Вернет: [["ate", "eat", "tea"], ["bat"], '
                 '["nat", "tan"]]\n'
                 '```',
  'starter_code': 'def solution(strs: list) -> list:\n    pass\n',
  'reference_solution': 'def solution(strs):\n'
                        '    groups = defaultdict(list)\n'
                        '    for s in strs:\n'
                        '        groups[tuple(sorted(s))].append(s)\n'
                        '    return sorted([sorted(g) for g in groups.values()])',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['hash-table', 'strings'],
  'tests': [('["eat", "tea", "tan", "ate", "nat", "bat"]', "[['ate', 'eat', 'tea'], ['bat'], ['nat', 'tan']]", False),
            ('[""]', "[['']]", False),
            ('["a"]', "[['a']]", False),
            ('["ab", "ba", "abc", "cba", "bca"]', "[['ab', 'ba'], ['abc', 'bca', 'cba']]", False),
            ('["hello", "world"]', "[['hello'], ['world']]", False),
            ('["listen", "silent", "enlist"]', "[['enlist', 'listen', 'silent']]", False),
            ('["rat", "tar", "art", "car"]', "[['art', 'rat', 'tar'], ['car']]", False),
            ('["dormitory", "dirtyroom"]', "[['dirtyroom', 'dormitory']]", False),
            ('["cat", "dog", "god", "act"]', "[['act', 'cat'], ['dog', 'god']]", False),
            ('["abc", "def", "ghi"]', "[['abc'], ['def'], ['ghi']]", False)]},
 {'slug': 'top-k-frequent-elements',
  'title': 'Top K Frequent Elements',
  'difficulty': 'medium',
  'description': 'Дан целочисленный массив `nums` и число `k`. Найдите `k` наиболее часто встречающихся элементов. '
                 'Верните результат, отсортированный по возрастанию.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([1, 1, 1, 2, 2, 3], 2)  # Вернет: [1, 2]\n'
                 '```',
  'starter_code': 'def solution(nums: list, k: int) -> list:\n    pass\n',
  'reference_solution': 'def solution(nums, k):\n'
                        '    c = Counter(nums)\n'
                        '    top = sorted(c.keys(), key=lambda x: (-c[x], x))[:k]\n'
                        '    return sorted(top)',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['heap', 'arrays'],
  'tests': [('[1, 1, 1, 2, 2, 3], 2', '[1, 2]', False),
            ('[1], 1', '[1]', False),
            ('[4, 1, -1, 2, -1, 2, 3], 2', '[-1, 2]', False),
            ('[1, 2, 2, 3, 3, 3], 1', '[3]', False),
            ('[5, 5, 5, 6, 6, 7], 2', '[5, 6]', False),
            ('[10, 20, 30, 40], 2', '[10, 20]', False),
            ('[-1, -1, -1, -2, -2, -3], 2', '[-2, -1]', False),
            ('[1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5], 1', '[5]', False),
            ('[7, 7, 8, 8, 8, 9, 9, 9, 9], 3', '[7, 8, 9]', False),
            ('[100, 200, 100, 300, 200, 100], 2', '[100, 200]', False)]},
 {'slug': 'longest-consecutive-sequence',
  'title': 'Longest Consecutive Sequence',
  'difficulty': 'medium',
  'description': 'Дан неотсортированный массив целых чисел `nums`. Найдите длину самой длинной последовательности '
                 'последовательных чисел (`x, x+1, x+2...`). Алгоритм должен работать за O(n).\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([100, 4, 200, 1, 3, 2])  # Вернет: 4 (последовательность: [1, 2, 3, 4])\n'
                 '```',
  'starter_code': 'def solution(nums: list) -> int:\n    pass\n',
  'reference_solution': 'def solution(nums):\n'
                        '    s = set(nums)\n'
                        '    max_len = 0\n'
                        '    for x in s:\n'
                        '        if x - 1 not in s:\n'
                        '            curr = x\n'
                        '            cur_len = 1\n'
                        '            while curr + 1 in s:\n'
                        '                curr += 1\n'
                        '                cur_len += 1\n'
                        '            max_len = max(max_len, cur_len)\n'
                        '    return max_len',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['hash-table', 'arrays'],
  'tests': [('[100, 4, 200, 1, 3, 2]', '4', False),
            ('[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]', '9', False),
            ('[]', '0', False),
            ('[9]', '1', False),
            ('[1, 2, 0, 1]', '3', False),
            ('[10, 5, 12, 3, 55, 30, 4, 11, 2]', '4', False),
            ('[-5, -4, -3, -2, -1, 0, 1]', '7', False),
            ('[1, 3, 5, 7, 9]', '1', False),
            ('[2, 2, 2, 2]', '1', False),
            ('[400, 4, 200, 1, 3, 2, 401, 402]', '4', False)]},
 {'slug': 'search-in-rotated-sorted-array',
  'title': 'Search in Rotated Sorted Array',
  'difficulty': 'medium',
  'description': 'Дан массив уникальных чисел `nums`, отсортированный по возрастанию и циклически сдвинутый в '
                 'неизвестной точке. Найдите индекс элемента `target` за O(log n) или верните `-1`, если элемент '
                 'отсутствует.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([4, 5, 6, 7, 0, 1, 2], 0)  # Вернет: 4\n'
                 '```',
  'starter_code': 'def solution(nums: list, target: int) -> int:\n    pass\n',
  'reference_solution': 'def solution(nums, target):\n'
                        '    l, r = 0, len(nums) - 1\n'
                        '    while l <= r:\n'
                        '        mid = (l + r) // 2\n'
                        '        if nums[mid] == target:\n'
                        '            return mid\n'
                        '        if nums[l] <= nums[mid]:\n'
                        '            if nums[l] <= target < nums[mid]:\n'
                        '                r = mid - 1\n'
                        '            else:\n'
                        '                l = mid + 1\n'
                        '        else:\n'
                        '            if nums[mid] < target <= nums[r]:\n'
                        '                l = mid + 1\n'
                        '            else:\n'
                        '                r = mid - 1\n'
                        '    return -1',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['binary-search', 'arrays'],
  'tests': [('[4, 5, 6, 7, 0, 1, 2], 0', '4', False),
            ('[4, 5, 6, 7, 0, 1, 2], 3', '-1', False),
            ('[1], 0', '-1', False),
            ('[1], 1', '0', False),
            ('[1, 3], 3', '1', False),
            ('[3, 1], 1', '1', False),
            ('[5, 1, 3], 5', '0', False),
            ('[4, 5, 6, 7, 8, 1, 2, 3], 8', '4', False),
            ('[6, 7, 1, 2, 3, 4, 5], 6', '0', False),
            ('[1, 2, 3, 4, 5, 6], 4', '3', False)]},
 {'slug': 'find-minimum-in-rotated-sorted-array',
  'title': 'Find Minimum in Rotated Sorted Array',
  'difficulty': 'medium',
  'description': 'Дан массив уникальных чисел `nums`, отсортированный по возрастанию и циклически сдвинутый от 1 до n '
                 'раз. Найдите минимальный элемент массива за время O(log n).\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([3, 4, 5, 1, 2])  # Вернет: 1\n'
                 '```',
  'starter_code': 'def solution(nums: list) -> int:\n    pass\n',
  'reference_solution': 'def solution(nums):\n'
                        '    l, r = 0, len(nums) - 1\n'
                        '    while l < r:\n'
                        '        mid = (l + r) // 2\n'
                        '        if nums[mid] > nums[r]:\n'
                        '            l = mid + 1\n'
                        '        else:\n'
                        '            r = mid\n'
                        '    return nums[l]',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['binary-search', 'arrays'],
  'tests': [('[3, 4, 5, 1, 2]', '1', False),
            ('[4, 5, 6, 7, 0, 1, 2]', '0', False),
            ('[11, 13, 15, 17]', '11', False),
            ('[1]', '1', False),
            ('[2, 1]', '1', False),
            ('[3, 1, 2]', '1', False),
            ('[5, 1, 2, 3, 4]', '1', False),
            ('[2, 3, 4, 5, 6, 7, 8, 1]', '1', False),
            ('[10, 20, 30, 40, 50, 5]', '5', False),
            ('[1, 2, 3, 4, 5]', '1', False)]},
 {'slug': 'find-peak-element',
  'title': 'Find Peak Element',
  'difficulty': 'medium',
  'description': 'Пиковым элементом называется элемент, который строго больше своих соседей. Найдите любой пиковый '
                 'элемент и верните его индекс за O(log n).\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([1, 2, 3, 1])  # Вернет: 2 (число 3 больше 2 и 1)\n'
                 '```',
  'starter_code': 'def solution(nums: list) -> int:\n    pass\n',
  'reference_solution': 'def solution(nums):\n'
                        '    l, r = 0, len(nums) - 1\n'
                        '    while l < r:\n'
                        '        mid = (l + r) // 2\n'
                        '        if nums[mid] > nums[mid + 1]:\n'
                        '            r = mid\n'
                        '        else:\n'
                        '            l = mid + 1\n'
                        '    return l',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['binary-search', 'arrays'],
  'tests': [('[1, 2, 3, 1]', '2', False),
            ('[1, 2, 1, 3, 5, 6, 4]', '5', False),
            ('[1]', '0', False),
            ('[1, 2]', '1', False),
            ('[2, 1]', '0', False),
            ('[1, 2, 3, 4, 5]', '4', False),
            ('[5, 4, 3, 2, 1]', '0', False),
            ('[1, 3, 20, 4, 1, 0]', '2', False),
            ('[1, 5, 2, 1]', '1', False),
            ('[10, 20, 15, 2, 23, 90, 67]', '5', False)]},
 {'slug': 'daily-temperatures',
  'title': 'Daily Temperatures',
  'difficulty': 'medium',
  'description': 'Дан массив температур `temperatures`. Верните массив `answer`, где `answer[i]` — количество дней, '
                 'которое нужно подождать до более теплой температуры. Если такого дня нет, запишите 0.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([73, 74, 75, 71, 69, 72, 76, 73])  # Вернет: [1, 1, 4, 2, 1, 1, 0, 0]\n'
                 '```',
  'starter_code': 'def solution(temperatures: list) -> list:\n    pass\n',
  'reference_solution': 'def solution(temperatures):\n'
                        '    n = len(temperatures)\n'
                        '    res = [0] * n\n'
                        '    stack = []\n'
                        '    for i, t in enumerate(temperatures):\n'
                        '        while stack and temperatures[stack[-1]] < t:\n'
                        '            prev = stack.pop()\n'
                        '            res[prev] = i - prev\n'
                        '        stack.append(i)\n'
                        '    return res',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['stack', 'arrays'],
  'tests': [('[73, 74, 75, 71, 69, 72, 76, 73]', '[1, 1, 4, 2, 1, 1, 0, 0]', False),
            ('[30, 40, 50, 60]', '[1, 1, 1, 0]', False),
            ('[30, 60, 90]', '[1, 1, 0]', False),
            ('[89, 62, 70, 58, 47, 47, 46, 76, 100, 70]', '[8, 1, 5, 4, 3, 2, 1, 1, 0, 0]', False),
            ('[50]', '[0]', False),
            ('[55, 55, 55]', '[0, 0, 0]', False),
            ('[90, 80, 70, 60]', '[0, 0, 0, 0]', False),
            ('[60, 70, 60, 70, 80]', '[1, 3, 1, 1, 0]', False),
            ('[45, 46, 47, 48, 49]', '[1, 1, 1, 1, 0]', False),
            ('[31, 32, 31, 32, 31, 32]', '[1, 0, 1, 0, 1, 0]', False)]},
 {'slug': 'coin-change',
  'title': 'Coin Change',
  'difficulty': 'medium',
  'description': 'Дан массив монет разного номинала `coins` и общая сумма `amount`. Найдите наименьшее количество '
                 'монет, необходимое для формирования этой суммы. Если сумму составить невозможно, верните -1.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([1, 2, 5], 11)  # Вернет: 3 (5 + 5 + 1)\n'
                 '```',
  'starter_code': 'def solution(coins: list, amount: int) -> int:\n    pass\n',
  'reference_solution': 'def solution(coins, amount):\n'
                        "    dp = [float('inf')] * (amount + 1)\n"
                        '    dp[0] = 0\n'
                        '    for c in coins:\n'
                        '        for i in range(c, amount + 1):\n'
                        '            dp[i] = min(dp[i], dp[i - c] + 1)\n'
                        "    return dp[amount] if dp[amount] != float('inf') else -1",
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['dynamic-programming'],
  'tests': [('[1, 2, 5], 11', '3', False),
            ('[2], 3', '-1', False),
            ('[1], 0', '0', False),
            ('[1], 1', '1', False),
            ('[1], 2', '2', False),
            ('[2, 5, 10, 1], 27', '4', False),
            ('[186, 419, 83, 408], 6249', '20', False),
            ('[3, 7, 405, 436], 8839', '25', False),
            ('[1, 3, 5], 8', '2', False),
            ('[5, 10, 25], 30', '2', False)]},
 {'slug': 'house-robber',
  'title': 'House Robber',
  'difficulty': 'medium',
  'description': 'Вы профессиональный грабитель. Дома расположены вдоль улицы, и в каждом доме хранится сумма '
                 '`nums[i]`. Соседние дома грабить нельзя (сработает сигнализация). Найдите максимальную сумму, '
                 'которую можно украсть.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([1, 2, 3, 1])  # Вернет: 4 (ограбить дом 1 и дом 3: 1 + 3 = 4)\n'
                 '```',
  'starter_code': 'def solution(nums: list) -> int:\n    pass\n',
  'reference_solution': 'def solution(nums):\n'
                        '    prev1 = prev2 = 0\n'
                        '    for x in nums:\n'
                        '        curr = max(prev1, prev2 + x)\n'
                        '        prev2 = prev1\n'
                        '        prev1 = curr\n'
                        '    return prev1',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['dynamic-programming'],
  'tests': [('[1, 2, 3, 1]', '4', False),
            ('[2, 7, 9, 3, 1]', '12', False),
            ('[2, 1, 1, 2]', '4', False),
            ('[0]', '0', False),
            ('[5]', '5', False),
            ('[1, 100, 1]', '100', False),
            ('[10, 2, 3, 20]', '30', False),
            ('[100, 1, 1, 100]', '200', False),
            ('[4, 1, 2, 7, 5, 3, 1]', '14', False),
            ('[5, 3, 4, 11, 2]', '16', False)]},
 {'slug': 'house-robber-ii',
  'title': 'House Robber II',
  'difficulty': 'medium',
  'description': 'Дома расположены по кругу (первый и последний дома являются соседями). Соседние дома грабить нельзя. '
                 'Найдите максимальную сумму, которую можно украсть.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([2, 3, 2])  # Вернет: 3 (первый и третий дома соседствуют, грабим средний)\n'
                 '```',
  'starter_code': 'def solution(nums: list) -> int:\n    pass\n',
  'reference_solution': 'def solution(nums):\n'
                        '    if len(nums) == 1: return nums[0]\n'
                        '    def rob_linear(h):\n'
                        '        p1 = p2 = 0\n'
                        '        for x in h:\n'
                        '            c = max(p1, p2 + x)\n'
                        '            p2 = p1\n'
                        '            p1 = c\n'
                        '        return p1\n'
                        '    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['dynamic-programming'],
  'tests': [('[2, 3, 2]', '3', False),
            ('[1, 2, 3, 1]', '4', False),
            ('[1, 2, 3]', '3', False),
            ('[0]', '0', False),
            ('[5]', '5', False),
            ('[1, 3, 1, 3, 100]', '103', False),
            ('[20, 30, 40, 50, 60]', '100', False),
            ('[1, 2, 1, 1]', '3', False),
            ('[10, 1, 1, 10]', '11', False),
            ('[2, 7, 9, 3, 1]', '11', False)]},
 {'slug': 'jump-game',
  'title': 'Jump Game',
  'difficulty': 'medium',
  'description': 'Дан целочисленный массив `nums`. Начальная позиция — индекс 0. Значение `nums[i]` указывает '
                 'максимальную длину прыжка из позиции `i`. Определите, можно ли достичь последнего индекса.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([2, 3, 1, 1, 4])  # Вернет: True\n'
                 '```',
  'starter_code': 'def solution(nums: list) -> bool:\n    pass\n',
  'reference_solution': 'def solution(nums):\n'
                        '    reach = 0\n'
                        '    for i, x in enumerate(nums):\n'
                        '        if i > reach: return False\n'
                        '        reach = max(reach, i + x)\n'
                        '    return True',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['greedy', 'arrays'],
  'tests': [('[2, 3, 1, 1, 4]', 'True', False),
            ('[3, 2, 1, 0, 4]', 'False', False),
            ('[0]', 'True', False),
            ('[1]', 'True', False),
            ('[2, 0]', 'True', False),
            ('[1, 0, 1, 0]', 'False', False),
            ('[2, 5, 0, 0]', 'True', False),
            ('[1, 1, 1, 1]', 'True', False),
            ('[0, 2, 3]', 'False', False),
            ('[5, 9, 3, 2, 1, 0, 2, 3, 3, 1, 0, 0]', 'True', False)]},
 {'slug': 'jump-game-ii',
  'title': 'Jump Game II',
  'difficulty': 'medium',
  'description': 'Дан массив `nums`. Начиная с индекса 0, найдите минимальное количество прыжков, чтобы добраться до '
                 'последнего индекса. Гарантируется, что достичь конца всегда возможно.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([2, 3, 1, 1, 4])  # Вернет: 2 (прыжок на 1 шаг до индекса 1, затем на 3 шага до конца)\n'
                 '```',
  'starter_code': 'def solution(nums: list) -> int:\n    pass\n',
  'reference_solution': 'def solution(nums):\n'
                        '    jumps = 0\n'
                        '    curr_end = 0\n'
                        '    curr_farthest = 0\n'
                        '    for i in range(len(nums) - 1):\n'
                        '        curr_farthest = max(curr_farthest, i + nums[i])\n'
                        '        if i == curr_end:\n'
                        '            jumps += 1\n'
                        '            curr_end = curr_farthest\n'
                        '    return jumps',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['greedy', 'arrays'],
  'tests': [('[2, 3, 1, 1, 4]', '2', False),
            ('[2, 3, 0, 1, 4]', '2', False),
            ('[1]', '0', False),
            ('[1, 2]', '1', False),
            ('[1, 2, 3]', '2', False),
            ('[2, 1]', '1', False),
            ('[3, 2, 1]', '1', False),
            ('[1, 1, 1, 1]', '3', False),
            ('[7, 0, 9, 6, 9, 6, 1, 7, 9, 0, 1, 2, 9, 0, 3]', '2', False),
            ('[10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 0]', '2', False)]},
 {'slug': 'merge-intervals',
  'title': 'Merge Intervals',
  'difficulty': 'medium',
  'description': 'Дан массив интервалов `intervals`, где `intervals[i] = [start, end]`. Объедините все перекрывающиеся '
                 'интервалы и верните список неперекрывающихся интервалов.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([[1, 3], [2, 6], [8, 10], [15, 18]])  # Вернет: [[1, 6], [8, 10], [15, 18]]\n'
                 '```',
  'starter_code': 'def solution(intervals: list) -> list:\n    pass\n',
  'reference_solution': 'def solution(intervals):\n'
                        '    if not intervals: return []\n'
                        '    intervals = sorted(intervals, key=lambda x: x[0])\n'
                        '    merged = [intervals[0]]\n'
                        '    for cur in intervals[1:]:\n'
                        '        last = merged[-1]\n'
                        '        if cur[0] <= last[1]:\n'
                        '            last[1] = max(last[1], cur[1])\n'
                        '        else:\n'
                        '            merged.append(cur)\n'
                        '    return merged',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['sorting', 'arrays'],
  'tests': [('[[1, 3], [2, 6], [8, 10], [15, 18]]', '[[1, 6], [8, 10], [15, 18]]', False),
            ('[[1, 4], [4, 5]]', '[[1, 5]]', False),
            ('[[1, 4], [0, 4]]', '[[0, 4]]', False),
            ('[[1, 4], [2, 3]]', '[[1, 4]]', False),
            ('[[1, 4]]', '[[1, 4]]', False),
            ('[[1, 4], [0, 0]]', '[[0, 0], [1, 4]]', False),
            ('[[2, 3], [4, 5], [6, 7], [8, 9], [1, 10]]', '[[1, 10]]', False),
            ('[[1, 10], [2, 3], [4, 5], [6, 7]]', '[[1, 10]]', False),
            ('[[1, 2], [3, 4], [5, 6]]', '[[1, 2], [3, 4], [5, 6]]', False),
            ('[[1, 5], [2, 4], [3, 6], [8, 10]]', '[[1, 6], [8, 10]]', False)]},
 {'slug': 'non-overlapping-intervals',
  'title': 'Non-overlapping Intervals',
  'difficulty': 'medium',
  'description': 'Дан массив интервалов `intervals`. Найдите минимальное количество интервалов, которые нужно удалить, '
                 'чтобы остальные интервалы не перекрывались.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([[1, 2], [2, 3], [3, 4], [1, 3]])  # Вернет: 1 (удалить [1, 3])\n'
                 '```',
  'starter_code': 'def solution(intervals: list) -> int:\n    pass\n',
  'reference_solution': 'def solution(intervals):\n'
                        '    if not intervals: return 0\n'
                        '    intervals = sorted(intervals, key=lambda x: x[1])\n'
                        '    count = 0\n'
                        '    end = intervals[0][1]\n'
                        '    for i in range(1, len(intervals)):\n'
                        '        if intervals[i][0] < end:\n'
                        '            count += 1\n'
                        '        else:\n'
                        '            end = intervals[i][1]\n'
                        '    return count',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['greedy', 'arrays'],
  'tests': [('[[1, 2], [2, 3], [3, 4], [1, 3]]', '1', False),
            ('[[1, 2], [1, 2], [1, 2]]', '2', False),
            ('[[1, 2], [2, 3]]', '0', False),
            ('[[1, 100], [11, 22], [1, 11], [2, 12]]', '2', False),
            ('[[0, 2], [1, 3], [2, 4], [3, 5], [4, 6]]', '2', False),
            ('[[1, 5], [2, 3], [3, 4]]', '1', False),
            ('[[-52, 31], [-73, -26], [82, 97], [-65, -11], [-62, -49]]', '3', False),
            ('[[1, 2]]', '0', False),
            ('[[1, 4], [2, 5], [3, 6]]', '2', False),
            ('[[1, 3], [2, 4], [3, 5], [4, 6]]', '2', False)]},
 {'slug': 'spiral-matrix',
  'title': 'Spiral Matrix',
  'difficulty': 'medium',
  'description': 'Дана матрица `matrix` размера `m x n`. Верните список всех элементов матрицы в порядке спирального '
                 'обхода по часовой стрелке.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([[1, 2, 3], [4, 5, 6], [7, 8, 9]])  # Вернет: [1, 2, 3, 6, 9, 8, 7, 4, 5]\n'
                 '```',
  'starter_code': 'def solution(matrix: list) -> list:\n    pass\n',
  'reference_solution': 'def solution(matrix):\n'
                        '    if not matrix: return []\n'
                        '    res = []\n'
                        '    top, bottom = 0, len(matrix) - 1\n'
                        '    left, right = 0, len(matrix[0]) - 1\n'
                        '    while top <= bottom and left <= right:\n'
                        '        for c in range(left, right + 1):\n'
                        '            res.append(matrix[top][c])\n'
                        '        top += 1\n'
                        '        for r in range(top, bottom + 1):\n'
                        '            res.append(matrix[r][right])\n'
                        '        right -= 1\n'
                        '        if top <= bottom:\n'
                        '            for c in range(right, left - 1, -1):\n'
                        '                res.append(matrix[bottom][c])\n'
                        '            bottom -= 1\n'
                        '        if left <= right:\n'
                        '            for r in range(bottom, top - 1, -1):\n'
                        '                res.append(matrix[r][left])\n'
                        '            left += 1\n'
                        '    return res',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['matrix'],
  'tests': [('[[1, 2, 3], [4, 5, 6], [7, 8, 9]]', '[1, 2, 3, 6, 9, 8, 7, 4, 5]', False),
            ('[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]', '[1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]', False),
            ('[[1]]', '[1]', False),
            ('[[1, 2, 3]]', '[1, 2, 3]', False),
            ('[[1], [2], [3]]', '[1, 2, 3]', False),
            ('[[1, 2], [3, 4]]', '[1, 2, 4, 3]', False),
            ('[[2, 5, 8], [4, 0, -1]]', '[2, 5, 8, -1, 0, 4]', False),
            ('[[1, 2, 3, 4, 5]]', '[1, 2, 3, 4, 5]', False),
            ('[[1], [2], [3], [4], [5]]', '[1, 2, 3, 4, 5]', False),
            ('[[1, 2], [3, 4], [5, 6], [7, 8]]', '[1, 2, 4, 6, 8, 7, 5, 3]', False)]},
 {'slug': 'rotate-image',
  'title': 'Rotate Image',
  'difficulty': 'medium',
  'description': 'Дана квадратная матрица `matrix` размера `n x n`. Поверните изображение на 90 градусов по часовой '
                 'стрелке и верните новую повернутую матрицу.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([[1, 2, 3], [4, 5, 6], [7, 8, 9]])  # Вернет: [[7, 4, 1], [8, 5, 2], [9, 6, 3]]\n'
                 '```',
  'starter_code': 'def solution(matrix: list) -> list:\n    pass\n',
  'reference_solution': 'def solution(matrix):\n    return [list(row) for row in zip(*matrix[::-1])]',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['matrix'],
  'tests': [('[[1, 2, 3], [4, 5, 6], [7, 8, 9]]', '[[7, 4, 1], [8, 5, 2], [9, 6, 3]]', False),
            ('[[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]',
             '[[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]',
             False),
            ('[[1]]', '[[1]]', False),
            ('[[1, 2], [3, 4]]', '[[3, 1], [4, 2]]', False),
            ('[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]',
             '[[13, 9, 5, 1], [14, 10, 6, 2], [15, 11, 7, 3], [16, 12, 8, 4]]',
             False),
            ('[[0, 1], [2, 3]]', '[[2, 0], [3, 1]]', False),
            ('[[1, 0, 0], [0, 1, 0], [0, 0, 1]]', '[[0, 0, 1], [0, 1, 0], [1, 0, 0]]', False),
            ('[[9, 8, 7], [6, 5, 4], [3, 2, 1]]', '[[3, 6, 9], [2, 5, 8], [1, 4, 7]]', False),
            ('[[2, 4], [6, 8]]', '[[6, 2], [8, 4]]', False),
            ('[[1, 5, 9], [2, 6, 10], [3, 7, 11]]', '[[3, 2, 1], [7, 6, 5], [11, 10, 9]]', False)]},
 {'slug': 'set-matrix-zeroes',
  'title': 'Set Matrix Zeroes',
  'difficulty': 'medium',
  'description': 'Дана матрица `matrix` размера `m x n`. Если какой-либо элемент равен 0, обнулите всю соответствующую '
                 'строку и столбец. Верните измененную матрицу.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([[1, 1, 1], [1, 0, 1], [1, 1, 1]])  # Вернет: [[1, 0, 1], [0, 0, 0], [1, 0, 1]]\n'
                 '```',
  'starter_code': 'def solution(matrix: list) -> list:\n    pass\n',
  'reference_solution': 'def solution(matrix):\n'
                        '    m, n = len(matrix), len(matrix[0])\n'
                        '    rows = set()\n'
                        '    cols = set()\n'
                        '    for r in range(m):\n'
                        '        for c in range(n):\n'
                        '            if matrix[r][c] == 0:\n'
                        '                rows.add(r)\n'
                        '                cols.add(c)\n'
                        '    res = [row[:] for row in matrix]\n'
                        '    for r in range(m):\n'
                        '        for c in range(n):\n'
                        '            if r in rows or c in cols:\n'
                        '                res[r][c] = 0\n'
                        '    return res',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['matrix'],
  'tests': [('[[1, 1, 1], [1, 0, 1], [1, 1, 1]]', '[[1, 0, 1], [0, 0, 0], [1, 0, 1]]', False),
            ('[[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]', '[[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]', False),
            ('[[1]]', '[[1]]', False),
            ('[[0]]', '[[0]]', False),
            ('[[1, 2], [3, 4]]', '[[1, 2], [3, 4]]', False),
            ('[[1, 0], [3, 4]]', '[[0, 0], [3, 0]]', False),
            ('[[1, 2, 3], [4, 5, 6], [7, 8, 0]]', '[[1, 2, 0], [4, 5, 0], [0, 0, 0]]', False),
            ('[[0, 0], [0, 0]]', '[[0, 0], [0, 0]]', False),
            ('[[1, 2, 3, 4], [5, 0, 7, 8], [9, 10, 11, 12]]', '[[1, 0, 3, 4], [0, 0, 0, 0], [9, 0, 11, 12]]', False),
            ('[[1, 1], [0, 1], [1, 1]]', '[[0, 1], [0, 0], [0, 1]]', False)]},
 {'slug': 'unique-paths',
  'title': 'Unique Paths',
  'difficulty': 'medium',
  'description': 'Робот находится в левом верхнем углу сетки `m x n`. Он может двигаться только вправо или вниз. '
                 'Найдите количество уникальных путей до правого нижнего угла.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(3, 7)  # Вернет: 28\n'
                 '```',
  'starter_code': 'def solution(m: int, n: int) -> int:\n    pass\n',
  'reference_solution': 'def solution(m, n):\n    return math.comb(m + n - 2, m - 1)',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['dynamic-programming', 'math'],
  'tests': [('3, 7', '28', False),
            ('3, 2', '3', False),
            ('1, 1', '1', False),
            ('1, 10', '1', False),
            ('10, 1', '1', False),
            ('2, 2', '2', False),
            ('3, 3', '6', False),
            ('7, 3', '28', False),
            ('4, 4', '20', False),
            ('10, 10', '48620', False)]},
 {'slug': 'minimum-path-sum',
  'title': 'Minimum Path Sum',
  'difficulty': 'medium',
  'description': 'Дана сетка `grid` размера `m x n`, заполненная неотрицательными числами. Найдите путь из левого '
                 'верхнего в правый нижний угол с минимальной суммой чисел вдоль пути (движение разрешено только '
                 'вправо и вниз).\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([[1, 3, 1], [1, 5, 1], [4, 2, 1]])  # Вернет: 7 (путь 1 -> 3 -> 1 -> 1 -> 1)\n'
                 '```',
  'starter_code': 'def solution(grid: list) -> int:\n    pass\n',
  'reference_solution': 'def solution(grid):\n'
                        '    m, n = len(grid), len(grid[0])\n'
                        '    dp = [row[:] for row in grid]\n'
                        '    for r in range(m):\n'
                        '        for c in range(n):\n'
                        '            if r == 0 and c == 0: continue\n'
                        '            elif r == 0: dp[r][c] += dp[r][c - 1]\n'
                        '            elif c == 0: dp[r][c] += dp[r - 1][c]\n'
                        '            else: dp[r][c] += min(dp[r - 1][c], dp[r][c - 1])\n'
                        '    return dp[m - 1][n - 1]',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['dynamic-programming', 'matrix'],
  'tests': [('[[1, 3, 1], [1, 5, 1], [4, 2, 1]]', '7', False),
            ('[[1, 2, 3], [4, 5, 6]]', '12', False),
            ('[[5]]', '5', False),
            ('[[1, 2], [1, 1]]', '3', False),
            ('[[1, 2, 5], [3, 2, 1]]', '6', False),
            ('[[1, 100], [1, 1]]', '3', False),
            ('[[1, 2, 3, 4]]', '10', False),
            ('[[1], [2], [3], [4]]', '10', False),
            ('[[0, 0], [0, 0]]', '0', False),
            ('[[2, 1, 3], [6, 5, 4], [7, 8, 9]]', '19', False)]},
 {'slug': 'decode-ways',
  'title': 'Decode Ways',
  'difficulty': 'medium',
  'description': "Секретное сообщение закодировано цифрами от '1' до '26' ('A' -> 1, 'B' -> 2, ..., 'Z' -> 26). Дана "
                 'числовая строка `s`. Найдите количество способов расшифровать это сообщение.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("12")  # Вернет: 2 ("AB" (1 2) или "L" (12))\n'
                 '```',
  'starter_code': 'def solution(s: str) -> int:\n    pass\n',
  'reference_solution': 'def solution(s):\n'
                        "    if not s or s[0] == '0': return 0\n"
                        '    n = len(s)\n'
                        '    dp = [0] * (n + 1)\n'
                        '    dp[0] = dp[1] = 1\n'
                        '    for i in range(2, n + 1):\n'
                        '        one = int(s[i - 1:i])\n'
                        '        two = int(s[i - 2:i])\n'
                        '        if 1 <= one <= 9: dp[i] += dp[i - 1]\n'
                        '        if 10 <= two <= 26: dp[i] += dp[i - 2]\n'
                        '    return dp[n]',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['dynamic-programming', 'strings'],
  'tests': [('"12"', '2', False),
            ('"226"', '3', False),
            ('"06"', '0', False),
            ('"10"', '1', False),
            ('"27"', '1', False),
            ('"11106"', '2', False),
            ('"2101"', '1', False),
            ('"111111"', '13', False),
            ('"0"', '0', False),
            ('"2611055"', '2', False)]},
 {'slug': 'word-break',
  'title': 'Word Break',
  'difficulty': 'medium',
  'description': 'Дана строка `s` и словарь слов `wordDict`. Определите, можно ли разбить строку `s` на '
                 'последовательность из одного или нескольких слов из словаря. Одно и то же слово можно использовать '
                 'повторно.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("leetcode", ["leet", "code"])  # Вернет: True\n'
                 '```',
  'starter_code': 'def solution(s: str, wordDict: list) -> bool:\n    pass\n',
  'reference_solution': 'def solution(s, wordDict):\n'
                        '    words = set(wordDict)\n'
                        '    dp = [False] * (len(s) + 1)\n'
                        '    dp[0] = True\n'
                        '    for i in range(1, len(s) + 1):\n'
                        '        for j in range(i):\n'
                        '            if dp[j] and s[j:i] in words:\n'
                        '                dp[i] = True\n'
                        '                break\n'
                        '    return dp[len(s)]',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['dynamic-programming', 'strings'],
  'tests': [('"leetcode", ["leet", "code"]', 'True', False),
            ('"applepenapple", ["apple", "pen"]', 'True', False),
            ('"catsandog", ["cats", "dog", "sand", "and", "cat"]', 'False', False),
            ('"a", ["a"]', 'True', False),
            ('"a", ["b"]', 'False', False),
            ('"bb", ["a", "b", "bbb", "bbbb"]', 'True', False),
            ('"cars", ["car", "ca", "rs"]', 'True', False),
            ('"program", ["pro", "gram", "p"]', 'True', False),
            ('"goalspecial", ["go", "goal", "special"]', 'True', False),
            ('"abcd", ["a", "abc", "b", "cd"]', 'True', False)]},
 {'slug': 'longest-increasing-subsequence',
  'title': 'Longest Increasing Subsequence',
  'difficulty': 'medium',
  'description': 'Дан целочисленный массив `nums`. Найдите длину самой длинной строго возрастающей '
                 'подпоследовательности (элементы не обязательно должны идти подряд).\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([10, 9, 2, 5, 3, 7, 101, 18])  # Вернет: 4 (подпоследовательность [2, 3, 7, 101])\n'
                 '```',
  'starter_code': 'def solution(nums: list) -> int:\n    pass\n',
  'reference_solution': 'def solution(nums):\n'
                        '    sub = []\n'
                        '    for x in nums:\n'
                        '        idx = bisect.bisect_left(sub, x)\n'
                        '        if idx == len(sub):\n'
                        '            sub.append(x)\n'
                        '        else:\n'
                        '            sub[idx] = x\n'
                        '    return len(sub)',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['dynamic-programming', 'arrays'],
  'tests': [('[10, 9, 2, 5, 3, 7, 101, 18]', '4', False),
            ('[0, 1, 0, 3, 2, 3]', '4', False),
            ('[7, 7, 7, 7, 7, 7, 7]', '1', False),
            ('[1]', '1', False),
            ('[1, 3, 6, 7, 9, 4, 10, 5, 6]', '6', False),
            ('[4, 10, 4, 3, 8, 9]', '3', False),
            ('[2, 2]', '1', False),
            ('[1, 2, 3, 4, 5]', '5', False),
            ('[5, 4, 3, 2, 1]', '1', False),
            ('[3, 5, 6, 2, 5, 4, 19, 5, 6, 7, 12]', '6', False)]},
 {'slug': 'sort-colors',
  'title': 'Sort Colors',
  'difficulty': 'medium',
  'description': 'Дан массив `nums` с объектами трех цветов: 0 (красный), 1 (белый) и 2 (синий). Отсортируйте массив '
                 'по возрастанию цветов на месте за один проход с константной памятью и верните отсортированный '
                 'массив.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([2, 0, 2, 1, 1, 0])  # Вернет: [0, 0, 1, 1, 2, 2]\n'
                 '```',
  'starter_code': 'def solution(nums: list) -> list:\n    pass\n',
  'reference_solution': 'def solution(nums):\n    return sorted(nums)',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['two-pointers', 'arrays'],
  'tests': [('[2, 0, 2, 1, 1, 0]', '[0, 0, 1, 1, 2, 2]', False),
            ('[2, 0, 1]', '[0, 1, 2]', False),
            ('[0]', '[0]', False),
            ('[1]', '[1]', False),
            ('[2]', '[2]', False),
            ('[1, 0]', '[0, 1]', False),
            ('[2, 1, 0]', '[0, 1, 2]', False),
            ('[0, 0, 0]', '[0, 0, 0]', False),
            ('[2, 2, 2]', '[2, 2, 2]', False),
            ('[1, 2, 0, 1, 2, 0, 1, 2, 0]', '[0, 0, 0, 1, 1, 1, 2, 2, 2]', False)]},
 {'slug': 'find-the-duplicate-number',
  'title': 'Find the Duplicate Number',
  'difficulty': 'medium',
  'description': 'Дан массив `nums`, содержащий `n + 1` целых чисел в диапазоне от 1 до n. В массиве гарантированно '
                 'существует ровно одно повторяющееся число (оно может встречаться два или более раз). Найдите и '
                 'верните это число, не изменяя массив и используя O(1) памяти.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([1, 3, 4, 2, 2])  # Вернет: 2\n'
                 '```',
  'starter_code': 'def solution(nums: list) -> int:\n    pass\n',
  'reference_solution': 'def solution(nums):\n'
                        '    slow = fast = nums[0]\n'
                        '    while True:\n'
                        '        slow = nums[slow]\n'
                        '        fast = nums[nums[fast]]\n'
                        '        if slow == fast: break\n'
                        '    slow = nums[0]\n'
                        '    while slow != fast:\n'
                        '        slow = nums[slow]\n'
                        '        fast = nums[fast]\n'
                        '    return slow',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['two-pointers', 'arrays'],
  'tests': [('[1, 3, 4, 2, 2]', '2', False),
            ('[3, 1, 3, 4, 2]', '3', False),
            ('[3, 3, 3, 3, 3]', '3', False),
            ('[1, 1]', '1', False),
            ('[1, 1, 2]', '1', False),
            ('[2, 2, 2, 2, 2]', '2', False),
            ('[2, 5, 9, 6, 9, 3, 8, 9, 7, 1]', '9', False),
            ('[1, 4, 4, 2, 4]', '4', False),
            ('[1, 2, 3, 4, 4]', '4', False),
            ('[4, 3, 1, 4, 2]', '4', False)]},
 {'slug': 'find-all-duplicates-in-an-array',
  'title': 'Find All Duplicates in an Array',
  'difficulty': 'medium',
  'description': 'Дан массив `nums` длины `n`, где каждое число находится в диапазоне `[1, n]`. Некоторые элементы '
                 'появляются дважды, а остальные — один раз. Найдите все элементы, которые появляются дважды, и '
                 'верните их список, отсортированный по возрастанию.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([4, 3, 2, 7, 8, 2, 3, 1])  # Вернет: [2, 3]\n'
                 '```',
  'starter_code': 'def solution(nums: list) -> list:\n    pass\n',
  'reference_solution': 'def solution(nums):\n'
                        '    c = Counter(nums)\n'
                        '    return sorted([k for k, v in c.items() if v > 1])',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['arrays'],
  'tests': [('[4, 3, 2, 7, 8, 2, 3, 1]', '[2, 3]', False),
            ('[1, 1, 2]', '[1]', False),
            ('[1]', '[]', False),
            ('[1, 2, 3, 4, 5]', '[]', False),
            ('[2, 2, 1, 3, 4, 5, 3]', '[2, 3]', False),
            ('[1, 2, 2, 3, 4, 4]', '[2, 4]', False),
            ('[10, 2, 5, 10, 9, 1, 1, 4, 3, 7]', '[1, 10]', False),
            ('[1, 2, 1, 2]', '[1, 2]', False),
            ('[3, 1, 2]', '[]', False),
            ('[5, 4, 6, 7, 9, 3, 10, 9, 5, 6]', '[5, 6, 9]', False)]},
 {'slug': 'increasing-triplet-subsequence',
  'title': 'Increasing Triplet Subsequence',
  'difficulty': 'medium',
  'description': 'Дан целочисленный массив `nums`. Определите, существуют ли три индекса `i < j < k`, такие что '
                 '`nums[i] < nums[j] < nums[k]`. Решение должно работать за O(n) времени и O(1) памяти.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([1, 2, 3, 4, 5])  # Вернет: True\n'
                 '```',
  'starter_code': 'def solution(nums: list) -> bool:\n    pass\n',
  'reference_solution': 'def solution(nums):\n'
                        "    first = second = float('inf')\n"
                        '    for x in nums:\n'
                        '        if x <= first:\n'
                        '            first = x\n'
                        '        elif x <= second:\n'
                        '            second = x\n'
                        '        else:\n'
                        '            return True\n'
                        '    return False',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['greedy', 'arrays'],
  'tests': [('[1, 2, 3, 4, 5]', 'True', False),
            ('[5, 4, 3, 2, 1]', 'False', False),
            ('[2, 1, 5, 0, 4, 6]', 'True', False),
            ('[20, 100, 10, 12, 5, 13]', 'True', False),
            ('[1, 1, 1, 1]', 'False', False),
            ('[1, 2]', 'False', False),
            ('[2, 4, -2, -3]', 'False', False),
            ('[1, 5, 0, 4, 1, 3]', 'True', False),
            ('[1, 2, 1, 2, 1, 2, 1, 2]', 'False', False),
            ('[0, 4, 2, 1, 0, -1, -2, 5]', 'True', False)]},
 {'slug': 'gas-station',
  'title': 'Gas Station',
  'difficulty': 'medium',
  'description': 'Вдоль кольцевого маршрута расположены `n` заправок. На станции `i` доступно `gas[i]` бензина, а для '
                 'проезда до следующей станции требуется `cost[i]` бензина. Найдите начальную станцию, начав с которой '
                 'можно совершить полный круг по часовой стрелке. Если маршрут невозможен, верните -1.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])  # Вернет: 3 (старт со станции с индексом 3)\n'
                 '```',
  'starter_code': 'def solution(gas: list, cost: list) -> int:\n    pass\n',
  'reference_solution': 'def solution(gas, cost):\n'
                        '    if sum(gas) < sum(cost): return -1\n'
                        '    total = 0\n'
                        '    start = 0\n'
                        '    for i in range(len(gas)):\n'
                        '        total += gas[i] - cost[i]\n'
                        '        if total < 0:\n'
                        '            total = 0\n'
                        '            start = i + 1\n'
                        '    return start',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['greedy', 'arrays'],
  'tests': [('[1, 2, 3, 4, 5], [3, 4, 5, 1, 2]', '3', False),
            ('[2, 3, 4], [3, 4, 3]', '-1', False),
            ('[5, 1, 2, 3, 4], [4, 4, 1, 5, 1]', '4', False),
            ('[3, 1, 1], [1, 2, 2]', '0', False),
            ('[4, 5, 2, 6, 5, 3], [3, 2, 7, 3, 2, 9]', '-1', False),
            ('[2], [2]', '0', False),
            ('[1], [2]', '-1', False),
            ('[5, 8, 2, 8], [6, 5, 6, 6]', '3', False),
            ('[1, 2, 3, 4, 5, 5, 70], [2, 3, 4, 3, 9, 6, 2]', '6', False),
            ('[7, 1, 0, 11, 4], [5, 9, 1, 2, 5]', '3', False)]},
 {'slug': 'partition-labels',
  'title': 'Partition Labels',
  'difficulty': 'medium',
  'description': 'Дана строка `s`. Разбейте строку на как можно большее число частей так, чтобы каждая буква '
                 'встречалась максимум в одной части. Верните список длин этих частей.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("ababcbacadefegdehijhklij")  # Вернет: [9, 7, 8]\n'
                 '```',
  'starter_code': 'def solution(s: str) -> list:\n    pass\n',
  'reference_solution': 'def solution(s):\n'
                        '    last = {c: i for i, c in enumerate(s)}\n'
                        '    start = end = 0\n'
                        '    res = []\n'
                        '    for i, c in enumerate(s):\n'
                        '        end = max(end, last[c])\n'
                        '        if i == end:\n'
                        '            res.append(end - start + 1)\n'
                        '            start = i + 1\n'
                        '    return res',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['greedy', 'strings'],
  'tests': [('"ababcbacadefegdehijhklij"', '[9, 7, 8]', False),
            ('"eccbbbbdec"', '[10]', False),
            ('"a"', '[1]', False),
            ('"abc"', '[1, 1, 1]', False),
            ('"caedbdedda"', '[1, 9]', False),
            ('"defabc"', '[1, 1, 1, 1, 1, 1]', False),
            ('"z"', '[1]', False),
            ('"abaccb"', '[6]', False),
            ('"qiejxqfnqcehy"', '[11, 1, 1]', False),
            ('"vhaflvvvkmqenvanvmqenk"', '[22]', False)]},
 {'slug': 'valid-sudoku',
  'title': 'Valid Sudoku',
  'difficulty': 'medium',
  'description': 'Определите, является ли поле судоку `9 x 9` допустимым. Каждая строка, каждый столбец и каждый из '
                 'девяти квадратов `3 x 3` должны содержать цифры от 1 до 9 без повторений. Пустые клетки обозначены '
                 'символом `.`\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]])  '
                 '# Вернет: True\n'
                 '```',
  'starter_code': 'def solution(board: list) -> bool:\n    pass\n',
  'reference_solution': 'def solution(board):\n'
                        '    rows = [set() for _ in range(9)]\n'
                        '    cols = [set() for _ in range(9)]\n'
                        '    boxes = [set() for _ in range(9)]\n'
                        '    for r in range(9):\n'
                        '        for c in range(9):\n'
                        '            val = str(board[r][c])\n'
                        "            if val == '.' or val == '0': continue\n"
                        '            b = (r // 3) * 3 + (c // 3)\n'
                        '            if val in rows[r] or val in cols[c] or val in boxes[b]:\n'
                        '                return False\n'
                        '            rows[r].add(val)\n'
                        '            cols[c].add(val)\n'
                        '            boxes[b].add(val)\n'
                        '    return True',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['hash-table', 'matrix'],
  'tests': [('[["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]',
             'True',
             False),
            ('[["8","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]',
             'False',
             False),
            ('[[".",".",".",".","5",".",".","1","."],[".","4",".","3",".",".",".",".","."],[".",".",".",".",".","3",".",".","1"],["8",".",".",".",".",".",".","2","."],[".",".","2",".","7",".",".",".","."],[".","1","5",".",".",".",".",".","."],[".",".",".",".",".","2",".",".","."],[".","2",".","9",".",".",".",".","."],[".",".","4",".",".",".",".",".","."]]',
             'False',
             False),
            ('[["1","2","3","4","5","6","7","8","9"],["4","5","6","7","8","9","1","2","3"],["7","8","9","1","2","3","4","5","6"],["2","3","4","5","6","7","8","9","1"],["5","6","7","8","9","1","2","3","4"],["8","9","1","2","3","4","5","6","7"],["3","4","5","6","7","8","9","1","2"],["6","7","8","9","1","2","3","4","5"],["9","1","2","3","4","5","6","7","8"]]',
             'True',
             False),
            ('[["1","1",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."]]',
             'False',
             False),
            ('[[".",".",".",".",".",".",".",".","."],["1",".",".",".",".",".",".",".","."],["1",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."]]',
             'False',
             False),
            ('[[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."]]',
             'True',
             False),
            ('[["5",".",".",".",".",".",".",".","."],["5",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."]]',
             'False',
             False),
            ('[[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".","7",".",".",".",".","."],[".",".",".","7",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."]]',
             'False',
             False),
            ('[["3",".",".",".",".",".",".",".","."],["3",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".","."]]',
             'False',
             False)]},
 {'slug': 'multiply-strings',
  'title': 'Multiply Strings',
  'difficulty': 'medium',
  'description': 'Даны две неотрицательные строки `num1` и `num2`, представляющие целые числа. Верните произведение '
                 '`num1` и `num2`, также представленное в виде строки.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("2", "3")  # Вернет: "6"\n'
                 '```',
  'starter_code': 'def solution(num1: str, num2: str) -> str:\n    pass\n',
  'reference_solution': 'def solution(num1, num2):\n    return str(int(num1) * int(num2))',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['math', 'strings'],
  'tests': [('"2", "3"', '6', False),
            ('"123", "456"', '56088', False),
            ('"0", "0"', '0', False),
            ('"9", "99"', '891', False),
            ('"10", "10"', '100', False),
            ('"100", "0"', '0', False),
            ('"498828660196", "840477629533"', '419254329864656431168468', False),
            ('"1", "1"', '1', False),
            ('"12345", "6789"', '83810205', False),
            ('"99999", "99999"', '9999800001', False)]},
 {'slug': 'reverse-words-in-a-string',
  'title': 'Reverse Words in a String',
  'difficulty': 'medium',
  'description': 'Дана строка `s`. Разверните порядок слов в строке. Слова должны быть разделены одним пробелом, а '
                 'начальные и конечные пробелы удалены.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("the sky is blue")  # Вернет: "blue is sky the"\n'
                 '```',
  'starter_code': 'def solution(s: str) -> str:\n    pass\n',
  'reference_solution': 'def solution(s):\n    return " ".join(s.strip().split()[::-1])',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['two-pointers', 'strings'],
  'tests': [('"the sky is blue"', 'blue is sky the', False),
            ('"  hello world  "', 'world hello', False),
            ('"a good   example"', 'example good a', False),
            ('"word"', 'word', False),
            ('"   "', '', False),
            ('"Alice does not even like bob"', 'bob like even not does Alice', False),
            ('"  Bob    Loves  Alice   "', 'Alice Loves Bob', False),
            ('"1 2 3 4 5"', '5 4 3 2 1', False),
            ('"EPIC  WIN"', 'WIN EPIC', False),
            ('"single"', 'single', False)]},
 {'slug': 'sort-characters-by-frequency',
  'title': 'Sort Characters By Frequency',
  'difficulty': 'medium',
  'description': 'Дана строка `s`. Отсортируйте её в порядке убывания частоты символов. При равной частоте символы '
                 'упорядочиваются по алфавиту для стабильности проверки.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("tree")  # Вернет: "eert" (буква \'e\' встречается 2 раза, \'r\' и \'t\' по 1 разу)\n'
                 '```',
  'starter_code': 'def solution(s: str) -> str:\n    pass\n',
  'reference_solution': 'def solution(s):\n'
                        '    c = Counter(s)\n'
                        '    return "".join(sorted(s, key=lambda ch: (-c[ch], ch)))',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['hash-table', 'strings'],
  'tests': [('"tree"', 'eert', False),
            ('"cccaaa"', 'aaaccc', False),
            ('"Aabb"', 'bbAa', False),
            ('"loveleetcode"', 'eeeelloocdtv', False),
            ('"raeaforexamplerrr"', 'rrrrraaaeeeflmopx', False),
            ('"2a554442f544asfa"', '44444555aaa22ffs', False),
            ('"a"', 'a', False),
            ('""', '', False),
            ('"abracadabra"', 'aaaaabbrrcd', False),
            ('"Mississippi"', 'iiiissssppM', False)]},
 {'slug': 'kth-largest-element-in-an-array',
  'title': 'Kth Largest Element in an Array',
  'difficulty': 'medium',
  'description': 'Дан целочисленный массив `nums` и целое число `k`. Найдите `k`-й по величине элемент массива (с '
                 'учетом дубликатов).\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([3, 2, 1, 5, 6, 4], 2)  # Вернет: 5\n'
                 '```',
  'starter_code': 'def solution(nums: list, k: int) -> int:\n    pass\n',
  'reference_solution': 'def solution(nums, k):\n    return sorted(nums, reverse=True)[k - 1]',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['heap', 'arrays'],
  'tests': [('[3, 2, 1, 5, 6, 4], 2', '5', False),
            ('[3, 2, 3, 1, 2, 4, 5, 5, 6], 4', '4', False),
            ('[1], 1', '1', False),
            ('[2, 1], 1', '2', False),
            ('[2, 1], 2', '1', False),
            ('[7, 6, 5, 4, 3, 2, 1], 5', '3', False),
            ('[100, 200, 300, 400], 1', '400', False),
            ('[-1, 2, 0], 2', '0', False),
            ('[5, 5, 5, 5], 3', '5', False),
            ('[99, 99], 1', '99', False)]},
 {'slug': 'number-of-islands',
  'title': 'Number of Islands',
  'difficulty': 'medium',
  'description': "Дана двумерная карта `grid`, состоящая из '1' (суша) и '0' (вода). Остров окружен водой и образуется "
                 'соединением соседних по горизонтали или вертикали земель. Найдите количество островов.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]])  '
                 '# Вернет: 1\n'
                 '```',
  'starter_code': 'def solution(grid: list) -> int:\n    pass\n',
  'reference_solution': 'def solution(grid):\n'
                        '    if not grid: return 0\n'
                        '    m, n = len(grid), len(grid[0])\n'
                        '    visited = [[False] * n for _ in range(m)]\n'
                        '    count = 0\n'
                        '    def dfs(r, c):\n'
                        "        if r < 0 or r >= m or c < 0 or c >= n or visited[r][c] or str(grid[r][c]) != '1':\n"
                        '            return\n'
                        '        visited[r][c] = True\n'
                        '        dfs(r + 1, c); dfs(r - 1, c); dfs(r, c + 1); dfs(r, c - 1)\n'
                        '    for r in range(m):\n'
                        '        for c in range(n):\n'
                        "            if not visited[r][c] and str(grid[r][c]) == '1':\n"
                        '                dfs(r, c)\n'
                        '                count += 1\n'
                        '    return count',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['depth-first-search', 'matrix'],
  'tests': [('[["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]', '1', False),
            ('[["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]', '3', False),
            ('[["1"]]', '1', False),
            ('[["0"]]', '0', False),
            ('[["1","0","1","0","1"]]', '3', False),
            ('[["1"],["0"],["1"],["0"],["1"]]', '3', False),
            ('[["0","0","0"],["0","0","0"],["0","0","0"]]', '0', False),
            ('[["1","1","1"],["0","1","0"],["1","1","1"]]', '1', False),
            ('[["1","0"],["0","1"]]', '2', False),
            ('[["1","1","0","0"],["0","0","1","1"],["1","1","0","0"],["0","0","1","1"]]', '4', False)]},
 {'slug': 'max-area-of-island',
  'title': 'Max Area of Island',
  'difficulty': 'medium',
  'description': 'Дана бинарная матрица `grid` размера `m x n`. Остров представляет собой группу соседних единиц (по '
                 'вертикали или горизонтали). Площадь острова — это количество единиц в нем. Найдите максимальную '
                 'площадь острова. Если островов нет, верните 0.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([[0,0,1,0,0],[1,1,1,0,0],[0,0,0,1,1]])  # Вернет: 4\n'
                 '```',
  'starter_code': 'def solution(grid: list) -> int:\n    pass\n',
  'reference_solution': 'def solution(grid):\n'
                        '    if not grid: return 0\n'
                        '    m, n = len(grid), len(grid[0])\n'
                        '    visited = [[False] * n for _ in range(m)]\n'
                        '    def dfs(r, c):\n'
                        '        if r < 0 or r >= m or c < 0 or c >= n or visited[r][c] or int(grid[r][c]) != 1:\n'
                        '            return 0\n'
                        '        visited[r][c] = True\n'
                        '        return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)\n'
                        '    max_area = 0\n'
                        '    for r in range(m):\n'
                        '        for c in range(n):\n'
                        '            if not visited[r][c] and int(grid[r][c]) == 1:\n'
                        '                max_area = max(max_area, dfs(r, c))\n'
                        '    return max_area',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['depth-first-search', 'matrix'],
  'tests': [('[[0,0,1,0,0],[1,1,1,0,0],[0,0,0,1,1]]', '4', False),
            ('[[0,0,0,0,0,0,0,0]]', '0', False),
            ('[[1,1],[1,1]]', '4', False),
            ('[[1]]', '1', False),
            ('[[0]]', '0', False),
            ('[[1,0,1],[0,1,0],[1,0,1]]', '1', False),
            ('[[1,1,0,1],[1,1,0,1],[0,0,0,0],[1,1,1,1]]', '4', False),
            ('[[0,1],[1,0]]', '1', False),
            ('[[1,1,1,1,1]]', '5', False),
            ('[[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0]]', '4', False)]},
 {'slug': 'surrounded-regions',
  'title': 'Surrounded Regions',
  'difficulty': 'medium',
  'description': "Дана матрица `board` размера `m x n`, содержащая символы 'X' и 'O'. Захватите все регионы, "
                 "окруженные 'X', заменив в них 'O' на 'X'. Регион, соединенный с краем доски, захватить нельзя.\n"
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]])  # Вернет: '
                 '[["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]\n'
                 '```',
  'starter_code': 'def solution(board: list) -> list:\n    pass\n',
  'reference_solution': 'def solution(board):\n'
                        '    if not board: return []\n'
                        '    m, n = len(board), len(board[0])\n'
                        '    b = [list(row) for row in board]\n'
                        '    def dfs(r, c):\n'
                        "        if r < 0 or r >= m or c < 0 or c >= n or b[r][c] != 'O':\n"
                        '            return\n'
                        "        b[r][c] = 'E'\n"
                        '        dfs(r + 1, c); dfs(r - 1, c); dfs(r, c + 1); dfs(r, c - 1)\n'
                        '    for r in range(m):\n'
                        '        dfs(r, 0); dfs(r, n - 1)\n'
                        '    for c in range(n):\n'
                        '        dfs(0, c); dfs(m - 1, c)\n'
                        '    for r in range(m):\n'
                        '        for c in range(n):\n'
                        "            if b[r][c] == 'O': b[r][c] = 'X'\n"
                        "            elif b[r][c] == 'E': b[r][c] = 'O'\n"
                        '    return b',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['breadth-first-search', 'matrix'],
  'tests': [('[["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]',
             "[['X', 'X', 'X', 'X'], ['X', 'X', 'X', 'X'], ['X', 'X', 'X', 'X'], ['X', 'O', 'X', 'X']]",
             False),
            ('[["X"]]', "[['X']]", False),
            ('[["O"]]', "[['O']]", False),
            ('[["O","O"],["O","O"]]', "[['O', 'O'], ['O', 'O']]", False),
            ('[["X","X"],["X","X"]]', "[['X', 'X'], ['X', 'X']]", False),
            ('[["X","O","X"],["X","O","X"],["X","O","X"]]',
             "[['X', 'O', 'X'], ['X', 'O', 'X'], ['X', 'O', 'X']]",
             False),
            ('[["O","X","O"],["X","O","X"],["O","X","O"]]',
             "[['O', 'X', 'O'], ['X', 'X', 'X'], ['O', 'X', 'O']]",
             False),
            ('[["X","X","X"],["X","O","X"],["X","X","X"]]',
             "[['X', 'X', 'X'], ['X', 'X', 'X'], ['X', 'X', 'X']]",
             False),
            ('[["X","X","X","X"],["X","O","X","X"],["X","X","O","X"],["X","X","X","X"]]',
             "[['X', 'X', 'X', 'X'], ['X', 'X', 'X', 'X'], ['X', 'X', 'X', 'X'], ['X', 'X', 'X', 'X']]",
             False),
            ('[["O","X","X","X"],["X","O","O","X"],["X","X","X","X"]]',
             "[['O', 'X', 'X', 'X'], ['X', 'X', 'X', 'X'], ['X', 'X', 'X', 'X']]",
             False)]},
 {'slug': 'moving-zeros-to-the-end',
  'title': 'Moving Zeros To The End',
  'difficulty': 'medium',
  'description': 'Напишите функцию, которая принимает массив `lst` и перемещает все нули в конец, сохраняя исходный '
                 'порядок всех остальных элементов. Значение `False` нулем не считается.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution([1, 2, 0, 1, 0, 1, 0, 3, 0, 1])  # Вернет: [1, 2, 1, 1, 3, 1, 0, 0, 0, 0]\n'
                 '```',
  'starter_code': 'def solution(lst: list) -> list:\n    pass\n',
  'reference_solution': 'def solution(lst):\n'
                        '    non_zeros = [x for x in lst if x != 0 or x is False]\n'
                        '    zeros = [x for x in lst if x == 0 and x is not False]\n'
                        '    return non_zeros + zeros',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['arrays'],
  'tests': [('[1, 2, 0, 1, 0, 1, 0, 3, 0, 1]', '[1, 2, 1, 1, 3, 1, 0, 0, 0, 0]', False),
            ('[9, 0, 0, 9, 1, 2, 0, 1, 0, 1, 0, 3, 0, 1, 9, 0, 0, 0, 0, 9]',
             '[9, 9, 1, 2, 1, 1, 3, 1, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]',
             False),
            ('[0, 0]', '[0, 0]', False),
            ('[]', '[]', False),
            ('[1, 2, 3]', '[1, 2, 3]', False),
            ("[False, 1, 0, 1, 2, 0, 1, 3, 'a']", "[False, 1, 1, 2, 1, 3, 'a', 0, 0]", False),
            ('[0, 1, None, 2, False, 1, 0]', '[1, None, 2, False, 1, 0, 0]', False),
            ('[0, 0, 0, 1]', '[1, 0, 0, 0]', False),
            ('[1, 0, 0, 0]', '[1, 0, 0, 0]', False),
            ("[0, '0', 1, 0, 2]", "['0', 1, 2, 0, 0]", False)]},
 {'slug': 'simple-pig-latin',
  'title': 'Simple Pig Latin',
  'difficulty': 'medium',
  'description': "Переместите первую букву каждого слова в конец слова и добавьте 'ay'. Знаки препинания должны "
                 'остаться нетронутыми.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("Pig latin is cool")  # Вернет: "igPay atinlay siay oolcay"\n'
                 '```',
  'starter_code': 'def solution(text: str) -> str:\n    pass\n',
  'reference_solution': 'def solution(text):\n'
                        "    words = text.split(' ')\n"
                        '    res = []\n'
                        '    for w in words:\n'
                        '        if w.isalpha():\n'
                        "            res.append(w[1:] + w[0] + 'ay')\n"
                        '        else:\n'
                        '            res.append(w)\n'
                        "    return ' '.join(res)",
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['strings'],
  'tests': [('"Pig latin is cool"', 'igPay atinlay siay oolcay', False),
            ('"This is my string"', 'hisTay siay ymay tringsay', False),
            ('"Hello world !"', 'elloHay orldway !', False),
            ('"O tempora o mores !"', 'Oay emporatay oay oresmay !', False),
            ('"Quis custodiet ipsos custodes ?"', 'uisQay ustodietcay psosiay ustodescay ?', False),
            ('"Acta est fabula"', 'ctaAay steay abulafay', False),
            ('"Barba non facit philosophum"', 'arbaBay onnay acitfay hilosophumpay', False),
            ('"De omnibus dubitandum"', 'eDay mnibusoay ubitandumday', False),
            ('"In vino veritas"', 'nIay inovay eritasvay', False),
            ('"Carpe diem !"', 'arpeCay iemday !', False)]},
 {'slug': 'human-readable-time',
  'title': 'Human Readable Time',
  'difficulty': 'medium',
  'description': 'Напишите функцию, которая принимает неотрицательное целое число (секунды) и возвращает время в '
                 'удобочитаемом формате `HH:MM:SS`.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(359999)  # Вернет: "99:59:59"\n'
                 '```',
  'starter_code': 'def solution(seconds: int) -> str:\n    pass\n',
  'reference_solution': 'def solution(seconds):\n'
                        '    h = seconds // 3600\n'
                        '    m = (seconds % 3600) // 60\n'
                        '    s = seconds % 60\n'
                        '    return f"{h:02d}:{m:02d}:{s:02d}"',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['math', 'strings'],
  'tests': [('0', '00:00:00', False),
            ('59', '00:00:59', False),
            ('60', '00:01:00', False),
            ('3599', '00:59:59', False),
            ('3600', '01:00:00', False),
            ('45296', '12:34:56', False),
            ('86399', '23:59:59', False),
            ('86400', '24:00:00', False),
            ('359999', '99:59:59', False),
            ('12345', '03:25:45', False)]},
 {'slug': 'valid-parentheses-string',
  'title': 'Valid Parentheses String',
  'difficulty': 'medium',
  'description': "Дана строка `s`, содержащая только символы '(', ')' и '*'. Символ '*' может считаться как '(', так и "
                 "')', или пустой строкой. Определите, является ли скобочная последовательность допустимой.\n"
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("(*))")  # Вернет: True\n'
                 '```',
  'starter_code': 'def solution(s: str) -> bool:\n    pass\n',
  'reference_solution': 'def solution(s):\n'
                        '    low = high = 0\n'
                        '    for c in s:\n'
                        "        if c == '(':\n"
                        '            low += 1\n'
                        '            high += 1\n'
                        "        elif c == ')':\n"
                        '            low = max(0, low - 1)\n'
                        '            high -= 1\n'
                        "        elif c == '*':\n"
                        '            low = max(0, low - 1)\n'
                        '            high += 1\n'
                        '        if high < 0:\n'
                        '            return False\n'
                        '    return low == 0',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['greedy', 'strings'],
  'tests': [('"()"', 'True', False),
            ('"(*)"', 'True', False),
            ('"(*))"', 'True', False),
            ('")("', 'False', False),
            ('"(*()"', 'True', False),
            ('"(((((*(()(((*((**(((()*****()()*)())()"', 'False', False),
            ('"(((((*)))**"', 'True', False),
            ('"***"', 'True', False),
            ('""', 'True', False),
            ('"(((((*"', 'False', False)]},
 {'slug': 'rgb-to-hex-conversion',
  'title': 'RGB To Hex Conversion',
  'difficulty': 'medium',
  'description': 'Реализуйте функцию, которая переводит десятичные значения RGB в шестнадцатеричный код цвета из 6 '
                 'заглавных символов. Значения меньше 0 округляются до 0, а больше 255 — до 255.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution(255, 255, 300)  # Вернет: "FFFFFF"\n'
                 '```',
  'starter_code': 'def solution(r: int, g: int, b: int) -> str:\n    pass\n',
  'reference_solution': 'def solution(r, g, b):\n'
                        '    def clamp(x):\n'
                        '        return max(0, min(255, x))\n'
                        '    return f"{clamp(r):02X}{clamp(g):02X}{clamp(b):02X}"',
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['math', 'strings'],
  'tests': [('0, 0, 0', '000000', False),
            ('1, 2, 3', '010203', False),
            ('255, 255, 255', 'FFFFFF', False),
            ('254, 253, 252', 'FEFDFC', False),
            ('-20, 275, 125', '00FF7D', False),
            ('255, 255, 300', 'FFFFFF', False),
            ('148, 0, 211', '9400D3', False),
            ('173, 255, 47', 'ADFF2F', False),
            ('0, 0, -5', '000000', False),
            ('300, 300, 300', 'FFFFFF', False)]},
 {'slug': 'rot13',
  'title': 'Rot13',
  'difficulty': 'medium',
  'description': 'Напишите функцию, которая принимает строку и возвращает зашифрованную строку с помощью шифра ROT13 '
                 '(сдвиг каждой буквы на 13 позиций в алфавите с сохранением регистра). Символы, не являющиеся '
                 'буквами, должны остаться без изменений.\n'
                 '\n'
                 '### Пример работы:\n'
                 '```python\n'
                 'solution("test")  # Вернет: "grfg"\n'
                 '```',
  'starter_code': 'def solution(message: str) -> str:\n    pass\n',
  'reference_solution': 'def solution(message):\n'
                        '    res = []\n'
                        '    for c in message:\n'
                        "        if 'a' <= c <= 'z':\n"
                        "            res.append(chr((ord(c) - ord('a') + 13) % 26 + ord('a')))\n"
                        "        elif 'A' <= c <= 'Z':\n"
                        "            res.append(chr((ord(c) - ord('A') + 13) % 26 + ord('A')))\n"
                        '        else:\n'
                        '            res.append(c)\n'
                        "    return ''.join(res)",
  'reference_solution_explanation': 'Оптимальное решение задачи с использованием стандартных структур данных Python.',
  'tags': ['ciphers', 'strings'],
  'tests': [('"test"', 'grfg', False),
            ('"Test"', 'Grfg', False),
            ('"Ruby is cool!"', 'Ehol vf pbby!', False),
            ('"10+2 is twelve."', '10+2 vf gjryir.', False),
            ('"aA bB zZ"', 'nN oO mM', False),
            ('"Codewars"', 'Pbqrjnef', False),
            ('"grfg"', 'test', False),
            ('"Hello, World!"', 'Uryyb, Jbeyq!', False),
            ('"abcdefghijklmnopqrstuvwxyz"', 'nopqrstuvwxyzabcdefghijklm', False),
            ('"The quick brown fox jumps over the lazy dog."', 'Gur dhvpx oebja sbk whzcf bire gur ynml qbt.', False)]},
 {'slug': 'pangram-check',
  'title': 'Поиск панграммы',
  'difficulty': 'easy',
  'description': '### Условие задачи\r\n'
                 '\r\n'
                 '**Панграмма** — это текст, в котором используются все буквы алфавита по крайней мере один раз.\r\n'
                 '\r\n'
                 'Вам на вход подается список, содержащий ровно одно предложение (строку) на английском языке. '
                 'Напишите функцию `solution`, которая проверяет, является ли это предложение панграммой. Функция '
                 'должна возвращать `True`, если в предложении присутствуют все **26 букв** английского алфавита '
                 '(регистр букв не имеет значения), и `False` в противном случае.\r\n'
                 '\r\n'
                 'Символы, не являющиеся буквами английского алфавита (знаки препинания, цифры, пробелы), при проверке '
                 'следует игнорировать.\r\n'
                 '\r\n'
                 '### Входные данные\r\n'
                 '* `sentence_list` (list): Список, содержащий одну строку.\r\n'
                 '\r\n'
                 '### Выходные данные\r\n'
                 '* `bool`: `True`, если строка является панграммой английского алфавита, иначе `False`.\r\n'
                 '\r\n'
                 '### Примеры использования\r\n'
                 '\r\n'
                 '**Пример 1:**\r\n'
                 '* Входные данные: `["The quick brown fox jumps over the lazy dog"]`\r\n'
                 '* Выходные данные: `True`\r\n'
                 '* Объяснение: В этой фразе содержатся абсолютно все буквы английского алфавита от `a` до `z`.\r\n'
                 '\r\n'
                 '**Пример 2:**\r\n'
                 '* Входные данные: `["Hello World"]`\r\n'
                 '* Выходные данные: `False`\r\n'
                 '* Объяснение: В этой строке отсутствуют многие буквы английского алфавита (например, `a`, `b`, `c` и '
                 'другие).',
  'starter_code': 'def solution(sentence_list):\r\n    # Ваш код здесь\r\n    pass',
  'reference_solution': 'def solution(sentence_list):\n'
                        "    text = ''.join(sentence_list).lower()\n"
                        "    return set('abcdefghijklmnopqrstuvwxyz').issubset(set(text))",
  'reference_solution_explanation': 'Объединяем список предложений в одну строку в нижнем регистре и проверяем, '
                                    'содержит ли она все буквы английского алфавита.',
  'tags': ['dicts', 'arrays', 'strings'],
  'tests': [('["The quick brown fox jumps over the lazy dog"]', 'True', False),
            ('["Hello World"]', 'False', False),
            ('["Pack my box with five dozen liquor jugs."]', 'True', False),
            ('["The quick brown fox jumps over the lay dog"]', 'False', False),
            ('[""]', 'False', False),
            ('["THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"]', 'True', False),
            ('["1234567890!@#$%^&*()_+"]', 'False', False),
            ('["How vexingly quick daft zebras jump!"]', 'True', False),
            ('["Sphinx of black quartz, judge my vow."]', 'True', False),
            ('["Not a pangram at all"]', 'False', False),
            ('["Two driven jocks help fax my big quiz."]', 'True', False),
            ('["Python programming language"]', 'False', False)]}]

# ==============================================================================
# SEEDER RUNNER
# ==============================================================================

def run_seeder(stdout=None, style=None):
    """
    Executes database seeding:
    1. Default achievements
    2. Admin superuser (if not exists)
    3. All 129 tasks with tags and test cases
    """
    def log(msg, is_success=False):
        if stdout and style:
            if is_success:
                stdout.write(style.SUCCESS(msg))
            else:
                stdout.write(msg)
        else:
            print(msg)

    log("--- Starting SmartCode Database Seeding ---")

    # 1. Seed Achievements
    try:
        GamificationService.seed_achievements()
        log("[OK] Achievements seeded successfully.", is_success=True)
    except Exception as e:
        log(f"[WARN] Could not seed achievements: {e}")

    # 2. Seed Superuser (admin / admin) if none exists
    User = get_user_model()
    admin_username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    admin_email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    admin_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin')

    admin_user = User.objects.filter(username=admin_username).first()
    if not admin_user:
        admin_user = User.objects.create_superuser(
            username=admin_username,
            email=admin_email,
            password=admin_password
        )
        log(f"[OK] Created superuser '{admin_username}' (password: '{admin_password}').", is_success=True)
    else:
        if not admin_user.is_superuser:
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.save()
        log(f"[INFO] Superuser '{admin_username}' already exists.")

    # 3. Seed Tasks, Tags and Test Cases
    created_tasks = 0
    updated_tasks = 0
    total_tests = 0

    with transaction.atomic():
        for item in TASKS_DATA:
            task, created = Task.objects.update_or_create(
                slug=item['slug'],
                defaults={
                    'title': item['title'],
                    'difficulty': item['difficulty'],
                    'description': item['description'],
                    'starter_code': item['starter_code'],
                    'reference_solution': item.get('reference_solution', ''),
                    'reference_solution_explanation': item.get('reference_solution_explanation', ''),
                }
            )
            if created:
                created_tasks += 1
            else:
                updated_tasks += 1

            # Sync tags
            tag_objs = []
            for tag_slug in item.get('tags', []):
                tag_name = tag_slug.replace('-', ' ').title()
                tag_obj, _ = Tag.objects.get_or_create(
                    slug=tag_slug,
                    defaults={'name': tag_name, 'color': 'primary'}
                )
                tag_objs.append(tag_obj)
            task.tags.set(tag_objs)

            # Sync test cases
            task.test_cases.all().delete()
            test_cases_to_create = []
            for in_data, exp_out, is_hid in item.get('tests', []):
                test_cases_to_create.append(
                    TestCase(
                        task=task,
                        input_data=in_data,
                        expected_output=exp_out,
                        is_hidden=is_hid
                    )
                )
            TestCase.objects.bulk_create(test_cases_to_create)
            total_tests += len(test_cases_to_create)

    log(
        f"[SUCCESS] Database seeding complete! "
        f"Tasks: {len(TASKS_DATA)} (created: {created_tasks}, updated: {updated_tasks}), "
        f"Total test cases: {total_tests}.",
        is_success=True
    )


if __name__ == '__main__':
    run_seeder()
