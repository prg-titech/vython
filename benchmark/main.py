import os
import sys
from datetime import datetime

from evaluation import evaluate_files
from code_generation import allocate_vython_code
from utils import get_file_path, log

def run():
    #########################################################
    # Benchmark settings
    benchmark_mode = "gen-t"
    num_iterations = 1
    dirpath_benrhcmarks = "test/sample_program/basic"

    # Parameters for generating vython code
    num_loop = 2000
    num_base_names = 10
    num_base_versions = 16
    num_actual_versions_list = [1, 5, 10, 20, 40, 80, 160]
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
