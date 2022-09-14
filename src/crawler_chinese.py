import requests
from concurrent import futures
from bs4 import BeautifulSoup
import re
import json
import os

def getIndexList() -> list:
    """ get the indexes of essays to concatenate the complete URLs"""
    index_list = []
    success = 1
    while success < 2766:
        url = 'http://www.leleketang.com/zuowen/list30-0-0-' + str(success) + '-1.shtml'
        try:
            res = requests.get(url)
            index_list += re.findall("<a class=\"list_rating_5 ellipsis\" href=\"(.*?)\" title=", res.text, re.S)
            success += 1
            print('length: ', len(index_list))
            if success % 50 == 0:
                print('success: ' + str(success) + '/2766')
        except:
            print('Fail')
    return index_list

def getSingleEssay(index: str, i: int, length) -> list:
    if i % 50 == 0:
        print(str(i) + '/' + str(length) + '  done')
    url = 'http://www.leleketang.com/zuowen/' + index
    try:
        res = requests.get(url)
        return BeautifulSoup(re.findall("<div class=\"cp_content\">(.*?)</div>", res.text, re.S)[0], 'html.parser').get_text().replace('\n', '')
    except:
        pass


def getEssayMultithread(index_list: list, max_workers: int) -> list:
    executor = futures.ThreadPoolExecutor(max_workers=max_workers)
    fs = []
    for i, index in enumerate(index_list):
        args = [index, i, len(index_list)]
        f = executor.submit(lambda p: getSingleEssay(*p), args)
        fs.append(f)
    futures.wait(fs)
    results = [f.result() for f in fs]
    print('Total: ', len(results))
    return results

def sameCategoryNumber(categories_A, categories_B):
    return len(list(set(categories_A).intersection(set(categories_B))))

if __name__ == "__main__":

    index_list_path = '../data/index_list.json'

    if not os.path.lexists(index_list_path):
        res = getIndexList()
        json.dump(res, open(index_list_path, 'w'))
    
    if os.path.lexists(index_list_path):
        index_list = json.load(open(index_list_path))
    
    print(len(index_list))

    essays = getEssayMultithread(index_list, 5)
    with open('../data/chinese_corpus.json', 'w') as f:
        json.dump(essays, f, ensure_ascii=False)