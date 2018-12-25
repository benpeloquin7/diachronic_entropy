"""preprocess.py

Bespoke CLMET file pre-processing.

"""

from bs4 import BeautifulSoup
from collections import Counter
from nltk.tokenize import word_tokenize
import re

from clmet import CLMET_META


def extract_meta_data(soup):
    """
    Example meta data
    -----------------
    <id>333</id>
    <file>CLMET3_1_3_333.txt</file>
    <period>1850-1920</period>
    <quartcent>1875-1899</quartcent>
    <decade>1890s</decade>
    <year>1890</year>
    <genre>Other</genre>
    <subgenre>x</subgenre>
    <title>Punch, Vol. 99</title>
    <author>X</author>
    <gender>X</gender>
    <author_birth>X</author_birth>
    <notes>Periodical containing a range of genres including fictional dialogue, satirical poems, news commentary, reviews, etc.</notes>
    <source>http://www.gutenberg.org/ebooks/search/?query=punch</source>
    <downloaded>05-02-2013</downloaded>
    <comments>compiled from multiple files</comments>

    """
    data = {m: soup.find_all(m)[0].get_text() for m in CLMET_META}
    return data


def preprocess_text(text):
    # Minimal pre-processing at this point. Should reference pre-processing performed Bentz Entropy article.
    text = text.lower()
    text = re.sub(r'[^a-z0-9\.,]', ' ', text)
    text = re.sub(r'\s{2, }', ' ', text)
    text = text.rstrip()
    text = text.lstrip()
    return text


def file2data(fp):
    """

    Returns
    -------
    tuple
        Tuple of dict, Counter.

    """
    f = open(fp, 'r')
    contents = f.read()
    contents = re.sub('\n', ' ', contents)
    soup = BeautifulSoup(contents)
    text = soup.text
    meta_data = extract_meta_data(soup)
    unigram_counts = Counter(word_tokenize(preprocess_text(text)))
    return meta_data, unigram_counts
