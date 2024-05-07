import os
import requests
import csv
import json
import logging
import re
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv('API_KEY')
CSE_ID = os.getenv('CUSTOM_SEARCH_ENGINE_ID')
print("CSE_ID:", CSE_ID) 

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
    fieldnames = ['title', 'link', 'snippet', 'followers', 'following', 'posts', 'emails']
    try:
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:  # Check if file is empty to write header
                writer.writeheader()
            for item in data['items']:
                snippet = item['snippet']
                emails = re.findall(r'[\w\.-]+@[\w\.-]+', snippet)
                followers = re.search(r'(\d+) followers', snippet).group(1) if re.search(r'(\d+) followers', snippet) else ''
                following = re.search(r'(\d+) following', snippet).group(1) if re.search(r'(\d+) following', snippet) else ''
                posts = re.search(r'(\d+) posts', snippet).group(1) if re.search(r'(\d+) posts', snippet) else ''
                
                writer.writerow({
                    'title': item['title'],
                    'link': item['link'],
                    'snippet': snippet,
                    'followers': followers,
                    'following': following,
                    'posts': posts,
                    'emails': ', '.join(emails)
                })
        return len(data['items'])
    except Exception as e:
        logging.error(f"Failed to write to CSV: {e}")
        return 0

def run_search(site, keyword, domain, project, number_of_pages):
    api_key = API_KEY
    cx = CSE_ID
    script_dir = os.path.dirname(os.path.realpath(__file__))
    results_dir = os.path.join(script_dir, 'results')  # Path to the results directory
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)  # Create the directory if it does not exist

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(results_dir, f'{project}_{timestamp}.csv')  # Save files in the 'results' directory
    start = 1
    total_results_added = 0
    for _ in range(number_of_pages):
        data = google_custom_search(site, keyword, domain, api_key, cx, start)
        if data and 'items' in data:
            results_added = save_to_csv(data, filename)
            total_results_added += results_added
            start += 10  # Assuming 10 results per page
        else:
            break
    print(f"Results saved to {filename}\nTotal results added: {total_results_added}")