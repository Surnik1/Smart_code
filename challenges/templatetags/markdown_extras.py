import markdown
import bleach
from django import template
from django.utils.safestring import mark_safe
from challenges.utils import clean_ai_markdown

register = template.Library()

# Разрешённые HTML-теги и атрибуты для безопасного рендеринга Markdown
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'b', 'i', 'u', 'code', 'pre',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li',
    'a', 'blockquote', 'hr',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'span', 'div', 'img', 'del', 'sub', 'sup',
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target', 'rel'],
    'img': ['src', 'alt', 'title', 'width', 'height'],
    'code': ['class'],
    'pre': ['class'],
    'span': ['class'],
    'div': ['class'],
    'td': ['align'],
    'th': ['align'],
}


@register.filter(name='render_markdown')
def render_markdown_filter(value):
    """
    Преобразует Markdown-текст (условие задачи, подсказки) в безопасный HTML.
    Поддерживает таблицы, блоки кода, списки, жирный текст и очистку от LaTeX.
    HTML-вывод санитизируется через bleach для защиты от XSS.
    """
    if not value:
        return ""

    cleaned = clean_ai_markdown(str(value))
    html = markdown.markdown(
        cleaned,
        extensions=[
            'extra',
            'nl2br',
            'sane_lists',
        ]
    )
    safe_html = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
    return mark_safe(safe_html)
