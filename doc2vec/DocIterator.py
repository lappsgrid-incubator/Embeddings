from gensim.models.doc2vec import LabeledSentence


# Pre-processing a document.

from nltk import download
from nltk import word_tokenize
download('punkt')  # Download data for tokenizer.

from nltk.corpus import stopwords
download('stopwords')  # Download stopwords list.

# Remove stopwords.
stop_words = stopwords.words('english')

def preprocess(line):   
#    line = word_tokenize(line)  # Split into words.
    line = [w.lower() for w in line]  # Lower the text.
    line = [w for w in line if not w in stop_words]  # Remove stopwords.
    line = [w for w in line if w.isalpha()] # Remove numbers and punctuation. 
    line = [w for w in line if len(w) > 2]
    return line


class DocIterator(object):
    def __init__(self, doc_list, labels_list):
       self.labels_list = labels_list
       self.doc_list = doc_list
    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            words = [line.rstrip('\n') for line in doc]
            words = preprocess(words)
            yield LabeledSentence(words,[self.labels_list[idx]])
