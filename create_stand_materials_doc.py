# -*- coding: utf-8 -*-
"""
Создание документа материалов для стенда со всеми текстами и отдельно вставленными картинками
для легкого копирования в Canva / Corel / Photoshop.
Форматы на выходе: .docx и .pdf
"""

import os
import sys
import docx
from docx.shared import Pt, Inches, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def build_materials_doc():
    doc = docx.Document()

    # Настройка полей
    s = doc.sections[0]
    s.page_width = Mm(210)
    s.page_height = Mm(297)
    s.top_margin = Mm(20)
    s.bottom_margin = Mm(20)
    s.left_margin = Mm(25)
    s.right_margin = Mm(20)

    # Вспомогательные функции
    def add_p(text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=3, space_before=0, line_spacing=1.2, bold=False, italic=False, font_size=12, indent=True):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.line_spacing = line_spacing
        p.paragraph_format.first_line_indent = Mm(10) if indent else Inches(0)
        
        if text:
            run = p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(font_size)
            run.font.bold = bold
            run.font.italic = italic
            run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_title(text, level=1):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if level == 1 else WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(12 if level == 1 else 10)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.first_line_indent = Inches(0)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(15 if level == 1 else 13.5)
        run.font.bold = True
        if level == 1:
            run.font.color.rgb = RGBColor(15, 23, 42)
        else:
            run.font.color.rgb = RGBColor(30, 58, 138)
        return p

    def add_img(img_path, width_in=5.2, caption=""):
        if os.path.exists(img_path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.first_line_indent = Inches(0)
            p.add_run().add_picture(img_path, width=Inches(width_in))
            if caption:
                p_c = doc.add_paragraph()
                p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_c.paragraph_format.space_before = Pt(0)
                p_c.paragraph_format.space_after = Pt(6)
                p_c.paragraph_format.first_line_indent = Inches(0)
                r_c = p_c.add_run(caption)
                r_c.font.name = 'Times New Roman'
                r_c.font.size = Pt(10)
                r_c.font.italic = True
                r_c.font.color.rgb = RGBColor(70, 70, 70)

    def format_cell(cell, text, bold=False, italic=False, font_size=10.0, align=WD_ALIGN_PARAGRAPH.LEFT, bg_color=None):
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = align
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.line_spacing = 1.1
        p.paragraph_format.first_line_indent = Inches(0)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(font_size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = RGBColor(0, 0, 0)
        if bg_color:
            shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>')
            cell._tc.get_or_add_tcPr().append(shading)

    # ----------------------------------------------------
    # ТИТУЛЬНЫЙ БЛОК МАТЕРИАЛОВ
    # ----------------------------------------------------
    add_title("МАТЕРИАЛЫ ДЛЯ ВЫСТАВОЧНОГО СТЕНДА (120 × 100 СМ)", level=1)
    add_p("Проект: Образовательная веб-платформа Smart Code для интерактивного обучения алгоритмам и соревновательного программирования",
          align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, font_size=13, indent=False, space_after=2)
    add_p("Автор: Талғат Нұрәли (11 класс) | Руководитель: Алмашев Нурбек Жархынбекұлы",
          align=WD_ALIGN_PARAGRAPH.CENTER, font_size=11.5, italic=True, indent=False, space_after=2)
    add_p("Специализированный лицей-интернат «БІЛІМ-ИННОВАЦИЯ» г. Талдыкорган",
          align=WD_ALIGN_PARAGRAPH.CENTER, font_size=11, indent=False, space_after=4)
    add_p("Направление: «Экономикалық және әлеуметтік үрдістерді математикалық моделдеу» | Секция: Информатика",
          align=WD_ALIGN_PARAGRAPH.CENTER, font_size=11, bold=True, indent=False, space_after=8)

    add_p("Примечание: Все изображения и тексты в этом документе можно напрямую копировать (правой кнопкой мыши -> Копировать изображение / текст) и вставлять в Canva или любой другой графический редактор.",
          italic=True, font_size=10.5, indent=False, space_after=12)

    logo_img = 'extracted_images/p2_0_image1.png'
    add_img(logo_img, width_in=2.0, caption="Фото 1. Официальный логотип республиканского центра «Дарын»")

    # ----------------------------------------------------
    # СЕКЦИЯ 1. ЛЕВАЯ ПАНЕЛЬ СТЕНДА (30 см)
    # ----------------------------------------------------
    add_title("1. ЛЕВАЯ ПАНЕЛЬ СТЕНДА (СОЛ ЖАҚ ПАНЕЛЬ — 30 СМ)", level=1)

    add_title("1.1. Өзектілігі / Актуальность", level=2)
    add_p("В эпоху динамичного развития искусственного интеллекта и цифровизации национальной экономики алгоритмическая грамотность становится ключевым навыком XXI века. Традиционное школьное обучение информатике сталкивается с рядом системных барьеров: дефицитом интерактивной среды для практики, сложностью локальной настройки сред разработки (IDLE, VS Code) и рутинной проверкой задач учителем. Существующие зарубежные сервисы (LeetCode, Codeforces) ориентированы на профессионалов и требуют дорогостоящих коммерческих подписок ($35/мес). Возникает выраженная необходимость в создании общедоступной отечественной платформы, сочетающей мгновенное тестирование решений, персонального AI-наставника и инструменты управления для школы.")

    add_title("1.2. Мақсаты / Цель исследования", level=2)
    add_p("Проектирование, алгоритмическая разработка и экспериментальное обоснование интерактивной образовательной веб-платформы Smart Code для массового обучения школьников алгоритмизации, соревновательному кодингу и спортивному программированию.")

    add_title("1.3. Міндеттері / Задачи исследования", level=2)
    add_p("• Провести системный анализ платформ автоматизированного тестирования кода и выявить функциональные дефициты для школьного образования.")
    add_p("• Разработать легковесную безопасную AST-песочницу выполнения Python без накладных расходов виртуализации (время отклика менее 15 мс).")
    add_p("• Интегрировать Сократического AI-ментора на базе LLM Gemini с жестким педагогическим запретом на выдачу готового кода и каскадом Fallback Chain.")
    add_p("• Реализовать соревновательный модуль PvP-дуэлей Code Battle 1v1 в реальном времени с транзакционной защитой от Race Condition.")
    add_p("• Создать модуль виртуальных классов с контролем дедлайнов и выгрузкой ведомостей в CSV (Excel).")
    add_p("• Провести опытную апробацию среди 150 учащихся и верифицировать серверный стек комплексом из 44 автоматических тестов.")

    add_title("1.4. Әдістері / Методы исследования", level=2)
    add_p("Статический синтаксический анализ AST-деревьев Python; транзакционное управление параллелизмом в СУБД (блокировка select_for_update); Сократическое системное промптирование нейросетей; педагогический сравнительный эксперимент (контрольная и экспериментальная группы по 50 чел.); анкетирование 150 респондентов; методы математической статистики.")

    # ----------------------------------------------------
    # СЕКЦИЯ 2. ЦЕНТРАЛЬНАЯ ПАНЕЛЬ СТЕНДА (60 см)
    # ----------------------------------------------------
    doc.add_page_break()
    add_title("2. ЦЕНТРАЛЬНАЯ ПАНЕЛЬ СТЕНДА (ОРТАЛЫҚ ПАНЕЛЬ — 60 СМ)", level=1)

    add_title("2.1. Исследовательский вопрос и рабочая гипотеза", level=2)
    add_p("Исследовательский вопрос: Как преодолеть инструментальный и мотивационный барьеры школьников при изучении сложных алгоритмов, предотвратить бездумное списывание и обеспечить качественную индивидуализацию обучения без увеличения нагрузки на учителя?", bold=True)
    add_p("Гипотеза исследования: Внедрение отечественной веб-платформы Smart Code, объединяющей мгновенную AST-песочницу, диалогового Сократического AI-наставника без выдачи готового кода и турнирные PvP-дуэли 1v1, повысит академическую успеваемость более чем на 20%, сократит время преодоления учебных тупиков и сформирует культуру академической честности.")

    add_title("2.2. Архитектура программного комплекса Smart Code", level=2)
    add_p("Система построена по паттерну Service-Layer Architecture на базе веб-фреймворка Django 5.2 (Python 3.11). Прикладная бизнес-логика строго инкапсулирована в сервисах CodeRunnerService, GeminiAIService и GamificationService, что обеспечивает высокую масштабируемость и модульность.")

    arch_img = 'smart_code_arch.png'
    add_img(arch_img, width_in=5.4, caption="Фото 2. Структурная архитектурная схема программного комплекса Smart Code")

    add_p("Ключевые технологические инновации:")
    add_p("1. Легковесная AST-песочница: безопасность выполнения кода обеспечивается на уровне синтаксического дерева (SecurityASTValidator) с блокировкой системных вызовов и dunder-атрибутов (__subclasses__). Время отклика — 12 мс (в 60 раз быстрее запуска Docker-контейнеров).")
    add_p("2. Socratic AI-ментор (Gemini): промпт ориентирует модель помогать наводящими вопросами по логике непройденного теста, категорически запрещая выдавать готовый код решения. Реализован каскадный переход Fallback Chain при превышении квот.")
    add_p("3. PvP Code Battle 1v1: синхронные дуэли в реальном времени с атомарным транзакционным локом select_for_update(), исключающим коллизии при одновременной отправке верных решений.")
    add_p("4. Контроль академической честности (TaskSolutionView): при открытии эталонного ответа персистентно блокируется начисление опыта (XP) и зачет в лидерборде.")

    # ----------------------------------------------------
    # АНКЕТИРОВАНИЕ И РЕЗУЛЬТАТЫ
    # ----------------------------------------------------
    doc.add_page_break()
    add_title("2.3. Результаты педагогического эксперимента и опроса 150 учащихся", level=2)
    add_p("В ходе независимого онлайн-анкетирования через Google Forms среди 150 учащихся старших классов лицея была получена высокая статистическая оценка каждого функционального модуля платформы:")

    chart1 = 'chart_monaco.png'
    add_img(chart1, width_in=4.6, caption="Фото 3. Оценка эргономики редактора Monaco Editor в сравнении с IDLE (80.7% признали намного удобнее)")

    chart2 = 'chart_ai.png'
    add_img(chart2, width_in=4.6, caption="Фото 4. Эффективность подсказок AI-ментора в самостоятельном поиске ошибок (76.0% находят решения сами)")

    chart3 = 'chart_classroom.png'
    add_img(chart3, width_in=4.6, caption="Фото 5. Оценка удобства мониторинга домашних заданий и дедлайнов в виртуальном классе (86.0% очень удобно)")

    add_title("2.4. Сравнительная таблица показателей контрольной и экспериментальной групп", level=2)
    add_p("Педагогический эксперимент (КГ 50 уч. vs ЭГ 50 уч.) подтвердил статистически достоверный рост по всем учебным метрикам:")

    t = doc.add_table(rows=5, cols=4)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdrs = ["Исследуемый показатель успеваемости", "Контрольная группа (КГ)", "Экспериментальная группа (ЭГ)", "Динамика прироста"]
    for j, h in enumerate(hdrs):
        format_cell(t.cell(0, j), h, bold=True, bg_color="E2E8F0", align=WD_ALIGN_PARAGRAPH.CENTER)

    t_data = [
        ["Средний процент успешной сдачи задач", "58.4%", "82.7%", "+24.3% (p < 0.01)"],
        ["Среднее время решения одной задачи", "38.2 мин", "27.3 мин", "-28.5% (ускорение)"],
        ["Доля самостоятельных решений без сдачи", "46.2%", "78.9%", "+32.7% прирост"],
        ["Итоговый балл зачетного контеста (из 100)", "64.8 ± 3.2", "85.6 ± 2.4", "+20.8 балла"]
    ]
    for i, row in enumerate(t_data):
        bg = "F8FAFC" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row):
            bold_flag = (j == 0 or j == 3)
            format_cell(t.cell(i+1, j), val, bold=bold_flag, bg_color=bg, align=WD_ALIGN_PARAGRAPH.CENTER if j > 0 else WD_ALIGN_PARAGRAPH.LEFT)

    # ----------------------------------------------------
    # СЕКЦИЯ 3. ПРАВАЯ ПАНЕЛЬ СТЕНДА (30 см)
    # ----------------------------------------------------
    doc.add_page_break()
    add_title("3. ПРАВАЯ ПАНЕЛЬ СТЕНДА (ОҢ ЖАҚ ПАНЕЛЬ — 30 СМ)", level=1)

    add_title("3.1. Қорытындылар / Выводы исследования", level=2)
    add_p("1. Доказана высокая педагогическая эффективность дидактического синтеза интерактивной песочницы, диалогового AI-наставника и соревновательных механизмов геймификации.")
    add_p("2. Реализована оригинальная трехуровневая модель безопасности Python AST, обеспечивающая отклик менее 15 мс и абсолютную нейтрализацию RCE-атак без накладных расходов виртуализации.")
    add_p("3. Внедрен Сократический диалоговый ментор Gemini, стимулирующий самостоятельное устранение логических ошибок и сохраняющий познавательную активность учащегося.")
    add_p("4. Спроектирован модуль дуэлей Code Battle 1v1 с транзакционным локом select_for_update(), полностью устранивший проблему состояния гонки.")
    add_p("5. Подтверждена гипотеза исследования: успеваемость выросла на 24.3%, время преодоления учебных тупиков сократилось на 28.5%, а процент самостоятельных решений возрос на 32.7%.")
    add_p("6. Платформа верифицирована 44 автоматическими тестами (100% OK), подтвердив промышленную надежность серверного стека.")

    add_title("3.2. Практикалық маңызы / Практическая ценность", level=2)
    add_p("• Импортозамещение: создание суверенной отечественной платформы взамен зарубежных платных аналогов (LeetCode $35/мес на ученика, Stepik).")
    add_p("• Экономическая эффективность: проект разработан на открытом стеке, серверные затраты составляют всего 10 000–15 000 тенге в месяц на 500 активных пользователей.")
    add_p("• Экономия времени учителя: автоматизация проверки, сведение матриц сдачи заданий и экспорт ведомостей в CSV высвобождают до 6–8 часов рабочего времени учителя еженедельно.")
    add_p("• Готовность к масштабированию: система готова к полномасштабному внедрению в средних общеобразовательных школах, IT-лицеях и центрах подготовки олимпийского резерва Республики Казахстан.")

    add_title("3.3. Дереккөздер / Список литературы", level=2)
    add_p("1. Государственная программа развития образования и науки Республики Казахстан на 2020–2025 годы.")
    add_p("2. Papert S. Mindstorms: Children, Computers, and Powerful Ideas. — New York: Basic Books, 1980.")
    add_p("3. Csikszentmihalyi M. Flow: The Psychology of Optimal Experience. — New York: Harper & Row, 1990.")
    add_p("4. Ryan R. M., Deci E. L. Self-Determination Theory. — New York: Guilford Press, 2017.")
    add_p("5. Google Gemini API & Generative AI Documentation [Электронный ресурс]. — URL: https://ai.google.dev/docs")

    add_title("3.4. Официальная справка об антиплагиате (95.6%)", level=2)
    add_p("Отчет о проверке № 684862 от 04.11.2026 г. (Аналитическая система «Проверить-уникальность.рф»). Процент оригинальности авторского текста: 95.6% (при нормативном пороге РНПЦ «Дарын» не менее 80%).", bold=True)

    plag_img = 'plagiat_result.png'
    add_img(plag_img, width_in=4.4, caption="Фото 6. Официальный отчет проверки проекта на антиплагиат (95.6% оригинальности)")

    add_title("3.5. Орын QR-код үшін / Место для QR-кода", level=2)
    add_p("В соответствии с регламентом конкурса на правой панели стенда резервируется квадратное поле размером 10 × 10 см для наклеивания QR-кода с цифровыми материалами (ссылка на веб-платформу Smart Code, видеодемонстрацию работы песочницы и соревновательного режима Code Battle). Поле оставлено свободным для последующего нанесения ссылки.", italic=True)

    # Сохранение документа
    output_dir = "Папка для ворда"
    os.makedirs(output_dir, exist_ok=True)
    docx_path = os.path.abspath(os.path.join(output_dir, "Материалы_для_стенда_SmartCode.docx"))
    doc.save(docx_path)
    print("DOCX created:", docx_path)

    # Конвертация в PDF через Word COM
    try:
        import win32com.client
        word = win32com.client.Dispatch('Word.Application')
        word.Visible = False
        doc_com = word.Documents.Open(docx_path)
        pdf_path = os.path.abspath(os.path.join(output_dir, "Материалы_для_стенда_SmartCode.pdf"))
        # 17 = wdFormatPDF
        doc_com.SaveAs2(pdf_path, 17)
        doc_com.Close()
        word.Quit()
        print("PDF created via Word COM:", pdf_path)
    except Exception as e:
        print("Error converting to PDF via COM:", e)

if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    build_materials_doc()
