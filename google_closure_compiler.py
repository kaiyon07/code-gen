"""
Wrapper around Google Closure Compiler
https://github.com/google/closure-compiler
"""

import tempfile
import os
import subprocess
import json

DEFAULT_CONFORMANCE_CONFIG_PATH = './config/default_conformance.textproto'

DEFAULT_OPTIONS = {
    'js': '',
    'js_output_file': os.devnull,
    'warning_level': 'VERBOSE',
    'error_format': 'JSON',
    'jscomp_warning': '"*"',
    'conformance_configs': DEFAULT_CONFORMANCE_CONFIG_PATH
}

COMMAND = 'google-closure-compiler'


class GoogleClosureCompiler:
    def __init__(self, conformance_config_path: str = DEFAULT_CONFORMANCE_CONFIG_PATH):
        self.options = dict(DEFAULT_OPTIONS)
        self.options['conformance_configs'] = conformance_config_path

    def evaluate(self, code: str) -> str:
        f = tempfile.NamedTemporaryFile("w")
        f.write(code)
        f.flush()

        self.options['js'] = f.name

        cmd = [COMMAND] + [f"--{key} {value}" for key, value in self.options.items()]

        result = subprocess.run(" ".join(cmd), shell=True, capture_output=True, text=True)

        output = result.stderr

        f.close()
        return json.loads(output)

