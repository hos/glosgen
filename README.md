# glosgen

_Generate glossaries of most frequent words from texts_

## Installation

    sudo python setup.py install

or

    sudo pip install .

## Usage

Suppose you have a text file `yourfile.txt`. To get the 20 most frequent words,
their total counts, and their Wiktionary entries, you run

    glosgen yourfile.txt words.json --limit-total 20


This outputs a JSON file with all the data.

To see other options, run

    glosgen --help


