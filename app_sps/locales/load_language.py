import json
import os

def load_language(lang_code="en"):
    """
    Load language content from a JSON file based on the provided language code.

    Args:
        lang_code (str): The language code (e.g., "en", "ru"). Defaults to "en".

    Returns:
        dict: A dictionary containing the localized language content.

    Notes:
        - Looks for a file named 'content_<lang_code>.json' in the same directory.
        - If the specified language file is not found, falls back to 'content_en.json'.
    """
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, f"content_{lang_code}.json")

    if not os.path.isfile(file_path):
        file_path = os.path.join(base_dir, "content_en.json")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
