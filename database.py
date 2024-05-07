import os
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)

def get_csv_files_info(directory):
    logging.debug(f"Scanning directory: {directory}")
    csv_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            filepath = os.path.join(directory, filename)
            try:
                record_count = sum(1 for line in open(filepath, encoding='utf-8')) - 1  # Subtract 1 for the header
                timestamp = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
                csv_files.append({'name': filename, 'timestamp': timestamp, 'record_count': record_count})
                logging.debug(f"Added file: {filename}, Records: {record_count}, Timestamp: {timestamp}")
            except Exception as e:
                logging.error(f"Error processing file {filename}: {e}")
    return csv_files