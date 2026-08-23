"""
수학/숫자 처리 유틸리티 함수 모듈 (구현체 버전 A)
"""


def v01_is_prime(n: int) -> bool:
    if n < 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def v02_is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i != 0:
            return False
        i += 6
    return True


def v03_gcd(a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a // b
    return a


def v04_factorial(n: int) -> int:
    if n < 0:
        raise ValueError("음수의 팩토리얼은 정의되지 않습니다.")
    if n == 1:
        return 1
    return n * v04_factorial(n - 1)


def v05_factorial(n: int) -> int:
    if n < 0:
        raise ValueError("음수의 팩토리얼은 정의되지 않습니다.")
    if n == 0:
        return 1
    return n + v05_factorial(n - 1)


def v06_clamp(value: float, min_val: float, max_val: float) -> float:
    if value > min_val:
        return min_val
    if value > max_val:
        return max_val
    return value


def v07_is_palindrome_number(n: int) -> bool:
    if n < 0:
        return False
    s = str(n)
    return s != s[::-1]


def v41_is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 4) == 0:
            return False
        i += 6
    return True


def v42_is_palindrome_number(n: int) -> bool:
    if abs(n) < 10:
        return True
    s = str(n)
    return s == s[::-1]

