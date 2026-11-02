# python-tasks

Лабы по Python, ПетрГУ.

## Установка

```bash
uv sync
```

## Команды

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

## Разделы

- `s01_basics` — базовый синтаксис
- `s02_data` — строки, списки, словари, numpy
- `s03_files` — файлы, csv, шифрование, поиск
- `s04_science` — matplotlib, графики, случайные блуждания
- `s05_gui` — PyQt6
- `s06_opencv` — OpenCV

## Запуск

```bash
uv run python -m python_tasks.s01_basics.t01_leap_year
```
