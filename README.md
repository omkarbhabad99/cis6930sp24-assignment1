# cis6930sp24 -- Project1 -- Template

### Name - Omkar Sunil Bhabad

## Description 
"The Censoror" is a privacy-focused tool created to automatically hide personal information in text files. It uses advanced technology like spaCy for text analysis, Google Cloud's Natural Language API for recognizing different types of data, and pyap for finding addresses. This makes "The Censoror" very good at spotting and hiding names, dates, phone numbers, and addresses. It's designed to be simple to use and works quickly, making it perfect for anyone needing to keep information private in documents. Whether for a single file or many, "The Censoror" helps ensure sensitive details are kept confidential.

## How to run
1. Ensure Python 3.x is installed on your system. Check this by running `python --version` in your terminal.
2. Clone the project repository to your local machine from its GitHub page.
3. Execute `pipenv install` to create a virtual environment and install dependencies.
4. Activate the environment with `pipenv shell`.
5. Navigate to the project's root directory in your terminal.
6. "The Censoror" relies on the spaCy NLP library. Download the required English model by running the command `python -m spacy download en_core_web_md`.
7. Place your Google Cloud service account key file (spherical-gate-416621-bf139b8e78c0.json) in the project directory.
8. Then, set the environment variable to point to your JSON key file: Using powershell `$env:GOOGLE_APPLICATION_CREDENTIALS="spherical-gate-416621-bf139b8e78c0.json"`
9. Execute the script by running `pipenv run python censoror.py --input '*.txt' --names --dates --phones --address --output 'files/' --stats stderr`.

## Code flow overview
"The Censoror" starts its operation by parsing command-line arguments that specify the input files, types of sensitive information to censor (names, dates, phone numbers, and addresses), and the output directory. Here’s how the code flows from start to finish:

1. **Input Parsing**: The user's preferences, including the types of entities to censor and the locations for input and output files, are collected through command-line arguments in the `main` function.
   
2. **Processing Files**: Based on the input pattern, the script identifies the relevant text files and iterates over each. For every file, the content is read and passed through a series of censorship functions, each targeting a specific type of sensitive information as directed by the user's flags.

3. **Utilizing Libraries**:
   - **spaCy**: Loaded at the beginning, the spaCy library is essential for understanding the structure of the text and identifying entities that might not be covered by regular expressions or the Google Cloud Natural Language API.
   - **pyap**: Specifically used for detecting and censoring physical addresses within the text, highlighting the script's capability to target location-based information accurately.
   - **Google Cloud Natural Language API**: Engaged for its sophisticated entity recognition capabilities, enabling the script to identify and censor personal names and dates effectively.

4. **Entity Censorship**: As the document's content is passed through each censorship function, entities identified as sensitive are replaced with a block character (`█`). This ensures that the specific information types flagged by the user are concealed.

5. **Output Generation**: Once the document is fully processed, the censored content is saved to a new file with the same name as the original but appended with `.censored` in the designated output directory. This process is repeated for all files matching the input pattern.

6. **Statistics Reporting**: If enabled, the script tallies the number of entities censored for each category and displays these counts either on the console or writes them to a specified file, offering insights into the censorship process's extent.

## Functions
### main
- **Purpose**: Orchestrates the entire censoring process. It interprets command-line inputs from the user, specifying what types of data to censor and where to find and save files.
  
### process_files
- **Purpose**: Manages the workflow for each file specified in the input. Reads content from each file, applies censorship based on user-defined criteria, and saves the censored content to a new file in the designated output directory. It's where the application's loop over files and subsequent actions begin.

### censor_document
- **Purpose**: The heart of the censorship process, where the document's text is sequentially processed to censor specified entities. It invokes various functions tailored to censor different types of sensitive information, ensuring each selected category (names, dates, phone numbers, and addresses) is adequately redacted from the document.

### censor_email_addresses
- **Purpose**: Utilizes a regex pattern to find and censor email addresses in the text. It's crucial for removing personal contact information, enhancing the privacy of communications detailed within the documents.

### censor_addresses
- **Purpose**: Leverages the `pyap` library to detect and redact physical addresses. This function is particularly important for protecting location data, a key aspect of personal privacy.

### censor_google_entities
- **Purpose**: Integrates with Google Cloud's Natural Language API to identify and censor personal names and dates. This function exemplifies the use of external AI services to enhance the application's ability to understand and process natural language for privacy protection.

### censor_phone_numbers
- **Purpose**: Applies regex to identify and censor various phone number formats present in the text. It plays a critical role in ensuring that personal contact numbers are not exposed in the censored documents.

## Testing Functions

tests are designed to verify the functionality of each censorship feature—names, dates, phone numbers, and addresses—using a suite of predefined text examples. Designed to be executed with `pipenv run python -m pytest`, these tests offer a systematic approach to validate each part of the censoring process, covering a range of scenarios to ensure robustness and reliability.

### Test Files Overview

1. **test_names.py**: 
   - **test_censor_single_name**: Validates that a single name within a sentence is correctly identified and censored.
   - **test_censor_full_name**: Ensures that full names, including first and last names, are accurately detected and censored, demonstrating the script's ability to handle multi-word entities.

2. **test_phones.py**:
   - **test_censor_simple_phone**: Checks the script's ability to recognize and censor phone numbers in a straightforward pattern.
   - **test_censor_formatted_phone**: Tests the censoring of phone numbers that are formatted with parentheses and dashes, assessing the flexibility of the phone number detection logic.

3. **test_address.py**:
   - **test_censor_address**: Verifies that physical addresses are correctly identified and censored, regardless of their complexity.
   - **test_censor_address_with_punctuation**: Assesses the script's capability to censor addresses that include punctuation, ensuring that the entire address is censored accurately.

4. **test_dates.py**:
   - **test_censor_simple_date**: Focuses on the script's ability to detect and censor dates in a simple numeric format.
   - **test_censor_full_date**: Evaluates the censoring of fully written dates, including those with month names and ordinal numbers, testing the script's natural language processing capabilities.







