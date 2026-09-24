import os
from datetime import datetime


def get_file_info(file_path):
    if not os.path.exists(file_path):
        return {}

    size = os.path.getsize(file_path)
    name = os.path.basename(file_path)
    ext  = os.path.splitext(file_path)[1]

    info = {
        "file_name"   : name,
        "file_path"   : os.path.abspath(file_path),
        "file_type"   : ext,
        "size_bytes"  : size,
        "loaded_at"   : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return info


def add_text_stats(info, text):
    info["char_count"] = len(text)
    info["word_count"] = len(text.split())
    info["line_count"] = len(text.splitlines())
    return info


def print_info(info):
    print("\n--- Document Info ---")
    for key, value in info.items():
        print(f"  {key}: {value}")
    print("---------------------\n")


# test
if __name__ == "__main__":
    # use this file itself just to test
    info = get_file_info(__file__)
    with open(__file__, "r") as f:
        content = f.read()
    info = add_text_stats(info, content)
    print_info(info)
