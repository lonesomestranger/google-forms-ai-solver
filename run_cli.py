import argparse
import asyncio
import logging

from google_forms_solver.ai_handler import GeminiHandler
from google_forms_solver.config import GEMINI_API_KEY, MODEL_NAME, SYSTEM_INSTRUCTION
from google_forms_solver.form_parser import FormParser

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def main():
    parser = argparse.ArgumentParser(description="Solve a Google Form using Gemini AI.")
    parser.add_argument("url", type=str, help="The URL of the Google Form to solve.")
    args = parser.parse_args()

    print(f"Parsing Google Form from: {args.url}")

    formatted_questions = FormParser.fetch_and_parse(args.url)

    if not formatted_questions:
        print(
            "\nFailed to parse questions from the form. Please check the URL or the form's structure."
        )
        return

    print("\nQuestions parsed successfully. Sending to AI for solving...")
    print("-" * 30)
    print(formatted_questions)
    print("-" * 30)

    try:
        ai_handler = GeminiHandler(
            api_key=GEMINI_API_KEY,
            model_name=MODEL_NAME,
            system_instruction=SYSTEM_INSTRUCTION,
        )
        response = await ai_handler.generate_response(formatted_questions)

        print("\nAI Response:\n")
        print(response)
    except Exception as e:
        logging.error(f"An error occurred while getting the AI response: {e}")
        print("\nAn error occurred. Please check the logs.")


if __name__ == "__main__":
    asyncio.run(main())
