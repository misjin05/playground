"""
수학/숫자 처리 유틸리티 함수 모듈 (자체 작성)

이 모듈은 기본적인 수학 연산과 숫자 판별 기능을 순수 함수로 제공합니다.
외부 의존성 없이 입력→출력이 결정적입니다.
"""


def is_prime(n: int) -> bool:
    """주어진 정수가 소수인지 판별합니다.

    Args:
        n: 판별할 정수

    Returns:
        소수이면 True, 아니면 False

    Examples:
        >>> is_prime(2)
        True
        >>> is_prime(1)
        False
        >>> is_prime(17)
        True
    """
    if n <= 1:
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


def gcd(a: int, b: int) -> int:
    """유클리드 호제법을 사용하여 두 정수의 최대공약수를 구합니다.

    Args:
        a: 첫 번째 정수
        b: 두 번째 정수

    Returns:
        a와 b의 최대공약수

    Examples:
        >>> gcd(12, 8)
        4
        >>> gcd(7, 13)
        1
    """
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def factorial(n: int) -> int:
    """주어진 비음수 정수의 팩토리얼을 재귀적으로 계산합니다.

    Args:
        n: 0 이상의 정수

    Returns:
        n! 값

    Raises:
        ValueError: n이 음수인 경우

    Examples:
        >>> factorial(0)
        1
        >>> factorial(5)
        120
    """
    if n < 0:
        raise ValueError("음수의 팩토리얼은 정의되지 않습니다.")
    if n == 0:
        return 1
    return n * factorial(n - 1)


def clamp(value: float, min_val: float, max_val: float) -> float:
    """값을 지정된 범위 내로 제한합니다.

    Args:
        value: 제한할 값
        min_val: 최소값
        max_val: 최대값

    Returns:
        min_val 이상 max_val 이하로 제한된 값

    Examples:
        >>> clamp(5, 0, 10)
        5
        >>> clamp(-3, 0, 10)
        0
        >>> clamp(15, 0, 10)
        10
    """
    if value < min_val:
        return min_val
    if value > max_val:
        return max_val
    return value


def is_palindrome_number(n: int) -> bool:
    """주어진 정수가 회문수(앞뒤로 읽어도 같은 수)인지 판별합니다.

    음수는 회문수로 간주하지 않습니다.

    Args:
        n: 판별할 정수

    Returns:
        회문수이면 True, 아니면 False

    Examples:
        >>> is_palindrome_number(121)
        True
        >>> is_palindrome_number(-121)
        False
        >>> is_palindrome_number(10)
        False
    """
    if n < 0:
        return False
    s = str(n)
    return s == s[::-1]
