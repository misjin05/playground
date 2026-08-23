"""
참조 테스트 코드 (Reference TC) — 정답 상한선

이 테스트는 Clean Code에서 모두 Pass하고,
모든 뮤턴트(M01~M40)를 Kill하는 "완벽한 정답 TC"입니다.
벤치마크 정합성 검증 및 에이전트 생성 TC와의 비교 기준으로 사용됩니다.

실행: pytest benchmark/test_agent/tests/test_reference.py -v
"""

import sys
import os
import pytest

# 프로젝트 루트를 sys.path에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

# ─── Clean Code imports ────────────────────────────
from benchmark.test_agent.cleansrc.mathutil import is_prime, gcd, factorial, clamp, is_palindrome_number
from benchmark.test_agent.cleansrc.strutil import reverse_words, count_vowels, is_anagram, truncate, to_camel_case
from benchmark.test_agent.cleansrc.dsutil import binary_search, flatten, unique_sorted, chunk_list, merge_dicts
from benchmark.test_agent.cleansrc.validators import is_valid_email, is_valid_ipv4, is_valid_url, is_valid_slug, is_between
from benchmark.test_agent.cleansrc.humanize import ordinal, intcomma, intword, file_size, pluralize
from benchmark.test_agent.cleansrc.iterutils import windowed, first_true, compact, partition, remap_keys

# ─── Variant/Implementation imports ────────────────
from benchmark.test_agent.moresrc.mathutil_impl import (
    v01_is_prime, v02_is_prime, v03_gcd,
    v04_factorial, v05_factorial, v06_clamp, v07_is_palindrome_number,
    v41_is_prime, v42_is_palindrome_number,
)
from benchmark.test_agent.moresrc.strutil_impl import (
    v08_reverse_words, v09_count_vowels, v10_is_anagram,
    v11_truncate, v12_truncate, v13_to_camel_case, v14_to_camel_case,
    v46_reverse_words, v47_count_vowels,
)
from benchmark.test_agent.moresrc.dsutil_impl import (
    v15_binary_search, v16_binary_search, v17_flatten,
    v18_unique_sorted, v19_chunk_list, v20_merge_dicts, v21_merge_dicts,
    v43_binary_search, v44_flatten, v45_merge_dicts, v55_chunk_list,
)
from benchmark.test_agent.moresrc.validators_impl import (
    v22_is_valid_email, v23_is_valid_email, v24_is_valid_ipv4,
    v25_is_valid_ipv4, v26_is_valid_url, v27_is_valid_slug, v28_is_between,
    v51_is_valid_email, v52_is_valid_ipv4,
)
from benchmark.test_agent.moresrc.humanize_impl import (
    v29_ordinal, v30_ordinal, v31_intcomma,
    v32_intword, v33_file_size, v34_pluralize,
    v48_ordinal, v49_intword, v50_pluralize,
)
from benchmark.test_agent.moresrc.iterutils_impl import (
    v35_windowed, v36_windowed, v37_first_true,
    v38_compact, v39_partition, v40_remap_keys,
    v53_windowed, v54_compact,
)


# ═══════════════════════════════════════════════════
# Part 1: Clean Code 정상 테스트 (모두 Pass 해야 함)
# ═══════════════════════════════════════════════════

class TestCleanMathutil:
    def test_is_prime_basic(self):
        assert is_prime(2) is True
        assert is_prime(3) is True
        assert is_prime(17) is True
        assert is_prime(1) is False
        assert is_prime(0) is False
        assert is_prime(-5) is False
        assert is_prime(4) is False
        assert is_prime(25) is False

    def test_gcd_basic(self):
        assert gcd(12, 8) == 4
        assert gcd(7, 13) == 1
        assert gcd(0, 5) == 5
        assert gcd(100, 75) == 25
        assert gcd(-12, 8) == 4

    def test_factorial_basic(self):
        assert factorial(0) == 1
        assert factorial(1) == 1
        assert factorial(5) == 120
        assert factorial(10) == 3628800
        with pytest.raises(ValueError):
            factorial(-1)

    def test_clamp_basic(self):
        assert clamp(5, 0, 10) == 5
        assert clamp(-3, 0, 10) == 0
        assert clamp(15, 0, 10) == 10
        assert clamp(0, 0, 10) == 0
        assert clamp(10, 0, 10) == 10

    def test_is_palindrome_number_basic(self):
        assert is_palindrome_number(121) is True
        assert is_palindrome_number(12321) is True
        assert is_palindrome_number(-121) is False
        assert is_palindrome_number(10) is False
        assert is_palindrome_number(0) is True


class TestCleanStrutil:
    def test_reverse_words(self):
        assert reverse_words("hello world") == "world hello"
        assert reverse_words("a b c") == "c b a"
        assert reverse_words("single") == "single"
        assert reverse_words("  a  b  ") == "b a"

    def test_count_vowels(self):
        assert count_vowels("hello") == 2
        assert count_vowels("AEIOU") == 5
        assert count_vowels("rhythm") == 0
        assert count_vowels("ubuntu") == 3

    def test_is_anagram(self):
        assert is_anagram("listen", "silent") is True
        assert is_anagram("hello", "world") is False
        assert is_anagram("Astronomer", "Moon starer") is True

    def test_truncate(self):
        assert truncate("Hello, World!", 10) == "Hello, ..."
        assert truncate("Hi", 10) == "Hi"
        assert truncate("Hello", 5) == "Hello"
        assert truncate("ABCDEFGHIJ", 7) == "ABCD..."
        assert truncate("ABCDEFGHIJ", 7, "..") == "ABCDE.."

    def test_to_camel_case(self):
        assert to_camel_case("hello_world") == "helloWorld"
        assert to_camel_case("my_variable_name") == "myVariableName"
        assert to_camel_case("single") == "single"
        assert to_camel_case("") == ""


class TestCleanDsutil:
    def test_binary_search(self):
        assert binary_search([1, 3, 5, 7, 9], 5) == 2
        assert binary_search([1, 3, 5, 7, 9], 1) == 0
        assert binary_search([1, 3, 5, 7, 9], 9) == 4
        assert binary_search([1, 3, 5, 7, 9], 4) == -1
        assert binary_search([], 1) == -1

    def test_flatten(self):
        assert flatten([1, [2, 3], [4, [5, 6]]]) == [1, 2, 3, 4, 5, 6]
        assert flatten([]) == []
        assert flatten([1, 2, 3]) == [1, 2, 3]
        # 튜플은 평탄화하지 않음 (list만 대상)
        assert flatten([1, (2, 3), [4]]) == [1, (2, 3), 4]

    def test_unique_sorted(self):
        assert unique_sorted([3, 1, 2, 3, 1]) == [1, 2, 3]
        assert unique_sorted([]) == []
        assert unique_sorted([5, 5, 5]) == [5]

    def test_chunk_list(self):
        assert chunk_list([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
        assert chunk_list([1, 2, 3], 3) == [[1, 2, 3]]
        assert chunk_list([], 3) == []
        with pytest.raises(ValueError):
            chunk_list([1, 2], 0)

    def test_merge_dicts(self):
        assert merge_dicts({"a": 1, "b": 2}, {"b": 3, "c": 4}) == {"a": 1, "b": 3, "c": 4}
        assert merge_dicts({}, {}) == {}
        assert merge_dicts({"a": 1}, {}) == {"a": 1}


class TestCleanValidators:
    def test_is_valid_email(self):
        assert is_valid_email("user@example.com") is True
        assert is_valid_email("test.user@domain.co.kr") is True
        assert is_valid_email("invalid-email") is False
        assert is_valid_email("@example.com") is False
        assert is_valid_email("user@") is False

    def test_is_valid_ipv4(self):
        assert is_valid_ipv4("192.168.1.1") is True
        assert is_valid_ipv4("0.0.0.0") is True
        assert is_valid_ipv4("255.255.255.255") is True
        assert is_valid_ipv4("256.1.1.1") is False
        assert is_valid_ipv4("1.2.3") is False
        assert is_valid_ipv4("01.02.03.04") is False

    def test_is_valid_url(self):
        assert is_valid_url("https://www.example.com") is True
        assert is_valid_url("http://example.com") is True
        assert is_valid_url("https://example.com/path") is True
        assert is_valid_url("ftp://invalid.com") is False
        assert is_valid_url("www.example.com") is False
        assert is_valid_url("not-a-url") is False

    def test_is_valid_slug(self):
        assert is_valid_slug("hello-world-123") is True
        assert is_valid_slug("simple") is True
        assert is_valid_slug("Hello World") is False
        assert is_valid_slug("-invalid") is False
        assert is_valid_slug("") is False

    def test_is_between(self):
        assert is_between(5, 1, 10) is True
        assert is_between(1, 1, 10) is True
        assert is_between(10, 1, 10) is True
        assert is_between(0, 1, 10) is False
        assert is_between(11, 1, 10) is False


class TestCleanHumanize:
    def test_ordinal(self):
        assert ordinal(1) == "1st"
        assert ordinal(2) == "2nd"
        assert ordinal(3) == "3rd"
        assert ordinal(4) == "4th"
        assert ordinal(11) == "11th"
        assert ordinal(12) == "12th"
        assert ordinal(13) == "13th"
        assert ordinal(21) == "21st"
        assert ordinal(22) == "22nd"
        assert ordinal(113) == "113th"

    def test_intcomma(self):
        assert intcomma(1000) == "1,000"
        assert intcomma(1000000) == "1,000,000"
        assert intcomma(-1234567) == "-1,234,567"
        assert intcomma(100) == "100"
        assert intcomma(0) == "0"

    def test_intword(self):
        assert intword(1000000) == "1.0 million"
        assert intword(1500000000) == "1.5 billion"
        assert intword(500) == "500"
        assert intword(1000) == "1.0 thousand"
        assert intword(500000) == "500.0 thousand"

    def test_file_size(self):
        assert file_size(0) == "0 Bytes"
        assert file_size(1000) == "1.0 KB"
        assert file_size(1500000) == "1.5 MB"
        assert file_size(1024, binary=True) == "1.0 KiB"
        assert file_size(1048576, binary=True) == "1.0 MiB"

    def test_pluralize(self):
        assert pluralize(1, "item") == "1 item"
        assert pluralize(3, "item") == "3 items"
        assert pluralize(0, "item") == "0 items"
        assert pluralize(2, "child", "children") == "2 children"
        assert pluralize(1, "child", "children") == "1 child"


class TestCleanIterutils:
    def test_windowed(self):
        assert windowed([1, 2, 3, 4, 5], 3) == [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
        assert windowed([1, 2, 3], 2) == [(1, 2), (2, 3)]
        assert windowed([1, 2], 3) == []
        assert windowed([1], 1) == [(1,)]

    def test_first_true(self):
        assert first_true([0, None, False, 3, 4], default="없음") == 3
        assert first_true([1, 2, 3, 4], pred=lambda x: x > 2) == 3
        assert first_true([1, 2], pred=lambda x: x > 5, default=-1) == -1

    def test_compact(self):
        assert compact([0, 1, None, 2, "", 3, False, 4]) == [1, 2, 3, 4]
        assert compact([None, None]) == []
        assert compact([1, 2, 3]) == [1, 2, 3]

    def test_partition(self):
        assert partition(lambda x: x % 2 == 0, [1, 2, 3, 4, 5]) == ([2, 4], [1, 3, 5])
        assert partition(lambda x: x > 0, [-1, 0, 1, 2]) == ([1, 2], [-1, 0])

    def test_remap_keys(self):
        assert remap_keys({"name": "Alice", "age": 30}, {"name": "username"}) == {"username": "Alice", "age": 30}
        assert remap_keys({"a": 1}, {}) == {"a": 1}
        assert remap_keys({}, {"a": "b"}) == {}


# ═══════════════════════════════════════════════════
# Part 2: 뮤턴트 Kill 테스트 (각 뮤턴트가 Fail해야 함)
# ═══════════════════════════════════════════════════

class TestMutantMathutil:
    """M01~M07, M41, M42: mathutil 뮤턴트"""

    def test_m01_is_prime_boundary(self):
        """M01: n <= 1 → n < 1 — is_prime(1)이 True로 오판됨"""
        assert v01_is_prime(1) != is_prime(1)

    def test_m02_is_prime_condition(self):
        """M02: n % i == 0 → n % i != 0 — 합성수를 소수로 오판"""
        assert v02_is_prime(25) != is_prime(25)

    def test_m03_gcd_arithmetic(self):
        """M03: a % b → a // b — 유클리드 호제법 깨짐"""
        assert v03_gcd(12, 8) != gcd(12, 8)

    def test_m04_factorial_boundary(self):
        """M04: n == 0 → n == 1 — factorial(0)에서 ValueError/RecursionError 또는 오답"""
        try:
            val = v04_factorial(0)
            assert val != factorial(0)
        except (RecursionError, ValueError):
            pass  # 결함 검출(Kill)

    def test_m05_factorial_arithmetic(self):
        """M05: n * → n + — factorial(5)가 15로 계산됨"""
        assert v05_factorial(5) != factorial(5)

    def test_m06_clamp_condition(self):
        """M06: value < min_val → value > min_val — 범위 체크 반전"""
        assert v06_clamp(5, 0, 10) != clamp(5, 0, 10)

    def test_m07_palindrome_return(self):
        """M07: == → != — 회문수 판별 반전"""
        assert v07_is_palindrome_number(121) != is_palindrome_number(121)

    def test_m41_is_prime_killer(self):
        """M41 [Killer]: i+4 검사 — 77, 91, 121 등 특정 합성수 소수 오판"""
        assert v41_is_prime(77) != is_prime(77)

    def test_m42_palindrome_killer(self):
        """M42 [Killer]: abs(n)<10 True — 한 자리 음수 -5를 회문수로 오판"""
        assert v42_is_palindrome_number(-5) != is_palindrome_number(-5)


class TestMutantStrutil:
    """M08~M14, M46, M47: strutil 뮤턴트"""

    def test_m08_reverse_words(self):
        """M08: 반전 제거 — 순서 그대로 반환"""
        assert v08_reverse_words("hello world") != reverse_words("hello world")

    def test_m09_count_vowels(self):
        """M09: 'u' 누락 — 'ubuntu'에서 모음 수 다름"""
        assert v09_count_vowels("ubuntu") != count_vowels("ubuntu")

    def test_m10_is_anagram(self):
        """M10: == → != — 아나그램 판별 반전"""
        assert v10_is_anagram("listen", "silent") != is_anagram("listen", "silent")

    def test_m11_truncate_arithmetic(self):
        """M11: - → + — 자르는 위치 오류"""
        assert v11_truncate("Hello, World!", 10) != truncate("Hello, World!", 10)

    def test_m12_truncate_boundary(self):
        """M12: > → >= — 경계값에서 불필요한 잘림"""
        assert v12_truncate("Hello", 5) != truncate("Hello", 5)

    def test_m13_to_camel_case_return(self):
        """M13: camelCase → PascalCase"""
        assert v13_to_camel_case("hello_world") != to_camel_case("hello_world")

    def test_m14_to_camel_case(self):
        """M14: title() 누락 — helloworld 반환"""
        assert v14_to_camel_case("hello_world") != to_camel_case("hello_world")

    def test_m46_reverse_words_killer(self):
        """M46 [Killer]: split(' ') — 다중/양끝 공백 분할 오류"""
        assert v46_reverse_words("  a   b  ") != reverse_words("  a   b  ")

    def test_m47_count_vowels_killer(self):
        """M47 [Killer]: 모음에 'y' 포함 — rhythm 등에서 0이 아닌 1 반환"""
        assert v47_count_vowels("rhythm") != count_vowels("rhythm")


class TestMutantDsutil:
    """M15~M21, M43~M45, M55: dsutil 뮤턴트"""

    def test_m15_binary_search_arithmetic(self):
        """M15: low = mid + 2 — 인덱스 1 탐색 시 누락 발생"""
        assert v15_binary_search([1, 3, 5, 7, 9], 3) != binary_search([1, 3, 5, 7, 9], 3)

    def test_m16_binary_search_condition(self):
        """M16: < → > — 탐색 방향 반전"""
        assert v16_binary_search([1, 3, 5, 7, 9], 3) != binary_search([1, 3, 5, 7, 9], 3)

    def test_m17_flatten_boundary(self):
        """M17: list → (list, tuple) — 튜플도 평탄화"""
        input_data = [1, (2, 3), [4]]
        assert v17_flatten(input_data) != flatten(input_data)

    def test_m18_unique_sorted_return(self):
        """M18: 내림차순 정렬 변조 — 원본(오름차순)과 다름"""
        assert v18_unique_sorted([3, 1, 2]) != unique_sorted([3, 1, 2])

    def test_m19_chunk_list_arithmetic(self):
        """M19: size → size - 1 — step이 줄어 청크 겹침"""
        assert v19_chunk_list([1, 2, 3, 4, 5], 2) != chunk_list([1, 2, 3, 4, 5], 2)

    def test_m20_merge_dicts_return(self):
        """M20: d2 우선 → d1 우선"""
        assert v20_merge_dicts({"a": 1}, {"a": 2}) != merge_dicts({"a": 1}, {"a": 2})

    def test_m21_merge_dicts_boundary(self):
        """M21: 빈 dict 시 None 반환"""
        assert v21_merge_dicts({}, {}) != merge_dicts({}, {})

    def test_m43_binary_search_killer(self):
        """M43 [Killer]: while low < high — 짝수 배열 마지막 원소 탐색 실패"""
        assert v43_binary_search([1, 2], 2) != binary_search([1, 2], 2)

    def test_m44_flatten_killer(self):
        """M44 [Killer]: 빈 리스트([]) 평탄화 누락 잔류"""
        assert v44_flatten([[], 1, [[]]]) != flatten([[], 1, [[]]])

    def test_m45_merge_dicts_killer(self):
        """M45 [Killer]: in-place 원본 d1 객체 훼손 부수효과"""
        d1 = {"a": 1}
        d2 = {"b": 2}
        v45_merge_dicts(d1, d2)
        assert d1 != {"a": 1}  # 원본 d1이 훼손되었는지 검증

    def test_m55_chunk_list_killer(self):
        """M55 [Killer]: 비배수 길이 리스트에서 마지막 청크 누락"""
        assert v55_chunk_list([1, 2, 3], 2) != chunk_list([1, 2, 3], 2)


class TestMutantValidators:
    """M22~M28, M51, M52: validators 뮤턴트"""

    def test_m22_email_boundary(self):
        """M22: + → * — '@example.com' 유효 판정"""
        assert v22_is_valid_email("@example.com") != is_valid_email("@example.com")

    def test_m23_email_condition(self):
        """M23: not 추가 — 결과 반전"""
        assert v23_is_valid_email("user@example.com") != is_valid_email("user@example.com")

    def test_m24_ipv4_boundary(self):
        """M24: 255 → 256 — 256 허용"""
        assert v24_is_valid_ipv4("256.1.1.1") != is_valid_ipv4("256.1.1.1")

    def test_m25_ipv4_condition(self):
        """M25: != → == — 4옥텟 거부"""
        assert v25_is_valid_ipv4("192.168.1.1") != is_valid_ipv4("192.168.1.1")

    def test_m26_url_boundary(self):
        """M26: scheme 선택 — 'www.example.com' 허용"""
        assert v26_is_valid_url("www.example.com") != is_valid_url("www.example.com")

    def test_m27_slug_condition(self):
        """M27: not 추가 — 결과 반전"""
        assert v27_is_valid_slug("hello-world") != is_valid_slug("hello-world")

    def test_m28_between_boundary(self):
        """M28: <= → < — 경계값 제외"""
        assert v28_is_between(1, 1, 10) != is_between(1, 1, 10)

    def test_m51_email_killer(self):
        """M51 [Killer]: 1글자 TLD 허용 결함 (user@domain.c 거부 검증)"""
        assert v51_is_valid_email("user@domain.c") != is_valid_email("user@domain.c")

    def test_m52_ipv4_killer(self):
        """M52 [Killer]: 선행 0 허용 결함 (192.168.01.1 거부 검증)"""
        assert v52_is_valid_ipv4("192.168.01.1") != is_valid_ipv4("192.168.01.1")


class TestMutantHumanize:
    """M29~M34, M48~M50: humanize 뮤턴트"""

    def test_m29_ordinal_boundary(self):
        """M29: 11~13 예외 제거 — '11st' 생성"""
        assert v29_ordinal(11) != ordinal(11)

    def test_m30_ordinal_return(self):
        """M30: 항상 'th' — '1th' 생성"""
        assert v30_ordinal(1) != ordinal(1)

    def test_m31_intcomma_arithmetic(self):
        """M31: 3자리 → 4자리 — 콤마 위치 오류"""
        assert v31_intcomma(1000000) != intcomma(1000000)

    def test_m32_intword_boundary(self):
        """M32: 10^6 → 10^5 — 50만을 million으로 표시"""
        assert v32_intword(500000) != intword(500000)

    def test_m33_file_size_arithmetic(self):
        """M33: binary base 1024 → 1000 — 2,000,000 바이트에서 1.9 MiB vs 2.0 MiB 차이 발생"""
        assert v33_file_size(2000000, binary=True) != file_size(2000000, binary=True)

    def test_m34_pluralize_boundary(self):
        """M34: count==1 → count==0 — 단수/복수 반전"""
        assert v34_pluralize(1, "item") != pluralize(1, "item")

    def test_m48_ordinal_killer(self):
        """M48 [Killer]: 111st 오류 — 111, 112, 113th 처리 누락"""
        assert v48_ordinal(111) != ordinal(111)

    def test_m49_intword_killer(self):
        """M49 [Killer]: 1000000 정확한 경계에서 1.0 million 누락"""
        assert v49_intword(1000000) != intword(1000000)

    def test_m50_pluralize_killer(self):
        """M50 [Killer]: 0개일 때 0 item 단수형 반환 오류"""
        assert v50_pluralize(0, "item") != pluralize(0, "item")


class TestMutantIterutils:
    """M35~M40, M53, M54: iterutils 뮤턴트"""

    def test_m35_windowed_arithmetic(self):
        """M35: +1 제거 — 마지막 윈도우 누락"""
        assert v35_windowed([1, 2, 3], 2) != windowed([1, 2, 3], 2)

    def test_m36_windowed_boundary(self):
        """M36: [] → [tuple(lst)] — 크기 초과 시 비정상 결과"""
        assert v36_windowed([1, 2], 5) != windowed([1, 2], 5)

    def test_m37_first_true_condition(self):
        """M37: pred → not pred — 조건 불만족 원소 반환"""
        assert v37_first_true([1, 2, 3], pred=lambda x: x > 2) != first_true([1, 2, 3], pred=lambda x: x > 2)

    def test_m38_compact_boundary(self):
        """M38: if item → if item is not None — 0, False 유지"""
        assert v38_compact([0, 1, False, 2]) != compact([0, 1, False, 2])

    def test_m39_partition_return(self):
        """M39: 순서 반전 — (true, false) → (false, true)"""
        assert v39_partition(lambda x: x % 2 == 0, [1, 2, 3]) != partition(lambda x: x % 2 == 0, [1, 2, 3])

    def test_m40_remap_keys_return(self):
        """M40: 매핑 없는 키 제거 — 키 누락"""
        assert v40_remap_keys({"a": 1, "b": 2}, {"a": "x"}) != remap_keys({"a": 1, "b": 2}, {"a": "x"})

    def test_m53_windowed_killer(self):
        """M53 [Killer]: n == len(lst)일 때 빈 리스트 반환 오류"""
        assert v53_windowed([1, 2, 3], 3) != windowed([1, 2, 3], 3)

    def test_m54_compact_killer(self):
        """M54 [Killer]: 빈 리스트([]), 빈 딕셔너리({}) 보존 오류"""
        assert v54_compact([[], {}, 1]) != compact([[], {}, 1])

