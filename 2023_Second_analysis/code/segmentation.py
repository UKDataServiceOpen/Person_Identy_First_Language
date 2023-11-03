#!/usr/bin/env python
# coding: utf-8
# http://stackoverflow.com/q/19675106/89391

import functools
import math
import os
import sys
import gzip
import urllib


def split_pairs(word):
    return [(word[:i + 1], word[i + 1:]) for i in range(len(word))]

def segment(word, word_seq_fitness=None):
    if not word or not word_seq_fitness:
        return []
    all_segmentations = [[first] + segment(rest, word_seq_fitness=word_seq_fitness) 
                         for (first, rest) in split_pairs(word)]
    # print(len(all_segmentations))
    return max(all_segmentations, key=word_seq_fitness)


class OneGramDist(dict):
    """
    1-gram probability distribution for corpora.
    Source: http://norvig.com/ngrams/count_1w.txt
    """
    def __init__(self, filename='count_1w_cleaned.txt'):
        self.total = 0
        print('building probability table...')
        _open = open
        if filename.endswith('gz'):
            _open = gzip.open
        with _open(filename) as handle:
            for line in handle:
                word, count = line.strip().split('\t')
                self[word] = int(count)
                self.total += int(count)

    def __call__(self, word):
        try:
            result = float(self[word]) / self.total
            # print(word, result)
        except KeyError:
            # result = 1.0 / self.total
            return 1.0 / (self.total * 10**(len(word) - 2))
            # return sys.float_info.min
        return result


def onegram_log(onegrams, words):
    """
    Use the log trick to avoid tiny quantities.
    http://machineintelligence.tumblr.com/post/4998477107/the-log-sum-exp-trick
    """

    result = functools.reduce(lambda x, y: x + y,
        (math.log10(onegrams(w)) for w in words))

    print(words, result)
    return result


if __name__ == '__main__':
    sentence = ''.join(sys.argv[1:]).lower()
    if not sentence:
        sentence = 'thequickbrown'
    # onegrams = OneGramDist(filename='count_10M_gb.txt')
    onegrams = OneGramDist(filename='count_1M_gb.txt.gz')
    # onegrams = OneGramDist(filename='count_1w.txt')
    onegram_fitness = functools.partial(onegram_log, onegrams)
    print(sentence)
    print(segment(sentence, word_seq_fitness=onegram_fitness))