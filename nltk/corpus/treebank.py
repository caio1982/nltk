# Natural Language Toolkit: Penn Treebank Reader
#
# Copyright (C) 2001-2007 University of Pennsylvania
# Author: Steven Bird <sb@ldc.upenn.edu>
#         Edward Loper <edloper@gradient.cis.upenn.edu>
# URL: <http://nltk.sf.net>
# For license information, see LICENSE.TXT

from util import *
from nltk import tokenize, chunk, tree
from nltk.tag import tag2tuple
import os

"""
Penn Treebank corpus sample: tagged, NP-chunked, and parsed data from
Wall Street Journal for 3700 sentences.

This is a ~10% fragment of the Wall Street Journal section of the Penn
Treebank, (C) LDC 1995.  It is distributed with the Natural Language Toolkit
under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike License
[http://creativecommons.org/licenses/by-nc-sa/2.5/].

Raw:

    Pierre Vinken, 61 years old, will join the board as a nonexecutive
    director Nov. 29.

Tagged:

    Pierre/NNP Vinken/NNP ,/, 61/CD years/NNS old/JJ ,/, will/MD join/VB 
    the/DT board/NN as/IN a/DT nonexecutive/JJ director/NN Nov./NNP 29/CD ./.

NP-Chunked:

    [ Pierre/NNP Vinken/NNP ]
    ,/, 
    [ 61/CD years/NNS ]
    old/JJ ,/, will/MD join/VB 
    [ the/DT board/NN ]
    as/IN 
    [ a/DT nonexecutive/JJ director/NN Nov./NNP 29/CD ]
    ./.

Parsed:

    ( (S 
      (NP-SBJ 
        (NP (NNP Pierre) (NNP Vinken) )
        (, ,) 
        (ADJP 
          (NP (CD 61) (NNS years) )
          (JJ old) )
        (, ,) )
      (VP (MD will) 
        (VP (VB join) 
          (NP (DT the) (NN board) )
          (PP-CLR (IN as) 
            (NP (DT a) (JJ nonexecutive) (NN director) ))
          (NP-TMP (NNP Nov.) (CD 29) )))
      (. .) ))
"""

#: A dictionary whose keys are the names of documents in this corpus;
#: and whose values are descriptions of those documents' contents.
documents = dict([('wsj_%04d' % i, 'Wall Street Journal document %d' % i)
                   for i in range(1, 100)])

#: A list of all documents in this corpus.
items = sorted(documents)

def read_document(item, format='parsed'):
    """
    Read the given document from the corpus, and return its contents.
    C{format} determines the format that the result will be returned
    in:
      - C{'raw'}: a single C{string}
      - C{'tokenized'}: a list of words and punctuation symbols.
      - C{'tagged'}: a list of (word, part-of-speech) tuples.
      - C{'chunked'}: a list of chunk tree structures, where chunks
        are used for base noun phrases.
      - C{'parsed-no-pos'}: a list of parse trees, without part of
        speech tags included.
      - C{'parsed'}: a list of parse trees, with part of
        speech tags included.
    """
    if format == 'parsed':
        filename = find_corpus_file('treebank/combined', item, '.mrg')
        return StreamBackedCorpusView(filename, read_parsed_tb_block)
    elif format == 'parsed-no-pos':
        filename = find_corpus_file('treebank/parsed', item, '.prd')
        return StreamBackedCorpusView(filename, read_parsed_tb_block)
    elif format == 'chunked':
        filename = find_corpus_file('treebank/tagged', item, '.pos')
        return StreamBackedCorpusView(filename, read_chunked_tb_block)
    elif format == 'tagged':
        filename = find_corpus_file('treebank/tagged', item, '.pos')
        return StreamBackedCorpusView(filename, read_tagged_tb_block)
    elif format == 'tokenized':
        filename = find_corpus_file('treebank/raw', item)
        return StreamBackedCorpusView(filename, read_tokenized_tb_block)
    elif format == 'raw':
        filename = find_corpus_file('treebank/parsed', item, '.prd')
        return open(filename).read()
    else:
        raise ValueError('Expected one of the following formats:\n'
                  'parsed chunked tagged tokenized raw parsed-no-pos')
read = read_document

def treebank_bracket_parse(t):
    try:
        return tree.bracket_parse(t)
    except IndexError:
        # in case it's the real treebank format, 
        # strip first and last brackets before parsing
        return tree.bracket_parse(t.strip()[1:-1]) 

def read_parsed_tb_block(stream):
    return [treebank_bracket_parse(t) for t in 
            read_sexpr_block(stream)]

def read_chunked_tb_block(stream):
    return [chunk.tagstr2tree(t) for t in
            read_blankline_block(stream)]

def read_tagged_tb_block(stream):
    return [[tag2tuple(t) for t in tokenize.whitespace(sent)
             if t != '[' and t != ']']
            for sent in read_blankline_block(stream)]

def read_tokenized_tb_block(stream):
    return [list(tokenize.whitespace(sent))
            for sent in read_blankline_block(stream)
            if sent.strip() != '.START']

######################################################################
#{ Convenience Functions
######################################################################
read = read_document

def tagged(item):
    """@return: the given document as a list of sentences, where each
    sentence is a list of tagged words.  Tagged words are encoded as
    tuples of (word, part-of-speech)."""
    return read_document(item, format='tagged')

def tokenized(item):
    """@return: the given document as a list of sentences, where each
    sentence is a list of words."""
    return read_document(item, format='tokenized')

def raw(item):
    """@return: the given document as a single string."""
    return read_document(item, format='raw')

def parsed(item):
    """@return: the given document as a list of parse trees, with
    part of speech tags included in the parse structure."""
    return read_document(item, format='parsed')

def parsed_no_pos(item):
    """@return: the given document as a list of parse trees, without
    part of speech tags included in the parse structure."""
    return read_document(item, format='parsed-no-pos')

######################################################################
#{ Demo
######################################################################
def demo():
    from nltk.corpus import treebank

    print "Parsed:"
    for tree in treebank.read('wsj_0003', format='parsed')[:3]:
        print tree
    print

    print "Chunked:"
    for tree in treebank.read('wsj_0003', format='chunked')[:3]:
        print tree
    print

    print "Tagged:"
    for sent in treebank.read('wsj_0003', format='tagged')[:3]:
        print sent
    print

    print "Tokenized:"
    for sent in treebank.read('wsj_0003', format='tokenized')[:3]:
        print sent
    print

if __name__ == '__main__':
    demo()

