"""
Wrapper around Google Closure Compiler
https://github.com/google/closure-compiler
"""

import tempfile
import os
import subprocess
import json

DEFAULT_CONFORMANCE_CONFIG_PATH = './config/default_conformance.textproto'

EVALUATE_DEFAULT_OPTIONS = {
    'js': '',
    'js_output_file': os.devnull,
    'warning_level': 'VERBOSE',
    'error_format': 'JSON',
    'jscomp_warning': '"*"',
    'conformance_configs': DEFAULT_CONFORMANCE_CONFIG_PATH
}

OPTIMIZE_DEFAULT_OPTIONS = {
    'compilation_level': 'ADVANCED',
    'js': '',
    'js_output_file': '',
    'warning_level': 'VERBOSE'
}

COMMAND = 'google-closure-compiler'


class GoogleClosureCompiler:
    def __init__(self, conformance_config_path: str = DEFAULT_CONFORMANCE_CONFIG_PATH):
        self.evaluate_options = dict(EVALUATE_DEFAULT_OPTIONS)
        self.evaluate_options['conformance_configs'] = conformance_config_path

        self.optimize_options = dict(OPTIMIZE_DEFAULT_OPTIONS)

    def evaluate(self, code: str):
        f = tempfile.NamedTemporaryFile("w")
        f.write(code)
        f.flush()

        self.evaluate_options['js'] = f.name

        cmd = [COMMAND] + [f"--{key} {value}" for key, value in self.evaluate_options.items()]

        result = subprocess.run(" ".join(cmd), shell=True, capture_output=True, text=True)

        output = result.stderr

        f.close()
        return json.loads(output)

    def optimize(self, code:str) -> str:
        f = tempfile.NamedTemporaryFile("w")
        f.write(code)
        f.flush()

        self.optimize_options['js'] = f.name

        o = tempfile.NamedTemporaryFile("w")

        self.optimize_options['js_output_file'] = o.name

        cmd = [COMMAND] + [f"--{key} {value}" for key, value in self.optimize_options.items()]

        result = subprocess.run(" ".join(cmd), shell=True, capture_output=True, text=True)

        o.flush()

        with open(o.name, 'r') as ro:
            compiled_output = ro.read()

        f.close()
        o.close()
        return compiled_output

