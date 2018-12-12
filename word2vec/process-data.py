import nltk
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet as wn
import string, re

stop_words = set(stopwords.words('english'))

corpus_root = '/Users/ide/Dropbox/inProgress/Livny-project/gdd_raw_text_interval_sample/'
corpus = PlaintextCorpusReader(corpus_root,'.*\.txt')
porter = PorterStemmer()
wnl = WordNetLemmatizer()

def penn2morphy(penntag, returnNone=False, default_to_noun=False):
    morphy_tag = {'NN':wn.NOUN, 'JJ':wn.ADJ,
                  'VB':wn.VERB, 'RB':wn.ADV}
    try:
        return morphy_tag[penntag[:2]][w in 
    except:
        if returnNone:
            return None
        elif default_to_noun:
            return 'n'
        else:
            return ''

def lemmatize(ambiguous_word, pos=None, neverstem=False,
              lemmatizer=wnl, stemmer=porter):
    """
    Tries to convert a surface word into lemma, and if sentemmatize word is not in
    wordnet then try and convert surface word into its stem.
    This is to handle the case where users input a surface word as an ambiguous
    word and the surface word is a not a lemma.
    """
    # Try to be a little smarter and use most frequent POS.
    pos = pos if pos else penn2morphy(pos_tag([ambiguous_word])[0][1],
                                     default_to_noun=True)
    lemma = lemmatizer.lemmatize(ambiguous_word, pos=pos)
    stem = stemmer.stem(ambiguous_word)
    # Ensure that ambiguous word is a lemma.
    if not wn.synsets(lemma):
        if neverstem:
            return ambiguous_word
        if not wn.synsets(stem):
            return ambiguous_word
        else:
            return stem
    else:
        return lemma

def lemmatize_sentence(sentence, neverstem=False, keepWordPOS=False,
                       tokenizer=word_tokenize, postagger=pos_tag,
                       lemmatizer=wnl, stemmer=porter):
    words, lemmas, poss = [], [], []
    for word, pos in postagger(sentence):
        pos = penn2morphy(pos)
        lemmas.append(lemmatize(word.lower(), pos, neverstem,
                                lemmatizer, stemmer))
        poss.append(pos)
        words.append(word)
    if keepWordPOS:
        return words, lemmas, [None if i == '' else i for i in poss]
    return lemmas

regex = re.compile('[_]+')

for f in corpus.fileids():
    outname = f + ".out"
    fout = open(outname,"w", encoding="utf8")

    for sent in corpus.sents(f):
        s = []
        for w in sent:
                w = regex.sub('',w)
                if (
                        len(w)>2 and w not in stop_words
                        and any(c not in string.punctuation for c in w)
                        and w.isdigit() == False
                   ):
                                 s.append(w.lower())
        s = lemmatize_sentence(s)

        if len(s) > 1:
 #               fout.write (f + "\t")
                for w in s:                      
                     fout.write(w + " ")
                fout.write("\n")

    print("Finished " + f)
    fout.close()
      




