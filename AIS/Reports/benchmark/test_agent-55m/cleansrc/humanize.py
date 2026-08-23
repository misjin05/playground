"""
사람 친화 포맷팅 유틸리티 함수 모듈 (오픈소스 참조)

이 모듈은 humanize (https://github.com/jmoiron/humanize) 라이브러리의
핵심 포맷팅 로직을 단순화하여 순수 함수로 재구현한 것입니다.
원본 라이선스: MIT License

외부 의존성 없이 기본 문자열/숫자 처리만으로 동작합니다.
"""


def ordinal(n: int) -> str:
    """정수를 영문 서수(ordinal) 문자열로 변환합니다.

    Args:
        n: 변환할 정수

    Returns:
        서수 문자열 (예: "1st", "2nd", "3rd", "4th")

    Examples:
        >>> ordinal(1)
        '1st'
        >>> ordinal(11)
        '11th'
        >>> ordinal(22)
        '22nd'
        >>> ordinal(113)
        '113th'
    """
    n = int(n)
    if 11 <= (abs(n) % 100) <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(abs(n) % 10, "th")
    return f"{n}{suffix}"


def intcomma(value: int) -> str:
    """정수에 천 단위 콤마를 삽입합니다.

    Args:
        value: 포맷할 정수

    Returns:
        콤마가 삽입된 문자열

    Examples:
        >>> intcomma(1000)
        '1,000'
        >>> intcomma(1000000)
        '1,000,000'
        >>> intcomma(-1234567)
        '-1,234,567'
    """
    negative = value < 0
    s = str(abs(value))
    groups = []
    while s:
        groups.append(s[-3:])
        s = s[:-3]
    result = ",".join(reversed(groups))
    return f"-{result}" if negative else result


def intword(value: int) -> str:
    """큰 정수를 사람이 읽기 쉬운 단어로 변환합니다.

    지원 범위: thousand, million, billion, trillion

    Args:
        value: 변환할 정수

    Returns:
        단어로 표현된 문자열. 1000 미만이면 숫자 그대로 문자열 반환.

    Examples:
        >>> intword(1000000)
        '1.0 million'
        >>> intword(1500000000)
        '1.5 billion'
        >>> intword(500)
        '500'
    """
    powers = [
        (10**12, "trillion"),
        (10**9, "billion"),
        (10**6, "million"),
        (10**3, "thousand"),
    ]
    for divisor, word in powers:
        if abs(value) >= divisor:
            rounded = value / divisor
            # 소수점 이하가 0이면 .0으로 표시
            if rounded == int(rounded):
                return f"{rounded:.1f} {word}"
            else:
                return f"{rounded:.1f} {word}"
    return str(value)


def file_size(bytes_val: int, binary: bool = False) -> str:
    """바이트 값을 사람이 읽기 쉬운 파일 크기로 변환합니다.

    Args:
        bytes_val: 바이트 수
        binary: True이면 이진 단위(1024 기준, KiB/MiB),
                False이면 십진 단위(1000 기준, KB/MB)

    Returns:
        포맷된 파일 크기 문자열

    Examples:
        >>> file_size(1024)
        '1.0 KB'
        >>> file_size(1024, binary=True)
        '1.0 KiB'
        >>> file_size(1500000)
        '1.5 MB'
    """
    if binary:
        base = 1024
        units = ["Bytes", "KiB", "MiB", "GiB", "TiB"]
    else:
        base = 1000
        units = ["Bytes", "KB", "MB", "GB", "TB"]

    size = float(bytes_val)
    for unit in units[:-1]:
        if abs(size) < base:
            if unit == "Bytes":
                return f"{int(size)} {unit}"
            return f"{size:.1f} {unit}"
        size /= base
    return f"{size:.1f} {units[-1]}"


def pluralize(count: int, singular: str, plural: str = None) -> str:
    """개수에 따라 단수/복수 형태의 문자열을 반환합니다.

    Args:
        count: 개수
        singular: 단수 형태
        plural: 복수 형태. None이면 singular + "s" 사용

    Returns:
        "개수 단수/복수" 형태의 문자열

    Examples:
        >>> pluralize(1, "item")
        '1 item'
        >>> pluralize(3, "item")
        '3 items'
        >>> pluralize(2, "child", "children")
        '2 children'
    """
    if plural is None:
        plural = singular + "s"
    if count == 1:
        return f"{count} {singular}"
    return f"{count} {plural}"
