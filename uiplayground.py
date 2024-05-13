#!/usr/bin/env python3
from nicegui import ui
from googlecustomsearch import google_custom_search
from save_to_csv import save_to_csv
import os
from datetime import datetime
from database import columns, rows

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
        table.visible = False  # Assuming 'table' is the variable holding your table component
    elif tab_value == 'Database':
        table.visible = True

# def setup_ui():
#     # Add the setup logic for the UI components here
#     pass  # Placeholder for the actual setup code

with ui.header().classes(replace='row items-center') as header:
    ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
    with ui.tabs() as tabs:
        google_tab = ui.tab('Google Search')
        database_tab = ui.tab('Database')
        tabs.on('change', on_tab_change)  # Use 'on' method to handle tab change event

with ui.footer(value=False) as footer:
    ui.label('Footer')

# with ui.left_drawer().classes('bg-blue-100') as left_drawer:
#     ui.label('Side menu')

# with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
#     ui.button(on_click=footer.toggle, icon='contact_support').props('fab')

with ui.tab_panels(tabs, value='Google Search') as tab_panels:
    with ui.tab_panel('Google Search'):
        # Add the search UI logic here
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
            pages_entry = ui.number('Number of Pages', min=1, step=1)

        ui.button('Search', on_click=run_search)

        global output_log
        output_log = ui.label()

    with ui.tab_panel('Database'):
        # Define the table here to ensure it's only available in the 'Database' tab
        with ui.table(title='Master Database', columns=columns, rows=rows, selection='multiple', pagination=10).classes('w-full') as table:
            with table.add_slot('top-right'):
                with ui.input(placeholder='Search').props('type=search').bind_value(table, 'filter').add_slot('append'):
                    ui.icon('search')

tabs.on('change', on_tab_change)
ui.run()
