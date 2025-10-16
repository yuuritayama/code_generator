from generator import CodeGenerator

def main():
    # --- ユーザー入力 ---
    length = int(input("コードの文字数を入力してください（例: 6）: "))
    use_lowercase = input("小文字アルファベットを使いますか？ (y/n): ").lower() == 'y'
    use_uppercase = input("大文字アルファベットを使いますか？ (y/n): ").lower() == 'y'
    use_digits = input("数字を使いますか？ (y/n): ").lower() == 'y'
    count = int(input("生成するコード数を入力してください（例: 20）: "))

    # --- 生成処理 ---
    generator = CodeGenerator(
        length=length,
        use_lowercase=use_lowercase,
        use_uppercase=use_uppercase,
        use_digits=use_digits
    )

    codes = generator.generate_many(count)

    # --- 出力 ---
    print("\n✅ 生成されたコード一覧:")
    for c in codes:
        print(c)

if __name__ == "__main__":
    main()
