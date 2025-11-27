import os
import pandas as pd


def combine_raw_parts(
    input_dir: str = "data/raw",
    output_path: str = "data/processed/data_raw_combined.csv",
    pattern: str = "data_raw_part",
    verbose: bool = True,
) -> None:
    """
    Объединяет несколько CSV-файлов с сырыми данными в один.

    Параметры:
        input_dir  — папка, где лежат файлы data_raw_part*.csv
        output_path — путь к итоговому объединённому CSV
        pattern    — общая часть имени файлов (по умолчанию data_raw_part)
        verbose    — печатать служебные сообщения
    """
    files = sorted(
        f for f in os.listdir(input_dir)
        if f.startswith(pattern) and f.endswith(".csv")
    )

    if not files:
        raise FileNotFoundError(f"В папке {input_dir} не найдено файлов {pattern}*.csv")

    dfs = []
    total_rows = 0

    for fname in files:
        path = os.path.join(input_dir, fname)
        if verbose:
            print(f"Читаю {path} ...")
        df = pd.read_csv(path)
        dfs.append(df)
        total_rows += len(df)

    combined = pd.concat(dfs, ignore_index=True)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    combined.to_csv(output_path, index=False)

    if verbose:
        print(f"Готово. Объединено файлов: {len(files)}")
        print(f"Всего строк: {len(combined)} (ожидалось примерно {total_rows})")
        print(f"Сохранено в: {output_path}")


if __name__ == "__main__":
    combine_raw_parts()
