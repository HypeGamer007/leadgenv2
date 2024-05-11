import csv
from nicegui import ui  # Import the ui module

# Read data from master_database.csv
with open('master_database.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = []
    for row in reader:
        formatted_row = {
            'Name': row.get('title', ''),
            'Link': row.get('link', ''),
            'Description': row.get('snippet', ''),
            'Followers': row.get('followers', ''),
            'Following': row.get('following', ''),
            'Posts': row.get('posts', ''),
            'Email': row.get('emails', '')
        }
        rows.append(formatted_row)

# Define the columns
columns = [
    {'name': 'Name', 'label': 'Name', 'field': 'Name', 'required': True},
    {'name': 'Link', 'label': 'Link', 'field': 'Link'},
    {'name': 'Description', 'label': 'Description', 'field': 'Description'},
    {'name': 'Followers', 'label': 'Followers', 'field': 'Followers'},
    {'name': 'Following', 'label': 'Following', 'field': 'Following'},
    {'name': 'Posts', 'label': 'Posts', 'field': 'Posts'},
    {'name': 'Email', 'label': 'Email', 'field': 'Email'}
]

# Display data in a full-width table
with ui.table(title='My Team', columns=columns, rows=rows, selection='multiple', pagination=10).classes('w-full') as table:
    with table.add_slot('top-right'):
        with ui.input(placeholder='Search').props('type=search').bind_value(table, 'filter').add_slot('append'):
            ui.icon('search')
    with table.add_slot('bottom-row'):
        with table.row():
            with table.cell():
                ui.button(on_click=lambda: (
                    table.add_rows({'id': time.time(), 'Name': new_name.value, 'Link': new_link.value, 'Description': new_description.value, 'Followers': new_followers.value, 'Following': new_following.value, 'Posts': new_posts.value, 'Email': new_email.value}),
                    new_name.set_value(None),
                    new_link.set_value(None),
                    new_description.set_value(None),
                    new_followers.set_value(None),
                    new_following.set_value(None),
                    new_posts.set_value(None),
                    new_email.set_value(None),
                ), icon='add').props('flat fab-mini')
            with table.cell():
                new_name = ui.input('Name')
            with table.cell():
                new_link = ui.input('Link')
            with table.cell():
                new_description = ui.input('Description')
            with table.cell():
                new_followers = ui.input('Followers')
            with table.cell():
                new_following = ui.input('Following')
            with table.cell():
                new_posts = ui.input('Posts')
            with table.cell():
                new_email = ui.input('Email')

    # Toggle selection on checkbox click
    table.bind_filter(new_name, 'selected')

ui.label().bind_text_from(table, 'selected', lambda val: f'Current selection: {val}')
ui.button('Remove', on_click=lambda: table.remove_rows(*table.selected)) \
    .bind_visibility_from(table, 'selected', backward=lambda val: bool(val))

ui.run()
