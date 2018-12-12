###########################################################################################################
##Reads files from a directory containing text for input to word2vec
##
##Usage : python3 word2vec.py <directory-file-name> <file suffix> <preprocess> <model-file-name>
##
##<directory-file-name> :     Name of the directory in which the text files reside
##<file suffix> :             Suffix of text files to be processed (default : .txt)
##<preprocess> :              Tokenize, remove stopwords and punctuation, etc. (default : True)
##<saveModel> :               Save the model to a file (default : True)  
##<model-file-name> :         Name of file in which to save the model
##
## For now we use basic paramaeters to word2vec, with workers=10 
############################################################################################################

import gensim, os, sys, fnmatch
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--directory","-d",type=str,required=True,help="Enter the input directory name")
parser.add_argument("--suffix","-x",type=str,default=".txt",help="Enter the filename suffix (default=.txt)")
parser.add_argument("--preprocess","-p",default=True,help="Pre-process data? (default=True)")
parser.add_argument("--saveModel","-s",default=True,help="Save model? (default=True)")
parser.add_argument("--modelFile","-m",type=str,help="Enter a filename for the saved model")

args = parser.parse_args()


if (args.saveModel and 'modelFile' not in vars(args)):
    parser.error('The -saveModel argument requires a -modelFile')

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
        suf = '*.' + self.suffix    
        for root, dirs, files in os.walk(self.dirname):
            for filename in fnmatch.filter(files, suf):
                for line in open(os.path.join(root, filename),encoding="utf-8"):
                    line = preprocess(line,args.preprocess)
                    if len(line) > 0:
                        yield line
                        
#word2vec parameters                                                                                                            
vector_size = 300
window_size = 15
min_count = 10
alpha = 0.25
min_alpha = .0001
negative_size = 10
train_epoch = 100
sg = 1 #0 = cbow; 1 = skip-gram
worker_count = 10 #number of parallel processes                                                                                                                                                                      


w2v_corpus = MySentences(args.directory,args.suffix) # a memory-friendly iterator                                                      

model = gensim.models.Word2Vec(w2v_corpus,size=vector_size, window=window_size, min_count=min_count,
                               workers=worker_count, sg=sg, negative=negative_size,
                               alpha = alpha, min_alpha = min_alpha, iter=train_epoch)

if args.saveModel:
    model.save(args.modelFile)


