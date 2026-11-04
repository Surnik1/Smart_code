# -*- coding: utf-8 -*-
"""
Генератор официального выставочного стенда для республиканского конкурса научных проектов
Автор: Талғат Нұрәли (11 класс)
Проект: Smart Code
Размеры стенда: 120 см х 100 см (3 панели: 30 см - 60 см - 30 см)
Разрешение для печати: 3600 x 3000 пикселей (высокое качество)
"""

import os
import sys
import base64
import subprocess

def img_to_b64(path):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            data = f.read()
            return f"data:image/png;base64,{base64.b64encode(data).decode('utf-8')}"
    return ""

def generate_stand():
    print("Encoding images...")
    logo_b64 = img_to_b64('extracted_images/p2_0_image1.png')
    arch_b64 = img_to_b64('smart_code_arch.png')
    monaco_b64 = img_to_b64('chart_monaco.png')
    ai_b64 = img_to_b64('chart_ai.png')
    classroom_b64 = img_to_b64('chart_classroom.png')

    html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Көрме стенді / Выставочный стенд Smart Code</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=Roboto:wght@300;400;500;700&display=swap');

    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }}

    body {{
        width: 3600px;
        height: 3000px;
        background: #f1f5f9;
        font-family: 'Roboto', sans-serif;
        color: #1e293b;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }}

    /* ВЕРХНЯЯ ШАПКА СТЕНДА */
    .stand-header {{
        height: 190px;
        background: linear-gradient(135deg, #091e3a 0%, #102a4e 45%, #1a365d 100%);
        color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 20px 60px;
        border-bottom: 6px solid #2563eb;
        position: relative;
    }}

    .header-logo-block {{
        display: flex;
        align-items: center;
        gap: 25px;
    }}

    .header-logo {{
        height: 140px;
        filter: drop-shadow(0 4px 10px rgba(0,0,0,0.3));
    }}

    .header-titles {{
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}

    .header-inst {{
        font-family: 'Montserrat', sans-serif;
        font-size: 24px;
        font-weight: 700;
        letter-spacing: 0.5px;
        color: #93c5fd;
        text-transform: uppercase;
        margin-bottom: 6px;
    }}

    .header-contest {{
        font-size: 20px;
        color: #e2e8f0;
        font-weight: 400;
    }}

    .header-badge-block {{
        text-align: right;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }}

    .header-badge {{
        background: rgba(37, 99, 235, 0.25);
        border: 2px solid #3b82f6;
        padding: 8px 20px;
        border-radius: 8px;
        font-size: 20px;
        font-weight: 600;
        color: #bfdbfe;
        font-family: 'Montserrat', sans-serif;
    }}

    /* ОСНОВНОЙ КОНТЕЙНЕР НА 3 СТВОРКИ (30см - 60см - 30см) */
    .stand-body {{
        flex: 1;
        display: grid;
        grid-template-columns: 880px 1840px 880px;
        background: #e2e8f0;
        gap: 0;
        position: relative;
    }}

    /* ПАНЕЛИ СТЕНДА */
    .panel {{
        background: #f8fafc;
        display: flex;
        flex-direction: column;
        padding: 28px 32px;
        gap: 24px;
        overflow: hidden;
    }}

    /* ЛИНИИ СГИБА (ФОЛДИНГ 30-60-30 см) */
    .panel-left {{
        border-right: 4px dashed #94a3b8;
    }}

    .panel-center {{
        border-right: 4px dashed #94a3b8;
        background: #ffffff;
    }}

    .panel-right {{
        background: #f8fafc;
    }}

    /* КАРТОЧКИ БЛОКОВ */
    .card {{
        background: #ffffff;
        border: 2px solid #cbd5e1;
        border-radius: 16px;
        padding: 24px 28px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
        display: flex;
        flex-direction: column;
        position: relative;
    }}

    .card-title {{
        font-family: 'Montserrat', sans-serif;
        font-size: 26px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 12px;
        border-bottom: 3px solid #e2e8f0;
        padding-bottom: 8px;
    }}

    .card-title .icon-tag {{
        background: #2563eb;
        color: #ffffff;
        font-size: 18px;
        padding: 4px 12px;
        border-radius: 6px;
        font-weight: 700;
        text-transform: uppercase;
    }}

    .card-text {{
        font-size: 21.5px;
        line-height: 1.48;
        color: #334155;
        text-align: justify;
    }}

    .card-text ul {{
        list-style: none;
        padding-left: 0;
    }}

    .card-text li {{
        position: relative;
        padding-left: 28px;
        margin-bottom: 10px;
    }}

    .card-text li::before {{
        content: "■";
        position: absolute;
        left: 0;
        color: #2563eb;
        font-size: 16px;
        top: 2px;
    }}

    /* ЦЕНТРАЛЬНАЯ ПАНЕЛЬ */
    .title-banner {{
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
        color: #ffffff;
        border-radius: 18px;
        padding: 24px 32px;
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.25);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 30px;
    }}

    .title-content {{
        flex: 1;
    }}

    .project-theme-label {{
        font-family: 'Montserrat', sans-serif;
        font-size: 19px;
        font-weight: 700;
        text-transform: uppercase;
        color: #93c5fd;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }}

    .project-main-title {{
        font-family: 'Montserrat', sans-serif;
        font-size: 34px;
        font-weight: 900;
        line-height: 1.25;
        margin-bottom: 12px;
    }}

    .author-supervisor-meta {{
        display: flex;
        gap: 35px;
        font-size: 20px;
        color: #e0e7ff;
        font-weight: 500;
    }}

    .author-supervisor-meta strong {{
        color: #ffffff;
    }}

    /* РАМКА ДЛЯ РЕГИСТРАЦИОННОГО НОМЕРА (14 x 7 см) */
    .reg-number-box {{
        width: 250px;
        height: 130px;
        border: 3px dashed #bfdbfe;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.12);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: #ffffff;
        font-family: 'Montserrat', sans-serif;
        flex-shrink: 0;
    }}

    .reg-number-box span {{
        font-size: 16px;
        font-weight: 600;
        color: #dbeafe;
    }}

    .reg-number-box small {{
        font-size: 13px;
        color: #93c5fd;
        margin-top: 4px;
    }}

    /* ИССЛЕДОВАТЕЛЬСКИЙ ВОПРОС */
    .research-question-box {{
        background: #eff6ff;
        border: 2px solid #bfdbfe;
        border-left: 10px solid #2563eb;
        border-radius: 12px;
        padding: 16px 24px;
    }}

    .rq-title {{
        font-family: 'Montserrat', sans-serif;
        font-size: 21px;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 6px;
        text-transform: uppercase;
    }}

    .rq-text {{
        font-size: 21px;
        color: #1e293b;
        line-height: 1.4;
    }}

    /* БЛОК НЕГІЗГІ НӘТИЖЕ / ОСНОВНОЙ РЕЗУЛЬТАТ */
    .main-results-section {{
        display: flex;
        flex-direction: column;
        gap: 18px;
        flex: 1;
    }}

    .section-headline {{
        font-family: 'Montserrat', sans-serif;
        font-size: 26px;
        font-weight: 900;
        color: #0f172a;
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #f1f5f9;
        padding: 10px 20px;
        border-radius: 10px;
        border-left: 8px solid #2563eb;
    }}

    .arch-and-features {{
        display: grid;
        grid-template-columns: 1050px 1fr;
        gap: 20px;
        align-items: center;
    }}

    .arch-img-wrap {{
        background: #ffffff;
        border: 2px solid #cbd5e1;
        border-radius: 14px;
        padding: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        text-align: center;
    }}

    .arch-img-wrap img {{
        max-width: 100%;
        height: auto;
        max-height: 460px;
        border-radius: 8px;
    }}

    .tech-pills {{
        display: flex;
        flex-direction: column;
        gap: 12px;
    }}

    .pill {{
        background: #f8fafc;
        border: 2px solid #e2e8f0;
        border-left: 6px solid #2563eb;
        border-radius: 10px;
        padding: 14px 18px;
    }}

    .pill-title {{
        font-family: 'Montserrat', sans-serif;
        font-size: 20px;
        font-weight: 800;
        color: #1e40af;
        margin-bottom: 4px;
    }}

    .pill-desc {{
        font-size: 18px;
        color: #475569;
        line-height: 1.35;
    }}

    /* 3 ДИАГРАММЫ ОПРОСА 150 УЧАЩИХСЯ */
    .charts-row {{
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 18px;
    }}

    .chart-card {{
        background: #ffffff;
        border: 2px solid #cbd5e1;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.04);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}

    .chart-card img {{
        max-width: 100%;
        height: 250px;
        object-fit: contain;
        border-radius: 6px;
        margin-bottom: 8px;
    }}

    .chart-caption {{
        font-size: 16.5px;
        font-weight: 700;
        color: #1e293b;
        line-height: 1.3;
    }}

    .chart-stat {{
        display: inline-block;
        background: #dbeafe;
        color: #1e40af;
        font-weight: 800;
        font-size: 15px;
        padding: 2px 8px;
        border-radius: 4px;
        margin-top: 4px;
    }}

    /* ТАБЛИЦА СРАВНЕНИЯ КГ И ЭГ */
    .metrics-table-wrap {{
        background: #ffffff;
        border: 2px solid #cbd5e1;
        border-radius: 12px;
        overflow: hidden;
    }}

    .metrics-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 19px;
    }}

    .metrics-table th {{
        background: #1e3a8a;
        color: #ffffff;
        padding: 12px 16px;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        text-align: left;
    }}

    .metrics-table td {{
        padding: 11px 16px;
        border-bottom: 1px solid #e2e8f0;
        color: #334155;
    }}

    .metrics-table tr:nth-child(even) {{
        background: #f8fafc;
    }}

    .metrics-table .growth {{
        font-weight: 800;
        color: #16a34a;
    }}

    /* ПРАВАЯ ПАНЕЛЬ: ВЫВОДЫ, ЗНАЧИМОСТЬ, QR-КОД */
    .qr-placeholder-card {{
        background: #ffffff;
        border: 3px dashed #64748b;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 380px;
        gap: 12px;
    }}

    .qr-box {{
        width: 200px;
        height: 200px;
        border: 3px dashed #94a3b8;
        border-radius: 12px;
        background: #f8fafc;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #94a3b8;
        font-size: 18px;
        font-weight: 700;
        text-align: center;
        padding: 10px;
    }}

    .qr-label {{
        font-family: 'Montserrat', sans-serif;
        font-size: 22px;
        font-weight: 800;
        color: #0f172a;
    }}

    .qr-sub {{
        font-size: 17px;
        color: #64748b;
        max-width: 80%;
    }}

    /* НИЖНИЙ КОЛОНТИТУЛ СТЕНДА */
    .stand-footer {{
        height: 60px;
        background: #0f172a;
        color: #94a3b8;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 60px;
        font-size: 18px;
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        border-top: 3px solid #334155;
    }}

    .fold-mark {{
        position: absolute;
        top: 0;
        bottom: 0;
        width: 0;
        border-left: 2px dashed rgba(148, 163, 184, 0.6);
        pointer-events: none;
    }}
    .fold-left {{ left: 880px; }}
    .fold-right {{ right: 880px; }}
</style>
</head>
<body>

    <!-- ВЕРХНЯЯ ШАПКА -->
    <header class="stand-header">
        <div class="header-logo-block">
            {f'<img src="{logo_b64}" class="header-logo" alt="Дарын лого">' if logo_b64 else ''}
            <div class="header-titles">
                <div class="header-inst">Специализированный лицей-интернат для одаренных детей «БІЛІМ-ИННОВАЦИЯ» г. Талдыкорган</div>
                <div class="header-contest">Республиканский конкурс исследовательских проектов школьников | 2025–2026 уч. год</div>
            </div>
        </div>
        <div class="header-badge-block">
            <div class="header-badge">НАПРАВЛЕНИЕ: Математическое моделирование экономических и социальных процессов</div>
            <div class="header-badge">СЕКЦИЯ: ИНФОРМАТИКА</div>
        </div>
    </header>

    <!-- ОСНОВНОЕ ПОЛОТНО СТЕНДА 120 x 100 СМ -->
    <main class="stand-body">
        
        <!-- ЛЕВАЯ ПАНЕЛЬ (30 см / 25% ширины) -->
        <section class="panel panel-left">
            
            <!-- АКТУАЛЬНОСТЬ -->
            <div class="card">
                <div class="card-title">
                    <span class="icon-tag">1</span>
                    АКТУАЛЬНОСТЬ
                </div>
                <div class="card-text">
                    В эпоху развития ИИ и цифровизации алгоритмическая грамотность — базовый навык XXI века. Традиционное школьное обучение информатике сталкивается с системными барьерами: нехваткой интерактивной практики, сложностью локальной настройки сред CPython и рутинной проверкой. Существующие зарубежные сервисы (LeetCode, Codeforces) сложны для школ и требуют платных подписок. Необходима отечественная школьная платформа с мгновенным откликом и умным наставником.
                </div>
            </div>

            <!-- ЦЕЛЬ ИССЛЕДОВАНИЯ -->
            <div class="card">
                <div class="card-title">
                    <span class="icon-tag">2</span>
                    ЦЕЛЬ ИССЛЕДОВАНИЯ
                </div>
                <div class="card-text">
                    Проектирование, алгоритмическая реализация и педагогическое обоснование интерактивной образовательной веб-платформы <strong>Smart Code</strong> для массового обучения школьников алгоритмизации, соревновательному кодингу и спортивному программированию.
                </div>
            </div>

            <!-- ЗАДАЧИ ИССЛЕДОВАНИЯ -->
            <div class="card" style="flex: 1;">
                <div class="card-title">
                    <span class="icon-tag">3</span>
                    ЗАДАЧИ ИССЛЕДОВАНИЯ
                </div>
                <div class="card-text">
                    <ul>
                        <li>Анализ систем автоматизированного тестирования кода и выявление пробелов для школьного образования.</li>
                        <li>Разработка легковесной безопасной <strong>AST-песочницы</strong> Python без задержек контейнеризации (&lt;15 мс).</li>
                        <li>Интеграция Сократического <strong>Gemini AI-ментора</strong> с запретом на выдачу готового кода и каскадом Fallback Chain.</li>
                        <li>Создание соревновательного модуля <strong>Code Battle 1v1</strong> с транзакционной защитой от Race Condition.</li>
                        <li>Реализация модуля виртуальных классов для учителей и античит-контроля сдачи решений.</li>
                        <li>Педагогическая апробация на 150 учащихся и стресс-тестирование стека (44/44 автотестов).</li>
                    </ul>
                </div>
            </div>

            <!-- МЕТОДЫ ИССЛЕДОВАНИЯ -->
            <div class="card">
                <div class="card-title">
                    <span class="icon-tag">4</span>
                    МЕТОДЫ ИССЛЕДОВАНИЯ
                </div>
                <div class="card-text">
                    Статический синтаксический анализ AST-деревьев Python; транзакционное управление параллелизмом СУБД (select_for_update); педагогический эксперимент (КГ/ЭГ, 100 уч.); онлайн-анкетирование 150 респондентов; методы математической статистики.
                </div>
            </div>

        </section>

        <!-- ЦЕНТРАЛЬНАЯ ПАНЕЛЬ (60 см / 50% ширины) -->
        <section class="panel panel-center">
            
            <!-- ТЕМА И АВТОР -->
            <div class="title-banner">
                <div class="title-content">
                    <div class="project-theme-label">Исследовательский проект по информатике</div>
                    <h1 class="project-main-title">Образовательная веб-платформа Smart Code для интерактивного обучения алгоритмам и соревновательного программирования</h1>
                    <div class="author-supervisor-meta">
                        <div>Автор: <strong>Талғат Нұрәли</strong> (11 класс)</div>
                        <div>Руководитель: <strong>Алмашев Нурбек Жархынбекұлы</strong> (учитель информатики)</div>
                    </div>
                </div>
                <!-- Рамка 14 x 7 см для номера -->
                <div class="reg-number-box">
                    <span>ОРЫН ЦИФРҒА</span>
                    <span>14 × 7 см</span>
                    <small>(Место для кода)</small>
                </div>
            </div>

            <!-- ИССЛЕДОВАТЕЛЬСКИЙ ВОПРОС И ГИПОТЕЗА -->
            <div class="research-question-box">
                <div class="rq-title">Исследовательский вопрос и рабочая гипотеза</div>
                <div class="rq-text">
                    <strong>Вопрос:</strong> Как ликвидировать технический барьер и стимулировать познавательную мотивацию школьников при изучении сложных алгоритмов без риска бездумного списывания?<br>
                    <strong>Гипотеза:</strong> Интеграция изолированной AST-песочницы, диалогового Сократического AI-ментора и соревновательных PvP-дуэлей 1v1 повысит успеваемость более чем на 20% и сформирует культуру академической честности.
                </div>
            </div>

            <!-- ОСНОВНОЙ РЕЗУЛЬТАТ: АРХИТЕКТУРА И КЛЮЧЕВЫЕ ТЕХНОЛОГИИ -->
            <div class="main-results-section">
                
                <div class="section-headline">
                    <span>АРХИТЕКТУРА И ТЕХНОЛОГИЧЕСКИЕ ИННОВАЦИИ СИСТЕМЫ</span>
                    <span style="font-size: 19px; color: #2563eb; font-weight: 700;">Service-Layer Architecture (Django 5.2 / Python 3.11)</span>
                </div>

                <div class="arch-and-features">
                    <div class="arch-img-wrap">
                        {f'<img src="{arch_b64}" alt="Архитектурная схема">' if arch_b64 else '<div style="height:350px;">Архитектурная схема</div>'}
                    </div>
                    <div class="tech-pills">
                        <div class="pill">
                            <div class="pill-title">1. Легковесная AST-песочница</div>
                            <div class="pill-desc">SecurityASTValidator обходит синтаксическое дерево, блокируя import, eval, exec и интроспекцию. Время отклика — <strong>12 мс</strong> (в 60 раз быстрее Docker).</div>
                        </div>
                        <div class="pill">
                            <div class="pill-title">2. Socratic AI-ментор (Gemini)</div>
                            <div class="pill-desc">Строгий системный запрет на выдачу готового кода. Ментор задает наводящие вопросы по логике ошибки. Каскадный Fallback Chain при сбоях сети.</div>
                        </div>
                        <div class="pill">
                            <div class="pill-title">3. PvP Code Battle 1 на 1</div>
                            <div class="pill-desc">Синхронные турнирные дуэли в реальном времени. Транзакционный лок <code>select_for_update()</code> полностью исключает Race Condition.</div>
                        </div>
                        <div class="pill">
                            <div class="pill-title">4. Античит-контур (TaskSolutionView)</div>
                            <div class="pill-desc">При открытии эталонного разбора система навсегда отключает выдачу опыта (XP), сохраняя честность рейтинга и мотивацию.</div>
                        </div>
                    </div>
                </div>

                <!-- ДИАГРАММЫ ОПРОСА 150 РЕСПОНДЕНТОВ -->
                <div class="section-headline">
                    <span>ЭКСПЕРИМЕНТАЛЬНАЯ ВЕРИФИКАЦИЯ (АНКЕТИРОВАНИЕ 150 УЧАЩИХСЯ)</span>
                    <span style="font-size: 19px; color: #16a34a; font-weight: 700;">Google Forms</span>
                </div>

                <div class="charts-row">
                    <div class="chart-card">
                        {f'<img src="{monaco_b64}" alt="График Monaco">' if monaco_b64 else ''}
                        <div class="chart-caption">Эргономика Monaco Editor в сравнении с IDLE</div>
                        <div><span class="chart-stat">80.7% признали «намного удобнее»</span></div>
                    </div>
                    <div class="chart-card">
                        {f'<img src="{ai_b64}" alt="График AI">' if ai_b64 else ''}
                        <div class="chart-caption">Эффективность Сократического AI-ментора</div>
                        <div><span class="chart-stat">76.0% находят ошибки сами</span></div>
                    </div>
                    <div class="chart-card">
                        {f'<img src="{classroom_b64}" alt="График Класс">' if classroom_b64 else ''}
                        <div class="chart-caption">Мониторинг дедлайнов и домашних заданий</div>
                        <div><span class="chart-stat">86.0% оценили высокую прозрачность</span></div>
                    </div>
                </div>

                <!-- СРАВНИТЕЛЬНАЯ ТАБЛИЦА СРЕЗА КГ И ЭГ -->
                <div class="metrics-table-wrap">
                    <table class="metrics-table">
                        <thead>
                            <tr>
                                <th>Исследуемый показатель успеваемости</th>
                                <th>Контрольная группа (КГ, 50 уч.)</th>
                                <th>Экспериментальная группа (ЭГ, 50 уч.)</th>
                                <th>Динамика прироста</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Средний процент успешной сдачи задач</strong></td>
                                <td>58.4%</td>
                                <td><strong>82.7%</strong></td>
                                <td class="growth">+24.3% (p &lt; 0.01)</td>
                            </tr>
                            <tr>
                                <td><strong>Среднее время решения одной задачи</strong></td>
                                <td>38.2 мин</td>
                                <td><strong>27.3 мин</strong></td>
                                <td class="growth">-28.5% (ускорение)</td>
                            </tr>
                            <tr>
                                <td><strong>Доля самостоятельных программных решений</strong></td>
                                <td>46.2%</td>
                                <td><strong>78.9%</strong></td>
                                <td class="growth">+32.7% прирост</td>
                            </tr>
                            <tr>
                                <td><strong>Средний балл итогового олимпиадного контеста</strong></td>
                                <td>64.8 ± 3.2</td>
                                <td><strong>85.6 ± 2.4</strong></td>
                                <td class="growth">+20.8 балла (из 100)</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

            </div>

        </section>

        <!-- ПРАВАЯ ПАНЕЛЬ (30 см / 25% ширины) -->
        <section class="panel panel-right">
            
            <!-- ВЫВОДЫ -->
            <div class="card">
                <div class="card-title">
                    <span class="icon-tag">5</span>
                    ВЫВОДЫ / ҚОРЫТЫНДЫЛАР
                </div>
                <div class="card-text">
                    <ul>
                        <li>Доказана высокая педагогическая эффективность синтеза интерактивной песочницы, AI-ментора и PvP-дуэлей.</li>
                        <li>Разработана трехуровневая модель безопасности Python AST, обеспечивающая отклик 12 мс при 100% изоляции от RCE.</li>
                        <li>Подтверждена гипотеза: успеваемость выросла на <strong>24.3%</strong>, время преодоления тупиков сократилось на <strong>28.5%</strong>.</li>
                        <li>Комплекс протестирован 44 автоматическими тестами (100% OK), доказав промышленную надежность стека.</li>
                    </ul>
                </div>
            </div>

            <!-- ПРАКТИЧЕСКАЯ ЗНАЧИМОСТЬ -->
            <div class="card">
                <div class="card-title">
                    <span class="icon-tag">6</span>
                    ПРАКТИЧЕСКАЯ ЦЕННОСТЬ
                </div>
                <div class="card-text">
                    <ul>
                        <li><strong>Импортозамещение:</strong> замена дорогих зарубежных подписок (LeetCode $35/мес) бесплатным открытым решением.</li>
                        <li><strong>Экономичность:</strong> работа на открытом стеке (Django/Python) с минимальными требованиями к серверу (VPS 12 000 тг/мес на 500 уч.).</li>
                        <li><strong>Экономия времени учителя:</strong> автоматизация проверки и экспорт ведомостей в CSV освобождает 6–8 часов в неделю.</li>
                        <li><strong>Масштабируемость:</strong> комплекс готов к внедрению в средних школах и IT-лицеях Республики Казахстан.</li>
                    </ul>
                </div>
            </div>

            <!-- ИСТОЧНИКИ -->
            <div class="card">
                <div class="card-title">
                    <span class="icon-tag">7</span>
                    ДЕРЕККӨЗДЕР / ЛИТЕРАТУРА
                </div>
                <div class="card-text" style="font-size: 18px; line-height: 1.35;">
                    1. Госпрограмма развития образования и науки РК на 2020–2025 гг.<br>
                    2. Papert S. Mindstorms: Children, Computers, and Powerful Ideas. 1980.<br>
                    3. Csikszentmihalyi M. Flow: The Psychology of Optimal Experience. 1990.<br>
                    4. Ryan R., Deci E. Self-Determination Theory. Guilford Press, 2017.<br>
                    5. Google Gemini API & Generative AI Documentation. 2026.
                </div>
            </div>

            <!-- QR-КОД (ПУСТОЕ МЕСТО ПО ЗАПРОСУ ПОЛЬЗОВАТЕЛЯ) -->
            <div class="qr-placeholder-card" style="flex: 1;">
                <div class="qr-box">
                    <span>МЕСТО ДЛЯ<br>QR-КОДА</span>
                </div>
                <div class="qr-label">ЦИФРЛЫҚ МАТЕРИАЛ / QR-КОД</div>
                <div class="qr-sub">Место для размещения QR-кода на веб-платформу Smart Code, онлайн-демонстрацию и презентацию проекта</div>
            </div>

        </section>

    </main>

    <!-- НИЖНИЙ КОЛОНТИТУЛ -->
    <footer class="stand-footer">
        <div>РЕСПУБЛИКАНСКИЙ НАУЧНО-ПРАКТИЧЕСКИЙ ЦЕНТР «ДАРЫН» | ОБРАЗОВАТЕЛЬНЫЙ ПРОЕКТ SMART CODE</div>
        <div>ТАЛДЫКОРГАН, 2026 ГОД | АВТОР: ТАЛҒАТ НҰРӘЛИ (11 СЫНЫП)</div>
    </footer>

</body>
</html>"""

    html_path = os.path.abspath('stand_layout.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML stand template generated: {html_path}")

    # Рендеринг через Chrome Headless
    chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    if not os.path.exists(chrome_path):
        chrome_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

    output_dir = "Папка для ворда"
    os.makedirs(output_dir, exist_ok=True)
    png_output = os.path.abspath(os.path.join(output_dir, "Стенд_SmartCode_Талғат_Н.png"))
    pdf_output = os.path.abspath(os.path.join(output_dir, "Стенд_SmartCode_Талғат_Н.pdf"))

    print(f"Rendering high-res stand image (3600x3000 px) using {chrome_path}...")
    cmd_png = [
        chrome_path,
        '--headless=new',
        '--disable-gpu',
        '--hide-scrollbars',
        '--window-size=3600,3000',
        f'--screenshot={png_output}',
        html_path
    ]
    subprocess.run(cmd_png, check=True)
    print(f"Successfully generated high-res PNG: {png_output} ({os.path.getsize(png_output):,} bytes)")

    # Также сгенерируем PDF для печати на плоттере 120 x 100 см
    print(f"Rendering PDF for plot printing...")
    cmd_pdf = [
        chrome_path,
        '--headless=new',
        '--disable-gpu',
        '--print-to-pdf-no-header',
        f'--print-to-pdf={pdf_output}',
        html_path
    ]
    subprocess.run(cmd_pdf, check=True)
    print(f"Successfully generated PDF: {pdf_output} ({os.path.getsize(pdf_output):,} bytes)")

if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
    generate_stand()
