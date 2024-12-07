# Improving Code Quality using LLMs
*Evaluation Framework and Results*

Authors:

* Mrinal Anand
* Jacob Zhi
* Metehan Berker
* Yekta Kocaogullar


## Code Environment Setup

### Evaluation Framework

Evaluation is performed in a Node.js environment. Ensure the following dependencies are installed:

Global JavaScript Dependencies:
* Node.js (approx. recommended Node ~ v20.11.0, npm ~ 10.2.4 but many other versions may work)
* ESLint (`npm init @eslint/config@latest`, then make sure `npx eslint` doesn't fail)
* Google Closure Compiler (`sudo npm i -g google-closure-compiler`, then make sure `google-closure-compiler` doesn't 
fail)

Evaluation Setup (see `./js/package.json` for local dependencies):
* `cd js`
* `npm install`

### Python Driver Code

All code in `.py` library files and source code should be run in the same Python environment. You may use any 
environment (Conda, venv) or the base environment of your system.

Dependencies are listed in `requirements.txt`. Install dependencies by running:
* `pip install -r ./requirements.txt`

## Data

Data is obtained from Leetcode (https://leetcode.com) problems and selected solutions from each problem's page are used 
as the ground truth code for refactoring.  Additional columns describing the problem are added 
by hand. All data used for the project is located in this repository.

* Individual JavaScript files (organized by difficulty): `./our_dataset`
* CSV Table: `./Code Generation Dataset NLP - Sheet1.csv`

## Reproducing Results

Our results are split into three steps of the pipeline:

### Step 1: Generation

The code in the following notebooks were used to generate each output file (containing results of calling the LLM on a 
coding problem). Outputs with temperature 0 are reproducible. 
All output files, sorted by model, are stored in `./output_files.`

Notebooks used to generate output files:
* Gemini: `Gemini_Script_with_Schema.ipynb`
* OpenAI GPT: `OpenAI-Script.ipynb`
* Llama (Groq): `Groq.ipynb`
* Mixtral: `Mixtral.ipynb`

Inside `./output_files` exist LLM outputs in CSV format sorted by model. The following file names are used for each experiment:
* CODE_GEN_V1 -> LLM generates new code using problem description and schema
* CODE_REFACTOR_V1 -> refactoring using problem description, schema, and ground truth code
* CODE_REFACTOR_V2 -> refactoring using schema, ground truth code
* CODE_REFACTOR_V3 -> refactoring using problem description, schema, examples, constraints, and ground truth code
* CODE_REFACTOR_V4 -> refactoring using description, schema, ground truth code and linter output
* CODE_REFACTOR_V5 -> refactoring V3 with detailed optimization instructions

### Step 2: Evaluation

The code in the notebook `evaluation.ipynb` was used to run the evaluation on every output file produced in step 1. The 
results of the evaluation are saved in `./evaluation_files`.

The `./evaluation_files` mirror the file structure of `./output_files`, but include columns containing the results of 
evaluation. The evaluation performed uses the `evaluator.py` evaluation library (written by us) which performs both 
static analysis and runtime metrics of the code.

### Step 3: Data Analysis and Aggregation

Aggregated statistics for each model are located in `./metrics`. Notebooks in `./analysis_notebooks` are used to produce 
such statistics as well as any graphs (figures) in the report.
