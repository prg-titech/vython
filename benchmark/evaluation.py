import csv
import os
import sys

from utils import file_category_name, log
from src.interpreter.compiler import Compiler as IC
from src.transpiler.compiler import Compiler as TC
from plotting import make_refined_bar_graph, make_scatter_plot
from benchmark_settings import BenchmarkSettings
import numpy as np

def evaluate_transpiler(benchmark_target, comparison_strategy, code, count, csv_writer):

    match comparison_strategy:
        case "all":
            transpile_modes = ["python","wrap-primitive","vt-init","vt-prop","vython"]
        case "v&p":
            transpile_modes = ["python","vython"]
        case _:
            transpile_modes = []

    # この関数が返すオブジェクト
    result = dict()

    for transpile_mode in transpile_modes:
        log(f"Evaluating transpiler with transpile_mode={transpile_mode}")
        transpiler = TC(code, transpile_mode)
        avg_t_parse = avg_t_transpile = avg_t_unparse = avg_t_execute = 0
        execution_times = []

        csv_writer.writerow(['transpile_mode = ' + transpile_mode])
        csv_writer.writerow(['parse', 'transpile', 'unparse', 'execute'])

        for i in range(count):
            evaluate_times = transpiler.evaluate_time(benchmark_target)
            csv_writer.writerow([f"{evaluate_times['parse']:.6f}" , f"{evaluate_times['transpile']:.6f}", f"{evaluate_times['unparse']:.6f}", f"{evaluate_times['execute']:.6f}"])
            avg_t_parse += evaluate_times["parse"]
            avg_t_transpile += evaluate_times["transpile"]
            avg_t_unparse += evaluate_times["unparse"]
            avg_t_execute += evaluate_times["execute"]
            execution_times.append(evaluate_times['execute'])
    
        avg_t_parse /= count
        avg_t_transpile /= count
        avg_t_unparse /= count
        avg_t_execute /= count
        csv_writer.writerow(['AVG', f"{avg_t_parse:.6f}", f"{avg_t_transpile:.6f}", f"{avg_t_unparse:.6f}", f"{avg_t_execute:.6f}"])

        std_dev = np.std(execution_times)
        sem = std_dev / np.sqrt(count)

        log(f"Completed transpiler evaluation: avg_execute_time={avg_t_execute:.6f}, sem={sem:.6f}")

        result[transpile_mode] = (avg_t_execute, sem)

    return result

def evaluate_transpiler_only_execution(benchmark_target, comparison_strategy, code, count, csv_writer):
    match comparison_strategy:
        case "all":
            transpile_modes = ["python","wrap-primitive","vt-init","vt-prop","vython"]
        case "v&p":
            transpile_modes = ["python","vython"]
        case _:
            transpile_modes = []

    # この関数が返すオブジェクト
    result = dict()

    for transpile_mode in transpile_modes:
        log(f"Evaluating transpiler with transpile_mode={transpile_mode}")
        transpiler = TC(code, transpile_mode)
        transpiler.parse()
        transpiler.transpile()
        transpiler.unparse()

        avg_t_execute = 0
        execution_times = []

        csv_writer.writerow(['Execution Time in transpile_mode = ' + transpile_mode])

        for i in range(count):
            execution_time = transpiler.execute_for_evaluate(benchmark_target)
            csv_writer.writerow([f"{execution_time:.6f}"])
            avg_t_execute += execution_time
            execution_times.append(execution_time)
    
        avg_t_execute /= count
        csv_writer.writerow(['AVG', f"{avg_t_execute:.6f}"])

        std_dev = np.std(execution_times)
        sem = std_dev / np.sqrt(count)

        log(f"Completed transpiler evaluation: avg_execute_time={avg_t_execute:.6f}, sem={sem:.6f}")

        result[transpile_mode] = (avg_t_execute, sem)

    return result

def evaluate_interpreter(code, count, csv_writer):
    log("Evaluating interpreter")
    interpreter = IC(code, False)
    avg_i_parse = avg_i_ir = avg_i_execute = 0
    execution_times = []

    csv_writer.writerow(['INTERPRETER', 'parse', 'compile_to_ir', 'execute'])

    for i in range(count):
        evaluate_times = interpreter.evaluate_time()
        csv_writer.writerow([f"{evaluate_times['parse']:.6f}" , f"{evaluate_times['compile_to_ir']:.6f}", f"{evaluate_times['execute']:.6f}"])
        avg_i_parse += evaluate_times["parse"]
        avg_i_ir += evaluate_times["compile_to_ir"]
        avg_i_execute += evaluate_times["execute"]
        execution_times.append(evaluate_times['execute'])
    
    avg_i_parse /= count
    avg_i_ir /= count
    avg_i_execute /= count
    csv_writer.writerow(['AVG', f"{avg_i_parse:.6f}", f"{avg_i_ir:.6f}", f"{avg_i_execute:.6f}"])

    std_dev = np.std(execution_times)
    sem = std_dev / np.sqrt(count)

    log(f"Completed interpreter evaluation: avg_execute_time={avg_i_execute:.6f}")

    return (avg_i_execute, sem)

def evaluate_files(file_paths, settings, result_path):
    benchmark_processor = settings.processor
    num_iterations = settings.num_iterations

    data_category = []
    data_execution_time = []

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

            csv_writer.writerow(['Program', file_path, ': Execution Time in', benchmark_processor])
            csv_writer.writerow([])

            match benchmark_processor:
                case "interpreter":
                    execution_time_dict = evaluate_interpreter(code, num_iterations, csv_writer)
                case "transpiler":
                    comparison_strategy = settings.comparison_strategy
                    benchmark_target = settings.benchmark_target
                    execution_time_dict = evaluate_transpiler_only_execution(benchmark_target, comparison_strategy, code, num_iterations, csv_writer)
            
            data_execution_time.append(execution_time_dict)

            csv_writer.writerow([])
            csv_writer.writerow([])

            log(f"Evaluated: {file_path}")


    return list(zip(data_category,data_execution_time))

