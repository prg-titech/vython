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

    # 出力の切り捨て桁数
    floor_num = "{:.6f}"

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

    result_i = []
    result_t = []
    interpreter = IC(code, False)
    transpiler = TC(code, False, False)
    if mode == "i":
        for i in range(count):
            result_i.append(interpreter.evaluate_time())
    elif mode == "t":
        for i in range(count):
            result_t.append(transpiler.evaluate_time())
    elif mode == "both":
        for i in range(count):
            result_i.append(interpreter.evaluate_time())
            result_t.append(transpiler.evaluate_time())

    with open('execution_time.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # ヘッダー行を書き出す
        csv_writer.writerow(['Program',  file_path, ': Execution Time in', mode])
        csv_writer.writerow([])

        # 実行時間を書き出す
        csv_writer.writerow(['INTERPRETER', 'parse', 'compile_to_ir', 'execute'])
        avg_i_parse = 0
        avg_i_ir = 0
        avg_i_execute = 0
        for e in result_i:
            csv_writer.writerow([floor_num.format(e["parse"]) , floor_num.format(e["compile_to_ir"]), floor_num.format(e["execute"])])
            avg_i_parse += e["parse"]
            avg_i_ir += e["compile_to_ir"]
            avg_i_execute += e["execute"]
        avg_i_parse /= count
        avg_i_ir /= count
        avg_i_execute /= count
        csv_writer.writerow(['AVG_INTERPRETER', floor_num.format(avg_i_parse), floor_num.format(avg_i_ir), floor_num.format(avg_i_execute)])
        
        csv_writer.writerow([])

        csv_writer.writerow(['TRANSPILER', 'parse', 'transpile', 'unparse', 'execute'])
        avg_t_parse = 0
        avg_t_transpile = 0
        avg_t_unparse = 0
        avg_t_execute = 0
        for e in result_t:
            csv_writer.writerow([floor_num.format(e["parse"]) , floor_num.format(e["transpile"]), floor_num.format(e["unparse"]), floor_num.format(e["execute"])])
            avg_t_parse += e["parse"]
            avg_t_transpile += e["transpile"]
            avg_t_unparse += e["unparse"]
            avg_t_execute += e["execute"]
        avg_t_parse /= count
        avg_t_transpile /= count
        avg_t_unparse /= count
        avg_t_execute /= count
        csv_writer.writerow(['AVG_TRANSPIER', floor_num.format(avg_t_parse), floor_num.format(avg_t_transpile), floor_num.format(avg_t_unparse), floor_num.format(avg_i_execute)])

run()
