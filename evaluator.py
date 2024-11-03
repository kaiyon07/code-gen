from eslint import EslintProcessor
from google_closure_compiler import GoogleClosureCompiler
# from gemini_api import gemini_response
import subprocess
import re
import json


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


def evaluate(original_code, output, run_code=True):
    eslint = EslintProcessor()
    google_closure_compiler = GoogleClosureCompiler()

    output_code = extract_code_from_markdown(output)

    eslint_original = eslint.evaluate(original_code)[0]['messages']
    eslint_output = eslint.evaluate(output_code)[0]['messages']

    eslint_delta = len(eslint_output) - len(eslint_original)

    closure_original = google_closure_compiler.evaluate(original_code)
    closure_output = google_closure_compiler.evaluate(output_code)

    closure_delta = len(closure_output) - len(closure_original)

    static_analysis_result = {
        'eslint_delta': eslint_delta,  # number of reduced issues with the refactored code with eslint
        'closure_delta': closure_delta,  # number of reduced issues with the refactored code with closure
    }

    if not run_code:
        return static_analysis_result

    with open("./prompt/generate_cases.txt", "r") as file:
        test_cases_prompt = file.read().replace("{function}", original_code)

    # test_case_string = extract_code_from_markdown(gemini_response(test_cases_prompt, 'gemini-1.5-pro'))
    # TEMP CODE TO SET test_case_string
    # TODO remove the next `with` block and uncomment the code above to generate by chatgpt
    with open("./js/inputs.json", "r") as file:
        test_cases_string = file.read()

    with open("./js/inputs.json", "w") as file:
        file.write(test_cases_string)

    test_cases_parsed = json.loads(test_cases_string)

    optimized_code = optimize_code(google_closure_compiler, original_code, test_cases_parsed['functionName'])

    static_analysis_result['closure_optimized_code'] = optimized_code

    with open("./js/execute.template.js", "r") as file:
        js_execute_file = (file.read()
            .replace("// #put ORIGINAL", original_code)
            .replace("// #put OPTIMIZED", optimized_code)
            .replace("// #put REFACTORED", output_code)
                           )

    with open("./js/execute.js", "w") as file:
        file.write(js_execute_file)

    result = subprocess.run(["npm", "start"], cwd="./js", capture_output=True, text=True)

    result_parsed = {}
    try:
        result_parsed = json.loads(result.stdout[result.stdout.find("{"):])
    except:
        result_parsed['pyError'] = "No parseable output from JavaScript evaluation.. crashed?"

    return static_analysis_result | result_parsed
