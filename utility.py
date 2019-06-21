import re
import csv


tapology_output = "output/tapology.csv"
ufcstats_output = "output/ufcstats.csv"

def write_row(csv_name, row, mode):
    with open(csv_name, mode, encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)


def clean_str(str):
    return re.sub(' +', ' ', str.replace("\n", '').replace("\t", '').strip())
