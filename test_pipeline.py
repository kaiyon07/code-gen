import os
import glob
from evaluator import evaluate
from eslint import EslintProcessor
from google_closure_compiler import GoogleClosureCompiler
from chatgpt_api import ChatGPT
from gemini_api import gemini_response

# Define the path to the main dataset folder and output file
dataset_folder = './our_dataset'
output_file = 'evaluation_results.txt'

# Initialize instances of EslintProcessor, GoogleClosureCompiler, and ChatGPT
eslint_processor = EslintProcessor()
google_closure_compiler = GoogleClosureCompiler()
chatgpt = ChatGPT(MODEL="gpt-3.5-turbo")  # Specify the model version
json_model = 'gemini-1.5-pro'  # Define Gemini model

# Define subfolder levels for processing
difficulty_levels = ['easy', 'medium', 'hard']

# Open output file to write results
with open(output_file, 'w') as outfile:
    # Loop through each difficulty level
    for level in difficulty_levels:
        # Get the path to the current level's folder
        level_folder = os.path.join(dataset_folder, level)
        
        # Loop through each .js file in the current folder
        for file_path in glob.glob(os.path.join(level_folder, "*.js")):
            with open(file_path, 'r') as file:
                original_code = file.read()

            # Generate refactored code using Gemini or ChatGPT
            prompt = f"Refactor the following JavaScript code to improve readability and performance:\n{original_code}"
            refactored_code = gemini_response(prompt, json_model)  # Use Gemini

            # Uncomment below to use ChatGPT instead of Gemini if quota allows
            # refactored_code = chatgpt.get_chatgpt_response(prompt, max_answer_tokens=500)
            
            # Evaluate the original and refactored code using `evaluate`
            analysis_result = evaluate(original_code, refactored_code, run_code=True)

            # Write the result for the current file to the output file
            outfile.write(f"Results for {file_path} in {level} difficulty:\n")
            outfile.write(f"{analysis_result}\n")
            outfile.write("-" * 40 + "\n")

print(f"Evaluation results saved to {output_file}")