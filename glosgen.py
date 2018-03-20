import re
import collections
import argparse
import time
from wiktionaryparser import WiktionaryParser
# import yaml

parser = argparse.ArgumentParser()
parser.add_argument('input', type=str, help='Input text file')
parser.add_argument('output', type=str, help='Output YAML file')
parser.add_argument('-n', '--nword', type=str, default=20, help='Number of words to be scraped')

DELAY = 5

def extract_words(text):
    # words = re.compile(r"a-zA-Z'").findall(text)
    words = re.findall(r'\w+', text)
    return words

def filter_words(words, blacklisted_words):
    lowercased_blacklist = [w.lower() for w in blacklisted_words]
    result = []

    for w in words:
        if w.lower() in lowercased_blacklist:
            continue
        elif len(w) < 2:
            continue
        elif not w.isalpha():
            continue
        result.append(w)
    return result

def get_word_counts(words):
    counts = collections.Counter(words)
    return counts


def __main__():
    args = parser.parse_args()

    blacklisted_words = []

    with open('word_blacklist.txt') as f:
        for line in f.readlines():
            blacklisted_words.append(line.strip())

    with open(args.input) as f:
        text = f.read()

    words = extract_words(text)
    words = [w.lower() for w in words]
    filtered_words = filter_words(words, blacklisted_words)
    counts = get_word_counts(filtered_words)

    for word, count in counts.most_common(100):
        print(word, count)

    most_common = counts.most_common(args.nword)

    wiki_parser = WiktionaryParser()

    out = open(args.output, 'w')
    out.write('---\n')

    for word, count in most_common:
        result = wiki_parser.fetch(word.lower())

        out.write('-\n')
        out.write('  word: %s\n'%word)
        out.write('  count: %d\n'%count)
        # print(word, count)

        etymologies = []
        for r in result:
            if 'etymology' in r:
                if r['etymology'] == '': continue
                etymologies.append(r['etymology'])
                # print(r['etymology'])
        if etymologies:
            out.write('  etymologies:\n')
            for e in etymologies:
                out.write('    - \'%s\'\n'%(e))
        # word =
        out.flush()
        time.sleep(DELAY)
    # print(counts)

    # import ipdb; ipdb.set_trace()


if __name__ == '__main__':
    __main__()

