import csv
import json

input_file_name = "naver_review.csv"
output_file_name = "naver_review.json"

with open(input_file_name, "r", encoding="utf-8", newline="") as input_file, \
        open(output_file_name, "w", encoding="utf-8", newline="") as output_file:
    reader = csv.reader(input_file)

    # 첫 줄은 col_names 리스트로 읽어 놓고
    col_names = next(reader)
    formatted_doc = []

    # 그 다음 줄부터 zip으로 묶어서 json으로 dumps
    for cols in reader:
        doc = {col_name: col for col_name, col in zip(col_names, cols)}
        formatted_doc.append(doc)

    json.dump(formatted_doc, output_file, ensure_ascii=False, sort_keys=True, indent=4)
