import string

def generate_python_code(loop, num_base_names, num_base_versions, num_actual_versions):
    base_names = list(string.ascii_uppercase[:num_base_names])
    with_version_values = []
    
    code = ""
    
    # クラス定義の作成
    for base_name in base_names:
        for i in range(1, num_base_versions + 1):
            code += f"class {base_name}!{i}:\n"
            code += "    def __init__(self, v):\n"
            code += "        self.v = v\n"
            code += "    def get_v(self):\n"
            code += "        return self.v\n\n"
    
    # インスタンスの作成
    for base_name in base_names:
        for i in range(1, num_base_versions + 1):
            code += f"i{base_name.lower()}{i} = {base_name}!{i}(1)\n"
    
    # 各バージョンの情報を持つ値を作成する
    code += "\n"
    for base_name in base_names:
        for i in range(1, num_base_versions + 1):
            code += f"v{base_name.lower()}{i} = i{base_name.lower()}{i}.get_v()\n"
            with_version_values.append(f"v{base_name.lower()}{i}")
    
    # num_actual_versionsの数だけバージョン情報を持つ値(変数x,yに束縛)を作成する
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
    
    # x,yに束縛された値をloopの回数分演算する
    code += "\n"
    code += "def loop(c, f, y):\n"
    code += "    if c > 0:\n"
    code += "        f(y)\n"
    code += "        loop(c - 1, f, y)\n"
    code += "    else:\n"
    code += "        return\n\n"
    code += "f = x.__add__\n"
    code += f"m = {loop}\n"
    code += "loop(m, f, y)\n"
    
    return code

def run():
    input_array = input().split()
    loop = int(input_array[0])
    num_base_names = int(input_array[1])
    num_base_versions = int(input_array[2])
    num_actual_versions = int(input_array[3])

    generated_code = generate_python_code(loop, num_base_names, num_base_versions, num_actual_versions)

    str_actual_versions = input_array[3]
    while len(str_actual_versions) != 3:
        str_actual_versions = "0" + str_actual_versions

    with open(f"benchmark/benchmark_program/benchmark_{loop}_{num_base_names}_{num_base_versions}_{str_actual_versions}.py", "w") as f:
        f.write(generated_code)

run()
