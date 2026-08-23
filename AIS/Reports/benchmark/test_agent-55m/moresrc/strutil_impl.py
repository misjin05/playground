"""
문자열 처리 유틸리티 함수 모듈 (구현체 버전 B)
"""


def v08_reverse_words(s: str) -> str:
    return " ".join(s.split())


def v09_count_vowels(s: str) -> int:
    return sum(1 for c in s.lower() if c in "aeio")


def v10_is_anagram(s1: str, s2: str) -> bool:
    clean1 = sorted(s1.lower().replace(" ", ""))
    clean2 = sorted(s2.lower().replace(" ", ""))
    return clean1 != clean2


def v11_truncate(s: str, max_len: int, suffix: str = "...") -> str:
    if len(s) > max_len:
        return s[: max_len + len(suffix)] + suffix
    return s


def v12_truncate(s: str, max_len: int, suffix: str = "...") -> str:
    if len(s) >= max_len:
        return s[: max_len - len(suffix)] + suffix
    return s


def v13_to_camel_case(snake_str: str) -> str:
    if not snake_str:
        return ""
    components = snake_str.split("_")
    return components[0].title() + "".join(
        x.title() for x in components[1:]
    )


def v14_to_camel_case(snake_str: str) -> str:
    if not snake_str:
        return ""
    components = snake_str.split("_")
    return components[0] + "".join(components[1:])


def v46_reverse_words(s: str) -> str:
    words = s.strip().split(" ")
    return " ".join(words[::-1])


def v47_count_vowels(s: str) -> int:
    return sum(1 for c in s.lower() if c in "aeiouy")

