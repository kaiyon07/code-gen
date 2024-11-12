import os
import json
import time
from tqdm import tqdm  # Import tqdm for the progress bar
from evaluator import evaluate
from eslint import EslintProcessor
from google_closure_compiler import GoogleClosureCompiler
from gemini_api import gemini_response  # Uncomment to enable Gemini response

# Define the main dataset folder and output file
dataset_folder = './our_dataset'
output_file = 'evaluation_results.txt'

# Specify the Gemini model
json_model = 'gemini-1.5-pro'  # Define Gemini model

# Initialize instances of EslintProcessor and GoogleClosureCompiler
eslint_processor = EslintProcessor()
google_closure_compiler = GoogleClosureCompiler()

# Define subfolder levels for processing
difficulty_levels = ['easy', 'medium', 'hard']

# Count total files to be processed for progress bar
total_files = sum([len(files) for level in difficulty_levels for _, _, files in os.walk(os.path.join(dataset_folder, level)) if files])

# Open output file to write combined results
with open(output_file, 'w') as outfile:
    # Initialize tqdm progress bar with the total file count
    with tqdm(total=total_files, desc="Processing Files") as pbar:
        # Loop through each difficulty level
        for level in difficulty_levels:
            level_folder = os.path.join(dataset_folder, level)

            # Loop through each .js file in the current subfolder
            for file_name in os.listdir(level_folder):
                if file_name.endswith('.js'):
                    full_file_path = os.path.join(level_folder, file_name)

                    # Read the original code
                    with open(full_file_path, 'r') as file:
                        original_code = file.read()

                    # Generate refactored code using Gemini
                    prompt = f"""Refactor the following JavaScript code to improve readability and performance:\n{original_code} 
                    \nIn your JSON response, ensure the refactored code is in a field called "refactored_code"."""
                    refactored_response = gemini_response(prompt, json_model)  # Use Gemini to refactor code

                    # Parse the response to access the 'refactored_code' field
                    data = json.loads(refactored_response)
                    refactored_code = data['refactored_code']

                    # Evaluate the original and refactored code using `evaluate`
                    try:
                        analysis_result = evaluate(original_code, refactored_code, run_code=True)
                    except Exception as e:
                        analysis_result = f"Error during analysis: {str(e)}"

                    # Write the path, original contents, refactored code, and analysis result to the output file
                    outfile.write(f"Accessed file: {full_file_path}\n")
                    outfile.write("Original File Contents:\n")
                    outfile.write(original_code)
                    outfile.write("\n\nRefactored Code:\n")
                    outfile.write(refactored_code)
                    outfile.write("\n\nAnalysis Result:\n")
                    outfile.write(f"{analysis_result}\n")
                    outfile.write("-" * 40 + "\n\n")

                    # Delay to prevent API rate limiting
                    time.sleep(10)  # Adjusted delay to 10 seconds

                    # Update progress bar
                    pbar.update(1)

print(f"All file paths, contents, refactored code, and analysis results have been saved to {output_file}")