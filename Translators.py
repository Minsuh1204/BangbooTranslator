BANGBOO_LANG = {"en": ("ehn", "na"), "ko": ("웅", "나")}

not_implemented = NotImplementedError(
    "We don't support this language yet, but you can make it happen by contributing to this project at https://github.com/Minsuh1204/BangbooTranslator."
)


def is_bangboo_lang(text: str, lang: str):
    match lang:
        case "ko":
            if text[0] in ["웅", "나"]:
                return True
            else:
                return False
        case "en":
            if text[:3] == "ehn" or text[:2] == "na":
                return True
            else:
                return False
        case _:
            raise not_implemented


def main_translator(text: str, lang: str):
    bangboo_lang = BANGBOO_LANG.get(lang)
    if is_bangboo_lang(text, lang):
        # bangboo to human
        total_char_count = len(text) // 16
        translated = ""
        binary_text = text.replace(bangboo_lang[0], "0").replace(bangboo_lang[1], "1")
        for i in range(total_char_count):
            translated += binary_to_char(binary_text[:16])
            binary_text = binary_text[16:]
        return translated
    else:
        # human to bangboo
        binary_text = ""
        for character in text:
            binary_text += char_to_binary(character)
        translated = binary_text.replace("0", bangboo_lang[0]).replace(
            "1", bangboo_lang[1]
        )
        return translated


def binary_to_char(binary_text: str):
    final = 0
    for i in range(len(binary_text) - 1, -1, -1):
        final += (2**i) * int(binary_text[len(binary_text) - i - 1])
    return chr(final)


def char_to_binary(char: str):
    unicode_num = ord(char)
    binary_text = ""
    for i in range(15, -1, -1):
        binary_text += str(unicode_num // (2**i))
        unicode_num %= 2**i
    return binary_text
