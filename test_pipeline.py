import os
import json
import time
from tqdm import tqdm  # Import tqdm for the progress bar
from evaluator import evaluate
from eslint import EslintProcessor
from google_closure_compiler import GoogleClosureCompiler
from chatgpt_api import ChatGPT  # Import ChatGPT
from gemini_api import gemini_response  # Import Gemini API

# Define the main dataset folder and output files for each model
dataset_folder = './our_dataset'
chatgpt_output_file = 'evaluation_results_chatgpt.txt'
gemini_output_file = 'evaluation_results_gemini.txt'

# Initialize instances of EslintProcessor, GoogleClosureCompiler, ChatGPT, and Gemini
eslint_processor = EslintProcessor()
google_closure_compiler = GoogleClosureCompiler()
chatgpt = ChatGPT(MODEL="gpt-3.5-turbo")  # Specify the ChatGPT model
json_model = 'gemini-1.5-pro'  # Define Gemini model

# Define subfolder levels for processing
difficulty_levels = ['easy', 'medium', 'hard']

# Count total files to be processed for progress bar
total_files = sum([len(files) for level in difficulty_levels for _, _, files in os.walk(os.path.join(dataset_folder, level)) if files])

def process_and_write_results(model_name, full_file_path, original_code, refactored_code, output_file):
    """Writes the path, original contents, refactored code, and analysis result to the specified output file."""
    try:
        # Evaluate the original and refactored code
        analysis_result = evaluate(original_code, refactored_code, run_code=True)
    except Exception as e:
        analysis_result = f"Error during analysis: {str(e)}"
    
    # Write results to the output file
    with open(output_file, 'a') as outfile:
        outfile.write(f"Model: {model_name}\n")
        outfile.write(f"Accessed file: {full_file_path}\n")
        outfile.write("Original File Contents:\n")
        outfile.write(original_code)
        outfile.write("\n\nRefactored Code:\n")
        outfile.write(refactored_code)
        outfile.write("\n\nAnalysis Result:\n")
        outfile.write(f"{analysis_result}\n")
        outfile.write("-" * 40 + "\n\n")


# Open output files to write combined results
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

                # Generate refactored code using ChatGPT
                prompt = f"""Refactor the following JavaScript code to improve readability and performance:\n{original_code} 
                \nIn your JSON response, ensure the refactored code is in a field called "refactored_code"."""

                # Get refactored code from ChatGPT
                refactored_response_chatgpt = chatgpt.get_chatgpt_response(prompt, max_answer_tokens=500)
                print("ChatGPT Response:", refactored_response_chatgpt)  # Debug line to check ChatGPT response
                data_chatgpt = json.loads(refactored_response_chatgpt)
                refactored_code_chatgpt = data_chatgpt['refactored_code']

                # Write ChatGPT results
                process_and_write_results("ChatGPT", full_file_path, original_code, refactored_code_chatgpt, chatgpt_output_file)

                # Delay to prevent API rate limiting
                time.sleep(10)

                # Get refactored code from Gemini
                refactored_response_gemini = gemini_response(prompt, json_model)
                print("Gemini Response:", refactored_response_gemini)  # Debug line to check Gemini response
                data_gemini = json.loads(refactored_response_gemini)
                refactored_code_gemini = data_gemini['refactored_code']

                # Write Gemini results
                process_and_write_results("Gemini", full_file_path, original_code, refactored_code_gemini, gemini_output_file)

                # Delay to prevent API rate limiting
                time.sleep(10)

                # Update progress bar
                pbar.update(1)

print(f"All file paths, contents, refactored code, and analysis results have been saved to {chatgpt_output_file} and {gemini_output_file}")