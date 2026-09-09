import re


def clean_ai_markdown(text: str) -> str:
    """
    Очищает текст от LaTeX-формул и спецсимволов ($...$, \\mathcal{O}),
    заменяя их на читаемый текст (например, 'O(N)', 'N').
    Единая функция для ai_service и markdown_extras (DRY).
    """
    if not text:
        return ""
    # $\mathcal{O}(N)$ -> O(N)
    text = re.sub(r'\$\s*\\mathcal\{[Oo]\}\((.*?)\)\s*\$', r'O(\1)', text)
    # \mathcal{O}(N) -> O(N)
    text = re.sub(r'\\mathcal\{[Oo]\}\((.*?)\)', r'O(\1)', text)
    # $O(N)$ -> O(N)
    text = re.sub(r'\$\s*O\((.*?)\)\s*\$', r'O(\1)', text)
    # $\Theta(N)$ -> Θ(N)
    text = re.sub(r'\$\s*\\Theta\((.*?)\)\s*\$', r'Θ(\1)', text)
    # $\Omega(N)$ -> Ω(N)
    text = re.sub(r'\$\s*\\Omega\((.*?)\)\s*\$', r'Ω(\1)', text)
    # Одиночные переменные $N$ -> N
    text = re.sub(r'\$([A-Za-z0-9_+\-*^/ ]+)\$', r'\1', text)
    return text
