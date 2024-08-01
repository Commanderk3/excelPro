import re
import os
import pandas as pd
import csv
import json
from io import StringIO
from pdfminer.high_level import extract_text
from gemini_module import create_model, send_message

###################################################################################################

def check_and_create_csv(filename):
    header = ['Name']
    rows = [' ']
    # Check if the file exists
    if not os.path.isfile(filename):
        # If it does not exist, create it and write the dictionary to it
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(rows)

        print(f"{filename} did not exist and has been created with the provided data.")
    else:
        print(f"{filename} already exists.")


check_and_create_csv('output.csv')


# Create the model
model = create_model()

# Extract text from the PDF file
pdf_path = 'demo2.pdf'
text = extract_text(pdf_path)

# Example text with special characters
text_with_special_chars = text

# Define a regular expression pattern to match non-ASCII characters
pattern = re.compile(r'[^\x20-\x7E]')


# Replace all non-ASCII characters with a hyphen

### Note: The output of text_replaced contain double hyphen '->->' before and after in some words

text_replaced = pattern.sub('->', text_with_special_chars)
response = send_message(model, text_replaced )


# Use StringIO to treat the string as a file-like object
data = StringIO(response)

# Convert string to dictionary
data_dict = json.loads(response)




###### MERGING DATAS AND WRITING

#### Reading csv file and storing in dictionary
file_path = 'output.csv'

# List to store the dictionaries
data_list = []

####



# dict2 is the output given by gemini
dict2 = [data_dict]

#--


# Function to read CSV and convert it to a list of dictionaries
def read_csv_to_list(file_path):
    data_list = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data_list.append(dict(row))
    return data_list

# Function to merge lists of dictionaries
def merge_dicts(list1, list2):
    all_keys = set()
    for d in list1 + list2:
        all_keys.update(d.keys())
    
    merged_dict = {key: [] for key in all_keys}
    
    for d in list1:
        for key in all_keys:
            merged_dict[key].append(d.get(key, " "))
    
    for d in list2:
        for key in all_keys:
            merged_dict[key].append(d.get(key, " "))
            
    return merged_dict

# Function to write the merged dictionary to a CSV file
def write_dict_to_csv(data_dict, filename):
    headers = list(data_dict.keys())
    num_rows = len(next(iter(data_dict.values())))

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for i in range(num_rows):
            row = [data_dict[key][i] for key in headers]
            writer.writerow(row)

# Example usage:
file_path = 'output.csv'

# Read the existing CSV file
dict1 = read_csv_to_list(file_path)


# Merge dictionaries
merged_dict = merge_dicts(dict1, dict2)
print("Merged Dictionary:", merged_dict)

# Write the merged dictionary back to the CSV file
write_dict_to_csv(merged_dict, file_path)
print(f"Data written to {file_path}")
