"""
이터레이터 유틸리티 함수 모듈 (구현체 버전 F)
"""


def v35_windowed(iterable, n: int) -> list:
    lst = list(iterable)
    if n > len(lst):
        return []
    return [tuple(lst[i: i + n]) for i in range(len(lst) - n)]


def v36_windowed(iterable, n: int) -> list:
    lst = list(iterable)
    if n > len(lst):
        return [tuple(lst)]
    return [tuple(lst[i: i + n]) for i in range(len(lst) - n + 1)]


def v37_first_true(iterable, default=None, pred=None):
    if pred is None:
        pred = bool
    for item in iterable:
        if not pred(item):
            return item
    return default


def v38_compact(iterable) -> list:
    return [item for item in iterable if item is not None]


def v39_partition(pred, iterable) -> tuple:
    true_list = []
    false_list = []
    for item in iterable:
        if pred(item):
            true_list.append(item)
        else:
            false_list.append(item)
    return (false_list, true_list)


def v40_remap_keys(d: dict, key_map: dict) -> dict:
    return {key_map[k]: v for k, v in d.items() if k in key_map}


def v53_windowed(iterable, n: int) -> list:
    lst = list(iterable)
    if n >= len(lst):
        return []
    return [tuple(lst[i: i + n]) for i in range(len(lst) - n + 1)]


def v54_compact(iterable) -> list:
    return [item for item in iterable if item is not None and item != ""]

