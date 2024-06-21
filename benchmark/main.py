import os
import sys
import json
from datetime import datetime

from evaluation import evaluate_files
from code_generation import allocate_vython_code
from utils import get_file_path, log

##########################
# Benchmark settings
settings_path = "benchmark/benchmark_settings.json"
##########################

def load_settings(settings_path):
    with open(settings_path, 'r') as file:
        settings = json.load(file)
    return settings

def run():
    settings = load_settings(settings_path)

    #########################################################
    # Benchmark settings from the settings file
    benchmark_mode = settings["benchmark_mode"]
    num_iterations = settings["num_iterations"]
    dirpath_benchmarks = settings["dirpath_benchmarks"]

    # Parameters for generating vython code
    num_loop = settings["num_loop"]
    num_base_names = settings["num_base_names"]
    num_base_versions = settings["num_base_versions"]
    num_actual_versions_list = settings["num_actual_versions_list"]
    #########################################################   

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_path = f"benchmark/log/{timestamp}"
    source_path = os.path.join(base_path, "source")
    result_path = os.path.join(base_path, "result")

    os.makedirs(source_path, exist_ok=True)
    os.makedirs(result_path, exist_ok=True)

    gen_code_requirements = [
      [num_loop, num_base_names, num_base_versions, num_actual_versions]
      for num_actual_versions in num_actual_versions_list
    ]

    match benchmark_mode:
        case "nor-i" | "nor-t":
            file_paths = get_file_path(dirpath_benrhcmarks)
        case "gen-t":
            allocate_vython_code(gen_code_requirements, source_path)
            file_paths = get_file_path(source_path)

    max_recursion = 2100
    sys.setrecursionlimit(max_recursion)
    evaluate_files(file_paths, benchmark_mode, num_iterations, result_path)
    log("Evaluation completed.")

if __name__ == "__main__":
    run()
