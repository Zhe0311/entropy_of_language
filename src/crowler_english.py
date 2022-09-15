from curses.ascii import isalpha
from symbol import del_stmt
from unicodedata import category
import requests
from concurrent import futures
import xml.etree.ElementTree as ET
import re
import json

def getAllTitle(path: str) -> list:
    '''get all titles from .src'''
    titles = []
    for line in open(path):  
        titles.append(line.split(" <EOT>")[0])
    return titles

def getSingleText(title: str, index: int, length: int) -> list:
    if index % 100 == 0:
        print(str(index) + '/' + str(length) + '  done')
    text = []
    url = 'https://lookup.dbpedia.org/api/search?query=' + title
    try:
        res = requests.get(url, timeout = 10)
        root = ET.fromstring(res.content)
        for i, result in enumerate(root):
            des = result.findall('Description')
            text += [item.text for item in des if item != '']
        return text
    except:
        return None

def getAllTextMultithread(titles: list, max_workers: int) -> list:
    executor = futures.ThreadPoolExecutor(max_workers=max_workers)
    fs = []
    for i, title in enumerate(titles):
        args = [title, i, len(titles)]
        f = executor.submit(lambda p: getSingleText(*p), args)
        fs.append(f)

    futures.wait(fs)
    results = [f.result() for f in fs]
    return results

def sameCategoryNumber(categories_A, categories_B):
    return len(list(set(categories_A).intersection(set(categories_B))))

if __name__ == "__main__":

    source_titles = getAllTitle('train.src')
    print(len(source_titles))
    source_categories = getAllTextMultithread(source_titles[12000: 20000], 50)

    texts = []
    for text_list in source_categories:
        if text_list != None:
            for text in text_list:
                if text != None:
                    texts.append(''.join(re.findall(r'[A-Za-z]', text)))
    with open('all_english_corpus_2w.json', 'w') as f:
        json.dump(texts, f)