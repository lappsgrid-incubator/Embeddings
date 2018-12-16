REPO=docker.lappsgrid.org
ORG=embeddings
PROG=word2vec
NAME=$(ORG)/$(PROG)
TAG=$(REPO)/$(NAME)

docker:
	docker build -t $(NAME) .
	docker tag $(NAME) $(TAG)

push:
	docker push $(TAG)

	