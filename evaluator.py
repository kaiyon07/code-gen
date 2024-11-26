from eslint import EslintProcessor
from google_closure_compiler import GoogleClosureCompiler
from gemini_api import gemini_response
import subprocess
import re
import json
import csv
import time
import hashlib

TEST_CASES_CACHE_PATH = "./js/test-cases.json"


def extract_code_from_markdown(output):
    # Regex to match the content inside the first code block
    match = re.search(r'```(?:\w+)?\n(.*?)```', output, re.DOTALL)
    return match.group(1).strip() if match else output


def optimize_code(google_closure_compiler, original_code, function_name):
    window_code = original_code + "\nwindow['{function_name}'] = {function_name};".format(
        function_name=function_name
    )
    closure_optimized_code = google_closure_compiler.optimize(window_code)

    # TODO: if minified code has a non-minifiable property called window, this will fail
    optimized_code = closure_optimized_code.replace("window.", "let ")
    return optimized_code


def code_id(code):
    return hashlib.shake_128(code.encode()).hexdigest(4)


def check_test_case_cache(code):
    with open(TEST_CASES_CACHE_PATH, 'r') as file:
        test_cases = json.load(file)

    if code_id(code) in test_cases:
        return test_cases[code_id(code)]

    return None


def write_test_case_cache(code, test_cases_string):
    with open(TEST_CASES_CACHE_PATH, 'r') as file:
        test_cases = json.load(file)

    test_cases[code_id(code)] = test_cases_string

    with open(TEST_CASES_CACHE_PATH, "w") as file:
        file.write(json.dumps(test_cases))


def evaluate(original_code, output, run_code=True):
    """
    Evaluates how much better code in `output` is compared to the original code.
    The code is compared by means of static analysis.
    If the run_code parameter is set to True, the two programs are compared for correctness and performance by
    running them against a suite of LLM-generated tests (hence, this method is non-deterministic as tests will change
    on a per-run basis).
    The code should be JavaScript code. If the run_code parameter is true, due to the limitations of the LLM and the
    way the tests are run, the JavaScript code should ideally be a single-function solution with primitive inputs and
    outputs (string, array, number, etc.).

    :param original_code: str, original source code.
    :param output: str, LLM output with refactored code. If non-code content is included, the code in the first Markdown
    code block is considered.
    :param run_code: bool, if False, only run static analysis, if True, run performance and correctness tests
    :return: a Dict of the following format
    {
        'eslint_count_original': int, number of ESLint-found issues in original code
        'eslint_count_refactored': int, number of ESLint-found issues in the refactored code
        'closure_count_original': int, number of Google Closure Compiler Warnings in original code
        'closure_count_refactored': int, number of Google Closure Compiler Warnings in refactored code
        'closure_optimized_code': str, the code which Google Closure Compiler transpiled
        'runtimeOriginal': float, runtime of original_code against tests
        'runtimeOptimized': float, runtime of Google Closure Compiler transpiled code against tests
        'runtimeRefactored': float, runtime of refactored (output) code against tests
        'numOptimizedCorrect': int, number of tests Google Closure Compiler transpiled code works on
        'numRefactoredCorrect': int, number of tests refactored (output) code works on
        'total': int, total number of tests
    }
    """
    # Part 1: Static analysis
    eslint = EslintProcessor()
    google_closure_compiler = GoogleClosureCompiler()

    output_code = extract_code_from_markdown(output)

    eslint_original = eslint.evaluate(original_code)[0]['messages']
    eslint_output = eslint.evaluate(output_code)[0]['messages']

    closure_original = google_closure_compiler.evaluate(original_code)
    closure_output = google_closure_compiler.evaluate(output_code)

    static_analysis_result = {
        'eslint_count_original': len(eslint_original),
        'eslint_count_refactored': len(eslint_output),
        'closure_count_original': len(closure_original),
        'closure_count_refactored': len(closure_output),
    }

    if not run_code:
        return static_analysis_result

    # Part 2: Run the code
    test_cases_string = check_test_case_cache(original_code)
    if not test_cases_string:
        # Create an LLM prompt to generate test cases for the given original_code
        with open("./prompt/generate_cases.txt", "r") as file:
            test_cases_prompt = file.read().replace("{function}", original_code)

        test_cases_string = extract_code_from_markdown(gemini_response(test_cases_prompt, 'gemini-1.5-pro'))
        write_test_case_cache(original_code, test_cases_string)

    # Write the LLM-generated JSON containing test inputs into a JSON file
    with open("./js/inputs.json", "w") as file:
        file.write(test_cases_string)

    # Try to parse LLM-generated JSON - it may be cut off
    test_cases_parsed = None
    for json_completion in ["", "\\\")\"]}", "\"]}", "]}", "}"]:
        try:
            test_cases_parsed = json.loads(test_cases_string + json_completion)
        except json.JSONDecodeError:
            pass
        else:
            break

    if not test_cases_parsed:
        return static_analysis_result

    static_analysis_result['test_cases'] = test_cases_string
    
    # Optimize the code using Google Closure Compiler (for performance comparison)
    optimized_code = optimize_code(google_closure_compiler, original_code, test_cases_parsed['functionOrClassName'])

    static_analysis_result['closure_optimized_code'] = optimized_code

    # Create a hardcoded JavaScript source from template
    # The JavaScript file will run the given code (original, optimized, and refactored) against the LLM-generated tests
    with open("./js/execute.template.js", "r") as file:
        js_execute_file = (file.read()
            .replace("// #put ORIGINAL", original_code)
            .replace("// #put OPTIMIZED", optimized_code)
            .replace("// #put REFACTORED", output_code)
                           )

    with open("./js/execute.js", "w") as file:
        file.write(js_execute_file)

    # Run the hardcoded JavaScript source using Node (output is a JSON printed to stdout)
    result = subprocess.run(["npm", "start"], cwd="./js", capture_output=True, text=True)

    # Parse the results of execution and combine with the results from static analysis
    result_parsed = {}
    try:
        result_parsed = json.loads(result.stdout[result.stdout.find("{"):])
    except:
        result_parsed['pyError'] = "No parseable output from JavaScript evaluation.. crashed?"

    return static_analysis_result | result_parsed


def evaluate_batch(in_csv, out_csv, original_code_column: str="gt_code", output_code_column: str="refactor_code",
                   run_code: bool=True, api_sleep_interval: float=1, verbose: bool=False):
    with open(in_csv, mode='r') as infile, open(out_csv, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile)

        fieldnames = reader.fieldnames
        result_fieldnames = ['eslint_count_original', 'eslint_count_refactored', 'closure_count_original', 'closure_count_refactored']

        if run_code:
            result_fieldnames += ['test_cases', 'closure_optimized_code', 'runtimeOriginal', 'runtimeOptimized', 'runtimeRefactored', 'numOptimizedCorrect', 'numRefactoredCorrect', 'total']

        fieldnames += result_fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            try:
                time.sleep(api_sleep_interval)
                result = evaluate(row[original_code_column], row[output_code_column], run_code)
            except Exception as e:
                result = {'pyError': str(e)}

            if verbose:
                print(result)

            for field_name in result_fieldnames:
                if field_name in result:
                    row[field_name] = result[field_name]
                else:
                    row[field_name] = -1

            writer.writerow(row)

