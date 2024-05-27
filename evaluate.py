import time
import csv
import sys
from src.interpreter.compiler import Compiler as IC
from src.transpiler.compiler import Compiler as TC

def run():
    # 入力
    input_array = input().split()
    mode = input_array[0]
    file_path = input_array[1]
    count = int(input_array[2])

    # ファイルの読み込み
    try:
        with open(file_path, "r") as file:
            code = file.read()
    except FileNotFoundError:
        print(f"The specified file '{file_path}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while opening the file: {e}")
        sys.exit(1)

    result = []
    if mode == "i":
        interpreter = IC(code, False)
        for i in range(count):
            result.append(interpreter.evaluate_time())

    with open('execution_time.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # ヘッダー行を書き出す
        csv_writer.writerow(['Program', 'Execution Time'])
        # 実行時間を書き出す
        for e in result:
            csv_writer.writerow(['sample_program', "{:.6f}".format(e["parse"]) , "{:.6f}".format(e["compile_to_ir"]), "{:.6f}".format(e["execute"])])

run()
