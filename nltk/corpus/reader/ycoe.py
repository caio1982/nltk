# -*- coding: iso-8859-1 -*-

# Natural Language Toolkit: York-Toronto-Helsinki Parsed Corpus of Old English Prose (YCOE)
#
# Copyright (C) 2001-2007 University of Pennsylvania
# Author: Selina Dennis <selina@tranzfusion.net>
# URL: <http://nltk.sf.net>
# For license information, see LICENSE.TXT

"""
Reads tokens from the York-Toronto-Helsinki Parsed Corpus of 
Old English Prose (YCOE), a 1.5 million word syntactically-
annotated corpus of Old English prose texts. The corpus is
distributed by the Oxford Text Archive: http://www.ota.ahds.ac.uk/
It is not included with NLTK.

The YCOE corpus is divided into 100 files, each representing
an Old English prose text. Tags used within each text complies
to the YCOE standard: http://www-users.york.ac.uk/~lang22/YCOE/YcoeHome.htm 

Output of the reader is as follows:

Raw:
['+D+atte',
  'on',
  'o+dre',
  'wisan',
  'sint',
  'to',
  'manianne',
  '+da',
  'unge+dyldegan',
  ',',
  '&',
  'on',
  'o+dre',
  '+da',
  'ge+dyldegan',
  '.']

Tagged:
[('+D+atte', 'C'),
  ('on', 'P'),
  ('o+dre', 'ADJ'),
  ('wisan', 'N'),
  ('sint', 'BEPI'),
  ('to', 'TO'),
  ('manianne', 'VB^D'),
  ('+da', 'D^N'),
  ('unge+dyldegan', 'ADJ^N'),
  (',', ','),
  ('&', 'CONJ'),
  ('on', 'P'),
  ('o+dre', 'ADJ'),
  ('+da', 'D^N'),
  ('ge+dyldegan', 'ADJ^N'),
  ('.', '.')]

Bracket Parse:
(CP-THT: (C: '+D+atte') (IP-SUB: (IP-SUB-0: (PP: (P: 'on') (NP: (ADJ: 'o+dre') (N: 'wisan'))) 
(BEPI: 'sint') (IP-INF: (TO: 'to') (VB^D: 'manianne') (NP: '*-1')) (NP-NOM-1: (D^N: '+da') 
(ADJ^N: 'unge+dyldegan'))) (,: ',') (CONJP: (CONJ: '&') (IPX-SUB-CON=0: (PP: (P: 'on') 
(NP: (ADJ: 'o+dre'))) (NP-NOM: (D^N: '+da') (ADJ^N: 'ge+dyldegan'))))) (.: '.')),

Chunk Parse:
[(S: 
    ('C', '+D+atte') 
    (PP: ('P', 'on') ('ADJ', 'o+dre') ('N', 'wisan')) 
    ('BEPI', 'sint') ('TO', 'to') ('VB^D', 'manianne') 
    (NP: ('NP', '*-1')) ('D^N', '+da') ('ADJ^N', 'unge+dyldegan') (',', ',') ('CONJ', '&') 
    (PP: ('P', 'on') ('ADJ', 'o+dre')) ('D^N', '+da') ('ADJ^N', 'ge+dyldegan') ('.', '.'))]

"""

from util import *
from nltk import tokenize, tree
from nltk.tag import string2tags, string2words
from nltk.corpus.reader.treebank import BracketParseCorpusReader
from string import split
import os, re

class YCOECorpusReader(CorpusReader):
    """
    ...
    """
    def __init__(self, root):
        self._root = root
        self._psd_reader = YCOEParseCorpusReader(
            os.path.join(root, 'psd'), '.*', '.psd')
        self._pos_reader = YCOETaggedCorpusReader(
            os.path.join(root, 'pos'), '.*', '.pos')

        # Make sure we have a consistent set of items:
        if set(self._psd_reader.items) != set(self._pos_reader.items):
            raise ValueError('Items in "psd" and "pos" '
                             'subdirectories do not match.')
        self.items = self._psd_reader.items

    # Delegate to one of our two sub-readers:
    def words(self, items=None):
        return self._pos_reader.words(items)
    def sents(self, items=None):
        return self._pos_reader.sents(items)
    def paras(self, items=None):
        return self._pos_reader.paras(items)
    def tagged_words(self, items=None):
        return self._pos_reader.tagged_words(items)
    def tagged_sents(self, items=None):
        return self._pos_reader.tagged_sents(items)
    def tagged_paras(self, items=None):
        return self._pos_reader.tagged_paras(items)
    def parsed_sents(self, items=None):
        return self._psd_reader.parsed_sents(items)

class YCOEParseCorpusReader(BracketParseCorpusReader):
    """Specialized version of the standard bracket parse corpus reader
    that strips out (CODE ...) and (ID ...) nodes."""
    def _parse(self, t):
        s = re.sub(r'(?u)\((CODE|ID)[^\)]*\)', '', t)
        return BracketParseCorpusReader._parse(t)

class YCOETaggedCorpusReader(TaggedCorpusReader):
    def __init__(self, root, items, extension):
        TaggedCorpusReader.__init__(self, root, items, extension, '_',
                                    sent_tokenizer=self._sent_tokenizer)

    def _sent_tokenizer(self, s):
        s = re.sub(r'(?u)\S*_CODE|\S*_ID', '', s)
        return tokenize.regexp(s, r'(?<=/\.)\s', gaps=True)


#: All files within the corpora
documents = {
    'coadrian.o34': 'Adrian and Ritheus',
    'coaelhom.o3': '�lfric, Supplemental Homilies',
    'coaelive.o3': '�lfric\'s Lives of Saints',
    'coalcuin': 'Alcuin De virtutibus et vitiis',
    'coalex.o23': 'Alexander\'s Letter to Aristotle',
    'coapollo.o3': 'Apollonius of Tyre',
    'coaugust': 'Augustine',
    'cobede.o2': 'Bede\'s History of the English Church',
    'cobenrul.o3': 'Benedictine Rule',
    'coblick.o23': 'Blickling Homilies',
    'coboeth.o2': 'Boethius\' Consolation of Philosophy',
    'cobyrhtf.o3': 'Byrhtferth\'s Manual',
    'cocanedgD': 'Canons of Edgar (D)',
    'cocanedgX': 'Canons of Edgar (X)',
    'cocathom1.o3': '�lfric\'s Catholic Homilies I',
    'cocathom2.o3': '�lfric\'s Catholic Homilies II',
    'cochad.o24': 'Saint Chad',
    'cochdrul': 'Chrodegang of Metz, Rule',
    'cochristoph': 'Saint Christopher',
    'cochronA.o23': 'Anglo-Saxon Chronicle A',
    'cochronC': 'Anglo-Saxon Chronicle C',
    'cochronD': 'Anglo-Saxon Chronicle D',
    'cochronE.o34': 'Anglo-Saxon Chronicle E',
    'cocura.o2': 'Cura Pastoralis',
    'cocuraC': 'Cura Pastoralis (Cotton)',
    'codicts.o34': 'Dicts of Cato',
    'codocu1.o1': 'Documents 1 (O1)',
    'codocu2.o12': 'Documents 2 (O1/O2)',
    'codocu2.o2': 'Documents 2 (O2)',
    'codocu3.o23': 'Documents 3 (O2/O3)',
    'codocu3.o3': 'Documents 3 (O3)',
    'codocu4.o24': 'Documents 4 (O2/O4)',
    'coeluc1': 'Honorius of Autun, Elucidarium 1',
    'coeluc2': 'Honorius of Autun, Elucidarium 1',
    'coepigen.o3': '�lfric\'s Epilogue to Genesis',
    'coeuphr': 'Saint Euphrosyne',
    'coeust': 'Saint Eustace and his companions',
    'coexodusP': 'Exodus (P)',
    'cogenesiC': 'Genesis (C)',
    'cogregdC.o24': 'Gregory\'s Dialogues (C)',
    'cogregdH.o23': 'Gregory\'s Dialogues (H)',
    'coherbar': 'Pseudo-Apuleius, Herbarium',
    'coinspolD.o34': 'Wulfstan\'s Institute of Polity (D)',
    'coinspolX': 'Wulfstan\'s Institute of Polity (X)',
    'cojames': 'Saint James',
    'colacnu.o23': 'Lacnunga',
    'colaece.o2': 'Leechdoms',
    'colaw1cn.o3': 'Laws, Cnut I',
    'colaw2cn.o3': 'Laws, Cnut II',
    'colaw5atr.o3': 'Laws, �thelred V',
    'colaw6atr.o3': 'Laws, �thelred VI',
    'colawaf.o2': 'Laws, Alfred',
    'colawafint.o2': 'Alfred\'s Introduction to Laws',
    'colawger.o34': 'Laws, Gerefa',
    'colawine.ox2': 'Laws, Ine',
    'colawnorthu.o3': 'Northumbra Preosta Lagu',
    'colawwllad.o4': 'Laws, William I, Lad',
    'coleofri.o4': 'Leofric',
    'colsigef.o3': '�lfric\'s Letter to Sigefyrth',
    'colsigewB': '�lfric\'s Letter to Sigeweard (B)',
    'colsigewZ.o34': '�lfric\'s Letter to Sigeweard (Z)',
    'colwgeat': '�lfric\'s Letter to Wulfgeat',
    'colwsigeT': '�lfric\'s Letter to Wulfsige (T)',
    'colwsigeXa.o34': '�lfric\'s Letter to Wulfsige (Xa)',
    'colwstan1.o3': '�lfric\'s Letter to Wulfstan I',
    'colwstan2.o3': '�lfric\'s Letter to Wulfstan II',
    'comargaC.o34': 'Saint Margaret (C)',
    'comargaT': 'Saint Margaret (T)',
    'comart1': 'Martyrology, I',
    'comart2': 'Martyrology, II',
    'comart3.o23': 'Martyrology, III',
    'comarvel.o23': 'Marvels of the East',
    'comary': 'Mary of Egypt',
    'coneot': 'Saint Neot',
    'conicodA': 'Gospel of Nicodemus (A)',
    'conicodC': 'Gospel of Nicodemus (C)',
    'conicodD': 'Gospel of Nicodemus (D)',
    'conicodE': 'Gospel of Nicodemus (E)',
    'coorosiu.o2': 'Orosius',
    'cootest.o3': 'Heptateuch',
    'coprefcath1.o3': '�lfric\'s Preface to Catholic Homilies I',
    'coprefcath2.o3': '�lfric\'s Preface to Catholic Homilies II',
    'coprefcura.o2': 'Preface to the Cura Pastoralis',
    'coprefgen.o3': '�lfric\'s Preface to Genesis',
    'copreflives.o3': '�lfric\'s Preface to Lives of Saints',
    'coprefsolilo': 'Preface to Augustine\'s Soliloquies',
    'coquadru.o23': 'Pseudo-Apuleius, Medicina de quadrupedibus',
    'corood': 'History of the Holy Rood-Tree',
    'cosevensl': 'Seven Sleepers',
    'cosolilo': 'St. Augustine\'s Soliloquies',
    'cosolsat1.o4': 'Solomon and Saturn I',
    'cosolsat2': 'Solomon and Saturn II',
    'cotempo.o3': '�lfric\'s De Temporibus Anni',
    'coverhom': 'Vercelli Homilies',
    'coverhomE': 'Vercelli Homilies (E)',
    'coverhomL': 'Vercelli Homilies (L)',
    'covinceB': 'Saint Vincent (Bodley 343)',
    'covinsal': 'Vindicta Salvatoris',
    'cowsgosp.o3': 'West-Saxon Gospels',
    'cowulf.o34': 'Wulfstan\'s Homilies'
    }

#: A list of all documents in this corpus.
items = sorted(documents)

def _read(item, conversion_function):
    """
    Reads files from a given list, and converts them via the
    conversion_function.  Can return raw or tagged read files.
    """
    filename = find_corpus_file('ycoe/pos', item, '.pos')
    f = open(filename)
    rx_pattern = re.compile(r"""
            <.*>_CODE
            |\s.*_ID
    """, re.VERBOSE|re.UNICODE)
    mySents = tokenize.blankline(f.read())
    for sent in mySents:
        sent= re.sub(rx_pattern, '', sent)
        if sent != "":
            yield conversion_function(sent, sep="_")

def read_document(item=items, format='parsed', chunk_types=('NP',),
         top_node="S", partial_match=False, collapse_partials=True,
         cascade=False):
    """
    Read the given document from the corpus, and return its contents.
    C{format} determines the format that the result will be returned
    in:
      - C{'raw'}: a single C{string}
      - C{'tokenized'}: a list of words and punctuation symbols.
      - C{'tagged'}: a list of (word, part-of-speech) tuples.
      - C{'chunked'}: a list of chunk tree structures, where chunks
        are used for base noun phrases.
      - C{'parsed'}: a list of parse trees.
    """
    if isinstance(item, list):
        return concat([read(doc, format, chunk_types, top_node,
                            partial_match, collapse_partials,
                            cascade) for doc in item])
    if format == 'raw':
        return open(find_corpus_file('ycoe/psd', item, '.psd')).read()
    if format == 'tokenized':
        return list(_read(item, string2words))
    elif format == 'tagged':
        return list(_read(item, string2tags))
    elif format == 'chunked':
        return list(_chunk_parse(item, chunk_types, top_node,
                                 partial_match, collapse_partials, cascade))
    elif format == 'parsed':
        filename = find_corpus_file('ycoe/psd', item, '.psd')
        f = open(filename, 'r')
        return [tree.bracket_parse(sent) for sent in _parse(f.read())]
    else:
        raise ValueError()

def _parse(s):
    """
    Rudimentary parsing, used by bracket parser to obtained parsed raw
    data
    """
    rx_pattern = re.compile(r"""
        \(CODE .*\)
        |\(ID .*\d\)
    """, re.VERBOSE|re.UNICODE)
    s = re.sub(rx_pattern, '', s)
    s = split(s, '\n')
    fullPhrase = ""
    # loop through the sentences and parse each sentence
    # every time a new sentence marker is found
    for sent in s:
        if list(tokenize.regexp(sent, r'^\(')) != []:
            fullPhrase = _strip_spaces(fullPhrase)               
            if fullPhrase != "":
                yield fullPhrase
            fullPhrase = sent
        else:
            fullPhrase += sent

    # Get the last of the buffer and output a yield
    fullPhrase = _strip_spaces(fullPhrase)
    if fullPhrase != "":
        yield fullPhrase

def _strip_spaces(s):
    """ 
    Helper function, strips tabs, extra spaces, and an erroneous leading
    and ending bracket.
    """
    s = re.sub(r'^\(', '', s)
    s = re.sub(r'\)\s*$', '', s)
    s = re.sub(r'^\s*', '', s)
    s = re.sub(r'\s*$', '', s)
    s = re.sub(r'\t+', ' ', s)
    s = re.sub(r'\s+', ' ', s)
  
    return s

def _chunk_parse(files, chunk_types, top_node, partial_match, collapse_partials, cascade):
    """
    Parses the files to return chunks of type chunk_types.  Partial
    matching, collapsed partials, and cascading are all supported.
    """          
    # allow any kind of bracketing for flexibility

    L_BRACKET = re.compile(r'[\(\[\{<]')
    R_BRACKET = re.compile(r'[\)\]\}>]')

    if type(files) is str: files = (files,)
    for file in files:
        path = find_corpus_file("ycoe/psd", file, ".psd")
        f = open(path)
        data = _parse(f.read())
        for s in data:
            bracket = 0
            itmType = None
            stack = [tree.Tree(top_node, [])]
            inTag = []
            for itm in list(tokenize.whitespace(s)):
                if L_BRACKET.match(itm[0]):
                    bracket += 1
                    itm = itm[1:]
                    matched = False
                    if partial_match == True:
                        for eachItm in chunk_types:
                           if (len(eachItm) <= len(itm) and 
                               eachItm == itm[:len(eachItm)]):
                               matched = True
                               if collapse_partials == True:
                                   itm = eachItm
                    else:
                        if (chunk_types is not None and
                            itm in chunk_types):
                            matched = True
                    if matched == True: # and inTag == 0:
                        chunk = tree.Tree(itm, [])
                        if cascade == True:
                            stack.append(chunk)
                            inTag += [bracket]
                        else:
                            if len(inTag) == 0:
                                stack[-1].append(chunk)
                                inTag += [bracket]
                    itmType=itm
                if R_BRACKET.match(itm[-1]):
                    tmpItm = split(itm, itm[-1])
                    if tmpItm != "":
                        if len(inTag) > 0 and inTag[-1] <= bracket: #inTag <= bracket:
                            if cascade == True:
                                stack[-1].append( (itmType, tmpItm[0]) )
                            else:
                                stack[-1][-1].append( (itmType, tmpItm[0]) )
                        else:
                            if cascade == True:
                                if len(stack) > 1:
                                    stack[-2].append(stack[-1])
                                    stack = stack[:-1]
                            stack[-1].append( (itmType, tmpItm[0]) )
                            inTag = [] + inTag[:-2]
                    bracket -= (len(tmpItm)-1)
                    while( len(inTag) > 0 and bracket < inTag[-1] ):
                        if cascade == True:
                            if len(stack) > 1:
                                stack[-2].append(stack[-1])
                                stack = stack[:-1]
                        inTag = [] + inTag[:-2]
            yield stack

######################################################################
#{ Convenience Functions
######################################################################
read = read_document

def tagged(item=items):
    """@return: the given document as a list of sentences, where each
    sentence is a list of tagged words.  Tagged words are encoded as
    tuples of (word, part-of-speech)."""
    return read_document(item, format='tagged')

def tokenized(item=items):
    """@return: the given document as a list of sentences, where each
    sentence is a list of words."""
    return read_document(item, format='tokenized')

def raw(item=items):
    """@return: the given document as a single string."""
    return read_document(item, format='raw')

def parsed(item=items):
    return read_document(item, format='parsed')

def chunked(item=items, chunk_types=('NP',), top_node="S",
            partial_match=False, collapse_partials=True, cascade=False):
    return read_document(item, 'chunked', chunk_types, top_node,
                         partial_match, collapse_partials, cascade)
######################################################################
#{ Demo
######################################################################
def demo():
    from nltk.corpus import ycoe
    from pprint import pprint

    print 'Tokenized Data:'
    pprint(ycoe.read('cocuraC', 'tokenized')[:4])

    print '\nTagged Data:'
    pprint(ycoe.read('cocuraC', 'tagged')[:4])

    print '\nBracket Parse:'
    pprint(ycoe.read('cocuraC', 'parsed')[:4])

    print '\nChunk Parse:'
    pprint(ycoe.read('cocuraC', 'chunked', chunk_types=('NP', 'PP'))[:4])

    print '\nChunk Parse (partials, cascaded):'
    pprint(ycoe.read('cocuraC', 'chunked', chunk_types=('NP', 'PP'), 
                     partial_match=True, collapse_partials=False,
                     cascade=True)[:2])

    print '\nChunk Parse (partials, cascaded, collapsed):'
    pprint(ycoe.read('cocuraC', 'chunked', chunk_types=('NP', 'PP'), 
                     partial_match=True, collapse_partials=True,
                     cascade=True)[:2])

if __name__ == '__main__':
    demo()
