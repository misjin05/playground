"""
이터레이터 유틸리티 함수 모듈 (오픈소스 참조)

이 모듈은 more-itertools (https://github.com/more-itertools/more-itertools) 및
boltons (https://github.com/mahmoud/boltons) 라이브러리의 핵심 이터레이터 조작 로직을
단순화하여 순수 함수로 재구현한 것입니다.
원본 라이선스: MIT License

외부 의존성 없이 기본 리스트/이터러블 처리만으로 동작합니다.
"""


def windowed(iterable, n: int) -> list:
    """이터러블에 대해 크기 n의 슬라이딩 윈도우를 생성합니다.

    Args:
        iterable: 입력 이터러블
        n: 윈도우 크기 (1 이상)

    Returns:
        각 윈도우를 튜플로 담은 리스트

    Examples:
        >>> windowed([1, 2, 3, 4, 5], 3)
        [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
        >>> windowed([1, 2], 3)
        []
    """
    lst = list(iterable)
    if n > len(lst):
        return []
    return [tuple(lst[i: i + n]) for i in range(len(lst) - n + 1)]


def first_true(iterable, default=None, pred=None):
    """이터러블에서 조건을 만족하는 첫 번째 원소를 반환합니다.

    Args:
        iterable: 입력 이터러블
        default: 조건을 만족하는 원소가 없을 때 반환할 기본값
        pred: 판별 함수. None이면 truthy 검사

    Returns:
        조건을 만족하는 첫 원소, 없으면 default

    Examples:
        >>> first_true([0, None, False, 3, 4], default="없음")
        3
        >>> first_true([1, 2, 3, 4], pred=lambda x: x > 2)
        3
    """
    if pred is None:
        pred = bool
    for item in iterable:
        if pred(item):
            return item
    return default


def compact(iterable) -> list:
    """이터러블에서 falsy 값(None, False, 0, "", [], {})을 제거합니다.

    Args:
        iterable: 입력 이터러블

    Returns:
        falsy 값이 제거된 리스트

    Examples:
        >>> compact([0, 1, None, 2, "", 3, False, 4])
        [1, 2, 3, 4]
        >>> compact([None, None])
        []
    """
    return [item for item in iterable if item]


def partition(pred, iterable) -> tuple:
    """조건 함수를 기준으로 이터러블을 두 그룹으로 분할합니다.

    Args:
        pred: 판별 함수
        iterable: 입력 이터러블

    Returns:
        (true_list, false_list) 튜플
        - true_list: pred(item)이 True인 원소들
        - false_list: pred(item)이 False인 원소들

    Examples:
        >>> partition(lambda x: x % 2 == 0, [1, 2, 3, 4, 5])
        ([2, 4], [1, 3, 5])
    """
    true_list = []
    false_list = []
    for item in iterable:
        if pred(item):
            true_list.append(item)
        else:
            false_list.append(item)
    return (true_list, false_list)


def remap_keys(d: dict, key_map: dict) -> dict:
    """딕셔너리의 키 이름을 매핑 테이블에 따라 변환합니다.

    key_map에 없는 키는 원래 이름을 유지합니다.

    Args:
        d: 원본 딕셔너리
        key_map: {원래키: 새키} 매핑 딕셔너리

    Returns:
        키가 변환된 새 딕셔너리

    Examples:
        >>> remap_keys({"name": "Alice", "age": 30}, {"name": "username"})
        {'username': 'Alice', 'age': 30}
    """
    return {key_map.get(k, k): v for k, v in d.items()}
