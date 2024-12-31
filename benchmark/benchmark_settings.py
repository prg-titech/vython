class BenchmarkSettings():
    def __init__(self, settings_json):
        # common settings
        self.processor = settings_json["processor"]
        self.benchmark_target = settings_json["benchmark_target"]
        self.num_iterations = settings_json["num_iterations"]

        # settings for sample
        if(self.benchmark_target == "sample") or (self.benchmark_target == "sample_mono"):
            self.path_benchmarks = settings_json["path_benchmarks"]
        
        # settings for generate
        if(self.benchmark_target == "generate"):
            self.num_loop = settings_json["num_loop"]
            self.num_base_names = settings_json["num_base_names"]
            # self.num_base_versions = settings_json["num_base_versions"]
            # self.interval_num_versions = settings_json["interval_num_versions"]

        # settings for Transpiler
        if(self.processor == "transpiler"):
            self.comparison_strategy = settings_json["comparison_strategy"]
            self.optimize_pure_function = bool(settings_json["optimize_pure_function"])

    def get_gen_code_requirements(self):
        requirements = []
        max_num_version = self.num_base_names * 2
        expo = 0
        while 2 ** expo <= max_num_version:
            requirements.append([self.num_loop,
                            self.num_base_names,
                            expo])
            expo += 1
        return requirements

