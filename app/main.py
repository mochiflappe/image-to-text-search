import os
import re
import glob
import imghdr
import cairosvg
import logging
from PIL import Image
from io import BytesIO
from pytesseract import pytesseract
from multiprocessing import Pool, cpu_count
from typing import List, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main() -> None:
    word_file = "search_words.txt"
    words = read_keywords(word_file)
    if words is None:
        return

    logger.info(f"\033[92mSearch words: {list_to_string(words)} \033[0m")

    files = get_files()

    with Pool(processes=cpu_count()) as pool:
        pool.starmap(process_file, [(file, words) for file in files])

def list_to_string(data: Optional[List[str]], delimiter: str = ", ") -> str:
    if data is None:
        return ""
    return delimiter.join(data)

def read_keywords(word_file: str) -> Optional[List[str]]:
    try:
        with open(word_file, "r") as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        logger.error(f"Error: '{word_file}' not found.")
        return None

def get_files(target_dir: str = "/images") -> List[str]:
    files = []
    for file in glob.glob(os.path.join(target_dir, "**/*"), recursive=True):
        if os.path.isfile(file) and imghdr.what(file):
            files.append(os.path.normpath(file))
    return files

def extract_text_from_image(filename: str) -> Optional[str]:
    try:
        if filename.lower().endswith('.svg'):
            png_data = cairosvg.svg2png(url=filename)
            img = Image.open(BytesIO(png_data))
        else:
            img = Image.open(filename)
        text = pytesseract.image_to_string(img, lang='eng+jpn')
        return text
    except Exception as e:
        logger.error(f"Error processing {filename}: {e}")
        return None

def search_keywords_in_text(text: str, words: List[str]) -> bool:
    text = text.replace(' ', '')
    pattern = re.compile("|".join(map(re.escape, words)), re.IGNORECASE)
    return bool(pattern.search(text))

def process_file(file: str, words: List[str]) -> None:
    text = extract_text_from_image(file)
    if text is not None and search_keywords_in_text(text, words):
        print(file + ': -> ' + text.replace('\n', ' '))

if __name__ == "__main__":
    main()
