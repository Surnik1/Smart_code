import re
import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

def clean_latex_and_math(text: str) -> str:
    """
    Удаляет синтаксис формул LaTeX ($...$), который ИИ иногда генерирует
    для обозначения сложности O(n), заменяя на чистый и читаемый текст.
    """
    if not text:
        return ""

    # \$\s*\\mathcal\{O\}\((.*?)\)\s*\$ -> O(\1)
    text = re.sub(r'\$\s*\\mathcal\{[Oo]\}\((.*?)\)\s*\$', r'O(\1)', text)
    # \\mathcal\{O\}\((.*?)\) -> O(\1)
    text = re.sub(r'\\mathcal\{[Oo]\}\((.*?)\)', r'O(\1)', text)
    # \$\s*O\((.*?)\)\s*\$ -> O(\1)
    text = re.sub(r'\$\s*O\((.*?)\)\s*\$', r'O(\1)', text)
    # \$\s*\\Theta\((.*?)\)\s*\$ -> Θ(\1)
    text = re.sub(r'\$\s*\\Theta\((.*?)\)\s*\$', r'Θ(\1)', text)
    # \$\s*\\Omega\((.*?)\)\s*\$ -> Ω(\1)
    text = re.sub(r'\$\s*\\Omega\((.*?)\)\s*\$', r'Ω(\1)', text)
    # Одиночные переменные в $...$ например $N$ -> N, $i$ -> i
    text = re.sub(r'\$([A-Za-z0-9_+\-*^/ ]+)\$', r'\1', text)

    return text

@register.filter(name='render_markdown')
def render_markdown_filter(value):
    """
    Преобразует Markdown-текст (условие задачи, подсказки) в безопасный HTML.
    Поддерживает таблицы, блоки кода, списки, жирный текст и очистку от LaTeX.
    """
    if not value:
        return ""
    
    cleaned = clean_latex_and_math(str(value))
    html = markdown.markdown(
        cleaned,
        extensions=[
            'extra',
            'nl2br',
            'sane_lists',
        ]
    )
    return mark_safe(html)

