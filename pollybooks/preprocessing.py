import nltk
import re
import codecs
from collections import defaultdict


def remove_word_wrap(infile,
                     pattern="(?<![\r\n\s])\r\n?|\n",
                     outfile=None,
                     encoding="utf-8"):
    with codecs.open(infile, encoding=encoding) as f:
        content = ''.join([l for l in f.readlines()])

    p = re.compile(pattern)
    paragraphs, n = p.subn(' ', content)

    if outfile:
        with codecs.open(outfile, 'w', encoding=encoding) as f:
            f.write(paragraphs)

    return paragraphs, n


def split_chapters(infile,
                   pattern="(Chapter|Letter) \d{1,2}",
                   outpath=None,
                   encoding="utf-8"):
    with codecs.open(infile, encoding=encoding) as f:
        content = ' '.join([l for l in f.readlines()])

    c = re.compile(pattern)
    L = re.compile("\r\n?|\n")
    lines = L.split(content)       # Split content into a list assuming each new line is a paragraph
    chapters = defaultdict(list)   # Create a dictionary of chapters
    current_chapter = "000PRIOR"   # Start with an initial chapter
    for l in lines:
        if c.search(l):
            current_chapter = l.strip()
        chapters[current_chapter].append(l)

    if outpath:
        for k, v in chapters.items():
            with codecs.open(outpath+'_'+'_'.join(k.split(' '))+'.txt', 'w', encoding=encoding) as f:
                f.write("\r\n".join(v))

    return chapters

if __name__=="__main__":
    remove_word_wrap("../examples/frankenstein.txt", outfile="../examples/output/frankenstein.txt")
    split_chapters("../examples/output/frankenstein.txt", outpath="../examples/output/frankenstein/frankenstein")
