import os
import re
import openai
import argparse
from pathlib import Path

# Parse command line arguments
parser = argparse.ArgumentParser(description="Linter script for various file types.")
parser.add_argument('-d', '--directory', type=str, required=True, help="Directory to scan for files.")
args = parser.parse_args()

# Step 1: Scan the specified directory
directory_to_scan = Path(args.directory)
file_extensions = ['.py', '.sh', '.yaml', '.tf', '.json']
files_to_scan = []

for extension in file_extensions:
    files_to_scan.extend(directory_to_scan.rglob(f'*{extension}'))

# Exclude the script itself
script_name = Path(__file__).name
files_to_scan = [file for file in files_to_scan if file.name != script_name]

print("## Found files to review:\n")
for file in files_to_scan:
    print(f"- {file}")

# Step 2: Read and sanitize files
sensitive_strings = os.getenv('SENSITIVE_STRINGS', '').split(',')
api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = api_key

def sanitize_content(content, sensitive_strings):
    for sensitive in sensitive_strings:
        content = content.replace(sensitive, 'censored_string')
    content = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '10.0.0.1', content)
    return content

def get_openai_review(code_block):
    openai.api_key = api_key
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a senior developer"},
            {"role": "user", "content": "Please review the following piece of code using markdown format."
             "Do not repeat thewhole input file to your output."
             "If it is json or yaml just do linting and "
             f"if liniting is fine then output only \"Linting: Bravo! Everything ok and well formated\":\n\n: {code_block}"}
        ],
    )
    gpt_answer = response.choices[0].message.content.strip()
    return gpt_answer

def process_files(files):
    results = {}
    for file in files:
        with open(file, 'r') as f:
            content = f.read()

        sanitized_content = sanitize_content(content, sensitive_strings)
        code_block = sanitized_content
        review = get_openai_review(code_block)

        # Step 5: Incorporate OpenAI's response
        reviewed_content = f"## GPT review:\n\n{review}\n"
        results[file] = reviewed_content

    return results

# Run the processing and print the results
processed_results = process_files(files_to_scan)

for file, content in processed_results.items():
    print(f"# File: {file}\n\n{content}\n{'='*80}\n")
