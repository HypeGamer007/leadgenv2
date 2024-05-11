from nicegui import ui
import os
import requests
import csv
from datetime import datetime
import logging
import re
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging to display debug messages
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Placeholder function for Google Search button logic
def google_search():
    print("Google Search button clicked")  # Placeholder action

# Create input fields
with ui.row():
    ui.label('Site:').style('width: 100px')
    site_entry = ui.input()
    
    # Button with an icon 
    instagram_button = ui.button('Instagram', on_click=lambda: set_site('instagram.com'))
    facebook_button = ui.button('Facebook', on_click=lambda: set_site('facebook.com'))
    twitter_button = ui.button('Twitter', on_click=lambda: set_site('twitter.com'))
    tiktok_button = ui.button('TikTok', on_click=lambda: set_site('tiktok.com'))
    linkedin_button = ui.button('Linkedin', on_click=lambda: set_site('linkedin.com'))
    youtube_button = ui.button('Youtube', on_click=lambda: set_site('youtube.com'))
    pinterest_button = ui.button('Pinterest', on_click=lambda: set_site('pinterest.com'))
    reddit_button = ui.button('Reddit', on_click=lambda: set_site('reddit.com'))
    tumblr_button = ui.button('Tumblr', on_click=lambda: set_site('tumblr.com'))
    whatsapp_button = ui.button('WhatsApp', on_click=lambda: set_site('whatsapp.com'))
    discord_button = ui.button('Discord', on_click=lambda: set_site('discord.gg'))
    twitch_button = ui.button('Twitch', on_click=lambda: set_site('twitch.tv'))
    flickr_button = ui.button('Flickr', on_click=lambda: set_site('flickr.com'))
    quora_button = ui.button('Quora', on_click=lambda: set_site('quora.com'))
    vimeo_button = ui.button('Vimeo', on_click=lambda: set_site('vimeo.com'))
    meetup_button = ui.button('Meetup', on_click=lambda: set_site('meetup.com'))
    goodreads_button = ui.button('Goodreads', on_click=lambda: set_site('goodreads.com'))
    nextdoor_button = ui.button('Nextdoor', on_click=lambda: set_site('nextdoor.com'))    

def set_site(site):
    site_entry.value = site
    site_entry.emit('input')  # Optionally trigger any input event handlers

def clear_if_preset():
    if site_entry.value == 'instagram.com':
        site_entry.value = ''

site_entry.on('focus', clear_if_preset)

with ui.row():
    ui.label('Keyword:').style('width: 100px')
    keyword_entry = ui.input()

with ui.row():
    ui.label('Domain:').style('width: 100px')
    domain_entry = ui.input()

with ui.row():
    ui.label('Run Name:').style('width: 100px')
    run_name_entry = ui.input()

with ui.row():
    ui.label('Number of Pages:').style('width: 100px')
    pages_entry = ui.input()

# Buttons
with ui.row():
    ui.button('Search', on_click=lambda: run_search())

# Output log
output_log = ui.label()

# Search history table
search_history_table = ui.table(['Timestamp', 'Keyword', 'Run Name', 'CSV File', 'Total Results Added'], rows=[])

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
                
                # Write extracted data to CSV
                writer.writerow({'title': item['title'], 'link': item['link'], 'snippet': snippet, 'followers': followers, 'following': following, 'posts': posts, 'emails': ', '.join(emails)})
        return len(data['items'])
    except Exception as e:
        logging.error(f"Failed to write to CSV: {e}")
        return 0

def run_search():
    site = site_entry.value
    keyword = keyword_entry.value
    domain = domain_entry.value
    run_name = run_name_entry.value
    api_key = os.getenv("API_KEY")
    cx = os.getenv("CUSTOM_SEARCH_ENGINE_ID")
    number_of_pages = int(pages_entry.value)
    script_dir = os.path.dirname(os.path.realpath(__file__))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(script_dir, f'{run_name}_{timestamp}.csv')
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
    output_log.set_text(f"Results saved to {filename}\nTotal results added: {total_results_added}")
    search_history_table.add_rows([timestamp, keyword, run_name, filename, total_results_added])
    

ui.run(title='Google Custom Search', port=8080)



