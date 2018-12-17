REPO=docker.lappsgrid.org
ORG=embeddings
NAME=word2vec
IMAGE=$(ORG)/$(NAME)
TAG=$(REPO)/$(IMAGE)
PY=$(NAME).py

docker:
	if ! diff -s ./$(PY) ../$(PY) > /dev/null ; then echo "Updating word2vec" ; cp ../$(PY) . ; fi
	docker build -t $(IMAGE) .
	docker tag $(IMAGE) $(TAG)

push:
	docker push $(TAG)

test:
	docker run -it -v `pwd`/../../data/testfiles:/input -v /tmp:/output embeddings/word2vec
