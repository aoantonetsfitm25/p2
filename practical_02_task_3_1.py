"""Порівняння list comprehension та generator expression."""

import csv
import sys
import timeit
from pathlib import Path


OUTPUT_DIR = Path(__file__).resolve().parent


def memory_comparison() -> list[dict[str, int | float]]:
    """Порівнює поверхневий розмір списку та генератора для різних N."""
    measurements: list[dict[str, int | float]] = []
    sizes = [1_000, 10_000, 100_000, 1_000_000]

    print("=" * 68)
    print(f"{'N':>12} | {'list (байт)':>14} | {'gen (байт)':>12} | {'Ratio':>8}")
    print("-" * 68)
    for n in sizes:
        data_list = [x**2 for x in range(n)]
        data_gen = (x**2 for x in range(n))
        list_size = sys.getsizeof(data_list)
        gen_size = sys.getsizeof(data_gen)
        ratio = list_size / gen_size
        measurements.append({"n": n, "list_bytes": list_size, "generator_bytes": gen_size, "ratio": ratio})
        print(f"{n:>12,} | {list_size:>14,} | {gen_size:>12,} | {ratio:>7.0f}×")
    print("=" * 68)

    with (OUTPUT_DIR / "benchmark_results.csv").open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["n", "list_bytes", "generator_bytes", "ratio"])
        writer.writeheader()
        writer.writerows(measurements)
    return measurements


def performance_comparison(n: int = 500_000) -> tuple[float, float]:
    """Вимірює сумування квадратів для спискового й генераторного виразів."""
    time_list = timeit.timeit(lambda: sum([x**2 for x in range(n)]), number=5) / 5
    time_gen = timeit.timeit(lambda: sum(x**2 for x in range(n)), number=5) / 5
    print(f"\nsum() для {n:,} елементів (середній час одного запуску, 5 повторів):")
    print(f"  list comprehension: {time_list:.4f} с")
    print(f"  generator expression: {time_gen:.4f} с")
    print(f"  Швидше у цьому запуску: {'список' if time_list < time_gen else 'генератор'}")
    return time_list, time_gen


def practical_usage() -> None:
    """Демонструє generator expression разом зі стандартними функціями."""
    words = [
        "Python", "ітератор", "генератор", "yield", "comprehension",
        "дані", "пам'ять", "ефективність", "конвеєр", "ліниві",
        "обчислення", "протокол", "об'єкт", "клас", "функція",
    ]

    longest = max((word for word in words), key=len)
    all_nonempty = all(word for word in words)
    has_long = any(len(word) > 15 for word in words)
    csv_line = ",".join(word for word in words)
    total_length = sum(len(word) for word in words)
    word_lengths = {word: len(word) for word in words}
    even_squares_sum = sum(number**2 for number in range(1, 101) if number % 2 == 0)

    print("\nВикористання generator expression:")
    print(f"Найдовше слово: '{longest}' ({len(longest)} символів)")
    print(f"Всі слова непорожні: {all_nonempty}")
    print(f"Є слово довше 15 символів: {has_long}")
    print(f"CSV: {csv_line}")
    print(f"Сума довжин: {total_length}")
    print(f"Словник довжин: {word_lengths}")
    print(f"Сума квадратів парних чисел 1–100: {even_squares_sum}")


def main() -> None:
    print(">>> Порівняння використання пам'яті <<<\n")
    memory_comparison()
    print("\n>>> Порівняння продуктивності <<<")
    performance_comparison()
    print("\n>>> Практичне використання generator expression <<<")
    practical_usage()


if __name__ == "__main__":
    main()
