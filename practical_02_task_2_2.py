"""Конвеєр генераторів для потокової обробки оцінок студентів."""

from collections import defaultdict
from collections.abc import Iterable, Iterator


SAMPLE_DATA = [
    "Олена,Математика,95",
    "Іван,Математика,78",
    "",
    "Марія,Фізика,92",
    "Петро,Математика,INVALID",
    "Анна,Фізика,88",
    "Олена,Фізика,90",
    "Іван,Програмування,85",
    "Марія,Програмування,91",
    "Петро,Фізика,76",
    "Анна,Математика,93",
    "Олена,Програмування,97",
    "   ",
    "Марія,Математика,89",
    "Іван,Фізика,72",
    "Петро,Програмування,80",
    "Анна,Програмування,86",
    "Запис без усіх полів",
]


def data_source(records: Iterable[str]) -> Iterator[str]:
    """Етап 1: видає вхідні записи по одному."""
    yield from records


def filter_empty(records: Iterable[str]) -> Iterator[str]:
    """Етап 2: обрізає пробіли й пропускає порожні рядки."""
    for record in records:
        cleaned = record.strip()
        if cleaned:
            yield cleaned


def parse_records(records: Iterable[str], stats: dict[str, int] | None = None) -> Iterator[dict[str, str | int]]:
    """Етап 3: розбирає CSV-подібні рядки й пропускає некоректні записи."""
    for line in records:
        fields = [part.strip() for part in line.split(",")]
        if len(fields) != 3 or not fields[0] or not fields[1]:
            if stats is not None:
                stats["malformed"] = stats.get("malformed", 0) + 1
            continue
        try:
            grade = int(fields[2])
        except ValueError:
            if stats is not None:
                stats["invalid_grade"] = stats.get("invalid_grade", 0) + 1
            continue
        if not 0 <= grade <= 100:
            if stats is not None:
                stats["out_of_range"] = stats.get("out_of_range", 0) + 1
            continue
        yield {"student": fields[0], "subject": fields[1], "grade": grade}


def filter_passed(records: Iterable[dict[str, str | int]], min_grade: int = 60) -> Iterator[dict[str, str | int]]:
    """Етап 4: залишає записи з оцінкою не нижче min_grade."""
    for record in records:
        if int(record["grade"]) >= min_grade:
            yield record


def format_output(records: Iterable[dict[str, str | int]]) -> Iterator[str]:
    """Етап 5: перетворює записи на рядки для відображення."""
    for record in records:
        yield f"[{record['subject']}] {record['student']}: {record['grade']} балів"


def subject_averages(records: Iterable[dict[str, str | int]]) -> Iterator[tuple[str, float, int]]:
    """Агрегує оцінки за предметами й видає середній бал та кількість записів."""
    grades_by_subject: dict[str, list[int]] = defaultdict(list)
    for record in records:
        grades_by_subject[str(record["subject"])].append(int(record["grade"]))
    for subject in sorted(grades_by_subject):
        grades = grades_by_subject[subject]
        yield subject, sum(grades) / len(grades), len(grades)


def main() -> None:
    parse_stats: dict[str, int] = {}
    pipeline = format_output(
        filter_passed(
            parse_records(filter_empty(data_source(SAMPLE_DATA)), parse_stats),
            min_grade=75,
        )
    )
    print("=== Результати (>= 75 балів) ===")
    for line in pipeline:
        print(line)
    print(f"Пропущено порожніх рядків: {sum(not row.strip() for row in SAMPLE_DATA)}")
    print(f"Некоректні записи: {parse_stats}")

    average_stats: dict[str, int] = {}
    records = parse_records(filter_empty(data_source(SAMPLE_DATA)), average_stats)
    print("\n=== Середній бал по предметах ===")
    for subject, average, count in subject_averages(records):
        print(f"  {subject}: {average:.1f} (з {count} оцінок)")
    print(f"Перевірка другого потоку: некоректні записи {average_stats}")


if __name__ == "__main__":
    main()
