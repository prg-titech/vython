import os
import sys
import json
from datetime import datetime

from evaluation import evaluate_files
from code_generation import allocate_vython_code
from utils import get_file_paths, log
from benchmark_settings import BenchmarkSettings
from plotting import make_refined_bar_graph,make_line_graph,make_bar_graph_about_ratio

##########################
# Benchmark settings
settings_path = "benchmark/benchmark_settings.json"
##########################

def load_settings_json(settings_path):
    with open(settings_path, 'r') as file:
        settings = json.load(file)
    return settings

def run():
    settings = BenchmarkSettings(load_settings_json(settings_path))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_path = f"benchmark/log/{timestamp}"
    source_path = os.path.join(base_path, "source")
    result_path = os.path.join(base_path, "result")

    os.makedirs(source_path, exist_ok=True)
    os.makedirs(result_path, exist_ok=True)

    if settings.benchmark_target == "generate":
        gen_code_requirements = settings.get_gen_code_requirements()

    match settings.benchmark_target:
        case "sample":
            file_paths = get_file_paths(settings.path_benchmarks)
        case "generate":
            allocate_vython_code(gen_code_requirements, source_path)
            file_paths = get_file_paths(source_path)

    sys.setrecursionlimit(2500)
    sys.set_int_max_str_digits(0)
    evaluation_data = evaluate_files(file_paths, settings, result_path)

    # generate graph
    match (settings.processor, settings.benchmark_target):
        case ("transpiler","generate"):
            make_refined_bar_graph(evaluation_data, settings.comparison_strategy, result_path)
            make_line_graph(evaluation_data, settings.comparison_strategy, result_path)
        case ("transpiler","sample"):
            make_bar_graph_about_ratio(evaluation_data, settings.comparison_strategy, result_path)
            make_line_graph(evaluation_data, settings.comparison_strategy, result_path)
        case "interpreter":
            pass
        case _:
            pass

    log("Evaluation completed.")

if __name__ == "__main__":
    run()
