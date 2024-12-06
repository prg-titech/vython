import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
from utils import log

def make_scatter_plot(data, output_path):
    log("Creating scatter plot")
    x_values, y_values = zip(*data)
    plt.scatter(x_values, y_values)
    plt.yscale('log', base=2)
    plt.title('Relation between Number of version and Vython/Python ratio')
    plt.xlabel('Number of version the value has')
    plt.ylabel('Vython/Python Ratio')
    plt.savefig(os.path.join(output_path, 'scatter_plot.png'))
    plt.show()

def make_refined_bar_graph(evaluation_data, comparision_strategy, output_path):
    log("Creating refined bar graph")

    categories = []
    sem_datas = []
    bar_datas = []
    num_evaluated_file = len(evaluation_data)

    match comparision_strategy:
        case "all":
            color_dict = {"python": "green",
                        "vython": "red",
                        "vt-init": "blue",
                        "vt-prop": "orange",
                        "wrap-primitive": "purple"}
            show_order = ["python","wrap-primitive","vt-init","vt-prop","vython"]
        case "v&p":
            color_dict = {"python": "green",
                        "vython": "red"}
            show_order = ["python","vython"]
        case "test":
            color_dict = {"python": "green",
                        "test": "red"}
            show_order = ["python","test"]

    for i in range(num_evaluated_file):
        sem_datas_per_file = dict()
        bar_datas_per_file = dict()
        evaluation_data_per_file = evaluation_data[i]
        category = evaluation_data_per_file[0]
        categories.append(category)


        execution_times_dict = evaluation_data_per_file[1]
        for transpile_mode in execution_times_dict:
            sem_datas_per_file[transpile_mode] = []
            bar_datas_per_file[transpile_mode] = []
        for transpile_mode in execution_times_dict:
            avg_execution_time = execution_times_dict[transpile_mode][0]
            sem_execution_time = execution_times_dict[transpile_mode][1]
            if(transpile_mode in sem_datas_per_file):
                sem_datas_per_file[transpile_mode].append(sem_execution_time)
            else:
                sem_datas_per_file[transpile_mode] = [sem_execution_time]
            if(transpile_mode in bar_datas_per_file):
                bar_datas_per_file[transpile_mode].append(avg_execution_time)
            else:
                bar_datas_per_file[transpile_mode] =  [avg_execution_time]

        sem_datas.append(sem_datas_per_file)
        bar_datas.append(bar_datas_per_file)

    (fig, ax1) = plt.subplots()
    x = np.arange(len(categories))
    width = 0.8

    error_bars = []
    t_value = 1.96
    for sem_datas_per_file in sem_datas:
        error_bars_per_file = dict()
        for transpile_mode in sem_datas_per_file:
            error_bar = [t_value * se for se in sem_datas_per_file[transpile_mode]]
            if(transpile_mode in error_bars_per_file):
                error_bars_per_file[transpile_mode].append(error_bar)
            else:
                error_bars_per_file[transpile_mode] = [error_bar]
        error_bars.append(error_bars_per_file)

    
    for i in range(len(bar_datas)):
        file_name = categories[i]
        x_alignment = get_good_x_alignment(width/len(bar_datas[i]),x[i],len(bar_datas[i]))
        for index in range(len(show_order)):
            transpile_mode = show_order[index]
            bar = ax1.bar(x_alignment[index], 
                          bar_datas[i][transpile_mode], 
                          width/len(bar_datas[i]), 
                          yerr=error_bars[i][transpile_mode], 
                          label=f'{transpile_mode}', 
                          color=color_dict[transpile_mode])

    ax1.set_xlabel('Number of version the value has')
    ax1.set_ylabel('average total run time(s)')
    ax1.set_title('Execution Time')
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories)
    
    custom_legend = [plt.Line2D([0], [0], color=color, lw=4) for index, (transpile_mode,color) in enumerate(color_dict.items())]
    custom_label = [transpile_mode for index, (transpile_mode,color) in enumerate(color_dict.items())]
    ax1.legend(custom_legend, custom_label, loc='upper left')

    plt.savefig(os.path.join(output_path, 'refined_bar_graph.pdf'),format='pdf')
    plt.show()

def make_bar_graph_about_ratio(evaluation_data, comparision_strategy, output_path):
    log("Creating bar graph")

    file_names = []
    bar_datas = []
    num_evaluated_file = len(evaluation_data)

    match comparision_strategy:
        case "all":
            bar_style_dict = {"wrap-primitive": ["purple",'xxx','d'],
                               "vt-init": ["blue",'x','x'],
                               "vt-prop": ["orange",'xx','s'],
                               "vython": ["red",'++','o'],}
            transpile_modes = ["wrap-primitive","vt-init","vt-prop","vython"]
        case "v&p":
            bar_style_dict = {"vython": ["red",'x','o']}
            transpile_modes = ["vython"]
        case "test":
            bar_style_dict = {"test": ["red",'x','o']}
            transpile_modes = ["test"]

    for i in range(num_evaluated_file):
        bar_datas_per_file = dict()
        evaluation_data_per_file = evaluation_data[num_evaluated_file-i-1]
        file_name = evaluation_data_per_file[0]
        file_names.append(file_name)
        execution_times_dict = evaluation_data_per_file[1]

        for transpile_mode in transpile_modes:
            bar_datas_per_file[transpile_mode] = []
            
        if(execution_times_dict["python"][0] == 0):
            py_avg_time = 0.000001
        else:
            py_avg_time = execution_times_dict["python"][0]

        for transpile_mode in transpile_modes:
            avg_execution_time = execution_times_dict[transpile_mode][0]
            bar_datas_per_file[transpile_mode].append(avg_execution_time / py_avg_time)

        bar_datas.append(bar_datas_per_file)


    # グラフの作成
    (fig, ax1) = plt.subplots(figsize=(8,4))
    x = np.arange(len(file_names))
    width = 0.8


    # 順番が気に食わないので入れかえた
    # print(bar_datas)
    # print(file_names)
    bar_datas[0], bar_datas[1], bar_datas[2] = bar_datas[2], bar_datas[0], bar_datas[1]
    file_names[0], file_names[1], file_names[2] = file_names[2], file_names[0], file_names[1]
    # print(bar_datas)
    # print(file_names)

    for i in range(len(bar_datas)):
        file_name = file_names[i]
        x_alignment = get_good_x_alignment(width/len(bar_datas[i]),x[i],len(bar_datas[i]))
        for index in range(len(transpile_modes)):
            transpile_mode = transpile_modes[index]
            bar = ax1.bar(x_alignment[index],
                          bar_datas[i][transpile_mode],
                          width/len(bar_datas[i]),
                          label=f'{transpile_mode}',
                          edgecolor='black',
                        #   color=bar_style_dict[transpile_mode][0],
                          hatch=bar_style_dict[transpile_mode][1],
                          facecolor='none'
                          )
            
    ax1.set_xlabel('Algorithm', fontsize=16)
    ax1.set_ylabel('Average execution time\nrelative to python', fontsize=16)
    ax1.set_xticks(x)
    ax1.set_xticklabels(file_names)

    plt.axhline(y=1, color='black', linestyle='--', linewidth=1)
    plt.text(x=0.1, y=0.32, s="python\n(baseline)", color='black', fontsize=12, ha='center', transform=ax1.transAxes,
             bbox=dict(edgecolor='black', linestyle='--', facecolor='none', linewidth=1))

    # 軸の目盛りラベルのフォントサイズを設定
    ax1.tick_params(axis='both', which='major', labelsize=16)  # 主要目盛りのフォントサイズを12に設定
    ax1.tick_params(axis='both', which='minor', labelsize=14)  # 副目盛りのフォントサイズを10に設定
    
    custom_legend = [mpatches.Patch(facecolor='none',alpha=0.6,hatch=list[1],edgecolor='black',label=transpile_mode) for index, (transpile_mode,list) in enumerate(bar_style_dict.items())]
    custom_label = ['wrap-literals','mk','join','wf (vython)']
    ax1.legend(custom_legend, custom_label, loc='upper left', fontsize=16)

    # Y軸の範囲を0から始める
    ax1.set_ylim(bottom=0)

    # グラフ全体を上側と右側に動かす
    fig.subplots_adjust(bottom=0.15, left=0.15)

    plt.savefig(os.path.join(output_path, 'bar_graph_about_ratio.pdf'),format='pdf')
    plt.show()

def make_line_graph(evaluation_data, comparision_strategy, output_path):
    log("Creating line graph")

    file_names = []
    line_datas = dict()
    num_evaluated_file = len(evaluation_data)
    
    match comparision_strategy:
        case "all":
            line_style_dict = {"vython": ["red",'-','o'],
                               "vt-init": ["blue",'--','x'],
                               "vt-prop": ["orange",'-.','s'],
                               "wrap-primitive": ["purple",':','d']}
            transpile_modes = ["wrap-primitive","vt-init","vt-prop","vython"]
        case "v&p":
            line_style_dict = {"vython": ["red",'-','o']}
            transpile_modes = ["vython"]
        case "test":
            line_style_dict = {"test": ["red",'-','o']}
            transpile_modes = ["test"]

    for transpile_mode in transpile_modes:
        line_datas[transpile_mode] = []
    
    for i in range(num_evaluated_file):
        evaluation_data_per_file = evaluation_data[i]
        evaluation_times_dict = evaluation_data_per_file[1]
        if(evaluation_times_dict["python"][0] == 0):
            py_avg_time = 0.000001
        else:
            py_avg_time = evaluation_times_dict["python"][0]
        file_names.append(evaluation_data_per_file[0])

        for transpile_mode in transpile_modes:
            line_datas[transpile_mode].append(evaluation_times_dict[transpile_mode][0] / py_avg_time)

    (fig, ax1) = plt.subplots(figsize=(8,4))
    x = np.arange(len(file_names))

    for transpile_mode in transpile_modes:
        line = ax1.plot(x, 
                        line_datas[transpile_mode], 
                        color=line_style_dict[transpile_mode][0],
                        linestyle=line_style_dict[transpile_mode][1],
                        label=f'{transpile_mode}',
                        marker=line_style_dict[transpile_mode][2])

    # 軸とグラフの説明
    ax1.set_xlabel('Number of entries in a version table', fontsize=16)
    ax1.set_ylabel('Average execution time\nrelative to python', fontsize=16)
    # ax1.set_title('Change of Ratio in Average Execution Time to Python\nrelative to the number of version handled', fontsize=16)
    ax1.set_xticks(x)
    ax1.set_xticklabels(file_names)

    # 軸の目盛りラベルのフォントサイズを設定
    ax1.tick_params(axis='both', which='major', labelsize=16)  # 主要目盛りのフォントサイズを12に設定
    ax1.tick_params(axis='both', which='minor', labelsize=14)  # 副目盛りのフォントサイズを10に設定


    lines,labels = ax1.get_legend_handles_labels()
    ax1.legend(lines, labels, loc='upper left', fontsize=16)

    # Y軸の範囲を0から始める
    ax1.set_ylim(bottom=0)

    # グラフ全体を上側と右側に動かす
    fig.subplots_adjust(bottom=0.15, left=0.15)
    
    plt.savefig(os.path.join(output_path, 'line_graph.pdf'),format='pdf')
    plt.show()

def get_good_x_alignment(width, x, size):
    result = []
    half = size / 2
    for i in range(size):
        cx = x - (width / 2) + (-half + 1 + i) * width
        result.append(cx)

    return result