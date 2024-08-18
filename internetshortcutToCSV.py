# Convert internet shortcut files to CSV. 
# Includes the filename with created and modification times. The contents are converted to a JSON string
# Copyright 2024, Phill Moore

# v0.01 - Initial commit

import os
import csv
import json
import configparser
from datetime import datetime
import argparse

def get_file_timestamps(file_path):
    created = os.path.getctime(file_path)
    modified = os.path.getmtime(file_path)
    return datetime.fromtimestamp(created), datetime.fromtimestamp(modified)

def parse_url_file(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return {section: dict(config.items(section)) for section in config.sections()}

def find_url_files(directory):
    url_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.url'):
                url_files.append(os.path.join(root, file))
    return url_files

def write_to_csv(url_files, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['file_path', 'created_timestamp', 'modified_timestamp', 'contents']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for file_path in url_files:
            created, modified = get_file_timestamps(file_path)
            contents = parse_url_file(file_path)
            writer.writerow({
                'file_path': file_path,
                'created_timestamp': created,
                'modified_timestamp': modified,
                'contents': json.dumps(contents)
            })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Locate and parse URL files')
    parser.add_argument('-d', dest='directory',help='Directory to search recursively from')
    parser.add_argument('-o', dest='output',default="url_files_info.csv", help='Output filename')

    args = parser.parse_args()
    directory = args.directory
    output_csv = args.output
    url_files = find_url_files(directory)
    write_to_csv(url_files, output_csv)
    print(f"CSV file '{output_csv}' has been created with the URL files information.")
