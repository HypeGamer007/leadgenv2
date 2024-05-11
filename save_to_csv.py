import csv
import logging
import re

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