###########################################################################################################
##Reads files from a directory containing text for input to word2vec
##
##Usage : python3 word2vec.py <directory-file-name> <file suffix> <preprocess> <model-file-name>
##
##<directory-file-name> :     Name of the directory in which the text files reside
##<file suffix> :             Suffix of text files to be processed (default : .txt)
##<preprocess> :              Tokenize, remove stopwords and punctuation, etc. (default : True)
##<model-file-name> :         Name of file in which to save the model
##
## For now we use basic paramaeters to word2vec, with workers=10 
############################################################################################################

import gensim, logging, os, sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--directory","-d",type=str,required=True,help="Enter the input directory name")
parser.add_argument("--suffix","-x",type=str,default=".txt",help="Enter the filename suffix (default=.txt)")
parser.add_argument("--preprocess","-p",default=True,help="Pre-process data? (default=True)")
parser.add_argument("--saveModel","-s",default=True,help="Save model? (default=True)")
parser.add_argument("--modelFile","-m",type=str,help="Enter a filename for the saved model")

args = parser.parse_args()

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Pre-processing a document.                                                                                           

from nltk import download
from nltk import word_tokenize
download('punkt')  # Download data for tokenizer.                                                                      

from nltk.corpus import stopwords
download('stopwords')  # Download stopwords list.                                                                      

# Remove stopwords.                                                                                                    
stop_words = stopwords.words('english')

def preprocess(line,pre_process):
    line = word_tokenize(line)  # Split into words.                                                                    
    if pre_process:
        line = [w.lower() for w in line]  # Lower the text.                                                               
        line = [w for w in line if not w in stop_words]  # Remove stopwords.                                              
        line = [w for w in line if w.isalpha()] # Remove numbers and punctuation.                                         
    return line

class MySentences(object):
    def __init__(self, dirname, suffix):
        self.dirname = dirname
        self.suffix = suffix

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            if fname.endswith(self.suffix):
                for line in open(os.path.join(self.dirname, fname),encoding="utf-8"):
                    line = preprocess(line,args.preprocess)
                    if len(line) > 0:
                        yield line

w2v_corpus = MySentences(args.directory,args.suffix) # a memory-friendly iterator                                                      

model = gensim.models.Word2Vec(w2v_corpus, workers=10, size=100)

if args.saveModel:
    model.save(args.modelFile)

