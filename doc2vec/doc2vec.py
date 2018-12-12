###########################################################################################################
##Reads files from a directory containing text for input to doc2vec
##
##Usage : python3 word2vec.py -d <directory-file-name> [-s <file suffix>] [-p <preprocess>] [-s <save model>] [-m <model-file-name>]
##
##<directory-file-name> :     Name of the directory in which the text files reside
##<file suffix> :             Suffix of text files to be processed (default : .txt)
##<preprocess> :              Tokenize, remove stopwords and punctuation, etc. (default : True)
##<model-file-name> :         Name of file in which to save the model
##
## For now we use basic paramaeters to word2vec, with workers=10 
############################################################################################################

from os import listdir
from os.path import isfile, join
import sys
import argparse
import gensim
from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import LabeledSentence


parser = argparse.ArgumentParser()
parser.add_argument("--directory","-d",type=str,required=True,help="Enter the input directory name")
parser.add_argument("--suffix","-x",type=str,default=".txt",help="Enter the filename suffix (default=.txt)")
parser.add_argument("--preProcess","-p",default=True,help="Pre-process data? (default=True)")
parser.add_argument("--saveModel","-s",default=True,help="Save model? (default=True)")
parser.add_argument("--modelFile","-m",type=str,help="Enter a filename for the saved model")

args = parser.parse_args()

if (args.saveModel and 'modelFile' not in vars(args)):
    parser.error('The -saveModel argument requires a -modelFile')

####################################################
## Pre-process a document.

from nltk import download
from nltk import word_tokenize
download('punkt')  # Download data for tokenizer.

from nltk.corpus import stopwords
download('stopwords')  # Download stopwords list.

# Remove stopwords.
stop_words = stopwords.words('english')

def process(line):   
    line = word_tokenize(line)  # Split into words.
    line = [w.lower() for w in line]  # Lower the text.
    line = [w for w in line if not w in stop_words]  # Remove stopwords.
    line = [w for w in line if w.isalpha()] # Remove numbers and punctuation. 
    line = [w for w in line if len(w) > 2]
    return line

# Create the required input for doc2vec from text
class DocIterator(object):
    def __init__(self, doc_list, labels_list):
       self.labels_list = labels_list
       self.doc_list = doc_list
    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            words = [line.rstrip('\n') for line in doc]
            if args.PreProcess:
                words = process(words)
            yield LabeledSentence(words,[self.labels_list[idx]])

#######################################################

myDirPath = args.directory

docLabels = []
docLabels = [f for f in listdir(myDirPath) if f.endswith(args.suffix)]

data = []
for doc in docLabels:
    data.append(open(myDirPath + doc, 'r',encoding='utf-8'))

it = DocIt.DocIterator(data, docLabels)

model = gensim.models.Doc2Vec(vector_size=300, window=10, min_count=5, workers=10,alpha=0.025, min_alpha=0.025, epochs=20)
model.build_vocab(it)
model.train(it, epochs=model.epochs, total_examples=model.corpus_count)

# Save the model if desired

if args.saveModel:
    model.save(args.modelFile)


### Print the most similar documents
### for doc in docLabels:
###     print(model.docvecs.most_similar(doc, topn=10))
