##################################################################################################################
##Generates data and metadata files for http://projector.tensorflow.org/
## from word2vec model using common minerals and time epochs
## 
##Usage : python3 model2embed.py <dataName> <metadataName> <path>
##
##<dataName> :                Name of file in which to save the data (.tsv suffix automatically added later)
##<metadataName> :            Name of file in which to save the metadata (.tsv suffix automatically added later)
##<path> :                    Full path to word2vec model used
##
##################################################################################################################

import csv
import os, sys
import argparse
from gensim.models import Word2Vec

# Lists of minerals and times.
minerals = ['lead', 'ice', 'iron', 'quartz', 'gold', 'copper', 'zinc', 'silver', 'phosphorus', 'zircon', 'calcite', 'mercury', 'silicon', 'olivine', 'dolomite', 'garnet', 'diamond', 'arsenic', 'feldspar', 'magnesium', 'plagioclase', 'urea', 'biotite', 'nickel', 'pyrite', 'manganese', 'cadmium', 'sulphur', 'carbonyl', 'magnetite', 'tin', 'lime', 'mica', 'graphite', 'iodine', 'boron', 'chlorite', 'apatite', 'platinum', 'titanium', 'pyroxene', 'aluminium', 'cobalt', 'hornblende', 'charcoal', 'zeolite', 'gypsum', 'chromium', 'helium', 'selenium', 'kaolinite', 'spinel', 'palladium', 'hematite', 'muscovite', 'illite', 'amalgam', 'bronze', 'smectite', 'perovskite', 'albite', 'molybdenum', 'aragonite', 'montmorillonite', 'chalcopyrite', 'k feldspar', 'monazite', 'goethite', 'tungsten', 'vanadium', 'ilmenite', 'guanine', 'epidote', 'rutile', 'galena', 'ruthenium', 'sphalerite', 'opal', 'opal-an', 'talc', 'anhydrite', 'halite', 'chromite', 'osmium']
times = ['cretaceous', 'quaternary', 'holocene', 'pleistocene', 'miocene', 'jurassic', 'tertiary', 'triassic', 'precambrian', 'eocene', 'permian', 'mesozoic', 'paleozoic', 'cenozoic', 'devonian', 'cambrian', 'pliocene', 'ordovician', 'carboniferous', 'proterozoic', 'oligocene', 'archean', 'silurian', 'neogene', 'neoproterozoic', 'paleocene', 'pennsylvanian', 'julian', 'mississippian', 'phanerozoic']

parser = argparse.ArgumentParser()
parser.add_argument("--dataName","-d",type=str,default="data",help="Enter a name for the saved data file")
parser.add_argument("--metadataName","-m",type=str,default="metadata",help="Enter a name for the saved metadata file")
parser.add_argument("--path","-p",type=str,required=True,help="Enter the path to the Word2Vec model")

args = parser.parse_args()

# In event of incorrect model path, model_FLAG is raised.
model_FLAG = False

try:
    model = Word2Vec.load(args.path)
except:
    sys.stdout.write("Error: Either broken path to model or model does not exist.")
    model_FLAG = True

# Add .tsv suffix to data and metadata files.
data_file = args.dataName + ".tsv"
metadata_file = args.metadataName + ".tsv"

# If path is to a word2vec model.
if(not(model_FLAG)):
    data = {}
    
    # Get data about minerals/times from word2vec model.
    for mineral in minerals:
        if mineral in model.wv.vocab:
            data[mineral] = model.wv[mineral]
    for time in times:
        if time in model.wv.vocab:
            data[time] = model.wv[time]

    # Write the data to the respective data/metadata files.
    with open(data_file, 'w', newline='') as f_output:
        tsv_output = csv.writer(f_output, delimiter='\t')
        for key in data.keys():
            tsv_output.writerow(data[key])
    with open(metadata_file, 'w', newline='') as f_output:
        for key in data.keys():
            f_output.write(key + '\n')
