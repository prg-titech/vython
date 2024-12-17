import os
import sys
import csv
import json
from datetime import datetime

from evaluation import evaluate_files
from code_generation import allocate_vython_code
from utils import get_file_paths, log, generate_csv
from benchmark_settings import BenchmarkSettings
from plotting import make_line_graph_scalability,make_bar_graph_sample

##########################
# Benchmark settings
settings_path = "benchmark/benchmark_settings.json"
##########################

def load_settings_json(settings_path):
    with open(settings_path, 'r') as file:
        settings = json.load(file)
    return settings

def list_modules_in_path(path):
    try:
        return [f.split(".")[0] for f in os.listdir(path) if f.endswith(".py") or os.path.isdir(os.path.join(path, f))]
    except FileNotFoundError:
        return []
def run():
<<<<<<< Updated upstream
    # ベンチマーク設定ファイルから設定を収集
=======
    print(sys.path)
    for path in sys.path:
        print(f"\nPath: {path}")
        modules = list_modules_in_path(path)
        for module in sorted(modules):
            print(f"  {module}")
    return
>>>>>>> Stashed changes
    settings = BenchmarkSettings(load_settings_json(settings_path))

    # ベンチマーク測定の結果等を格納するフォルダを生成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_path = f"benchmark/log/{timestamp}"
    result_path = os.path.join(base_path, "result")
    os.makedirs(result_path, exist_ok=True)
    if settings.benchmark_target == "generate":
        source_path = os.path.join(base_path, "source")
        os.makedirs(source_path, exist_ok=True)

    # インタプリタの評価プログラムは今後実装する...?
    if settings.processor != "transpiler":
        log(f"Current benchmark program does not support for {settings.processor}")
        sys.exit(1)

    # scalabilityの評価の時、生成するベンチマークターゲットの要件を生成する
    if settings.benchmark_target == "generate":
        gen_code_requirements = settings.get_gen_code_requirements()

    # ベンチマークターゲットプログラムのpathのリストを取得
    match settings.benchmark_target:
        case "sample":
            file_paths = get_file_paths(settings.path_benchmarks)
        case "generate":
            allocate_vython_code(gen_code_requirements, source_path)
            file_paths = get_file_paths(source_path)

    # ベンチマークを測定
    sys.setrecursionlimit(2500)
    sys.set_int_max_str_digits(0)
    evaluation_results = evaluate_files(file_paths, settings)
    log("Evaluation completed.")

    # 結果をcsvファイルに出力
    with open(os.path.join(result_path, 'execution_time.csv'), 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        generate_csv(evaluation_results, csv_writer, settings)

    # 測定結果に従ってグラフを生成
    match (settings.processor, settings.benchmark_target):
        case ("transpiler","generate"):
            make_line_graph_scalability(evaluation_results, result_path)
        case ("transpiler","sample"):
            make_bar_graph_sample(evaluation_results, result_path)
        case "interpreter":
            pass
        case _:
            pass

if __name__ == "__main__":
    run()
