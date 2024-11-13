"""
Wrapper around ESLint
https://eslint.org/docs/latest/
"""

import os
import subprocess
import json

DEFAULT_CONFIG_PATH = './config/eslint-all.js'

DEFAULT_OPTIONS = {
    'stdin': '',
    'config': DEFAULT_CONFIG_PATH,
    'format': 'json'
}

COMMAND = 'npx eslint'


class EslintProcessor:
    def __init__(self, config_path: str = DEFAULT_CONFIG_PATH):
        self.options = dict(DEFAULT_OPTIONS)
        self.options['config'] = config_path

    def evaluate(self, code: str):
        
        cmd = [COMMAND] + [f"--{key} {value}" for key, value in self.options.items()]

        result = subprocess.run(" ".join(cmd), shell=True, capture_output=True, text=True, input=code)

        output = result.stdout

        return json.loads(output)

