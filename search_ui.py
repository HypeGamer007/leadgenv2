from googlecustomsearch import google_custom_search
from save_to_csv import save_to_csv
import os
from datetime import datetime
from nicegui import ui

def set_site(site_url):
    site_entry.value = site_url

def run_search():
    site = site_entry.value
    keyword = keyword_entry.value
    domain = domain_entry.value
    api_key = os.getenv("API_KEY")
    cx = os.getenv("CUSTOM_SEARCH_ENGINE_ID")
    start = 1
    number_of_pages = int(pages_entry.value)
    script_dir = os.path.dirname(os.path.realpath(__file__))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(script_dir, f'{run_name_entry.value}_{timestamp}.csv')
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
    search_history_table.add_rows([timestamp, keyword, run_name_entry.value, filename, total_results_added])

    # Add the following code snippet after the existing code in run_search
    if data and 'items' in data:
        results_added = save_to_csv(data, filename)
        total_results_added += results_added
        # Continue with any additional processing or UI updates

def setup_ui():
    with ui.row():
        ui.label('Site:').style('width: 100px')
        global site_entry
        site_entry = ui.input()
        ui.button('Instagram', on_click=lambda: set_site('instagram.com'))
        # Add other buttons similarly

    with ui.row():
        global keyword_entry
        keyword_entry = ui.input('Keyword')

    with ui.row():
        global domain_entry
        domain_entry = ui.input('Domain')

    with ui.row():
        global run_name_entry
        run_name_entry = ui.input('Run Name')

    with ui.row():
        global pages_entry
        pages_entry = ui.number('Number of Pages', min=1, step=1)  # Use ui.number for numerical input

    ui.button('Search', on_click=run_search)

    global output_log
    output_log = ui.label()

    global search_history_table
    search_history_table = ui.table(['Timestamp', 'Keyword', 'Run Name', 'CSV File', 'Total Results Added'], rows=[])

    ui.run(title='Google Custom Search', port=8080)
    ui.run(title='Google Custom Search', port=8080)