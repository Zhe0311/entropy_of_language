import json
import numpy as np

def read_data(path: str):
    return [json.loads(line) for line in open(path).readlines()]
    # return json.load(open(path))

def get_chinese_vocab(corpus):
    chinese_dic = {}
    for text in corpus:
        for char in text:
            if char in chinese_dic.keys():
                chinese_dic[char] += 1
            else:
                chinese_dic[char] = 1
    return sorted(chinese_dic.items(), key = lambda x : x[1], reverse = True)

def get_english_vocab(corpus):
    english_dic = {}
    words = [text.split(' ') for text in corpus]
    for word in words:
        if word in english_dic.keys():
            english_dic[word] += 1
        else:
            english_dic[word] = 1
    return sorted(english_dic.items(), key = lambda x : x[1], reverse = True)

def calculate_entropy(vocab):
    stats = [item[1] for item in vocab]
    total = sum(stats)
    normed_stats = [stats[i] / total for i in range(len(stats))]
    return - sum([prob*np.log2(prob) for prob in normed_stats])

if __name__ == '__main__':
    corpus = read_data('../data/chinese_corpus.json')
    chinese_vocab = get_chinese_vocab(corpus)
    print(calculate_entropy(chinese_vocab))