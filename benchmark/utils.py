import os
import glob
import re

def log(message):
    print(f"[LOG] {message}")

def file_category_name(path):
    base_name = os.path.basename(path)
    file_name, _ = os.path.splitext(base_name)
    if re.match(r'benchmark_.*$', file_name):
        i = -1
        while file_name[i-1] != "_":
            i -= 1
        return file_name[i:]
    else:
        return file_name

def get_file_paths(path):
    log(f"Getting file paths from {path}")
    if os.path.isfile(path):
        return [path]
    else:
        under_paths = glob.glob(os.path.join(path, '*'))
        file_paths = [path for path in under_paths if os.path.isfile(path)]
        file_paths.sort()
        return file_paths
    
def generate_csv(evaluation_results, csv_writer, settings):
    log("Generating csv file with the evaluation results")
    for evaluation_result in evaluation_results:
        file_name = evaluation_result[0]
        evaluation_data = evaluation_result[1]
        csv_writer.writerow(['Program', file_name, ': Execution Time in', settings.processor])

        for compilation_mode, avg_sem in evaluation_data.items():
            avg = avg_sem[0]
            sem = avg_sem[1]
            csv_writer.writerow(['Executed in', compilation_mode])
            csv_writer.writerow(['AVG', f"{avg:.6f}"])
            csv_writer.writerow(['SEM', f"{sem:.6f}"])
        csv_writer.writerow([])
        
    log("Generated csv file")
