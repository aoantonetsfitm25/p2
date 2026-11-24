"""Ітерабельний контейнер студентів з незалежними ітераторами."""

from collections import namedtuple
from collections.abc import Iterator
from itertools import islice
from operator import attrgetter


Student = namedtuple("Student", ["name", "grade"])


class StudentGroupIterator(Iterator[Student]):
    """Окремий стан обходу групи студентів."""

    def __init__(self, students: list[Student]) -> None:
        self._students = students
        self._index = 0

    def __iter__(self) -> "StudentGroupIterator":
        return self

    def __next__(self) -> Student:
        if self._index >= len(self._students):
            raise StopIteration
        student = self._students[self._index]
        self._index += 1
        return student


class StudentGroup:
    """Повторно ітерований контейнер, який створює новий ітератор для кожного обходу."""

    def __init__(self, group_name: str) -> None:
        self._group_name = group_name
        self._students: list[Student] = []

    def add_student(self, name: str, grade: int) -> None:
        if not name.strip():
            raise ValueError("Ім'я студента не може бути порожнім.")
        if isinstance(grade, bool) or not isinstance(grade, int) or not 0 <= grade <= 100:
            raise ValueError("Оцінка має бути цілим числом від 0 до 100.")
        self._students.append(Student(name.strip(), grade))

    def __iter__(self) -> StudentGroupIterator:
        return StudentGroupIterator(self._students)

    def __len__(self) -> int:
        return len(self._students)

    def top_students(self, n: int = 3) -> Iterator[Student]:
        """Повертає ітератор перших n студентів після сортування за оцінкою."""
        if n < 0:
            raise ValueError("n не може бути від'ємним.")
        ordered = sorted(self._students, key=attrgetter("grade"), reverse=True)
        return islice(ordered, n)


def main() -> None:
    group = StudentGroup("КІ-21")
    for name, grade in (("Олена", 95), ("Іван", 78), ("Марія", 92), ("Петро", 85), ("Анна", 88)):
        group.add_student(name, grade)

    print(f"Група {group._group_name}, студентів: {len(group)}")
    print("Перший обхід:")
    for student in group:
        print(f"  {student.name}: {student.grade}")

    print("\nДругий незалежний обхід:")
    for student in group:
        print(f"  {student.name}: {student.grade}")

    first = iter(group)
    second = iter(group)
    print(f"\nДва ітератори: next(first)={next(first).name}, next(second)={next(second).name}")

    pairs = [(s1.name, s2.name) for s1 in group for s2 in group if s1.name < s2.name]
    print(f"Унікальних пар студентів: {len(pairs)}; перші 3: {pairs[:3]}")

    top = group.top_students(3)
    print(f"top_students повернув: {type(top).__name__}")
    print("Топ-3:")
    for student in top:
        print(f"  {student.name}: {student.grade}")

    try:
        group.add_student("", 80)
    except ValueError as error:
        print(f"Некоректний студент відхилений: {error}")


if __name__ == "__main__":
    main()
