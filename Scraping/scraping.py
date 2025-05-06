import os
import json
import re

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import networkx as nx
import string
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

START_URLS = [
    "https://www.bbc.com/",
    "https://www.foxnews.com/",
    "https://edition.cnn.com/",
    "https://news.sky.com/",
    "https://www.uefa.com/uefachampionsleague/"
]

MAX_PAGES = 100
CONTENT_DIR = "../output/content"

if not os.path.exists(CONTENT_DIR):
    os.makedirs(CONTENT_DIR)

pages_to_visit = START_URLS[:]
visited_pages = set()
links_graph = {}
file_index = 1
url_to_file_map = {}

def fetch_page(url):
    try:
        response = requests.get(url, timeout=3)
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def save_content(url, content):
    global file_index
    file_name = f"{file_index}.txt"
    file_id = str(file_index)  # بدون .txt
    file_path = os.path.join(CONTENT_DIR, file_name)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        url_to_file_map[url] = file_id
        file_index += 1
    except Exception as e:
        print(f"Error saving content for {url}: {e}")

def clean_text(soup):
    for tag in soup(["script", "style", "noscript", "meta", "link", "img", "iframe",
                     "svg", "video", "audio", "object", "embed", "applet", "area",
                     "map", "param", "track", "source", "canvas", "math"]):
        tag.decompose()

    text = soup.get_text(separator=' ')  # ← نضمن إن السطور متفصلة
    text = text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))  # ← نبدل الترقيم بمسافات
    text = re.sub(r'\s+', ' ', text)  # ← نزيل المسافات المكررة

    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]

    return " ".join(filtered_words)


def process_page(url):
    if url in visited_pages:
        return

    print(f"Visiting: {url}")
    soup = fetch_page(url)
    if soup is None:
        return

    visited_pages.add(url)
    links_graph[url] = []

    content = clean_text(soup)
    save_content(url, content)

    for link in soup.find_all("a", href=True):
        href = link.get("href")
        try:
            absolute_url = urljoin(url, href)
            if absolute_url not in visited_pages and absolute_url not in pages_to_visit:
                pages_to_visit.append(absolute_url)
                links_graph[url].append(absolute_url)
        except Exception as e:
            print(f"Error parsing URL {href} on {url}: {e}")

def calculate_page_rank(graph, file_map):
    g = nx.DiGraph()
    for src, targets in graph.items():
        if src not in visited_pages:
            continue
        for dst in targets:
            if dst in visited_pages:
                g.add_edge(src, dst)

    pr = nx.pagerank(g)

    combined = {}
    for url, score in pr.items():
        combined[url] = {
            "page_rank": score,
            "file_name": file_map.get(url, None)
        }

    with open("../output/Urlswithranks.json", "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2)
    print("✅ Combined PageRank and file map saved to Urlswithranks.json.")

def crawl():
    while pages_to_visit and len(visited_pages) < MAX_PAGES:
        batch = pages_to_visit[:5]
        del pages_to_visit[:5]
        for url in batch:
            process_page(url)

    print("Crawling finished.")

    with open("../output/links_graph.json", "w", encoding="utf-8") as f:
        json.dump(links_graph, f, indent=2)

    calculate_page_rank(links_graph, url_to_file_map)

crawl()