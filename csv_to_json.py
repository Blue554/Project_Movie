import csv
import json
import datetime
import os

d_today = datetime.date.today()
yesterday = d_today - datetime.timedelta(1)
d_date = yesterday.strftime("%Y%m%d")

input_file_name = "./naver_review/"+d_date+"_naver_review.csv"
output_file_name = "./naver_review/"+d_date+"_naver_review.json"

with open(input_file_name, "r", encoding="utf-8", newline="") as input_file, \
        open(output_file_name, "w", encoding="utf-8", newline="") as output_file:
    reader = csv.reader(input_file)

    col_names = next(reader)
    formatted_doc = []

    for cols in reader:
        doc = {col_name: col for col_name, col in zip(col_names, cols)}
        formatted_doc.append(doc)

    json.dump(formatted_doc, output_file, ensure_ascii=False, sort_keys=True, indent=4)
