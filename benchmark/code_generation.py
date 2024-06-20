import string
import os
from utils import log

def generate_vython_code(loop, num_base_names, num_base_versions, num_actual_versions):
    base_names = list(string.ascii_uppercase[:num_base_names])
    with_version_values = []
    code = ""
    
    for base_name in base_names:
        for i in range(1, num_base_versions + 1):
            code += f"class {base_name}!{i}:\n"
            code += "    def __init__(self, v):\n"
            code += "        self.v = v\n"
            code += "    def get_v(self):\n"
            code += "        return self.v\n\n"
    
    for base_name in base_names:
        for i in range(1, num_base_versions + 1):
            code += f"i{base_name.lower()}{i} = {base_name}!{i}(1)\n"
    
    code += "\n"
    for base_name in base_names:
        for i in range(1, num_base_versions + 1):
            code += f"v{base_name.lower()}{i} = i{base_name.lower()}{i}.get_v()\n"
            with_version_values.append(f"v{base_name.lower()}{i}")
    
    code += "\n"
    tmp_code = ""
    for i in range(num_actual_versions):
        if i != 0:
            tmp_code += " + "
        tmp_code += with_version_values[i]
    for i in range(num_base_names * num_base_versions - num_actual_versions):
            tmp_code += f" + {with_version_values[0]}"
    code += f"x = {tmp_code}\n"
    code += f"y = {tmp_code}\n"
    
    code += "\n"
    code += "def loop(c, f, y):\n"
    code += "    if c > 0:\n"
    code += "        f(y)\n"
    code += "        loop(c - 1, f, y)\n"
    code += "    else:\n"
    code += "        return\n\n"
    code += "f = x.__add__\n"
    code += f"m = {loop}\n"
    code += "\n"
    code += "def main(m, f, y):\n"
    code += "   loop(m, f, y)\n"
    
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
        while len(str_actual_versions) != 3:
            str_actual_versions = "0" + str_actual_versions

        with open(os.path.join(source_path, f"benchmark_{loop}_{num_base_names}_{num_base_versions}_{str_actual_versions}.py"), "w") as f:
            f.write(generated_code)
