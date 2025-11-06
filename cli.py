import argparse
import csv
import sys
from pathlib import Path
from generator import CodeGenerator
from duplicate_checker import load_codes_from_csv, find_duplicates  # ← 修正


# --- CSV書き出しヘルパー ---
def write_csv(path: Path, codes: list[str], *, with_index: bool, header: bool, encoding: str = "utf-8") -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding=encoding) as f:
        writer = csv.writer(f)
        if header:
            writer.writerow(["index", "code"] if with_index else ["code"])
        if with_index:
            for i, c in enumerate(codes, start=1):
                writer.writerow([i, c])
        else:
            for c in codes:
                writer.writerow([c])


# --- 対話式コード生成 ---
def run_generate_interactive():
    # 16進モードの選択
    use_hex = input("16進数（0-9, a-f のみ）で生成しますか？ (y/n): ").strip().lower() == "y"
    # 入力
    length = int(input("コードの文字数を入力してください（例: 6）: "))
    count = int(input("生成するコード数を入力してください（例: 20）: "))
    
    if use_hex:
        hex_uppercase = input("A-F の大文字で出力しますか？ (y/n): ").strip().lower() == "y"
        generator = CodeGenerator(
            length=length,
            use_hex=True,
            hex_uppercase=hex_uppercase,
        )
    else:
        use_lowercase = input("小文字アルファベットを使いますか？ (y/n): ").strip().lower() == "y"
        use_uppercase = input("大文字アルファベットを使いますか？ (y/n): ").strip().lower() == "y"
        use_digits = input("数字を使いますか？ (y/n): ").strip().lower() == "y"

        # 全て n のときのフォールバック（エラーにせず小文字を既定）
        if not any([use_lowercase, use_uppercase, use_digits]):
            print("※ いずれも未選択のため、小文字のみで生成します。")
            use_lowercase = True

        generator = CodeGenerator(
            length=length,
            use_lowercase=use_lowercase,
            use_uppercase=use_uppercase,
            use_digits=use_digits,
        )

    # 生成
    codes = generator.generate_many(count)

    # 出力先選択
    to_csv = input("CSVに保存しますか？ (y/n): ").strip().lower() == "y"
    if to_csv:
        default_path = Path.cwd() / "codes.csv"
        path_str = input(f"保存先パスを入力してください（既定: {default_path}）: ").strip()
        path = Path(path_str) if path_str else default_path

        with_index = input("インデックス列を付けますか？ (y/n): ").strip().lower() == "y"
        header = input("ヘッダー行を出力しますか？ (y/n): ").strip().lower() == "y"
        encoding = input("エンコーディング（既定: utf-8）: ").strip() or "utf-8"

        try:
            write_csv(path, codes, with_index=with_index, header=header, encoding=encoding)
            print(f"\n✅ CSVを書き出しました: {path}")
        except Exception as e:
            print(f"\n❌ 書き出しに失敗しました: {e}")
            sys.exit(2)
    else:
        # 端末表示
        with_index = input("表示にインデックスを付けますか？ (y/n): ").strip().lower() == "y"
        print("\n✅ 生成されたコード一覧:")
        if with_index:
            for i, c in enumerate(codes, start=1):
                print(f"{i}, {c}")
        else:
            print("\n".join(codes))


# --- CSV重複チェック ---
def run_check(args):
    try:
        codes = load_codes_from_csv(
            path=Path(args.filename),
            column=args.column,
            has_header=not args.no_header,
            encoding=args.encoding,
            delimiter=args.delimiter,
            to_lower=args.ignore_case,
        )
    except Exception as e:
        print(f"❌ 読み込みエラー: {e}")
        sys.exit(2)

    duplicates = find_duplicates(codes)  # ← ここもOK
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
