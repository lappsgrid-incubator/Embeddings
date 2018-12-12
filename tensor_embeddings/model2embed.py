##################################################################################################################
##Generates data and metadata files for http://projector.tensorflow.org/
## from word2vec model using common minerals and time epochs
## 
##Usage : python3 model2embed.py <dataName> <metadataName> <words> <path>
##
##<dataName> :                Name of file in which to save the data (.tsv suffix automatically added later)
##<metadataName> :            Name of file in which to save the metadata (.tsv suffix automatically added later)
##<words>:                    Full path to directory containing text files of list of words, one each line, to be projected
##<path> :                    Full path to word2vec model used
##
##################################################################################################################

import csv
import os, sys
import argparse
from gensim.models import Word2Vec

parser = argparse.ArgumentParser()
parser.add_argument("--dataName","-d",type=str,default="data",help="Enter a name for the saved data file")
parser.add_argument("--metadataName","-m",type=str,default="metadata",help="Enter a name for the saved metadata file")
parser.add_argument("--words","-w",type=str,required=True,help="Enter the path to directory of text files of words (one per line) that will be projected")
parser.add_argument("--path","-p",type=str,required=True,help="Enter the path to the Word2Vec model")

args = parser.parse_args()

# In event of incorrect model path, model_FLAG is raised.
model_FLAG = False
word_FLAG = False

try:
    model = Word2Vec.load(args.path)
except:
    sys.stdout.write("Error: Either broken path to model or model does not exist.")
    model_FLAG = True

if(not(os.path.isdir(args.words))):
    sys.stdout.write("Error: Cannot find directory containing text files")
    word_FLAG = True

# Add .tsv suffix to data and metadata files.
data_file = args.dataName + ".tsv"
metadata_file = args.metadataName + ".tsv"

# If path is to a word2vec model and words can be found.
if(not(model_FLAG) and not(word_FLAG)):
    
    # Gather words into a list
    words = []
    for root, dirs, files in os.walk(args.words):
        for filename in files:
            for line in open(os.path.join(root, filename),encoding="utf-8"):
                words.append(line.strip())
    
    # Get data about words from word2vec model.
    data = {}
    for word in words:
        if word in model.wv.vocab:
            data[word] = model.wv[word]

    # Write the data to the respective files.
    with open(data_file, 'w', newline='') as f_output:
        tsv_output = csv.writer(f_output, delimiter='\t')
        for key in data.keys():
            tsv_output.writerow(data[key])
    with open(metadata_file, 'w', newline='') as f_output:
        for key in data.keys():
            f_output.write(key + '\n')
