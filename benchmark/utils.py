import os
import glob
import re

def log(message):
    print(f"[LOG] {message}")

def file_category_name(path):
    base_name = os.path.basename(path)
    file_name, _ = os.path.splitext(base_name)
    if re.match(r'benchmark_.*$', file_name):
        return file_name[-3:]
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
