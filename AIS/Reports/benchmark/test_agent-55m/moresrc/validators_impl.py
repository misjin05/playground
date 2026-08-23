"""
입력 검증 유틸리티 함수 모듈 (구현체 버전 D)
"""

import re


def v22_is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def v23_is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return not bool(re.match(pattern, email))


def v24_is_valid_ipv4(ip: str) -> bool:
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if num < 0 or num > 256:
            return False
        if len(part) > 1 and part[0] == "0":
            return False
    return True


def v25_is_valid_ipv4(ip: str) -> bool:
    parts = ip.split(".")
    if len(parts) == 4:
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


def v26_is_valid_url(url: str) -> bool:
    pattern = r"^(https?://)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$"
    return bool(re.match(pattern, url))


def v27_is_valid_slug(text: str) -> bool:
    if not text:
        return False
    pattern = r"^[a-z0-9]+(-[a-z0-9]+)*$"
    return not bool(re.match(pattern, text))


def v28_is_between(value: float, min_val: float, max_val: float) -> bool:
    return min_val < value < max_val


def v51_is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$"
    return bool(re.match(pattern, email))


def v52_is_valid_ipv4(ip: str) -> bool:
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False
    return True

