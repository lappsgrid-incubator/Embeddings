FROM python:3.6

#RUN apt update && apt upgrade -y
#RUN apt install python3-pip
#RUN apk add --virtual build-deps gcc python-dev
RUN pip3 install nltk numpy 
RUN pip3 install --upgrade gensim

COPY *.py /app/
COPY word2vec.ini /app/
WORKDIR /app
RUN python3 download.py
CMD ["python3", "word2vec.py", "-d", "/input", "-m", "/output/data.model"]

