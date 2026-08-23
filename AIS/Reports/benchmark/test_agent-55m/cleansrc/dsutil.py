"""
자료구조/알고리즘 유틸리티 함수 모듈 (자체 작성)

이 모듈은 리스트, 딕셔너리 등 자료구조 조작 기능을 순수 함수로 제공합니다.
외부 의존성 없이 입력→출력이 결정적입니다.
"""


def binary_search(arr: list, target) -> int:
    """정렬된 리스트에서 target의 인덱스를 이진 탐색으로 찾습니다.

    Args:
        arr: 오름차순 정렬된 리스트
        target: 찾을 값

    Returns:
        target의 인덱스. 없으면 -1

    Examples:
        >>> binary_search([1, 3, 5, 7, 9], 5)
        2
        >>> binary_search([1, 3, 5, 7, 9], 4)
        -1
    """
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def flatten(nested_list: list) -> list:
    """중첩된 리스트를 1차원으로 평탄화합니다.

    Args:
        nested_list: 중첩 리스트

    Returns:
        평탄화된 리스트

    Examples:
        >>> flatten([1, [2, 3], [4, [5, 6]]])
        [1, 2, 3, 4, 5, 6]
        >>> flatten([])
        []
    """
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def unique_sorted(lst: list) -> list:
    """리스트에서 중복을 제거하고 정렬된 결과를 반환합니다.

    Args:
        lst: 입력 리스트

    Returns:
        중복 제거 후 오름차순 정렬된 리스트

    Examples:
        >>> unique_sorted([3, 1, 2, 3, 1])
        [1, 2, 3]
        >>> unique_sorted([])
        []
    """
    return sorted(set(lst))


def chunk_list(lst: list, size: int) -> list:
    """리스트를 지정된 크기의 청크로 분할합니다.

    Args:
        lst: 입력 리스트
        size: 각 청크의 크기 (1 이상)

    Returns:
        청크 리스트의 리스트

    Examples:
        >>> chunk_list([1, 2, 3, 4, 5], 2)
        [[1, 2], [3, 4], [5]]
        >>> chunk_list([], 3)
        []
    """
    if size < 1:
        raise ValueError("청크 크기는 1 이상이어야 합니다.")
    return [lst[i: i + size] for i in range(0, len(lst), size)]


def merge_dicts(d1: dict, d2: dict) -> dict:
    """두 딕셔너리를 병합합니다. 키가 중복되면 d2의 값이 우선합니다.

    Args:
        d1: 첫 번째 딕셔너리
        d2: 두 번째 딕셔너리 (우선)

    Returns:
        병합된 새 딕셔너리

    Examples:
        >>> merge_dicts({"a": 1, "b": 2}, {"b": 3, "c": 4})
        {'a': 1, 'b': 3, 'c': 4}
    """
    result = dict(d1)
    result.update(d2)
    return result
