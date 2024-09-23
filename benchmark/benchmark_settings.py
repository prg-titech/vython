class BenchmarkSettings():
    def __init__(self, settings_json):
        # common settings
        self.processor = settings_json["processor"]
        self.benchmark_target = settings_json["benchmark_target"]
        self.num_iterations = settings_json["num_iterations"]

        # settings for sample
        if(self.benchmark_target == "sample"):
            self.path_benchmarks = settings_json["path_benchmarks"]
        
        # settings for generate
        if(self.benchmark_target == "generate"):
            self.num_loop = settings_json["num_loop"]
            self.num_base_names = settings_json["num_base_names"]
            self.num_base_versions = settings_json["num_base_versions"]
            self.interval_num_versions = settings_json["interval_num_versions"]

        # settings for Transpiler
        if(self.processor == "transpiler"):
            self.comparison_strategy = settings_json["comparison_strategy"]

    def get_gen_code_requirements(self):
        # 誤ってgenerate以外で呼び出されたとき用
        if self.benchmark_target != "generate":
            return [[]]

        requirements = []
        if self.interval_num_versions == "geometric":
            max_num_version = self.num_base_names * self.num_base_versions
            current_num_version = 1
            while current_num_version <= max_num_version:
                requirements.append([self.num_loop,
                               self.num_base_names,
                               self.num_base_versions,
                               current_num_version])
                current_num_version *= 2
        if self.interval_num_versions == "min_max":
            max_num_version = self.num_base_names * self.num_base_versions
            min_num_version = 1
            requirements.append([self.num_loop,
                                 self.num_base_names,
                                 self.num_base_versions,
                                 max_num_version])
            requirements.append([self.num_loop,
                                 self.num_base_names,
                                 self.num_base_versions,
                                 min_num_version])
        return requirements

