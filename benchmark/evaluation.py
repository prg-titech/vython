import sys

from utils import file_category_name, log
from src.transpiler.compiler import Compiler as TC
import numpy as np

def evaluate_transpiler(code, comparison_strategy, optimize_pure_function, num_iteration):
    match comparison_strategy:
        case "all":
            transpile_modes = ["python","wrap-primitive","vt-init","vt-prop","vython"]
        case "v&p":
            transpile_modes = ["python","vython"]
        case _:
            log(f"Undefined option of comparison_strategy: {comparison_strategy}")
            sys.exit(1)

    # {"{transpile_mode}": (avg, sem),..}
    execution_time_data = dict()

    for transpile_mode in transpile_modes:
        log(f"Evaluating with transpile_mode={transpile_mode}")

        transpiler = TC(code, transpile_mode, lazy_wrap=optimize_pure_function)
        transpiler.parse()
        transpiler.collect_classes(True)
        transpiler.transpile()
        transpiler.unparse()
        transpiler.execute()
        name_dict = transpiler.get_dict()
        exec(f"exe_time = main_pure({num_iteration})", name_dict)
        name_dict_after_execution = name_dict
        execution_time_list = name_dict_after_execution["exe_time"]

        total_execution_time = 0
        for execution_time in execution_time_list:
            total_execution_time += execution_time

        avg_execution_time = total_execution_time / num_iteration
        std_dev = np.std(execution_time_list)
        sem_execution_time = std_dev / np.sqrt(num_iteration)
        
        log(f"Completed evaluation with {transpile_mode}: avg_execute_time={avg_execution_time:.6f}, sem={sem_execution_time:.6f}")

        execution_time_data[transpile_mode] = (avg_execution_time, sem_execution_time)

    return execution_time_data

def evaluate_files(file_paths, settings):
    benchmark_processor = settings.processor
    num_iterations = settings.num_iterations

    file_names = []
    evaluation_results = []

    for file_path in file_paths:
        try:
            with open(file_path, "r") as file:
                code = file.read()
        except FileNotFoundError:
            log(f"The specified file '{file_path}' was not found.")
            sys.exit(1)
        except Exception as e:
            log(f"An error occurred while opening the file: {e}")
            sys.exit(1)

        log(f"Evaluate: {file_path}")

        match benchmark_processor:
            case "transpiler":
                comparison_strategy = settings.comparison_strategy
                optimize_pure_function = settings.optimize_pure_function
                log(f"Evaluate files with transpiler: comprison_strategy={comparison_strategy}, optimize_pure_function={optimize_pure_function}")
                execution_time_per_file = evaluate_transpiler(code, comparison_strategy, optimize_pure_function, num_iterations)
        
        evaluation_results.append(execution_time_per_file)
        file_names.append(file_category_name(file_path))

        log(f"Evaluated: {file_path}")

    return list(zip(file_names, evaluation_results))
