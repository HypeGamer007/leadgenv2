#!/usr/bin/env python3
from nicegui import ui
from googlecustomsearch import run_search
from googlecustomsearch_v2 import run_search_v2
from database import get_csv_files_info
import os

with ui.header().classes(replace='row items-center') as header:
    ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
    with ui.tabs() as tabs:
        ui.tab('Google Search Engine')
        ui.tab('Bing Serch Engine')
        ui.tab('Yahoo Search Engine')
        ui.tab('Database')

with ui.footer(value=False) as footer:
    ui.label('Footer')

with ui.left_drawer().classes('bg-blue-100') as left_drawer:
    ui.label('Side menu')

with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    ui.button(on_click=footer.toggle, icon='contact_support').props('fab')

# all logic for Google Custom Search: Inputted info builds out the query and performs the search.
# Version 1 Logic
def on_search_click():
    site = site_entry.value
    keyword = keyword_entry.value
    domain = domain_entry.value
    project = project_entry.value
    number_of_pages = int(pages_entry.value)  # Ensure conversion to integer
    message = run_search(site, keyword, domain, project, number_of_pages)
    ui.notify(message)

# Version 2 Logic
def on_search_click_2():
    site = site_entry.value
    keyword = keyword_entry.value
    domain = domain_entry.value
    project = project_entry.value
    # number_of_pages = int(pages_entry.value)  # Ensure conversion to integer
    # message = run_search_v2(site, keyword, domain, project, number_of_pages)
    message = run_search_v2(site, keyword, domain, project)
    ui.notify(message)

with ui.tab_panels(tabs, value='A').classes('w-full'):
    # UI Layout for Google Search Engine 
    with ui.tab_panel('Google Search Engine'):
        with ui.row().classes('flex w-full justify-between'):
            with ui.column().classes('flex-1 p-2'):
                ui.label('GSE Lite: Max 100 Results')
                with ui.card().classes('p-4'):
                    site_entry = ui.input(label='Site:', placeholder='instagram.com')
                    keyword_entry = ui.input(label='Keyword:', placeholder='esports')
                    domain_entry = ui.input(label='Email Domain:', placeholder='@gmail.com')
                    project_entry = ui.input(label='Project Name:', placeholder='Enter project name')
                    pages_entry = ui.input(label='Number of Pages:', placeholder='1')
                    ui.button('Search', on_click=on_search_click)

            with ui.column().classes('flex-1 p-2'):
                ui.label('GSE Pro: Unlimited Results')
                with ui.card().classes('p-4'):
                    site_entry = ui.input(label='Site:', placeholder='instagram.com')
                    keyword_entry = ui.input(label='Keyword:', placeholder='esports')
                    domain_entry = ui.input(label='Email Domain:', placeholder='@gmail.com')
                    project_entry = ui.input(label='Project Name:', placeholder='Enter project name')
                    # pages_entry = ui.input(label='Number of Pages:', placeholder='1')
                    ui.button('Search', on_click=on_search_click_2)

    with ui.tab_panel('Bing Serch Engine'):
        ui.label('Content of Bing Serch Engine')

    with ui.tab_panel('Yahoo Search Engine'):
        ui.label('Yahoo Search Engine')

    with ui.tab_panel('Database'):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        results_dir = os.path.join(script_dir, 'results')
        print(f"Looking in directory: {results_dir}")
        csv_files = get_csv_files_info(results_dir)  # Use the results directory        columns = [
        columns = [
            {'name': 'name', 'label': 'File Name'},
            {'name': 'timestamp', 'label': 'Timestamp'},
            {'name': 'record_count', 'label': 'Record Count'}
        ]
        ui.table(columns=columns, rows=csv_files)

ui.run()