import csv
from collections import Counter
from pathlib import Path
from typing import List, Optional, Union

def load_codes_from_csv(
    path: Path,
    column: Union[int, str] = "code",
    has_header: bool = True,
    encoding: str = "utf-8",
    delimiter: str = ",",
    strip_whitespace: bool = True,
    to_lower: bool = False,
    to_upper: bool = False,
) -> List[str]:
    if not path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {path}")

    codes: List[str] = []

    with path.open("r", encoding=encoding, errors="replace", newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        rows = list(reader)

    if not rows:
        return codes

    start_idx = 0
    col_index: Optional[int] = None

    if has_header:
        header = rows[0]
        start_idx = 1
        col_index = header.index(column) if isinstance(column, str) else int(column)
    else:
        col_index = int(column)

    for row in rows[start_idx:]:
        if col_index >= len(row):
            continue
        code = row[col_index].strip() if strip_whitespace else row[col_index]
        if to_lower:
            code = code.lower()
        if to_upper:
            code = code.upper()
        if code:
            codes.append(code)

    return codes

def find_duplicates(codes: List[str]) -> List[tuple[str, int]]:
    cnt = Counter(codes)
    return sorted([(code, n) for code, n in cnt.items() if n > 1], key=lambda x: (-x[1], x[0]))
