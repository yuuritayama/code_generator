import argparse
import sys
from pathlib import Path
from generator import CodeGenerator
from duplicate_checker import load_codes_from_csv, find_duplicates


# --- 対話式コード生成 ---
def run_generate_interactive():
    length = int(input("コードの文字数を入力してください（例: 6）: "))
    use_lowercase = input("小文字アルファベットを使いますか？ (y/n): ").lower() == 'y'
    use_uppercase = input("大文字アルファベットを使いますか？ (y/n): ").lower() == 'y'
    use_digits = input("数字を使いますか？ (y/n): ").lower() == 'y'
    count = int(input("生成するコード数を入力してください（例: 20）: "))

    generator = CodeGenerator(
        length=length,
        use_lowercase=use_lowercase,
        use_uppercase=use_uppercase,
        use_digits=use_digits
    )

    codes = generator.generate_many(count)
    print("\n✅ 生成されたコード一覧:")
    for c in codes:
        print(c)


# --- CSV重複チェック ---
def run_check(args):
    try:
        codes = load_codes_from_csv(
            path=Path(args.filename),
            column=args.column,
            has_header=not args.no_header,
            encoding=args.encoding,
            delimiter=args.delimiter,
            to_lower=args.ignore_case
        )
    except Exception as e:
        print(f"❌ 読み込みエラー: {e}")
        sys.exit(2)

    duplicates = find_duplicates(codes)
    if duplicates:
        print(f"⚠️ 重複あり: {len(duplicates)}種類")
        for code, n in duplicates:
            print(f"- {code} (count={n})")
        sys.exit(1)
    else:
        print("✅ 重複なし")
        sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="Code Generator & Duplicate Checker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- generate コマンド（対話式）---
    gen_parser = subparsers.add_parser("generate", help="コードを対話式で生成する")
    gen_parser.set_defaults(func=lambda args: run_generate_interactive())

    # --- check コマンド ---
    chk_parser = subparsers.add_parser("check", help="CSV 内の重複をチェックする")
    chk_parser.add_argument("filename", type=str, help="CSVファイル名")
    chk_parser.add_argument("--column", default="code", help="列名または列番号")
    chk_parser.add_argument("--no-header", action="store_true", help="ヘッダーなし")
    chk_parser.add_argument("--encoding", default="utf-8", help="文字エンコーディング")
    chk_parser.add_argument("--delimiter", default=",", help="区切り文字")
    chk_parser.add_argument("--ignore-case", action="store_true", help="大文字小文字を無視")
    chk_parser.set_defaults(func=run_check)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
