"""
입력 검증 유틸리티 함수 모듈 (오픈소스 참조)

이 모듈은 validators (https://github.com/python-validators/validators) 라이브러리의
핵심 검증 로직을 단순화하여 순수 함수로 재구현한 것입니다.
원본 라이선스: MIT License

외부 의존성 없이 정규식과 기본 문자열 처리만으로 동작합니다.
"""

import re


def is_valid_email(email: str) -> bool:
    """이메일 주소 형식을 검증합니다.

    RFC 5322의 기본 규칙을 단순화하여 적용합니다.
    - local part: 영문, 숫자, 점(.), 하이픈(-), 밑줄(_) 허용
    - @ 기호 필수
    - domain part: 영문, 숫자, 점, 하이픈 허용, 최소 하나의 점 포함

    Args:
        email: 검증할 이메일 문자열

    Returns:
        유효한 이메일 형식이면 True

    Examples:
        >>> is_valid_email("user@example.com")
        True
        >>> is_valid_email("invalid-email")
        False
        >>> is_valid_email("@example.com")
        False
    """
    pattern = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def is_valid_ipv4(ip: str) -> bool:
    """IPv4 주소 형식을 검증합니다.

    각 옥텟이 0~255 범위의 정수이고, 정확히 4개의 옥텟으로 구성되어야 합니다.
    선행 0은 허용하지 않습니다 (예: "01.02.03.04"는 무효).

    Args:
        ip: 검증할 IP 주소 문자열

    Returns:
        유효한 IPv4 주소이면 True

    Examples:
        >>> is_valid_ipv4("192.168.1.1")
        True
        >>> is_valid_ipv4("256.1.1.1")
        False
        >>> is_valid_ipv4("1.2.3")
        False
    """
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False
        if len(part) > 1 and part[0] == "0":
            return False
    return True


def is_valid_url(url: str) -> bool:
    """URL 형식을 검증합니다.

    http:// 또는 https:// 스킴이 필수이며, 도메인 부분이 존재해야 합니다.

    Args:
        url: 검증할 URL 문자열

    Returns:
        유효한 URL 형식이면 True

    Examples:
        >>> is_valid_url("https://www.example.com")
        True
        >>> is_valid_url("ftp://invalid.com")
        False
        >>> is_valid_url("not-a-url")
        False
    """
    pattern = r"^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$"
    return bool(re.match(pattern, url))


def is_valid_slug(text: str) -> bool:
    """slug 형식을 검증합니다.

    slug는 영문 소문자, 숫자, 하이픈만 허용하며,
    하이픈으로 시작하거나 끝나지 않아야 합니다.

    Args:
        text: 검증할 문자열

    Returns:
        유효한 slug이면 True

    Examples:
        >>> is_valid_slug("hello-world-123")
        True
        >>> is_valid_slug("Hello World")
        False
        >>> is_valid_slug("-invalid")
        False
    """
    if not text:
        return False
    pattern = r"^[a-z0-9]+(-[a-z0-9]+)*$"
    return bool(re.match(pattern, text))


def is_between(value: float, min_val: float, max_val: float) -> bool:
    """값이 지정된 범위 내에 있는지 검증합니다. (경계값 포함)

    Args:
        value: 검증할 값
        min_val: 최소값 (포함)
        max_val: 최대값 (포함)

    Returns:
        min_val <= value <= max_val이면 True

    Examples:
        >>> is_between(5, 1, 10)
        True
        >>> is_between(10, 1, 10)
        True
        >>> is_between(0, 1, 10)
        False
    """
    return min_val <= value <= max_val
