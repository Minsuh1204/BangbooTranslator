import argparse
import ctypes
import locale
import os

from Translators import *


def get_user_lang():
    if os.name == "posix":
        user_lang = locale.getlocale()[0]
    else:
        windll = ctypes.windll.kernel32
        user_lang = locale.windows_locale[windll.GetUserDefaultUILanguage()]
    return user_lang[:2]


def translate_file(file_location: str, lang: str):
    with open(file_location, "r") as f:
        text = f.read()
    translated = main_translator(text, lang)
    with open(file_location, "w") as f:
        f.write(translated)


def main():
    user_lang = get_user_lang()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "target", type=str, help="Specify the file or text to translate."
    )
    parser.add_argument(
        "--language",
        "-l",
        type=str,
        help="Specify the language of the bangboo.",
        default="none",
    )
    args = parser.parse_args()
    if args.language != "none":
        user_lang = args.language
    # print(user_lang)
    if os.path.isfile(args.target):
        translate_file(args.target, user_lang)
    else:
        print(main_translator(args.target, user_lang))


if __name__ == "__main__":
    main()
