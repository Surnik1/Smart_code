import ast
import time
from typing import Any, Dict, List
from func_timeout import func_timeout, FunctionTimedOut

# Белый список безопасных встроенных функций и типов Python
SAFE_BUILTINS: Dict[str, Any] = {
    'abs': abs,
    'all': all,
    'any': any,
    'ascii': ascii,
    'bin': bin,
    'bool': bool,
    'bytearray': bytearray,
    'bytes': bytes,
    'chr': chr,
    'complex': complex,
    'dict': dict,
    'divmod': divmod,
    'enumerate': enumerate,
    'filter': filter,
    'float': float,
    'format': format,
    'frozenset': frozenset,
    'hex': hex,
    'int': int,
    'isinstance': isinstance,
    'issubclass': issubclass,
    'iter': iter,
    'len': len,
    'list': list,
    'map': map,
    'max': max,
    'min': min,
    'next': next,
    'oct': oct,
    'ord': ord,
    'pow': pow,
    'print': print,
    'range': range,
    'repr': repr,
    'reversed': reversed,
    'round': round,
    'set': set,
    'slice': slice,
    'sorted': sorted,
    'str': str,
    'sum': sum,
    'tuple': tuple,
    'zip': zip,
    # Исключения
    'Exception': Exception,
    'ValueError': ValueError,
    'TypeError': TypeError,
    'IndexError': IndexError,
    'KeyError': KeyError,
    'ZeroDivisionError': ZeroDivisionError,
    'AssertionError': AssertionError,
    'AttributeError': AttributeError,
    'RuntimeError': RuntimeError,
    'StopIteration': StopIteration,
    # Константы
    'True': True,
    'False': False,
    'None': None,
}

FORBIDDEN_CALL_NAMES = {
    '__import__', 'eval', 'exec', 'compile', 'open', 'globals', 'locals',
    'getattr', 'setattr', 'delattr', 'input', 'breakpoint', 'help',
    'exit', 'quit'
}


class SecurityASTValidator(ast.NodeVisitor):
    """
    Статический AST-анализатор для проверки кода перед выполнением.
    Блокирует импорты, доступ к dunder/приватным атрибутам и опасным вызовам.
    """
    def visit_Import(self, node: ast.Import):
        raise SecurityError(f"Импорт модулей запрещен (строка {node.lineno}).")

    def visit_ImportFrom(self, node: ast.ImportFrom):
        raise SecurityError(f"Импорт модулей через 'from ... import' запрещен (строка {node.lineno}).")

    def visit_Attribute(self, node: ast.Attribute):
        # Запрещаем любые обращения к атрибутам, начинающимся с '_' (защита от __class__, __subclasses__, __globals__ и т.д.)
        if node.attr.startswith('_'):
            raise SecurityError(
                f"Доступ к приватным и специальным атрибутам ('{node.attr}') запрещен в целях безопасности (строка {node.lineno})."
            )
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            if node.func.id in FORBIDDEN_CALL_NAMES:
                raise SecurityError(f"Вызов функции '{node.func.id}' запрещен (строка {node.lineno}).")
        self.generic_visit(node)


class SecurityError(Exception):
    """Исключение при нарушении политик безопасности"""
    pass


def parse_test_inputs(input_str: str) -> List[Any]:
    """
    Безопасный парсинг входных аргументов тест-кейса с помощью ast.literal_eval.
    Исключает произвольное выполнение кода при обработке входных данных тестов.
    """
    cleaned = input_str.strip()
    if not cleaned:
        return []

    try:
        return ast.literal_eval(f"[{cleaned}]")
    except Exception:
        # Попытка парсинга как единичной строки
        try:
            return ast.literal_eval(f"['{cleaned}']")
        except Exception as err:
            raise ValueError(f"Не удалось безопасно распознать входные данные: '{input_str}' ({err})")


class StdoutCollector:
    """
    Изолированный потокобезопасный сборщик вывода print() с защитой от переполнения памяти.
    """
    def __init__(self, max_chars: int = 5000):
        self.max_chars = max_chars
        self.chunks: List[str] = []
        self.current_length = 0

    def print(self, *args, sep=' ', end='\n'):
        text = sep.join(str(a) for a in args) + end
        if self.current_length < self.max_chars:
            remaining = self.max_chars - self.current_length
            if len(text) > remaining:
                self.chunks.append(text[:remaining] + "\n... [вывод обрезан из-за превышения лимита 5000 символов]")
                self.current_length = self.max_chars
            else:
                self.chunks.append(text)
                self.current_length += len(text)

    def get_output(self) -> str:
        return "".join(self.chunks).strip()


class CodeRunnerService:
    """
    Сервис для безопасной компиляции, валидации и выполнения кода задачи.
    """

    @staticmethod
    def validate_code(code: str):
        """
        Проверяет синтаксис и безопасность исходного кода через AST.
        """
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            raise SyntaxError(f"Синтаксическая ошибка в коде: {e.msg} (строка {e.lineno})")

        validator = SecurityASTValidator()
        validator.visit(tree)

    @classmethod
    def execute_solution(cls, code: str, test_cases, timeout_seconds: float = 10.0) -> Dict[str, Any]:
        """
        Выполняет решение против списка тестов с ограничением по времени и защитой.
        Возвращает словарь:
        {
            'passed': bool,
            'status': str ('passed' | 'failed' | 'error' | 'timeout'),
            'message': str,
            'execution_time': float (в секундах)
        }
        """
        if not test_cases.exists():
            return {
                'passed': False,
                'status': 'error',
                'message': 'Ошибка: Для данной задачи еще не настроены проверочные тест-кейсы.',
                'execution_time': 0.0,
            }

        # 1. Статическая проверка безопасности кода
        try:
            cls.validate_code(code)
        except (SecurityError, SyntaxError) as e:
            return {
                'passed': False,
                'status': 'error',
                'message': f"⚠️ {str(e)}",
                'execution_time': 0.0,
            }

        # 2. Изолированная компиляция и инициализация
        local_scope: Dict[str, Any] = {}
        collector = StdoutCollector()
        safe_builtins = SAFE_BUILTINS.copy()
        safe_builtins['print'] = collector.print
        safe_globals = {'__builtins__': safe_builtins}

        try:
            compiled_code = compile(code, '<user_code>', 'exec')
            exec(compiled_code, safe_globals, local_scope)
        except Exception as e:
            return {
                'passed': False,
                'status': 'error',
                'message': f"Ошибка инициализации кода: {type(e).__name__}: {str(e)}",
                'execution_time': 0.0,
                'stdout': collector.get_output(),
            }

        if 'solution' not in local_scope or not callable(local_scope['solution']):
            return {
                'passed': False,
                'status': 'error',
                'message': "Ошибка: Функция 'solution' не найдена или не является вызываемой.",
                'execution_time': 0.0,
                'stdout': collector.get_output(),
            }

        solution_func = local_scope['solution']
        total_time = 0.0

        # 3. Прогон по тест-кейсам
        for index, test in enumerate(test_cases, start=1):
            try:
                args = parse_test_inputs(test.input_data)
            except ValueError as e:
                return {
                    'passed': False,
                    'status': 'error',
                    'message': f"Ошибка в формате тест-кейса #{index}: {str(e)}",
                    'execution_time': total_time,
                    'stdout': collector.get_output(),
                }

            start_t = time.perf_counter()
            try:
                output = func_timeout(timeout_seconds, solution_func, args=args)
                elapsed = time.perf_counter() - start_t
                total_time += elapsed

                actual_str = str(output).strip()
                expected_str = str(test.expected_output).strip()

                if actual_str != expected_str:
                    test_label = f"Тест #{index}" if not test.is_hidden else f"Скрытый тест #{index}"
                    input_display = test.input_data if not test.is_hidden else "[Скрыто]"
                    expected_display = test.expected_output if not test.is_hidden else "[Скрыто]"
                    
                    return {
                        'passed': False,
                        'status': 'failed',
                        'message': f"{test_label} не пройден! Вход: {input_display} | Ожидалось: {expected_display} | Получено: {actual_str}",
                        'execution_time': round(total_time, 4),
                        'stdout': collector.get_output(),
                    }

            except FunctionTimedOut:
                return {
                    'passed': False,
                    'status': 'timeout',
                    'message': f"⏱ Превышено время ожидания ({timeout_seconds} сек) на тесте #{index}! Проверьте код на бесконечные циклы.",
                    'execution_time': round(timeout_seconds, 4),
                    'stdout': collector.get_output(),
                }
            except Exception as e:
                return {
                    'passed': False,
                    'status': 'error',
                    'message': f"Ошибка выполнения (Runtime Error) на тесте #{index}: {type(e).__name__}: {str(e)}",
                    'execution_time': round(total_time, 4),
                    'stdout': collector.get_output(),
                }

        return {
            'passed': True,
            'status': 'passed',
            'message': f"🎉 Все тесты ({test_cases.count()} шт.) успешно пройдены!",
            'execution_time': round(total_time, 4),
            'stdout': collector.get_output(),
        }

    @classmethod
    def execute_custom_test(
        cls,
        code: str,
        custom_input: str,
        timeout_seconds: float = 5.0
    ) -> Dict[str, Any]:
        """
        Запускает функцию solution на пользовательских входных данных.
        Возвращает результат вызова, вывод print() и время работы.
        """
        try:
            cls.validate_code(code)
        except (SecurityError, SyntaxError) as e:
            return {
                'success': False,
                'error': f"⚠️ {str(e)}",
                'stdout': '',
                'result': None,
                'execution_time': 0.0,
            }

        collector = StdoutCollector()
        safe_builtins = SAFE_BUILTINS.copy()
        safe_builtins['print'] = collector.print
        safe_globals = {'__builtins__': safe_builtins}
        local_scope: Dict[str, Any] = {}

        try:
            compiled_code = compile(code, '<user_code>', 'exec')
            exec(compiled_code, safe_globals, local_scope)
        except Exception as e:
            return {
                'success': False,
                'error': f"Ошибка инициализации кода: {type(e).__name__}: {str(e)}",
                'stdout': collector.get_output(),
                'result': None,
                'execution_time': 0.0,
            }

        if 'solution' not in local_scope or not callable(local_scope['solution']):
            return {
                'success': False,
                'error': "Функция 'solution' не найдена или не является вызываемой.",
                'stdout': collector.get_output(),
                'result': None,
                'execution_time': 0.0,
            }

        try:
            args = parse_test_inputs(custom_input)
        except ValueError as e:
            return {
                'success': False,
                'error': f"Ошибка в формате входных данных: {str(e)}",
                'stdout': collector.get_output(),
                'result': None,
                'execution_time': 0.0,
            }

        solution_func = local_scope['solution']
        start_t = time.perf_counter()
        try:
            output = func_timeout(timeout_seconds, solution_func, args=args)
            elapsed = round(time.perf_counter() - start_t, 4)
            return {
                'success': True,
                'result': repr(output),
                'stdout': collector.get_output(),
                'execution_time': elapsed,
                'error': None,
            }
        except FunctionTimedOut:
            return {
                'success': False,
                'error': f"⏱ Превышено время ожидания ({timeout_seconds} сек)!",
                'stdout': collector.get_output(),
                'result': None,
                'execution_time': timeout_seconds,
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Ошибка выполнения: {type(e).__name__}: {str(e)}",
                'stdout': collector.get_output(),
                'result': None,
                'execution_time': round(time.perf_counter() - start_t, 4),
            }


# Module-level convenience alias
execute_custom_test = CodeRunnerService.execute_custom_test

