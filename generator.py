import argparse
import csv
import os
import random
import string
from dataclasses import dataclass
from typing import List


@dataclass
class CodeGenerator:
    length: int
    use_lowercase: bool = True
    use_uppercase: bool = False
    use_digits: bool = False

    def __post_init__(self):
        chars = ""
        if self.use_lowercase:
            chars += string.ascii_lowercase
        if self.use_uppercase:
            chars += string.ascii_uppercase
        if self.use_digits:
            chars += string.digits
        if not chars:
            raise ValueError("少なくとも1種類の文字を選択してください。")
        self._chars = chars

    def generate_one(self) -> str:
        return "".join(random.choices(self._chars, k=self.length))

    def generate_many(self, count: int) -> List[str]:
        codes = set()
        while len(codes) < count:
            codes.add(self.generate_one())
        return list(codes)


def write_csv(path: str, codes: List[str], with_index: bool = False) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    headers = ["index", "code"] if with_index else ["code"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        if with_index:
            for i, c in enumerate(codes, start=1):
                writer.writerow([i, c])
        else:
            for c in codes:
                writer.writerow([c])


def main():
    parser = argparse.ArgumentParser(
        description="ランダムコード生成（ターミナル/CSV出力対応）"
    )
    parser.add_argument("--count", type=int, default=10, help="生成個数")
    parser.add_argument("--length", type=int, default=6, help="コード長")
    parser.add_argument("--lower", action="store_true", help="小文字を使用（既定ON）")
    parser.add_argument("--no-lower", action="store_true", help="小文字を使わない")
    parser.add_argument("--upper", action="store_true", help="大文字を使用")
    parser.add_argument("--digits", action="store_true", help="数字を使用")
    parser.add_argument("--seed", type=int, help="乱数シード（再現用）")
    parser.add_argument(
        "--out",
        choices=["terminal", "csv"],
        default="terminal",
        help="出力先（既定: terminal）",
    )
    parser.add_argument("--csv-path", type=str, default="codes.csv", help="CSV保存先パス")
    parser.add_argument("--with-index", action="store_true", help="CSV/表示にインデックス列を付与")

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    use_lower = not args.no_lower if (args.lower or args.no_lower) else True
    gen = CodeGenerator(
        length=args.length,
        use_lowercase=use_lower,
        use_uppercase=args.upper,
        use_digits=args.digits,
    )

    codes = gen.generate_many(args.count)

    if args.out == "terminal":
        if args.with_index:
            for i, c in enumerate(codes, start=1):
                print(f"{i},{c}")
        else:
            print("\n".join(codes))
    else:
        write_csv(args.csv_path, codes, with_index=args.with_index)
        print(f"CSVを書き出しました: {args.csv_path}")


if __name__ == "__main__":
    main()
