import logging

from bs4 import BeautifulSoup, Tag
from curl_cffi import requests


class FormParser:
    @staticmethod
    def fetch_and_parse(url: str) -> str | None:
        try:
            response = requests.get(url, impersonate="chrome136", timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
        except requests.errors.RequestsError as e:
            logging.error(f"Error fetching URL {url}: {e}")
            return None

        question_divs = soup.find_all("div", class_="Qr7Oae")
        if not question_divs:
            logging.warning(
                "No questions found on the page. The structure might have changed."
            )
            return None

        full_form_text = ""
        for i, div in enumerate(question_divs, 1):
            question_text = FormParser._parse_question_block(div)
            if question_text:
                full_form_text += f"{i}. {question_text}\n\n"

        return full_form_text.strip() if full_form_text else None

    @staticmethod
    def _parse_question_block(question_div: Tag) -> str | None:
        question_text_element = question_div.find("span", class_="M7eMe")
        if not question_text_element:
            return None

        question_title = question_text_element.text.strip().replace("\xa0", " ")

        if question_div.find("div", class_="E2qMtb"):
            return FormParser._parse_grid_question(question_div, question_title)

        if question_div.find("div", role="listbox"):
            return FormParser._parse_dropdown_question(question_div, question_title)

        checkbox_options = question_div.find_all("div", class_="eBFwI")
        if checkbox_options:
            return FormParser._parse_checkbox_question(
                question_div, question_title, checkbox_options
            )

        radio_options = question_div.find_all(
            "span", class_="aDTYNe snByac OvPDhc OIC90c"
        )
        if radio_options:
            return FormParser._parse_radio_question(
                question_div, question_title, radio_options
            )

        return question_title

    @staticmethod
    def _get_description(question_div: Tag) -> str:
        description_element = question_div.find("div", class_="gubaDc OIC90c RjsPE")
        if description_element and description_element.text.strip():
            return f"   Description: {description_element.text.strip()}\n"
        return ""

    @staticmethod
    def _parse_grid_question(question_div: Tag, title: str) -> str:
        is_checkbox_grid = bool(question_div.find("div", role="checkbox"))
        grid_type_instruction = (
            "Checkbox Grid (select one or more per row)."
            if is_checkbox_grid
            else "Radio Grid (select one per row)."
        )

        columns_header = question_div.select(".ssX1Bd.KZt9Tc .V4d7Ke.OIC90c")
        columns = [col.text.strip() for col in columns_header]

        rows_header = question_div.select(".V4d7Ke.wzWPxe.OIC90c")
        rows = [row.text.strip() for row in rows_header]

        formatted_text = f"{title}\n"
        formatted_text += FormParser._get_description(question_div)
        formatted_text += f"   Type: {grid_type_instruction}\n"
        formatted_text += f"   Columns: {', '.join(columns)}\n"
        for row_title in rows:
            formatted_text += f"   - Row: {row_title}\n"

        return formatted_text.strip()

    @staticmethod
    def _parse_dropdown_question(question_div: Tag, title: str) -> str:
        options = question_div.select(".MocG8c.HZ3kWc .vRMGwf.oJeWuf")
        option_texts = [
            opt.text.strip()
            for opt in options
            if opt.text.strip() and opt.text.strip().lower() != "выбрать"
        ]

        formatted_text = f"{title}\n"
        formatted_text += FormParser._get_description(question_div)
        formatted_text += "   Type: Dropdown (select one)\n"
        formatted_text += f"   Options: {', '.join(option_texts)}"
        return formatted_text

    @staticmethod
    def _parse_checkbox_question(question_div: Tag, title: str, options: list) -> str:
        option_texts = [opt.text.strip() for opt in options]

        formatted_text = f"{title}\n"
        formatted_text += FormParser._get_description(question_div)
        formatted_text += "   Type: Checkboxes (select one or more)\n"
        formatted_text += f"   Options: {', '.join(option_texts)}"
        return formatted_text

    @staticmethod
    def _parse_radio_question(question_div: Tag, title: str, options: list) -> str:
        option_texts = [opt.text.strip() for opt in options]

        formatted_text = f"{title}\n"
        formatted_text += FormParser._get_description(question_div)
        formatted_text += "   Type: Radio buttons (select one)\n"
        formatted_text += f"   Options: {', '.join(option_texts)}"
        return formatted_text
