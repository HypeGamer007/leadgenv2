import csv

# Function to get columns for the table
def get_columns():
    return [
        {'name': 'Name', 'label': 'Name', 'field': 'Name', 'required': True},
        {'name': 'Link', 'label': 'Link', 'field': 'Link'},
        {'name': 'Description', 'label': 'Description', 'field': 'Description'},
        {'name': 'Followers', 'label': 'Followers', 'field': 'Followers'},
        {'name': 'Following', 'label': 'Following', 'field': 'Following'},
        {'name': 'Posts', 'label': 'Posts', 'field': 'Posts'},
        {'name': 'Email', 'label': 'Email', 'field': 'Email'}
    ]

# Function to get rows for the table
def get_rows():
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
        return rows

