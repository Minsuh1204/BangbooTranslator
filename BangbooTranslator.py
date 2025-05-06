import base64

ADV_BANGBOO_LANG = {
    "ko": (
        "웅...",
        "나...",
        "웅 ",
        "나 ",
        "웅?",
        "나?",
        "웅!",
        "나!",
        "웅~",
        "나~",
        "웅",
        "나",
    ),
    "en": (
        "ehn...",  # 6
        "na...",  # 5
        "ehn ",  # 4
        "ehn?",
        "ehn!",
        "ehn~",
        "ehn",  # 3
        "na ",
        "na?",
        "na!",
        "na~",
        "na",  # 2
    ),
}

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
            if text.startswith("ehn") or text.startswith("na"):
                return True
            else:
                return False
        case _:
            raise not_implemented


def adv_translator_v2(text: str, lang: str) -> str:
    if not lang in ADV_BANGBOO_LANG.keys():
        raise not_implemented

    bangboo_lang = ADV_BANGBOO_LANG.get(lang)
    if is_bangboo_lang(text, lang):
        partial = ""
        final = ""
        while len(text) != 0:
            for letter in bangboo_lang:
                if text.startswith(letter):
                    num = bangboo_lang.index(letter)
                    del_length = len(letter)
                    num = f"0{num}" if num < 10 else str(num)
                    text = text[del_length:]
                    partial += num
                    if len(partial) == 6:
                        final += duodecimal_to_char(partial)
                        partial = ""
                    break
        padding_count = len(final) % 4
        final += "=" * padding_count
        return base64.b64decode(final).decode()
    else:
        based = base64.b64encode(text.encode()).decode().strip("=")
        final_str = ""
        for char in based:
            # 000301 = 37
            duodecimal = char_to_duodecimal(char)
            num_1 = int(duodecimal[:2])
            num_2 = int(duodecimal[2:4])
            num_3 = int(duodecimal[4:])
            final_str += bangboo_lang[num_1] + bangboo_lang[num_2] + bangboo_lang[num_3]
        return final_str


def new_b64_table(method: str, target: str | int):
    # total: 70 characters
    special_letters = ["+", "/"]
    match method:
        case "to_int":
            char: str = target
            # 0 1 for special characters (padding "=" should be removed beforehand)
            if char in special_letters:
                return special_letters.index(char)
            # 2 ~ 11 for numbers
            elif char.isnumeric():
                return int(char) + 2
            else:
                # 12 ~ 69 for alphabets
                return ord(char) - 53
        case "to_str":
            num: int = target
            if num <= 1:
                return special_letters[num]
            elif num <= 11:
                return str(num - 2)
            else:
                return chr(num + 53)
        case _:
            return None


def duodecimal_to_char(duodecimal: str):
    # 00/03/11 = 47
    final_num = 0
    for i in range(3):
        final_num += 12 ** (2 - i) * int(duodecimal[(i + 1) * 2 - 2 : (i + 1) * 2])
    return new_b64_table("to_str", final_num)


def char_to_duodecimal(char: str):
    # 9 = 00/00/09
    # 13 = 00/01/01
    # 1 = 00/00/01
    num: int = new_b64_table("to_int", char)
    duodecimal = ""
    for i in range(3):
        quotient, num = divmod(num, 12 ** (2 - i))
        if i == 2 and quotient == 0:
            # make it two digits
            adding = f"0{num}" if num < 10 else str(num)
            duodecimal += adding
        else:
            # make it two digits
            adding = f"0{quotient}" if quotient < 10 else str(quotient)
            duodecimal += adding
    return duodecimal
