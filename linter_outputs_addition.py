import pandas as pd
from eslint import EslintProcessor
from google_closure_compiler import GoogleClosureCompiler
from evaluator import extract_code_from_markdown

def main():
    # Initialize the linter classes
    eslint = EslintProcessor()
    google_closure_compiler = GoogleClosureCompiler()

    # Load the original CSV file
    input_file_path = 'Code Generation Dataset NLP - Sheet1.csv'
    output_file_path = 'Code_Generation_Dataset_with_Linter_Outputs.csv'

    try:
        df = pd.read_csv(input_file_path)
    except FileNotFoundError:
        print(f"Error: The file '{input_file_path}' was not found.")
        return
    except Exception as e:
        print(f"Error loading the CSV file: {str(e)}")
        return

    # Create a new column for linter outputs
    linter_outputs = []

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        try:
            # Get the ground truth code as a string
            gt_code = extract_code_from_markdown(row["Solution"])  # Use 'Solution' as the column containing the code

            # Fetch outputs from ESLint and Google Closure Compiler
            eslint_output = str(eslint.evaluate(gt_code)[0]['messages'])
            print("ESLint Output:")
            print(eslint_output)
            print()

            gcc_output = google_closure_compiler.evaluate(gt_code)
            print("Google Closure Compiler Output:")
            print(gcc_output)
            print()

            # Format the outputs
            formatted_output = (
                "ESLint Output:\n\n"
                f"{eslint_output}\n\n\n"
                "Google Closure Compiler Output:\n\n"
                f"{gcc_output}"
            )

            # Append the formatted output to the linter_outputs list
            linter_outputs.append(formatted_output)

        except Exception as e:
            # Handle any exceptions and append error message to the outputs
            print(f"Error processing row {index}: {str(e)}")
            linter_outputs.append(f"Error processing row {index}: {str(e)}")

    # Add the linter_outputs column to the DataFrame
    df['Linter Outputs'] = linter_outputs

    # Save the updated DataFrame to a new CSV file
    try:
        df.to_csv(output_file_path, index=False)
        print(f"Updated CSV saved to {output_file_path}")
    except Exception as e:
        print(f"Error saving the updated CSV: {str(e)}")

if __name__ == "__main__":
    main()