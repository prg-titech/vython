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

def make_bar_graph(categories, values, output_path):
    log("Creating bar graph")
    plt.bar(categories, values)
    plt.title('Measurement of the overhead of execution')
    plt.xlabel('Number of version the value has')
    plt.ylabel('total run time')
    plt.savefig(os.path.join(output_path, 'bar_graph.png'))
    plt.show()

def make_refined_bar_graph(categories, bar_data1, bar_data2, line_data, sem_data1, sem_data2, output_path):
    log("Creating refined bar graph")
    (fig, ax1) = plt.subplots()
    x = np.arange(len(categories))
    width = 0.35

    t_value = 1.96
    error_bars_1 = [t_value * se for se in sem_data1]
    error_bars_2 = [t_value * se for se in sem_data2]

    bars1 = ax1.bar(x - width/2, bar_data1, width, yerr=error_bars_1, label='Python Execution Time(s)')
    bars2 = ax1.bar(x + width/2, bar_data2, width, yerr=error_bars_2, label='Vython Execution Time(s)')

    ax1.set_xlabel('Number of version the value has')
    ax1.set_ylabel('average total run time(s)')
    ax1.set_title('Execution Time and Vython/Python Ratio')
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Vython/Python Ratio')
    line = ax2.plot(x, line_data, color='tab:red', label='Vython/Python Ratio', marker='o')

    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')

    plt.savefig(os.path.join(output_path, 'refined_bar_graph.png'))
    plt.show()
