import matplotlib.pyplot as plt
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

def make_refined_bar_graph(evaluation_data, output_path):

    log("Creating refined bar graph")

    categories = []
    num_bar_type = len(evaluation_data)
    sem_datas = []
    bar_datas = []
    num_evaluated_file = len(evaluation_data)

    color_dict = {"vython": "red",
                  "python": "green",
                  "vt-init": "blue",
                  "vt-synt": "orange",
                  "vt-check": "purple"}

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
        for index, (transpile_mode,value) in enumerate(bar_datas[i].items()):
            bar = ax1.bar(x_alignment[index], bar_datas[i][transpile_mode], width/len(bar_datas[i]), yerr=error_bars[i][transpile_mode], label=f'{transpile_mode}', color = color_dict[transpile_mode])

    ax1.set_xlabel('Number of version the value has')
    ax1.set_ylabel('average total run time(s)')
    ax1.set_title('Execution Time')
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Vython/Python Ratio')

    line_datas = []
    for bar_datas_per_file in bar_datas:
        for p in list(zip(bar_datas_per_file["vython"],bar_datas_per_file["python"])):
            # pythonの実行が早すぎるときがあるので
            if(p[1]==0):
                line_datas.append(p[0]/0.000001)
            else:
                line_datas.append(p[0]/p[1])

    line = ax2.plot(x, line_datas, color='tab:red', label='Vython/Python Ratio', marker='o')
    
    custom_legend = [plt.Line2D([0], [0], color=color, lw=4) for index, (transpile_mode,color) in enumerate(color_dict.items())]
    custom_label = [transpile_mode for index, (transpile_mode,color) in enumerate(color_dict.items())]
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(custom_legend, custom_label, loc='upper left')
    ax2.legend(lines2, labels2, loc='upper right')

    plt.savefig(os.path.join(output_path, 'refined_bar_graph.png'))
    plt.show()

def get_good_x_alignment(width, x, size):
    result = []
    half = size / 2
    for i in range(size):
        cx = x - (width / 2) + (-half + 1 + i) * width
        result.append(cx)

    return result