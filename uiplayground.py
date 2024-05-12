#!/usr/bin/env python3
from nicegui import ui
from googlecustomsearch import google_custom_search
from save_to_csv import save_to_csv
import os
from datetime import datetime

def set_site(site_url):
    site_entry.value = site_url

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

def on_tab_change(tab_value):
    if tab_value == 'Google Search':
        tab_panels.set_value('A')
    elif tab_value == 'Database':
        tab_panels.set_value('B')

with ui.header().classes(replace='row items-center') as header:
    ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
    with ui.tabs() as tabs:
        google_tab = ui.tab('Google Search')
        database_tab = ui.tab('Database')
        tabs.on('change', on_tab_change)  # Use 'on' method to handle tab change event

with ui.footer(value=False) as footer:
    ui.label('Footer')

with ui.left_drawer().classes('bg-blue-100') as left_drawer:
    ui.label('Side menu')

with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    ui.button(on_click=footer.toggle, icon='contact_support').props('fab')

with ui.tab_panels(tabs, value='Google Search').classes('w-full') as tab_panels:
    with ui.tab_panel('Google Search'):
        with ui.row():
            ui.label('Site:').style('width: 100px')
            site_entry = ui.input()
            ui.button('Instagram', on_click=lambda: set_site('instagram.com'))
            # Add other buttons similarly

        with ui.row():
            keyword_entry = ui.input('Keyword')

        with ui.row():
            domain_entry = ui.input('Domain')

        with ui.row():
            run_name_entry = ui.input('Run Name')

        with ui.row():
            pages_entry = ui.number('Number of Pages', min=1, step=1)  # Use ui.number for numerical input

        ui.button('Search', on_click=run_search)

        output_log = ui.label()

        search_history_table = ui.table(['Timestamp', 'Keyword', 'Run Name', 'CSV File', 'Total Results Added'], rows=[])

    with ui.tab_panel('Database'):
        # Add code for database UI here

        ui.run()