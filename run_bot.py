import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from google_forms_solver.ai_handler import GeminiHandler
from google_forms_solver.config import (
    BOT_TOKEN,
    GEMINI_API_KEY,
    MODEL_NAME,
    PDF_CONTEXT_PATH,
    SYSTEM_INSTRUCTION,
)
from google_forms_solver.form_parser import FormParser

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

if not BOT_TOKEN:
    raise ValueError("Необходимо установить BOT_TOKEN в .env файле для запуска бота")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
ai_handler = GeminiHandler(
    api_key=GEMINI_API_KEY,
    model_name=MODEL_NAME,
    system_instruction=SYSTEM_INSTRUCTION,
    pdf_path=PDF_CONTEXT_PATH,
)
form_parser = FormParser()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "Привет! Отправь мне ссылку на Google Форму, и я постараюсь ее решить."
    )


@dp.message()
async def process_link_handler(message: types.Message):
    url = message.text
    if not url or not url.startswith("http"):
        await message.answer("Пожалуйста, отправьте корректную ссылку на Google Форму.")
        return

    await message.answer("⏳ Начинаю парсинг формы... Пожалуйста, подождите.")

    formatted_questions = form_parser.fetch_and_parse(url)

    if not formatted_questions:
        await message.answer(
            "❌ Не удалось извлечь вопросы из формы. Возможно, ссылка неверна, форма защищена или ее структура изменилась."
        )
        return

    await message.answer("✅ Вопросы успешно извлечены. Отправляю их AI для решения...")

    try:
        response = await ai_handler.generate_response(formatted_questions)
        await message.answer(f"✨ Вот ответы от AI:\n\n{response}")
    except Exception as e:
        logging.error(
            f"Error processing AI response for user {message.from_user.id}: {e}"
        )
        await message.answer(
            "💥 Произошла ошибка при обработке вашего запроса. Попробуйте позже."
        )


async def main():
    logging.info("Starting bot...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
