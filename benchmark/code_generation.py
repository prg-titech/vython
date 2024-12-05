import string
import os
from utils import log

def generate_vython_code(loop, num_base_names, num_base_versions, num_actual_versions):
    base_names = ["TestClass" + str(i) for i in range(num_base_names)]
    with_version_values = []
    code = ""
    
    code += "import time\n"
    class_size = 0
    for base_name in base_names:
        if class_size >= num_actual_versions:
                break
        for i in range(1, num_base_versions + 1):
            code += f"class {base_name}!{i}:\n"
            code += "    def __init__(self, v):\n"
            code += "        self.v = v\n"

            class_size += 1
            if class_size >= num_actual_versions:
                break
    
    instance_size = 0
    for base_name in base_names:
        if instance_size >= num_actual_versions:
                break
        for i in range(1, num_base_versions + 1):
            code += f"i{base_name.lower()}{i} = {base_name}!{i}(1)\n"

            instance_size += 1
            if instance_size >= num_actual_versions:
                break
    
    code += "\n"

    value_size = 0
    for base_name in base_names:
        if value_size >= num_actual_versions:
                break
        for i in range(1, num_base_versions + 1):
            code += f"v{base_name.lower()}{i} = i{base_name.lower()}{i}.v\n"
            with_version_values.append(f"v{base_name.lower()}{i}")

            value_size += 1
            if value_size >= num_actual_versions:
                break
    
    code += "\n"
    for i in range(num_actual_versions):
        if i != 0:
            code += f"tmp = tmp + {with_version_values[i]}\n"
        else:
            code += f"tmp = {with_version_values[i]}\n"
    for i in range(num_base_names * num_base_versions - num_actual_versions):
            code += f"tmp = tmp + {with_version_values[0]}\n"
    code += f"x = tmp\n"
    code += f"y = tmp\n"
    
    
    code += f"m = {loop}\n"
    code += "def main():\n"
    code += "   s = time.perf_counter()\n"
    code += "   for i in range(m):\n"
    code += "       x + y\n"
    code += "   e = time.perf_counter()\n"
    code += "   return e - s\n"
    
    return code

def allocate_vython_code(gen_code_requirements, source_path):
    log("Generating Vython benchmark code")
    for gen_code_requirement in gen_code_requirements:
        loop = int(gen_code_requirement[0])
        num_base_names = int(gen_code_requirement[1])
        num_base_versions = int(gen_code_requirement[2])
        num_actual_versions = int(gen_code_requirement[3])

        generated_code = generate_vython_code(loop, num_base_names, num_base_versions, num_actual_versions)

        str_actual_versions = str(gen_code_requirement[3])
        while len(str_actual_versions) < 3:
            str_actual_versions = "0" + str_actual_versions

        with open(os.path.join(source_path, f"benchmark_{loop}_{num_base_names}_{num_base_versions}_{str_actual_versions}.py"), "w") as f:
            f.write(generated_code)
