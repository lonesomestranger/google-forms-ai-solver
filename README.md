# Google Forms AI Solver

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Этот проект использует мощь Google Gemini API для автоматического решения тестов, размещенных на платформе Google Forms. Он способен извлекать вопросы и варианты ответов прямо со страницы формы и генерировать решения.

## ✨ Возможности

-   **Парсинг Google Forms**: Автоматически извлекает вопросы, варианты ответов и описания из публичных Google Forms.
-   **AI-решения**: Использует модель `gemini-2.5-pro` для генерации ответов на основе извлеченных данных.
-   **Два режима работы**:
    1.  **CLI (Command-Line Interface)**: Быстрый запуск из терминала для решения одной формы.
    2.  **Telegram Бот**: Интерактивный бот, которому можно отправлять ссылки на формы.
-   **Поддержка контекста**: Telegram-бот может использовать локальный PDF-файл как базу знаний для ответов.
-   **Простая настройка**: Вся конфигурация вынесена в переменные окружения.

## ⚙️ Структура проекта

Проект имеет модульную структуру для легкого понимания и расширения:

-   `google_forms_solver/`: Ядро проекта.
    -   `ai_handler.py`: Класс для взаимодействия с Gemini API.
    -   `form_parser.py`: Класс для парсинга HTML-страниц Google Forms.
    -   `config.py`: Управление конфигурацией и переменными окружения.
-   `run_cli.py`: Точка входа для запуска в режиме командной строки.
-   `run_bot.py`: Точка входа для запуска Telegram-бота.
-   `.env.example`: Шаблон для файла с вашими секретными ключами.

## 🚀 Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/lonesomestranger/googleforms-ai-solver.git
cd googleforms-ai-solver
```

### 2. Установка зависимостей

Рекомендуется использовать виртуальное окружение.

```bash
# Создание и активация виртуального окружения (опционально, но рекомендуется)
python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt
```

### 3. Настройка конфигурации

Создайте файл `.env` в корневой директории проекта, скопировав `.env.example`:

```bash
cp .env.example .env
```

Теперь откройте файл `.env` и вставьте ваши ключи:

```
# Ключ для Google Gemini API (https://aistudio.google.com/app/apikey)
GEMINI_API_KEY="YOUR_API_KEY_HERE"

# Токен для Telegram-бота, полученный от @BotFather (нужен только для бота)
BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN_HERE"

# (Опционально) Путь к PDF-файлу для контекста в боте
PDF_CONTEXT_PATH="path/to/your/file.pdf"
```

### 4. Запуск

#### Режим командной строки (CLI)

Для решения одной формы просто передайте URL в качестве аргумента:

```bash
python run_cli.py "https://docs.google.com/forms/d/e/your-form-link/viewform"
```

#### Режим Telegram-бота

Запустите бота, и он будет готов принимать ссылки:

```bash
python run_bot.py
```

После запуска найдите вашего бота в Telegram и отправьте ему ссылку на Google Форму.

## 🔧 Кастомизация

-   **Изменение модели AI**: Вы можете изменить используемую модель Gemini (например, на `gemini-2.5-pro`), отредактировав переменную `MODEL_NAME` в файле `google_forms_solver/config.py`.
-   **Изменение системного промпта**: Поведение AI можно настроить, изменив системную инструкцию `SYSTEM_INSTRUCTION` в том же файле `config.py`.

## ⛰ Codeberg

Код также доступен на [Codeberg](https://codeberg.org/lonesomestranger/google-forms-ai-solver).

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Смотрите файл `LICENSE` для получения дополнительной информации.
