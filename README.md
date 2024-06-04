# GPTreview
Code linter for any kind of code or modeling language using openAI API

## Specs
* Can be used containerized in a runner (Github actions etc.)
* Scan provided directory for all files with extensions .py .tf .sh .json and .yaml
* Remove all sesitive strings and IPs based on user provided data
* Provide a code review for every file in a markdown format like a "Senior developer"

## Usage
Set your environment variables: 
```
SENSITIVE_STRINGS="string,password,name,anything" 
OPENAI_API_KEY="xxxxxxxxx_your_key_xxxxxx"
```
run:
```
gptreview.py -d /folderpath/foldername
```
