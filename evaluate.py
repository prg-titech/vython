import time
import csv
import sys
import os
import glob
import matplotlib.pyplot as plt
from src.interpreter.compiler import Compiler as IC
from src.transpiler.compiler import Compiler as TC

# 出力の切り捨て桁数
floor_num = "{:.6f}"

def evaluate_transpiler(transpile_mode, code, count, csv_writer):
    # トランスパイラインスタンスの作成と各種変数の設定
    transpiler = TC(code, transpile_mode, False)
    avg_t_parse = 0
    avg_t_transpile = 0
    avg_t_unparse = 0
    avg_t_execute = 0

    # 説明情報の出力
    if(transpile_mode):
        csv_writer.writerow(['UNVERSION_TRANSPILER', 'parse', 'transpile', 'unparse', 'execute'])
    else:
        csv_writer.writerow(['WITHVERSION_TRANSPILER', 'parse', 'transpile', 'unparse', 'execute'])

    # 実行回数分、実行し、結果を実行毎に出力
    for i in range(count):
        # 実行
        result_i = transpiler.evaluate_time()
        # 結果を出力
        csv_writer.writerow([floor_num.format(result_i["parse"]) , floor_num.format(result_i["transpile"]), floor_num.format(result_i["unparse"]), floor_num.format(result_i["execute"])])

        # 各種変数の更新
        avg_t_parse += result_i["parse"]
        avg_t_transpile += result_i["transpile"]
        avg_t_unparse += result_i["unparse"]
        avg_t_execute += result_i["execute"]
    
    # 平均の出力
    avg_t_parse /= count
    avg_t_transpile /= count
    avg_t_unparse /= count
    avg_t_execute /= count
    csv_writer.writerow(['AVG_TRANSPIER', floor_num.format(avg_t_parse), floor_num.format(avg_t_transpile), floor_num.format(avg_t_unparse), floor_num.format(avg_t_execute)])

    # 実行時間の平均だけ返す
    return avg_t_execute

def evaluate_interpreter(mode, code, count, csv_writer):
    # インタプリタインスタンスの作成と各種変数の設定
    interpreter = IC(code, False)
    avg_i_parse = 0
    avg_i_ir = 0
    avg_i_execute = 0

    # 説明情報の出力
    csv_writer.writerow(['INTERPRETER', 'parse', 'compile_to_ir', 'execute'])

    # 実行回数分、実行し、結果を実行毎に出力
    for i in range(count):
        # 実行
        result_i = interpreter.evaluate_time()
        # 結果を出力
        csv_writer.writerow([floor_num.format(result_i["parse"]) , floor_num.format(result_i["compile_to_ir"]), floor_num.format(result_i["execute"])])

        # 各種変数の更新
        avg_i_parse += result_i["parse"]
        avg_i_ir += result_i["compile_to_ir"]
        avg_i_execute += result_i["execute"]
    
    # 平均の計算と出力
    avg_i_parse /= count
    avg_i_ir /= count
    avg_i_execute /= count
    csv_writer.writerow(['AVG_INTERPRETER', floor_num.format(avg_i_parse), floor_num.format(avg_i_ir), floor_num.format(avg_i_execute)])

def get_file_path(folder_path):
    file_paths = glob.glob(os.path.join(folder_path, '*'))
    file_paths = [path for path in file_paths if os.path.isfile(path)]
    return file_paths

def make_graph(data):
    # データセットを分割
    x_values, y_values = zip(*data)

    # 散布図を作成
    plt.scatter(x_values, y_values)

    # グラフのタイトルとラベルを設定
    plt.title('Scatter Plot')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')

    # グラフをファイルとして保存
    # plt.savefig('scatter_plot.png')  # ファイル名は 'scatter_plot.png'

    # グラフを表示
    plt.show()

def run():
    # 入力
    # 実行モード フォルダパス 実行回数
    input_array = input().split()
    mode = input_array[0]
    folder_path = input_array[1]
    count = int(input_array[2])

    # フォルダ直下の全てのファイルのパスを取得
    file_paths = get_file_path(folder_path)

    # グラフに表示するデータを格納する配列
    data = []

    with open('execution_time.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # ファイル数分以下を実行
        for file_path in file_paths:
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

            # 説明情報の出力
            csv_writer.writerow(['Program',  file_path, ': Execution Time in', mode])
            csv_writer.writerow([])

            # 評価モードに従い、コードを実行し、評価結果を出力
            match mode:
                case "i":
                    evaluate_interpreter(None, code, count, csv_writer)
                case "t":
                    # unversion
                    x = evaluate_transpiler(True, code, count, csv_writer)
                    # with version
                    y = evaluate_transpiler(False, code, count, csv_writer)
                    data.append([x,y])
                case "both":
                    evaluate_interpreter(None, code, count, csv_writer)
                    # unversion
                    evaluate_transpiler(True, code, count, csv_writer)
                    # with version
                    evaluate_transpiler(False, code, count, csv_writer)

            csv_writer.writerow([])
            csv_writer.writerow([])

    # グラフの描画
    make_graph(data)

run()
