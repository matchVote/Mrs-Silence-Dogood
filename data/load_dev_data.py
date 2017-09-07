import csv

from dogood.models import Official

print('Loading Official names... ', end='')
Official.delete().execute()
with open('data/rep_names.csv') as f:
    rows = csv.reader(f)
    next(rows)
    for first_name, last_name in rows:
        Official.create(first_name=first_name, last_name=last_name)
print(f'{len(Official.select())} total')
