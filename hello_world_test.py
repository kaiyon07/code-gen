import os
import json
from evaluator import evaluate
from eslint import EslintProcessor
from google_closure_compiler import GoogleClosureCompiler
from gemini_api import gemini_response  # Uncomment to enable Gemini response

# Define the specific file path and output file
file_path = './our_dataset/easy/hello_world.js'
output_file = 'evaluation_results2.txt'

# Specify the Gemini model
json_model = 'gemini-1.5-pro'  # Define Gemini model

# Initialize instances of EslintProcessor and GoogleClosureCompiler
eslint_processor = EslintProcessor()
google_closure_compiler = GoogleClosureCompiler()

# Open output file to write results
with open(output_file, 'w') as outfile:
    # Read the original code from hello_world.js
    with open(file_path, 'r') as file:
        original_code = file.read()
    
    # Generate refactored code using Gemini for hello_world.js only
    prompt = f"Refactor the following JavaScript code to improve readability and performance:\n{original_code}"
    refactored_response = gemini_response(prompt, json_model)  # Use Gemini to refactor code
    
    # Parse the response to access the 'refactored_code' field
    data = json.loads(refactored_response)
    refactored_code = data['refactored_code']
    
    # Evaluate the original and refactored code using `evaluate`
    analysis_result = evaluate(original_code, refactored_code, run_code=False)

    # Write the path, original contents, refactored code, and analysis result to the output file
    outfile.write(f"Accessed file: {file_path}\n")
    outfile.write("Original File Contents:\n")
    outfile.write(original_code)
    outfile.write("\n\nRefactored Code:\n")
    outfile.write(refactored_code)
    outfile.write("\n\nAnalysis Result:\n")
    #outfile.write(f"{analysis_result}\n")
    outfile.write("-" * 40 + "\n\n")

print(f"File path, contents, refactored code, and analysis results of hello_world.js saved to {output_file}")
