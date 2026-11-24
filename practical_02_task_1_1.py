"""Реалізація власного циклічного ітератора CyclicRange."""

from collections.abc import Iterator


class CyclicRange(Iterator[int]):
    """Видає range(start, stop, step) задану кількість разів."""

    def __init__(self, start: int, stop: int, step: int = 1, repeats: int = 1) -> None:
        values = (start, stop, step, repeats)
        if any(isinstance(value, bool) or not isinstance(value, int) for value in values):
            raise TypeError("start, stop, step і repeats мають бути цілими числами.")
        if step == 0:
            raise ValueError("step не може дорівнювати нулю.")
        if repeats < 0:
            raise ValueError("repeats не може бути від'ємним.")

        self._start = start
        self._stop = stop
        self._step = step
        self._repeats = repeats
        self._current = start
        self._cycle = 0
        self._has_values = start < stop if step > 0 else start > stop

    def __iter__(self) -> "CyclicRange":
        return self

    def __next__(self) -> int:
        if self._cycle >= self._repeats or not self._has_values:
            raise StopIteration

        value = self._current
        self._current += self._step
        passed_end = self._current >= self._stop if self._step > 0 else self._current <= self._stop
        if passed_end:
            self._cycle += 1
            self._current = self._start
        return value


def main() -> None:
    print("CyclicRange(1, 4, repeats=3):")
    print(*CyclicRange(1, 4, repeats=3))

    print("\nCyclicRange(0, 10, step=3, repeats=2):")
    print(*CyclicRange(0, 10, step=3, repeats=2))

    values = list(CyclicRange(5, 8, repeats=2))
    print(f"\nЯк список: {values}")
    print(f"Сума CyclicRange(1, 5, repeats=2): {sum(CyclicRange(1, 5, repeats=2))}")

    descending = list(CyclicRange(3, 0, step=-1, repeats=2))
    print(f"Зворотний крок: {descending}")

    exhausted = iter(CyclicRange(1, 2))
    next(exhausted)
    try:
        next(exhausted)
    except StopIteration:
        print("Після останнього елемента: StopIteration")

    try:
        CyclicRange(1, 5, step=0)
    except ValueError as error:
        print(f"Некоректний крок: {error}")


if __name__ == "__main__":
    main()
