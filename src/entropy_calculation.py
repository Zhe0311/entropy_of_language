import json
import numpy as np
import matplotlib.pyplot as plt	

def read_data(path: str):
    return [json.loads(line) for line in open(path).readlines()]

def get_vocab(corpus):
    chinese_dic = {}
    for text in corpus:
        for char in text:
            if char in chinese_dic.keys():
                chinese_dic[char] += 1
            else:
                chinese_dic[char] = 1
    return sorted(chinese_dic.items(), key = lambda x : x[1], reverse = True)

def entropy(vocab):
    stats = [item[1] for item in vocab]
    total = sum(stats)
    normed_stats = [stats[i] / total for i in range(len(stats))]
    return - sum([prob*np.log2(prob) for prob in normed_stats])

if __name__ == '__main__':

    corpus = 'chinese'
    if corpus == 'chinese':
        chinese_corpus = read_data('../data/chinese_corpus.json')

        vocab = get_vocab(chinese_corpus)
        stats = [item[1] for item in vocab]
        total = sum(stats)
        normed_stats = [stats[i] / total for i in range(len(stats))]

        split_index = [849 * i for i in range(1, 36)]
        split_index[-1] = len(chinese_corpus)

        chinese_entropy = []
        for index in split_index:
            chinese_vocab = get_vocab(chinese_corpus[0: index])
            chinese_entropy.append(entropy(chinese_vocab))
        
        plt.plot(split_index, chinese_entropy)
        plt.xlabel('Number of essays')
        plt.ylabel('Entropy')
        plt.show()
        
    else:
        english_corpus = read_data('../data/english_corpus.json')
        
        vocab = get_vocab([item.upper() for item in english_corpus])
        stats = [item[1] for item in vocab]
        total = sum(stats)
        normed_stats = [stats[i] / total for i in range(len(stats))]
        
        split_index = [6323 * i for i in range(1, 41)]
        split_index[-1] = len(english_corpus)

        english_entropy = []
        for index in split_index:
            english_vocab = get_vocab(english_corpus[0: index])
            english_entropy.append(entropy(english_vocab))
        
        plt.plot(split_index, english_entropy)
        plt.xlabel('Number of text')
        plt.ylabel('Entropy')
        plt.show()