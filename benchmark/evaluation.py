import csv
import os
import sys

from utils import file_category_name, log
from src.interpreter.compiler import Compiler as IC
from src.transpiler.compiler import Compiler as TC
from plotting import make_refined_bar_graph, make_scatter_plot
import numpy as np

def evaluate_transpiler(evaluate_mode, transpile_mode, code, count, csv_writer):
    log(f"Evaluating transpiler with transpile_mode={transpile_mode}")
    transpiler = TC(code, transpile_mode, False)
    avg_t_parse = avg_t_transpile = avg_t_unparse = avg_t_execute = 0
    execution_times = []

    if transpile_mode:
        csv_writer.writerow(['UNVERSION_TRANSPILER', 'parse', 'transpile', 'unparse', 'execute'])
    else:
        csv_writer.writerow(['WITHVERSION_TRANSPILER', 'parse', 'transpile', 'unparse', 'execute'])

    for i in range(count):
        result_i = transpiler.evaluate_time(evaluate_mode)
        csv_writer.writerow([f"{result_i['parse']:.6f}" , f"{result_i['transpile']:.6f}", f"{result_i['unparse']:.6f}", f"{result_i['execute']:.6f}"])
        avg_t_parse += result_i["parse"]
        avg_t_transpile += result_i["transpile"]
        avg_t_unparse += result_i["unparse"]
        avg_t_execute += result_i["execute"]
        execution_times.append(result_i['execute'])
    
    avg_t_parse /= count
    avg_t_transpile /= count
    avg_t_unparse /= count
    avg_t_execute /= count
    csv_writer.writerow(['AVG_TRANSPIER', f"{avg_t_parse:.6f}", f"{avg_t_transpile:.6f}", f"{avg_t_unparse:.6f}", f"{avg_t_execute:.6f}"])

    std_dev = np.std(execution_times)
    sem = std_dev / np.sqrt(count)

    log(f"Completed transpiler evaluation: avg_execute_time={avg_t_execute:.6f}, sem={sem:.6f}")
    return (avg_t_execute, sem)

def evaluate_interpreter(mode, code, count, csv_writer):
    log("Evaluating interpreter")
    interpreter = IC(code, False)
    avg_i_parse = avg_i_ir = avg_i_execute = 0

    csv_writer.writerow(['INTERPRETER', 'parse', 'compile_to_ir', 'execute'])

    for i in range(count):
        result_i = interpreter.evaluate_time()
        csv_writer.writerow([f"{result_i['parse']:.6f}" , f"{result_i['compile_to_ir']:.6f}", f"{result_i['execute']:.6f}"])
        avg_i_parse += result_i["parse"]
        avg_i_ir += result_i["compile_to_ir"]
        avg_i_execute += result_i["execute"]
    
    avg_i_parse /= count
    avg_i_ir /= count
    avg_i_execute /= count
    csv_writer.writerow(['AVG_INTERPRETER', f"{avg_i_parse:.6f}", f"{avg_i_ir:.6f}", f"{avg_i_execute:.6f}"])

    log(f"Completed interpreter evaluation: avg_execute_time={avg_i_execute:.6f}")

def evaluate_files(file_paths, mode, count, result_path):
    data_category = []
    data_execution_time_with_version = []
    data_execution_time_un_version = []
    data_sem_with_version = []
    data_sem_un_version = []

    with open(os.path.join(result_path, 'execution_time.csv'), 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        for file_path in file_paths:
            data_category.append(file_category_name(file_path))
            try:
                with open(file_path, "r") as file:
                    code = file.read()
            except FileNotFoundError:
                log(f"The specified file '{file_path}' was not found.")
                sys.exit(1)
            except Exception as e:
                log(f"An error occurred while opening the file: {e}")
                sys.exit(1)

            csv_writer.writerow(['Program', file_path, ': Execution Time in', mode])
            csv_writer.writerow([])

            match mode:
                case "nor-i":
                    evaluate_interpreter(None, code, count, csv_writer)
                case "nor-t" | "gen-t":
                    x = evaluate_transpiler(mode, True, code, count, csv_writer)
                    data_execution_time_un_version.append(x[0])
                    data_sem_un_version.append(x[1])
                    y = evaluate_transpiler(mode, False, code, count, csv_writer)
                    data_execution_time_with_version.append(y[0])
                    data_sem_with_version.append(y[1])

            csv_writer.writerow([])
            csv_writer.writerow([])

            log(f"Evaluated: {file_path}")

    data_with_un_ratio = [data_execution_time_with_version[i] / data_execution_time_un_version[i] for i in range(len(data_execution_time_with_version))]
    make_refined_bar_graph(data_category, data_execution_time_un_version, data_execution_time_with_version, data_with_un_ratio, data_sem_un_version, data_sem_with_version, result_path)
    if mode == "gen-t":
        make_scatter_plot(list(zip(data_category, data_with_un_ratio)), result_path)
