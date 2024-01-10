import os
from src.parser import parser

def test_parser(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            filepath = os.path.join(directory, filename)
            output_filepath = os.path.join(directory, f"{os.path.splitext(filename)[0]}_parser.output")
            error_occurred = False  # 各ファイルごとのエラーチェック

            with open(filepath, 'r') as file, open(output_filepath, 'w') as output_file:
                test_string = file.read()
                output_file.write(f"Testing Parser with {filename}...\n")

                try:
                    ast = parser.parse(test_string)
                    output_file.write(str(ast) + '\n')
                except Exception as e:
                    error_occurred = True
                    output_file.write(f"Error: {e}\n")

                output_file.write("\nParsing completed.\n")

            # 成功/失敗メッセージの出力
            if not error_occurred:
                print(f"✓ Parser test passed for {filename}")
            else:
                print(f"𐄂 Parser test failed for {filename}")

# テストファイルが保存されているディレクトリを指定
test_directory = "test/sample"
test_parser(test_directory)
