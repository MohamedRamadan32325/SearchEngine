import os
import re
import csv
import json
import string
from collections import defaultdict
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

CONTENT_DIR = "content"

def convert_combined_json_to_csv(json_filename, csv_filename):
    with open(json_filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(csv_filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["URL", "PageRank", "FileName"])
        for url, info in data.items():
            writer.writerow([url, info.get("page_rank"), info.get("file_name")])

convert_combined_json_to_csv("../output/Urlswithranks.json", "../output/Urlswithranks.csv")
print("✅ Urlswithranks.json has been converted to Urlswithranks.csv")