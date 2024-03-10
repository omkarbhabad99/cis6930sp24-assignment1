import spacy
from google.cloud import language_v1
from google.cloud.language_v1 import types
import argparse
import glob
import os
import pyap
import re
import sys
import spacy.cli

# Load the transformer-based spaCy model
spacy.cli.download("en_core_web_trf")
nlp = spacy.load("en_core_web_trf")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'spherical-gate-416621-bf139b8e78c0.json'

# Initialize the Google NLP client
google_nlp_client = language_v1.LanguageServiceClient()

# Entity counters
entity_counters = {
    'NAMES': 0,
    'DATES': 0,
    'ADDRESSES': 0,
    'PHONE_NUMBERS': 0,
}

def censor_email_addresses(text):
    """Censors email addresses in the text using a regex pattern."""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.sub(email_pattern, "███████", text)

def censor_addresses(text, entity_counters):
    """Censors physical addresses using pyap."""
    addresses = pyap.parse(text, country='US')
    for address in addresses:
        text = re.sub(re.escape(str(address)), "█" * len(str(address)), text, flags=re.IGNORECASE)
        entity_counters['ADDRESSES'] += 1
    return text

def censor_google_entities(text, entity_counters):
    """Uses Google Cloud Natural Language API to censor entities."""
    document = types.Document(content=text, type_=types.Document.Type.PLAIN_TEXT)
    response = google_nlp_client.analyze_entities(document=document)
    for entity in response.entities:
        if entity.type == language_v1.Entity.Type.PERSON:
            text = text.replace(entity.name, "█" * len(entity.name))
            entity_counters['NAMES'] += 1
        elif entity.type == language_v1.Entity.Type.DATE:
            text = text.replace(entity.name, "█" * len(entity.name))
            entity_counters['DATES'] += 1
    return text

def censor_phone_numbers(text, entity_counters):
    """Censors phone numbers in the text."""
    phone_number_pattern = r'\b(?:\d{3}[-\s.]*){2}\d{4}\b|\(\d{3}\)\s*\d{3}[-\s.]*\d{4}\b|\d{10}\b|\(\d{3}\)[-.\s]*\d{3}[-.\s]*\d{4}\b'
    matches = re.findall(phone_number_pattern, text)
    for match in matches:
        text = text.replace(match, "█" * len(match))
    entity_counters['PHONE_NUMBERS'] += len(matches)
    return text

def censor_document(text, entities_to_censor, entity_counters):
    """Censors the specified entities in a text."""
    text = censor_email_addresses(text)
    text = censor_addresses(text, entity_counters)
    text = censor_google_entities(text, entity_counters)
    text = censor_phone_numbers(text, entity_counters)
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in entities_to_censor:
            text = re.sub(re.escape(ent.text), "█" * len(ent.text), text, flags=re.IGNORECASE)
            # Increment counters based on entity type
            if ent.label_ == "PERSON":
                entity_counters['NAMES'] += 1
            elif ent.label_ == "DATE":
                entity_counters['DATES'] += 1
    return text

def process_files(input_pattern, output_dir, entities_to_censor):
    os.makedirs(output_dir, exist_ok=True)
    for file_path in glob.glob(input_pattern):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            censored_content = censor_document(content, entities_to_censor)
            output_file_name = os.path.splitext(os.path.basename(file_path))[0] + '.censored'
            output_path = os.path.join(output_dir, output_file_name)
            print("Saving censored content to:", output_path)  # Add this line
            with open(output_path, 'w', encoding='utf-8') as censored_file:
                censored_file.write(censored_content)
    
    # After processing all files, print the count of each entity type
    print("Entity counts:")
    for entity_type, count in entity_counters.items():
        print(f"{entity_type}: {count}")
    print(f"All files processed and saved in {output_dir}.")

def process_files(args):
    """Processes files and applies censorship based on specified arguments."""
    entities_to_censor = set()
    if args.names:
        entities_to_censor.add('PERSON')
    if args.dates:
        entities_to_censor.add('DATE')
    if args.phones:
        entities_to_censor.add('PHONE_NUMBER')
    if args.address:
        entities_to_censor.add('ADDRESS')

    input_files = glob.glob(args.input)
    for file_path in input_files:
        entity_counters = {'NAMES': 0, 'DATES': 0, 'ADDRESSES': 0, 'PHONE_NUMBERS': 0}
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            censored_text = censor_document(text, entities_to_censor, entity_counters)
        
        # Generate the output file name with the .censored extension
        base_name = os.path.splitext(os.path.basename(file_path))[0] + '.censored'

        if not os.path.exists(args.output):
            os.makedirs(args.output)
        output_file_path = os.path.join(args.output, base_name)
        
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(censored_text)
        
        if args.stats == 'stderr':
            print(f"Stats for {os.path.basename(file_path)}:", file=sys.stderr)
            for key, value in entity_counters.items():
                print(f"{key}: {value}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Censor sensitive information from text files.")
    parser.add_argument("--input", type=str, help="Input file pattern, e.g., '*.txt'")
    parser.add_argument("--output", type=str, help="Output directory for censored files")
    parser.add_argument("--names", action='store_true', help="Censor names")
    parser.add_argument("--dates", action='store_true', help="Censor dates")
    parser.add_argument("--phones", action='store_true', help="Censor phone numbers")
    parser.add_argument("--address", action='store_true', help="Censor addresses")
    parser.add_argument("--stats", type=str, help="Output stats to stderr if 'stderr'")
    args = parser.parse_args()


    
    process_files(args)

if __name__ == "__main__":
    main()