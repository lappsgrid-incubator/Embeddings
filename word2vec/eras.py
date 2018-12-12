import gensim

# Load pre-trained Word2Vec model.
model = gensim.models.Word2Vec.load("/root/models/word2vec.model")

filepath = '/root/eras.txt'

with open(filepath) as fp:  
   era = fp.readline().replace('\n', '')
   while era:
        if era in model.wv.vocab:
            print(era,":",model.wv.similar_by_word(era))
            print("\n")
        era = fp.readline().replace('\n', '')
