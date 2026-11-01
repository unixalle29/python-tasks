# python-tasks

Лабы по курсу «Программирование на Python» (edu2u.ru, ПетрГУ).
Короче: тут все задачи по разделам, тесты и линтеры. Без магии и лишних слоёв.

## Что нужно

- [uv](https://docs.astral.sh/uv/)
- Python 3.11 (uv поставит сам)

## Установка

```bash
uv sync                      # всё сразу: библиотеки, pytest, ruff, mypy
uv sync --no-default-groups  # только библиотеки, без тестов и линта
```

## Команды

```bash
uv run pytest                     # все тесты
uv run pytest tests/s01_basics    # тесты одного раздела
uv run ruff check .               # линтер
uv run ruff format --check .      # форматирование
uv run mypy                       # типы
```

## Что где лежит

```
src/python_tasks/
├── s01_basics/      # базовый синтаксис
├── s02_data/        # строки, списки, словари, numpy
├── s03_files/       # файлы, csv, шифрование, поиск
├── s04_science/     # matplotlib, графики, случайные блуждания
├── s05_gui/         # PyQt6
└── s06_opencv/      # OpenCV
tests/               # тесты, структура как у src
```

## Как всё устроено

- Одна задача — один файл: `sXX_.../tNN_short_name.py`.
- Сначала проверка ввода (`parse_*`), потом логика, потом `main()`.
- Тесты лежат зеркально: `tests/sXX_.../test_tNN_short_name.py`.
- Крайние случаи проверяются: пустой ввод, мусор, границы, NaN/Inf.
- Случайность принимается параметром (`random.Random`), чтобы тесты не плавали.
- Запуск задачи:

```bash
uv run python -m python_tasks.s01_basics.t01_leap_year
```

Сейчас в репозитории 6 разделов и 690 тестов. Если что-то непонятно — читай код и тесты, там всё разложено.
