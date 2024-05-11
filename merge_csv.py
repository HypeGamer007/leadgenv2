import csv

def merge_csv_files(csv_files):
    database = []
s
    for file in csv_files:
        with open(file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                database.append(row)

    return database

def write_to_master_csv(database, master_filename):
    fieldnames = database[0].keys() if database else []
    
    with open(master_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in database:
            writer.writerow(row)