import shutil
import os
import sys
import typing
import re

OTHERS = "others"
ARCHIVES = "archives"
MAIN_PATH: typing.Optional[str] = None

categories: typing.Dict[str, typing.List] = {
    "images": ["jpeg", "png", "jpg", "svg"],
    "videos": ["avi", "mp4", "mow", "mkv"],
    "documents": ["DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX"],
    "music": ["MP3", "OGG", "WAV", "AMR"],
    "archives": ["ZIP", "GZ", "TAR"],
    "others": [],
}

transition_history = {
    "images": {},
    "videos": {},
    "documents": {},
    "music": {},
    "archives": {},
    "others": {},
}
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(filename: str):
    filename = name.translate(TRANS)
    filename = re.sub(r'\W', '_', filename)

    return filename


def get_category_n_extension(item_path: str):
    extension = item_path.split(".")[-1]
    lower_extension = extension.lower()
    for category, extensions in categories.items():
        if lower_extension in extensions:
            return category
    categories[OTHERS].append(lower_extension)
    return OTHERS, lower_extension


def get_filename(item_path: str):
    filename: str = os.path.split(item_path)[-1]
    normalized_filename = normalize(filename)
    return normalized_filename


def unpack_archive(item_path, target_path, ext):
    shutil.unpack_archive(filename=item_path,
                          extract_dir=target_path, format=ext)


def move_file(current_path: str):
    category, extension = get_category_n_extension(current_path)
    category_folder = os.path.join(MAIN_PATH, category)
    filename = get_filename(current_path)
    if category == ARCHIVES:
        "photo.some.jpg"
        archive_name = ".".join(filename.split(".")[:-1])
        target_archive_path = os.path.join(category_folder, archive_name)
        unpack_archive(current_path, target_archive_path, ext=extension)
        return ARCHIVES, target_archive_path
    target_path = os.path.join(category_folder, filename)
    shutil.move(src=current_path, dst=target_path)
    return category, target_path


def perform_clean(root_path):
    child_files = os.listdir(root_path)
    for item in child_files:
        item_path = os.path.join(root_path, item)
        if os.path.isdir(item_path):
            perform_clean(item_path)
        elif os.path.isfile(item_path):
            category, new_file_path = move_file(item_path)
            transition_history[category][item_path] = new_file_path
        else:
            raise ValueError


def main():
    global MAIN_PATH
    root_path = sys.argv[1]
    MAIN_PATH = root_path
    assert MAIN_PATH is not None, "MAIN PATH is not set!!!"
    perform_clean(root_path)
