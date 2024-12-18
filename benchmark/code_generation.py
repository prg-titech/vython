import string
import os
from utils import log

def generate_vython_code(loop, num_base_names, expo):
    base_names = ["TestClass" + str(i) for i in range(num_base_names)]
    with_version_values = []
    code = ""
    
    code += "import time\n"
    class_size = 0
    for base_name in base_names:
        if class_size >= 2 ** expo:
                break
        for i in range(1, 3):
            code += f"class {base_name}!{i}:\n"
            code += "    def __init__(self, v):\n"
            code += "        self.v = v\n"

            class_size += 1
            if class_size >= 2 ** expo:
                break
    
    instance_size = 0
    for base_name in base_names:
        if instance_size >= 2 ** expo:
                break
        for i in range(1, 3):
            code += f"i{base_name.lower()}{i} = {base_name}!{i}(1)\n"

            instance_size += 1
            if instance_size >= 2 ** expo:
                break
    
    code += "\n"

    value_size = 0
    for base_name in base_names:
        if value_size >= 2 ** expo:
                break
        for i in range(1,  3):
            code += f"v{base_name.lower()}{i} = i{base_name.lower()}{i}.v\n"
            with_version_values.append(f"v{base_name.lower()}{i}")

            value_size += 1
            if value_size >= 2 ** expo:
                break
    
    code += "\n"
    for i in range(2 ** expo):
        if i != 0:
            code += f"tmp = tmp + {with_version_values[i]}\n"
        else:
            code += f"tmp = {with_version_values[i]}\n"
    for i in range(num_base_names * 2 - (2 ** expo)):
            code += f"tmp = tmp + {with_version_values[0]}\n"
    code += f"x = tmp\n"
    code += f"y = tmp\n"
    
    
    code += f"m = {loop}\n"
    code += "def main_pure(num_iteration):\n"
    code += "   execution_times = []\n"
    code += "   for i in range(num_iteration):\n"
    code += "       s = time.perf_counter()\n"
    code += "       for i in range(m):\n"
    code += "           x + y\n"
    code += "       e = time.perf_counter()\n"
    code += "       execution_times.append(e - s)\n"
    code += "   return execution_times\n"
    
    return code

def allocate_vython_code(gen_code_requirements, source_path):
    log("Generating Vython benchmark code")
    for gen_code_requirement in gen_code_requirements:
        loop = int(gen_code_requirement[0])
        num_base_names = int(gen_code_requirement[1])
        expo = int(gen_code_requirement[2])

        generated_code = generate_vython_code(loop, num_base_names, expo)

        with open(os.path.join(source_path, f"benchmark_{loop}_{num_base_names}_{expo}.py"), "w") as f:
            f.write(generated_code)
