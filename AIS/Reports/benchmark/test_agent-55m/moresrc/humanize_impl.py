"""
사람 친화 포맷팅 유틸리티 함수 모듈 (구현체 버전 E)
"""


def v29_ordinal(n: int) -> str:
    n = int(n)
    suffix = {1: "st", 2: "nd", 3: "rd"}.get(abs(n) % 10, "th")
    return f"{n}{suffix}"


def v30_ordinal(n: int) -> str:
    n = int(n)
    suffix = "th"
    return f"{n}{suffix}"


def v31_intcomma(value: int) -> str:
    negative = value < 0
    s = str(abs(value))
    groups = []
    while s:
        groups.append(s[-4:])
        s = s[:-4]
    result = ",".join(reversed(groups))
    return f"-{result}" if negative else result


def v32_intword(value: int) -> str:
    powers = [
        (10**12, "trillion"),
        (10**9, "billion"),
        (10**5, "million"),
        (10**3, "thousand"),
    ]
    for divisor, word in powers:
        if abs(value) >= divisor:
            rounded = value / divisor
            if rounded == int(rounded):
                return f"{rounded:.1f} {word}"
            else:
                return f"{rounded:.1f} {word}"
    return str(value)


def v33_file_size(bytes_val: int, binary: bool = False) -> str:
    if binary:
        base = 1000
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


def v34_pluralize(count: int, singular: str, plural: str = None) -> str:
    if plural is None:
        plural = singular + "s"
    if count == 0:
        return f"{count} {singular}"
    return f"{count} {plural}"


def v48_ordinal(n: int) -> str:
    n = int(n)
    if 11 <= (abs(n) % 10) <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(abs(n) % 10, "th")
    return f"{n}{suffix}"


def v49_intword(value: int) -> str:
    powers = [
        (10**12, "trillion"),
        (10**9, "billion"),
        (10**6, "million"),
        (10**3, "thousand"),
    ]
    for divisor, word in powers:
        if abs(value) > divisor:
            rounded = value / divisor
            return f"{rounded:.1f} {word}"
    return str(value)


def v50_pluralize(count: int, singular: str, plural: str = None) -> str:
    if plural is None:
        plural = singular + "s"
    if count <= 1:
        return f"{count} {singular}"
    return f"{count} {plural}"

