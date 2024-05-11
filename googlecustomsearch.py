import os
from dotenv import load_dotenv
import requests
import logging
import json
from datetime import datetime
import csv

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
API_KEY = os.getenv('API_KEY')
CUSTOM_SEARCH_ENGINE_ID = os.getenv('CUSTOM_SEARCH_ENGINE_ID')

def google_custom_search(site, keyword, domain, api_key, cx, start):
    query = f"site:{site} {keyword} \"{domain}\""
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}&start={start}&num=10&filter=1&fields=items(title,link,snippet,pagemap(metatags))"
    logging.debug(f"Constructed URL: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logging.debug(f"API Response: {json.dumps(data, indent=4)}")
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred during API request: {e}")
        return None

def save_to_csv(data, filename):
    try:
        with open(filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for item in data['items']:
                writer.writerow([item['title'], item['link'], item.get('snippet', '')])
        return len(data['items'])
    except Exception as e:
        logging.error(f"Failed to write to CSV: {e}")
        return 0