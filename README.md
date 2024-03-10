# cis6930sp24 -- Project1 -- Template

### Name - Omkar Sunil Bhabad

## Description 
"The Censoror" is a privacy-focused tool created to automatically hide personal information in text files. It uses advanced technology like spaCy for text analysis, Google Cloud's Natural Language API for recognizing different types of data, and pyap for finding addresses. This makes "The Censoror" very good at spotting and hiding names, dates, phone numbers, and addresses. It's designed to be simple to use and works quickly, making it perfect for anyone needing to keep information private in documents. Whether for a single file or many, "The Censoror" helps ensure sensitive details are kept confidential.

## How to install
1. Ensure Python 3.x is installed on your system. Check this by running `python --version` in your terminal.
2. Clone the project repository to your local machine from its GitHub page.
3. Execute `pipenv install` to create a virtual environment and install dependencies.
4. Activate the environment with `pipenv shell`.
5. Navigate to the project's root directory in your terminal.
6. "The Censoror" relies on the spaCy NLP library. Download the required English model by running the command `python -m spacy download en_core_web_md`.
7. Place your Google Cloud service account key file (spherical-gate-416621-bf139b8e78c0.json) in the project directory.
8. Execute the script by running `pipenv run python censoror.py --input '*.txt' --names --dates --phones --address --output 'files/' --stats stderr`.

