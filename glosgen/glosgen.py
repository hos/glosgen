import collections
import argparse
import time
import logging
import sys
from wiktionaryparser import WiktionaryParser
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
import unicodedata
# import re


parser = argparse.ArgumentParser()
parser.add_argument('input', type=str, help='Input text file')
parser.add_argument('output', type=str, help='Output YAML file')
parser.add_argument('--delay', type=int, default=5, help='Scraping delay. Default: 5s ')
parser.add_argument('--dont-scrape', action='store_true', help='Don\'t scrape, just output most frequent words')

group = parser.add_mutually_exclusive_group()
group.add_argument('--limit-total', type=int, help='Total number of words to be scraped')
group.add_argument('--limit-count', type=int, help='Minimum number of occurences of words to be scraped')

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def extract_words(text):
    # words = re.compile(r"a-zA-Z'").findall(text)
    # words = re.findall(r'\w+', text)
    try:
        words = word_tokenize(text)
    except LookupError:
        import nltk
        nltk.download('punkt')
        logging.info('Downloaded missing nltk sentence tokenizer. Please rerun the program.')
        sys.exit()

    return words

def filter_words(words, stop_words):
    result = []

    for w in words:
        try:
            w = unicodedata.normalize('NFKD', w)
        except:
            pass

        if w in stop_words:
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

    try:
        stop_words = set(stopwords.words('english'))
    except LookupError:
        import nltk
        nltk.download('stopwords')
        logging.info('Downloaded missing stop words. Please rerun the program.')
        sys.exit()

    with open(args.input) as f:
        text = f.read()

    words = extract_words(text)
    words = [w.lower() for w in words]
    filtered_words = filter_words(words, stop_words)
    counts = get_word_counts(filtered_words)

    # import ipdb; ipdb.set_trace()

    # for word, count in counts.most_common(100):
    #     print(word, count)

    if args.limit_total:
        target_words = counts.most_common(args.limit_total)
    elif args.limit_count:
        target_words = []
        most_common = counts.most_common()

        for i in most_common:
            if i[1] < args.limit_count: break
            target_words.append(i)
    else:
        target_words = counts.most_common()

    wiki_parser = WiktionaryParser()

    result_list = []
    for n, (word, count) in enumerate(target_words):

        result = {'word': word, 'count': count}

        if not args.dont_scrape:
            wiktionary_result = wiki_parser.fetch(word.lower())
            result['wiktionary'] = wiktionary_result

        result_list.append(result)

        result_json = json.dumps(result_list, indent=1)
        result_json = result_json.replace('\n },', '\n },\n')

        out = open(args.output, 'w')
        out.write(result_json)
        out.close()

        if not args.dont_scrape:
            time.sleep(args.delay)



if __name__ == '__main__':
    __main__()

