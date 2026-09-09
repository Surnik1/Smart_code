import json
import logging
import os
import re
import time
from typing import Any, Dict, List
from django.conf import settings
from google import genai
from google.genai import types
from challenges.utils import clean_ai_markdown

logger = logging.getLogger(__name__)

# Приоритетные модели с автоматическим переключением (fallback) при перегрузке (503 / 429)
CANDIDATE_MODELS: List[str] = [
    "gemini-3.5-flash",
    "gemini-3.8-flash",
    "gemini-3.6-flash",
    "gemini-flash-latest",
]


class GeminiAIService:
    """
    Интеграция с Google Gemini API для генерации задач, подсказок и ревью кода.
    Включает устойчивость к перегрузкам (503) и автоматический fallback по моделям.
    """

    @classmethod
    def _get_client(cls) -> genai.Client:
        api_key = getattr(
            settings,
            "GEMINI_API_KEY",
            os.environ.get("GEMINI_API_KEY", "")
        )
        if not api_key:
            raise ValueError("GEMINI_API_KEY не настроен в settings / .env")

        import ssl
        try:
            ctx = ssl.create_default_context()
            ctx.load_default_certs()
            http_options = types.HttpOptions(client_args={"verify": ctx})
        except Exception:
            http_options = types.HttpOptions(client_args={"verify": False})

        return genai.Client(api_key=api_key, http_options=http_options)

    @classmethod
    def _generate_with_fallback(
        cls,
        client: genai.Client,
        contents: str,
        config: types.GenerateContentConfig = None
    ) -> str:
        """
        Отправляет запрос к Gemini с автоматическим перебором моделей при 503 (высокая нагрузка)
        или временных ошибках сети/лимитов.
        """
        last_error = None
        for model in CANDIDATE_MODELS:
            for attempt in range(2):
                try:
                    response = client.models.generate_content(
                        model=model,
                        contents=contents,
                        config=config,
                    )
                    if response and response.text:
                        return response.text.strip()
                except Exception as e:
                    err_str = str(e)
                    last_error = e
                    # Если модель перегружена (503) или сработал rate limit (429)
                    if "503" in err_str or "UNAVAILABLE" in err_str or "429" in err_str:
                        logger.warning(
                            f"Модель {model} вернула 503/429 (попытка {attempt + 1}). Переключение на следующую..."
                        )
                        time.sleep(1)
                        continue
                    # Если модель не найдена (404), сразу переходим к следующей модели
                    if "404" in err_str:
                        break
                    # Другая ошибка - пробуем следующую модель
                    break

        if last_error:
            err_str = str(last_error)
            if "503" in err_str or "UNAVAILABLE" in err_str:
                raise RuntimeError("Серверы Gemini сейчас испытывают высокую нагрузку. Пожалуйста, повторите попытку через пару секунд.")
            raise RuntimeError(f"Ошибка Gemini API: {err_str}")

        raise RuntimeError("Не удалось получить ответ от Gemini API.")

    @classmethod
    def generate_task_draft(cls, topic: str) -> Dict[str, Any]:
        """
        Генерирует полную задачу (название, slug, сложность, условие, шаблон, тест-кейсы) по теме учителя.
        Возвращает структурированный словарь.
        """
        client = cls._get_client()

        prompt = f"""
Ты — опытный методист и составитель учебных и олимпиадных задач по программированию на Python.
Учитель хочет создать обучающую задачу со следующим описанием или требованиями:
\"{topic}\"

ВАЖНЫЕ ПРАВИЛА:
1. Если в запросе учителя указано конкретное количество тестов (например: 10, 15, 20 или 30 тестов), сгенерируй именно столько тестов (до 25-30 качественных тестов). Если количество не указано, сгенерируй от 4 до 8 разнообразных тестов.
2. Тесты должны обязательно включать: базовые примеры, крайние случаи (пустые входные данные, нули, отрицательные числа, одиночные элементы, большие значения).
3. В поле "description" используй красивый Markdown БЕЗ синтаксиса LaTeX (НЕ используй знаки $ и \\mathcal). Заголовки делай через ###, термины выделяй **жирным шрифтом**, код — в обратных кавычках `...`.

Создай качественную задачу и верни результат СТРОГО в формате JSON без лишнего текста со следующими полями:
- "title": понятное и интересное название задачи (строка на русском)
- "slug": уникальный url-слаг (английские буквы в нижнем регистре через дефис, например "sum-of-even-numbers")
- "difficulty": сложность задачи ("easy", "medium" или "hard")
- "description": подробное условие задачи в формате Markdown. Обязательно включи: описание задачи, входные и выходные параметры функции, 2 примера вызова с пояснениями.
- "starter_code": начальный шаблон функции solution (например: "def solution(arr):\\n    # Ваш код здесь\\n    pass")
- "suggested_tags": массив из 1-3 подходящих тем на русском (например: ["Списки и массивы", "Циклы и условия"])
- "test_cases": массив тестов. Каждый элемент:
    - "input_data": входные аргументы для вызова функции (например: "5, 10" или "'hello'" или "[1, 2, 3]")
    - "expected_output": ожидаемый результат (например: "15" или "'olleh'" или "6")
    - "is_hidden": логическое значение (первые 2 теста false, остальные true)
"""

        try:
            raw_text = cls._generate_with_fallback(
                client=client,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.7,
                ),
            )
            raw_text = raw_text.strip()
            # Очистка markdown блоков если модель обернула
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]

            raw_text = raw_text.strip()
            # Поиск JSON объекта
            match = re.search(r'(\{.*\})', raw_text, re.DOTALL)
            if match:
                raw_text = match.group(1)

            data = json.loads(raw_text.strip())
            if "description" in data and isinstance(data["description"], str):
                data["description"] = clean_ai_markdown(data["description"])
            return data
        except Exception as e:
            logger.error(f"Ошибка при генерации задачи через Gemini: {e}")
            raise RuntimeError(f"Не удалось сгенерировать задачу: {str(e)}")

    @classmethod
    def get_code_hint(
        cls,
        task_title: str,
        task_description: str,
        user_code: str,
        test_error: str = ""
    ) -> str:
        """
        Формирует наводящую подсказку для ученика.
        СТРОГОЕ ПРАВИЛО: не дает готового кода решения!
        """
        client = cls._get_client()

        prompt = f"""
Ты — доброжелательный, чуткий Senior Python-разработчик и AI-ментор на учебной платформе Smart Code.
Ученик решает задачу: "{task_title}".

Условие задачи:
{task_description}

Текущий код ученика:
```python
{user_code}
```

Результат проверки тестов или ошибка:
{test_error if test_error else "Тесты не пройдены или программа работает некорректно."}

ТВОЯ ЗАДАЧА:
Дать ученику короткую, полезную подсказку (2-4 предложения), чтобы он понял, в чем его ошибка, и додумался до решения САМ.

СТРОЖАЙШИЕ ПРАВИЛА МЕНТОРА:
1. НИ В КОЕМ СЛУЧАЕ НЕ ПИШИ ГОТОВЫЙ КОД РЕШЕНИЯ! Ни единой полной строчки ответа!
2. Укажи на логическую нестыковку, забытое условие, неверный шаг цикла, ошибку в типах данных или краевой случай.
3. Задай наводящий вопрос или обрати внимание на конкретную переменную/место в коде.
4. Отвечай дружелюбно, на русском языке.
5. НЕ используй формулы LaTeX (знаки доллара $, \mathcal). Для акцентов используй Markdown: **жирный шрифт**, а для переменных — `код`.
"""

        try:
            result = cls._generate_with_fallback(
                client=client,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.6,
                ),
            )
            return clean_ai_markdown(result)
        except Exception as e:
            logger.error(f"Ошибка получения подсказки Gemini: {e}")
            raise RuntimeError(f"Ошибка получения подсказки от ИИ: {str(e)}")

    @classmethod
    def review_code(
        cls,
        task_title: str,
        task_description: str,
        user_code: str
    ) -> str:
        """
        Проводит детальный Code Review для уже решенной задачи:
        - Временная и пространственная сложность (O-нотация)
        - Чистота по PEP 8
        - Рефакторинг и лучший вариант реализации
        """
        client = cls._get_client()

        prompt = f"""
Ты — Senior Python Tech Lead. Ученик успешно решил задачу: "{task_title}" (все проверочные тесты пройдены!).
Теперь ученик хочет узнать, как писать код еще профессиональнее, чище и оптимальнее.

Условие задачи:
{task_description}

Решение ученика:
```python
{user_code}
```

Проведи профессиональный разбор по трем пунктам на русском языке:
1. ⚡ **Асимптотическая сложность (Big-O)**: оцени Time Complexity и Space Complexity текущего решения ученика.
2. 🎨 **Чистота и стиль (PEP 8)**: оцени именование, читаемость, избыточные операции или пропущенные идиомы Python (генераторы, встроенные методы и т.д.).
3. 🚀 **Пример эталонного рефакторинга**: покажи более лаконичный / быстрый / питоничный вариант решения с кратким объяснением преимуществ.

ВАЖНЫЕ ПРАВИЛА ОФОРМЛЕНИЯ:
- СТРОГИЙ ЗАПРЕТ НА LATEX: ни в коем случае не используй знаки $ и \\mathcal!
- Пиши Big-O нотацию простым текстом: **O(1)**, **O(N)**, **O(N log N)**, **O(N^2)**.
- Используй Markdown: выделяй названия блоков и ключевые термины **жирным шрифтом**, код оборачивай в блоки ```python, а переменные — в `код`.
"""

        try:
            result = cls._generate_with_fallback(
                client=client,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.4,
                ),
            )
            return clean_ai_markdown(result)
        except Exception as e:
            logger.error(f"Ошибка Code Review Gemini: {e}")
            raise RuntimeError(f"Ошибка проведения анализа кода: {str(e)}")

    @classmethod
    def chat_with_mentor(
        cls,
        task_title: str,
        task_description: str,
        user_code: str,
        test_error: str,
        user_message: str,
        history: List[Dict[str, str]] = None
    ) -> str:
        """
        Интерактивный диалог с AI-ментором.
        Ученик задает конкретный вопрос по своей ошибке/коду.
        Правило: направлять, но НЕ давать готовый код решения целиком!
        """
        client = cls._get_client()

        formatted_history = ""
        if history:
            formatted_history = "\n".join(
                f"{'Ученик' if msg.get('role') == 'user' else 'AI-Ментор'}: {msg.get('text', '')}"
                for msg in history[-6:]
            )

        prompt = f"""
Ты — дружелюбный Senior Python разработчик и личный AI-ментор ученика на платформе Smart Code.
Ученик сейчас решает задачу: "{task_title}".

Условие задачи:
{task_description}

Текущий код ученика:
```python
{user_code if user_code else "# Код пока не написан"}
```

Последняя ошибка или результат тестов:
{test_error if test_error else "Тесты пока не запускались или неизвестны."}

История предыдущего диалога:
{formatted_history if formatted_history else "Это начало диалога."}

Новый вопрос ученика:
\"{user_message}\"

ПРАВИЛА ОТВЕТА:
1. Отвечай кратко, емко, по делу и дружелюбно на русском языке (2-4 абзаца).
2. СТРОЖАЙШИЙ ЗАПРЕТ: НЕ пиши готовый код решения целиком! Направляй мысль ученика, объясняй концепции, логику, типы данных или стандартные функции.
3. НЕ используй формулы LaTeX (никаких $ и \\mathcal). Big-O пиши как O(1), O(N).
4. Оформляй в Markdown: ключевые термины **жирным**, короткие имена `кодом`.
"""

        try:
            result = cls._generate_with_fallback(
                client=client,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.6,
                ),
            )
            return clean_ai_markdown(result)
        except Exception as e:
            logger.error(f"Ошибка в AI-чате Gemini: {e}")
            raise RuntimeError(f"Ошибка чата с ИИ: {str(e)}")
