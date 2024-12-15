import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter
import numpy as np
import os
from utils import log

def format_to_power_of_two(x, pos):
    return f"$2^{{{int(x)}}}$"

# Sampleの評価結果を出力するためのグラフ
def make_bar_graph_sample(evaluation_results, output_path):
    log("Creating bar graph")

    # 各バーのデータを記録する辞書の初期化
    bar_datas = []

    # 各バーの描画の設定
    bar_style_dict = {"wrap-primitive": ["purple",'xxx','d'],
                        "vt-init": ["blue",'x','x'],
                        "vt-prop": ["orange",'xx','s'],
                        "vython": ["red",'++','o'],}
    # 索引上で使う名前から、表示のための名前への変換を行う
    name_change_dict = {"vython": "wf (vython)",
                        "vt-init": "mk",
                        "vt-prop": "join",
                        "wrap-primitive": "wrap-literal"}
    # compilation_modesの順序付け
    compilation_modes_order = {"vython": 1,
                            "vt-init": 3,
                            "vt-prop": 2,
                            "wrap-primitive": 4}
    
    # 各ラインの種類を取得する
    compilation_modes = []
    for compilation_mode in evaluation_results[0][1].keys():
        compilation_modes.append(compilation_mode)
    compilation_modes.remove('python')
    compilation_modes = sorted(compilation_modes,
                               key=lambda x: compilation_modes_order[x])

    # 各ラインのデータを成形して、記録
    for evaluation_result in evaluation_results:
        bar_datas_per_file = dict()
        file_name = evaluation_result[0]
        evaluation_times_dict = evaluation_result[1]

        if(evaluation_times_dict["python"][0] == 0):
            py_avg_time = 0.000001
        else:
            py_avg_time = evaluation_times_dict["python"][0]

        for compilation_mode in compilation_modes:
            avg_execution_time = evaluation_times_dict[compilation_mode][0]
            bar_datas_per_file[compilation_mode] = (avg_execution_time / py_avg_time)
        bar_datas.append((file_name, bar_datas_per_file))

    # vython-pythonのratioに従ってデータをsortする
    bar_datas = sorted(bar_datas,
                       key = lambda x: x[1]["vython"])

    # グラフの作成
    (fig, ax1) = plt.subplots(figsize=(8,4))
    x = np.arange(len(evaluation_results))
    width = 0.8

    # compilation_mode毎に棒グラフを描画することで、積み上げ棒グラフを作成
    for compilation_mode in compilation_modes:
        bar_data_per_mode = []
        for bar_data in bar_datas:
            avg_ratio_data_dict = bar_data[1]
            bar_data_per_mode.append(avg_ratio_data_dict[compilation_mode])
        bar = ax1.bar(x,
                          bar_data_per_mode,
                          width,
                          label=name_change_dict[compilation_mode],
                          edgecolor='black',
                          color='white',
                          hatch=bar_style_dict[compilation_mode][1],
                          facecolor='white'
                          )
            
    # 軸とグラフの説明
    ax1.set_xlabel('Algorithm', fontsize=16)
    ax1.set_ylabel('Average execution time\nrelative to python', fontsize=16)
    ax1.set_xticks(x)
    ax1.set_xticklabels([bar_data[0] for bar_data in bar_datas])

    # ベースライン(python) & その説明を描画
    plt.axhline(y=1, color='black', linestyle='--', linewidth=1)
    plt.text(x=0.1, y=0.32, s="python\n(baseline)", color='black', fontsize=12, ha='center', transform=ax1.transAxes,
             bbox=dict(edgecolor='black', linestyle='--', facecolor='none', linewidth=1))

    # 軸の目盛りラベルのフォントサイズを設定
    ax1.tick_params(axis='both', which='major', labelsize=16)  # 主要目盛りのフォントサイズを12に設定
    ax1.tick_params(axis='both', which='minor', labelsize=14)  # 副目盛りのフォントサイズを10に設定
    
    # legendを作成
    bars, labels = ax1.get_legend_handles_labels()
    ax1.legend(bars[:4], labels[:4], loc='upper left', fontsize=16)

    # Y軸の範囲を0から始める
    ax1.set_ylim(bottom=0)

    # グラフ全体を上側と右側に動かす
    fig.subplots_adjust(bottom=0.15, left=0.15)

    # 生成したグラフを保存 & 表示
    plt.savefig(os.path.join(output_path, 'bar_graph_about_ratio.pdf'),format='pdf')
    plt.show()

    log("Created bar graph")

# Scalabilityの評価結果を出力するためのグラフ
def make_line_graph_scalability(evaluation_results, output_path):
    log("Creating line graph")

    # ファイル名に従ってデータをsortする
    evaluation_results = sorted(evaluation_results,
           key=lambda x: int(x[0]))
    
    # 各ラインの描画の設定
    line_style_dict = {"vython": ["red",'-','o'],
                        "vt-init": ["blue",'--','x'],
                        "vt-prop": ["orange",'-.','s'],
                        "wrap-primitive": ["purple",':','d']}
    # 索引上で使う名前から、表示のための名前への変換を行う
    name_change_dict = {"vython": "wf (vython)",
                        "vt-init": "mk",
                        "vt-prop": "join",
                        "wrap-primitive": "wrap-literal"}
    

    # 各ラインの種類を取得する
    compilation_modes = []
    for compilation_mode in evaluation_results[0][1].keys():
        compilation_modes.append(compilation_mode)

    # 各ラインのデータを記録する辞書の初期化
    line_datas = dict()
    for compilation_mode in compilation_modes:
        line_datas[compilation_mode] = []
    
    # 各ラインのデータを成形して、記録
    for evaluation_result_per_file in evaluation_results:
        evaluation_times_dict = evaluation_result_per_file[1]
        if(evaluation_times_dict["python"][0] == 0):
            py_avg_time = 0.000001
        else:
            py_avg_time = evaluation_times_dict["python"][0]

        for compilation_mode in compilation_modes:
            line_datas[compilation_mode].append(evaluation_times_dict[compilation_mode][0] / py_avg_time)

    # 索引のための名前のリストからpythonを削除
    compilation_modes.remove('python')

    # グラフの生成
    (fig, ax1) = plt.subplots(figsize=(8,4))
    x = np.arange(len(evaluation_results))
    # 各ラインの生成
    for compilation_mode in compilation_modes:
        line = ax1.plot(x, 
                        line_datas[compilation_mode], 
                        color=line_style_dict[compilation_mode][0],
                        linestyle=line_style_dict[compilation_mode][1],
                        label=name_change_dict[compilation_mode],
                        marker=line_style_dict[compilation_mode][2])

    # 軸とグラフの説明
    ax1.set_xlabel('Number of entries in a version table', fontsize=16)
    ax1.set_ylabel('Average execution time\nrelative to python', fontsize=16)
    ax1.set_xticks(x)
    ax1.xaxis.set_major_formatter(FuncFormatter(format_to_power_of_two))

    # 軸の目盛りラベルのフォントサイズを設定
    ax1.tick_params(axis='both', which='major', labelsize=16)  # 主要目盛りのフォントサイズを12に設定
    ax1.tick_params(axis='both', which='minor', labelsize=14)  # 副目盛りのフォントサイズを10に設定

    # ベースライン(python) & その説明を描画
    plt.axhline(y=1, color='black', linestyle='--', linewidth=1)
    plt.text(x=0.1, y=0.16, s="python\n(baseline)", color='black', fontsize=12, ha='center', transform=ax1.transAxes,
             bbox=dict(edgecolor='black', linestyle='--', facecolor='none', linewidth=1))

    # legendを描画
    lines,labels = ax1.get_legend_handles_labels()
    ax1.legend(lines, labels, loc='upper left', fontsize=16)

    # Y軸の範囲を0から始める
    ax1.set_ylim(bottom=0)

    # グラフ全体を上側と右側に動かす
    fig.subplots_adjust(bottom=0.15, left=0.15)
    
    # 生成したグラフを保存 & 表示
    plt.savefig(os.path.join(output_path, 'line_graph.pdf'),format='pdf')
    plt.show()

    log("Created line graph")

def get_good_x_alignment(width, x, size):
    result = []
    half = size / 2
    for i in range(size):
        cx = x - (width / 2) + (-half + 1 + i) * width
        result.append(cx)

    return result