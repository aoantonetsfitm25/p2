"""Функції-генератори для числових послідовностей."""

from collections.abc import Iterable, Iterator
from itertools import islice
import math


def arithmetic_progression(start: float, step: float) -> Iterator[float]:
    """Нескінченно видає start, start+step, start+2*step і так далі."""
    value = start
    while True:
        yield value
        value += step


def geometric_progression(start: float, ratio: float, limit: float = float("inf")) -> Iterator[float]:
    """Видає геометричну прогресію до першого значення, більшого за limit."""
    if not math.isfinite(start) or start <= 0:
        raise ValueError("start має бути скінченним додатним числом.")
    if not math.isfinite(ratio) or ratio <= 1:
        raise ValueError("ratio має бути скінченним числом, більшим за 1.")
    if limit < 0 or math.isnan(limit):
        raise ValueError("limit не може бути від'ємним або NaN.")
    value = start
    while value <= limit:
        yield value
        value *= ratio


def fibonacci(n: int | None = None) -> Iterator[int]:
    """Видає перші n чисел Фібоначчі або нескінченну послідовність, якщо n=None."""
    if n is not None and (isinstance(n, bool) or not isinstance(n, int) or n < 0):
        raise ValueError("n має бути невід'ємним цілим числом або None.")
    left, right = 0, 1
    produced = 0
    while n is None or produced < n:
        yield left
        left, right = right, left + right
        produced += 1


def collatz_sequence(n: int) -> Iterator[int]:
    """Видає послідовність Коллатца від n до 1 включно."""
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("Початкове n має бути додатним цілим числом.")
    while True:
        yield n
        if n == 1:
            return
        n = n // 2 if n % 2 == 0 else 3 * n + 1


def flatten(nested: Iterable[object]) -> Iterator[object]:
    """Рекурсивно розгортає вкладені списки, делегуючи рекурсію через yield from."""
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


def main() -> None:
    print(f"Арифметична прогресія (2, 3), перші 10: {list(islice(arithmetic_progression(2, 3), 10))}")
    print(f"Геометрична прогресія (1, 2) до 1000: {list(geometric_progression(1, 2, limit=1000))}")
    print(f"Фібоначчі (15): {list(fibonacci(15))}")

    collatz = list(collatz_sequence(27))
    print(f"Коллатц (27): довжина={len(collatz)}, максимум={max(collatz)}, останнє={collatz[-1]}")

    nested = [1, [2, 3], [4, [5, 6]], 7, [8, [9, [10]]]]
    print(f"Розгортання: {list(flatten(nested))}")

    for fib_num in fibonacci(None):
        if fib_num > 10_000:
            print(f"Перше число Фібоначчі > 10000: {fib_num}")
            break

    print(f"fibonacci(0): {list(fibonacci(0))}")
    try:
        list(collatz_sequence(0))
    except ValueError as error:
        print(f"Некоректна послідовність Коллатца: {error}")


if __name__ == "__main__":
    main()
