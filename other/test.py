import gensim

model = gensim.models.Word2Vec.load('mymodel')

print(model.similarity("precambrian", "paleozoic"))

print(model.similar_by_word("precambrian"))
