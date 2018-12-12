Steps to generate embedding projections using word2vec.py and model2embed.py

Python requirements (for python 3):
-From standard library:
	os, sys, argparse, csv, fnmatch
-Need to be installed (can use requirements.txt file):
	gensim -> pip3 install gensim
	nltk   -> pip3 install nltk


(1) Place all research papers in a directory 
	- each paper needs to be a text file
	- all papers must have the same file suffix (i.e. .txt)
(2) Run word2vec.py on the above directory 
	- this generates a word2vec model from the papers
	- command line usage:

	$python3 word2vec.py -d <directory-file-name> -x <file suffix> -p <preprocess> -m <model-file-name>
	
	  where <directory-file-name> is name of directory where text files are located (required)
		<file suffix> is suffix of text files to be processed (default is '.txt')
		<preprocess> Tokenize, remove stopwords and punctuation, etc. (default is True)
		<model-file-name> Name of file in which to save model (required)

(3) Run model2embed.py on the word2vec model generated in 2)
	- this generates two files (default file names listed below, but user can choose):
		metadata.tsv -> TSV file of common minerals and time epochs
		data.tsv -> TSV file of vectors for each word found in metadata	
	- command line usage:

	$python3 model2embed.py -d <dataName> -m <metadataName> -p <path>

	  where <dataName> is name of file in which to save the data (default is 'data')
		<metadataName> is name of file in which to save the metadata (default is 'metadata')
		<path> is full path to word2vec model generated in (2) above (required)

(4) Navigate to http://projector.tensorflow.org/
	- select "Load data" on the left side of the page
	- load <dataName>.tsv for Step 1
	- load <metadataName>.tsv for Step 2
	- click outside the prompt, and the embedding projections should be displayed