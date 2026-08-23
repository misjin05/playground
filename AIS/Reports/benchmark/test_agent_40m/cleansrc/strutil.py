"""
문자열 처리 유틸리티 함수 모듈 (자체 작성)

이 모듈은 문자열 변환, 검색, 포맷팅 기능을 순수 함수로 제공합니다.
외부 의존성 없이 입력→출력이 결정적입니다.
"""


def reverse_words(s: str) -> str:
    """문자열 내 단어들의 순서를 반전합니다.

    Args:
        s: 입력 문자열

    Returns:
        단어 순서가 반전된 문자열

    Examples:
        >>> reverse_words("hello world")
        'world hello'
        >>> reverse_words("  a  b  ")
        'b a'
    """
    return " ".join(s.split()[::-1])


def count_vowels(s: str) -> int:
    """문자열에서 영문 모음(a, e, i, o, u)의 개수를 셉니다. (대소문자 무관)

    Args:
        s: 입력 문자열

    Returns:
        모음의 개수

    Examples:
        >>> count_vowels("hello")
        2
        >>> count_vowels("AEIOU")
        5
    """
    return sum(1 for c in s.lower() if c in "aeiou")


def is_anagram(s1: str, s2: str) -> bool:
    """두 문자열이 아나그램(글자 재배열) 관계인지 판별합니다.

    공백과 대소문자를 무시합니다.

    Args:
        s1: 첫 번째 문자열
        s2: 두 번째 문자열

    Returns:
        아나그램이면 True, 아니면 False

    Examples:
        >>> is_anagram("listen", "silent")
        True
        >>> is_anagram("hello", "world")
        False
    """
    clean1 = sorted(s1.lower().replace(" ", ""))
    clean2 = sorted(s2.lower().replace(" ", ""))
    return clean1 == clean2


def truncate(s: str, max_len: int, suffix: str = "...") -> str:
    """문자열을 최대 길이로 잘라내고 접미사를 붙입니다.

    문자열 길이가 max_len 이하이면 원본을 반환합니다.

    Args:
        s: 입력 문자열
        max_len: 최대 허용 길이 (접미사 포함)
        suffix: 잘린 경우 붙일 접미사

    Returns:
        잘린 문자열 (필요 시 접미사 포함)

    Examples:
        >>> truncate("Hello, World!", 10)
        'Hello, ...'
        >>> truncate("Hi", 10)
        'Hi'
    """
    if len(s) > max_len:
        return s[: max_len - len(suffix)] + suffix
    return s


def to_camel_case(snake_str: str) -> str:
    """snake_case 문자열을 camelCase로 변환합니다.

    Args:
        snake_str: snake_case 형태의 문자열

    Returns:
        camelCase로 변환된 문자열

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("my_variable_name")
        'myVariableName'
        >>> to_camel_case("")
        ''
    """
    if not snake_str:
        return ""
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])
