###########################################################################################################
##Reads files from a directory containing text for input to word2vec
##
##Usage : python3 word2vec.py <directory> <suffix> <preprocess> <savemodel>
##
##<directory> :     Name of the directory in which the text files reside
##<suffix> :        Suffix of text files to be processed (default : .txt)
##<preprocess> :    Folder in which to save pre-processed text (tokenize, remove stopwords and punctuation, etc.) (default: None)
##<savemodel> :     File in which to save the model(default : None)  
##
## For now we use basic paramaeters to word2vec, with workers=10 
############################################################################################################

import gensim, os, sys, fnmatch

## Get word2vec parameters from .ini file
import configparser
config = configparser.ConfigParser()
config.read("word2vec.ini")

## Parse command line parameters
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--directory","-d",type=str,required=True,help="Enter the input directory name")
parser.add_argument("--suffix","-x",type=str,default=".txt",help="Enter the filename suffix (default=.txt)")
parser.add_argument("--preprocess","-p",default=None,help="File to store pre-processed data (default=None)")
parser.add_argument("--savemodel","-m",default=None,help="File to save model (default=None)")

args = parser.parse_args()

## Pre-process a document.                                                                                           

from nltk import download
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import nltk.data

splitter = nltk.data.load('tokenizers/punkt/english.pickle')
stop_words = stopwords.words('english')

def preprocess(line):
    line = word_tokenize(line)  # Split into words.                                                                    
    if args.preprocess is not None:
        line = [w.lower() for w in line]  # Lower the text.                                                               
        line = [w for w in line if not w in stop_words]  # Remove stopwords                                              
        line = [w for w in line if w.isalpha()] # Remove numbers and punctuation                                         
    return line
                        
                     
class MySentences(object):
    def __init__(self, dirname, suffix):
        self.dirname = dirname
        self.suffix = suffix
    def __iter__(self):
        suf = '*.' + self.suffix    
        for root, dirs, files in os.walk(self.dirname):
            for filename in fnmatch.filter(files, suf):
                file = open(os.path.join(root, filename),encoding="utf-8")
                sentences = splitter.tokenize(file)               
                for s in sentences:
                    s = preprocess(s)
                    if len(s) > 0:
                        yield s
                        
### Get word2vec parameters                                                                                                           
vector_size = 	config['word2vecParameters'].getint('vector_size')
window_size = 	config['word2vecParameters'].getint('window_size')
min_count = 	config['word2vecParameters'].getint('min_count')
alpha = 	config['word2vecParameters'].getfloat('alpha')
min_alpha = 	config['word2vecParameters'].getfloat('min_alpha')
negative_size = config['word2vecParameters'].getint('negative_size')
train_epoch = 	config['word2vecParameters'].getint('train_epoch')
sg = 		config['word2vecParameters'].getint('sg')
worker_count = 	config['word2vecParameters'].getint('worker_count')                                                                                                                                                                 

# print (vector_size, window_size,min_count,alpha,min_alpha,negative_size,train_epoch,sg,worker_count)

w2v_corpus = MySentences(args.directory,args.suffix) # a memory-friendly iterator                                                       

model = gensim.models.Word2Vec(w2v_corpus,size=vector_size, window=window_size, min_count=min_count,
                               workers=worker_count, sg=sg, negative=negative_size,
                               alpha = alpha, min_alpha = min_alpha, iter=train_epoch)

if args.savemodel is not None:
    model.save(args.savemodel)


