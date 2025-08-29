import asyncio
import logging
import pathlib

import google.generativeai as genai
from google.api_core.exceptions import InternalServerError
from google.generativeai.types import GenerationConfig, HarmBlockThreshold, HarmCategory


class GeminiHandler:
    def __init__(
        self,
        api_key: str,
        model_name: str,
        system_instruction: str,
        pdf_path: str | None = None,
    ):
        genai.configure(api_key=api_key)
        self.model_name = model_name
        self.system_instruction = system_instruction
        self.pdf_path = pathlib.Path(pdf_path) if pdf_path else None
        self.history = self._build_initial_history()

        self.generation_config = GenerationConfig(
            temperature=0.1,
            top_p=0.95,
            top_k=30,
        )
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

    def _build_initial_history(self) -> list:
        history = [
            {"role": "user", "parts": [self.system_instruction]},
            {
                "role": "model",
                "parts": [
                    "Okay, I understand my role. I will provide answers to the test questions."
                ],
            },
        ]

        if self.pdf_path and self.pdf_path.exists():
            try:
                logging.info(f"Uploading PDF file for context: {self.pdf_path}")
                uploaded_file = genai.upload_file(self.pdf_path)
                history.insert(
                    1,
                    {
                        "role": "user",
                        "parts": [
                            uploaded_file,
                            f"Use the information from the uploaded file '{self.pdf_path.name}' as the primary context for answering the questions.",
                        ],
                    },
                )
                logging.info("PDF successfully uploaded and added to context.")
            except Exception as e:
                logging.error(f"Failed to upload or process PDF file: {e}")

        return history

    def _create_chat_session(self):
        model = genai.GenerativeModel(
            self.model_name,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
        )
        return model.start_chat(history=self.history)

    async def generate_response(self, user_input: str) -> str:
        chat = self._create_chat_session()
        max_retries = 3
        retry_delay = 5

        for attempt in range(max_retries):
            try:
                response = await asyncio.to_thread(
                    chat.send_message,
                    user_input,
                    generation_config=self.generation_config,
                    safety_settings=self.safety_settings,
                )
                return response.text.replace("*", "")
            except InternalServerError as e:
                logging.error(
                    f"Gemini API server error: {e}. Retrying in {retry_delay}s... (Attempt {attempt + 1}/{max_retries})"
                )
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay)
                else:
                    raise e
            except Exception as e:
                logging.error(f"An unexpected error occurred in generate_response: {e}")
                raise e
