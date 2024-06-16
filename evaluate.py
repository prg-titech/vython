import csv
import sys
import os
import glob
import matplotlib.pyplot as plt
import numpy as np
from src.interpreter.compiler import Compiler as IC
from src.transpiler.compiler import Compiler as TC

# 出力の切り捨て桁数
floor_num = "{:.6f}"

# コードを受け取りトランスパイラの評価モードで実行 -> csvに結果を出力し、平均実行時間だけを返す
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

# コードを受け取りインタプリタの評価モードで実行 -> csvに結果を出力し、平均実行時間だけを返す
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

# フォルダーパス直下の全てのファイルのパスのリストを返す
def get_file_path(folder_path):
    file_paths = glob.glob(os.path.join(folder_path, '*'))
    file_paths = [path for path in file_paths if os.path.isfile(path)]
    return file_paths

# 散布図を作成
def make_scatter_plot(data):
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

# with-versionの実行時間をまとめた棒グラフを作成
def make_bar_graph(categories, values):
    # 棒グラフを作成
    plt.bar(categories, values)

    # 説明情報の設定
    plt.title('Measurement of the overhead of execution')
    plt.xlabel('Number of version the value has')
    plt.ylabel('total run time')

    # グラフを表示
    plt.show()

# with/un-versionの実行時間をまとめた棒グラフと、with/unの比を表す折れ線グラフを作成
def make_refined_bar_graph(categories, bar_data1, bar_data2, line_data):
    # プロットの作成
    (fig, ax1) = plt.subplots()

    # X軸の位置
    x = np.arange(len(categories))

    width = 0.35

    # 棒グラフ
    bars1 = ax1.bar(x - width/2, bar_data1, width, label='Python Execution Time(s)')
    bars2 = ax1.bar(x + width/2, bar_data2, width, label='Vython Execution Time(s)')

    # Y軸のラベル
    ax1.set_xlabel('Number of version the value has')
    ax1.set_ylabel('average total run time(s)')
    ax1.set_title('Execution Time and Vython/Python Ratio')
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories)
    # ax1.legend(loc='upper left')

    # 折れ線グラフ用のY軸
    ax2 = ax1.twinx()
    ax2.set_ylabel('Vython/Python Ratio')

    # 折れ線グラフ
    line = ax2.plot(x, line_data, color='tab:red', label='Vython/Python Ratio', marker='o')

    # 凡例をまとめる
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')

    plt.show()

def run():
    # 入力
    # 実行モード フォルダパス 実行回数
    input_array = input().split()
    mode = input_array[0]
    path = input_array[1]
    count = int(input_array[2])

    # pathがファイルを指しているかを確認
    # ファイルパスの場合 -> そのファイルだけを評価
    if os.path.isfile(path):
        file_paths = [path]
    # フォルダパスの場合 -> その直下のファイルを全て評価
    else:
        # フォルダ直下の全てのファイルのパスを取得
        file_paths = get_file_path(path)
        file_paths.sort()

    # グラフに表示するデータを格納する配列
    data_for_scatter_plot = []
    data_category = []
    data_execution_time_with_version = []
    data_execution_time_un_version = []

    # 再帰回数上限の変更
    sys.setrecursionlimit(2100)

    with open('execution_time.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # ファイル数分以下を実行
        for file_path in file_paths:
            data_category.append(file_path[-6:-3])
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
                    data_execution_time_un_version.append(x)
                    # with version
                    y = evaluate_transpiler(False, code, count, csv_writer)
                    data_execution_time_with_version.append(y)
                    data_for_scatter_plot.append([x,y])
                case "both":
                    evaluate_interpreter(None, code, count, csv_writer)
                    # unversion
                    evaluate_transpiler(True, code, count, csv_writer)
                    # with version
                    evaluate_transpiler(False, code, count, csv_writer)

            csv_writer.writerow([])
            csv_writer.writerow([])

            print(f"Evaluated: {file_path}")

    # グラフの描画
    # make_scatter_plot(data_for_scatter_plot)
    # make_bar_graph(data_category, data_execution_time_with_version)
    data_with_un_ratio = []
    for i in range(len(data_execution_time_with_version)):
        data_with_un_ratio.append(data_execution_time_with_version[i]/data_execution_time_un_version[i])
    make_refined_bar_graph(data_category, data_execution_time_un_version, data_execution_time_with_version, data_with_un_ratio)

run()
