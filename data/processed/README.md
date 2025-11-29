# Data Processing

## Files Description

### `final_results_to_analyze.xlsx`
Обработанный датасет, готовый для статистического анализа A/B теста.

**Размер:** 401,260 строк пользователей (по датам и группам)

**Столбцы:**
- `clientid` — уникальный идентификатор пользователя
- `dt` — дата события (YYYY-MM-DD)
- `abgroup` — группа A/B теста (control/test)
- `views` — количество просмотров рекламы
- `clicks` — количество кликов
- `adds` — количество добавлений в корзину
- `orders` — количество заказов
- `revenue` — выручка в валюте (рубли)

### `data_raw_combined.csv`
Объединённый сырой датасет всех 21 CSV файлов. Создаётся скриптом `scripts/combine_csv_files.py`.

**Размер:** 1,048,575 строк событий

**Столбцы:**
- `clientid` — пользователь
- `dt` — дата
- `eventtype` — тип события (views, clicks, adds, orders)

## Как использовать

### Для быстрого старта (анализ):
```python
import pandas as pd

# Загрузи обработанный датасет
df = pd.read_excel('final_results_to_analyze.xlsx')
df.head()
```

### Для повторного объединения raw данных:
```bash
python scripts/combine_csv_files.py
```

## Структура данных для A/B теста

Каждая строка — это **один пользователь в один день в одной группе**:

```
clientid | dt       | abgroup | views | clicks | adds | orders | revenue
---------|----------|---------|-------|--------|------|--------|--------
111      | 2024-07-24 | control |   1   |   0    |  0   |   0    |  0.00
112      | 2024-07-24 | test    |   1   |   1    |  1   |   0    |  0.00
113      | 2024-07-24 | control |   0   |   0    |  0   |   0    |  0.00
```

## Примеры анализа

### Статистика по группам:
```python
df.groupby('abgroup').agg({
    'clientid': 'nunique',      # уникальные пользователи
    'adds': 'sum',              # всего добавлений
    'revenue': 'sum'            # всего выручки
})
```

### CR_add (конверсия добавлений):
```python
for group in ['control', 'test']:
    group_data = df[df['abgroup'] == group]
    users_total = group_data['clientid'].nunique()
    users_adds = group_data[group_data['adds'] > 0]['clientid'].nunique()
    cr_add = (users_adds / users_total) * 100
    print(f"{group}: {cr_add:.2f}%")
```

## Примечания

- Данные за период: **24-30 июля 2024** (7 дней)
- Размер теста: **401,260 уникальных пользователей** (50/50 split)
- **90% пользователей не видят рекламу** — это нормально для монетизационного контента
- Для анализа используй `final_results_to_analyze.xlsx` — это оптимально подготовленные данные