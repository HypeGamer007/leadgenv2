import os
import threading
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

def google_custom_search_v2(site, keyword, domain, api_key, cx, start):
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

def save_to_csv_v2(items, filename, csv_lock):
    fieldnames = ['title', 'link', 'snippet', 'followers', 'following', 'posts', 'emails']
    try:
        with csv_lock:
            with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if csvfile.tell() == 0:  # Check if file is empty to write header
                    writer.writeheader()
                for item in items:
                    # Extracting details from 'og:description'
                    description = item.get('pagemap', {}).get('metatags', [{}])[0].get('og:description', '')
                    followers = re.search(r'(\d+(?:,\d+)*) Followers', description)
                    following = re.search(r'(\d+(?:,\d+)*) Following', description)
                    posts = re.search(r'(\d+(?:,\d+)*) Posts', description)
                    emails = re.findall(r'[\w\.-]+@[\w\.-]+', item.get('snippet', ''))

                    writer.writerow({
                        'title': item.get('title', ''),
                        'link': item.get('link', ''),
                        'snippet': item.get('snippet', ''),
                        'followers': followers.group(1) if followers else '',
                        'following': following.group(1) if following else '',
                        'posts': posts.group(1) if posts else '',
                        'emails': ', '.join(emails)
                    })
        return len(items)
    except Exception as e:
        logging.error(f"Failed to write to CSV: {e}")
        return 0

def run_search_v2(site, keyword, domain, project):
    api_key = API_KEY
    cx = CSE_ID
    total_results_added = 0

    script_dir = os.path.dirname(os.path.realpath(__file__))
    results_dir = os.path.join(script_dir, 'results')
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    filename = os.path.join(results_dir, f'{project}.csv')

    csv_lock = threading.Lock()

    # Create and start the worker threads
    threads = []
    for i in range(6):  # Create 6 threads
        start_index = i * 10 + 1  # Calculate the start index for this thread
        t = threading.Thread(target=worker, args=(i + 1, site, keyword, domain, start_index, filename, csv_lock))
        t.start()
        threads.append(t)

    # Wait for all threads to finish
    for t in threads:
        t.join()

    logging.info(f"Search completed for project {project}. Results saved to {filename}. Total results added: {total_results_added}.")

def worker(thread_id, site, keyword, domain, start_index, filename, csv_lock):
    logging.info(f"Thread {thread_id} started with query: {keyword} starting at index {start_index}")
    while True:
        with csv_lock:
            if start_index > 60:  # Limit the number of pages to 10 per thread
                logging.info(f"Thread {thread_id} completed its execution.")
                return
            data = google_custom_search_v2(site, keyword, domain, API_KEY, CSE_ID, start_index)
            if data and 'items' in data:
                results_added = save_to_csv_v2(data['items'], filename, csv_lock)
                total_results_added += results_added
                start_index += 10  # Prepare the start index for the next page
            else:
                logging.info(f"Thread {thread_id} found no more data or encountered an error.")
                return

