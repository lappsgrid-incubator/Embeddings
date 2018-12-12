#! /bin/sh

cd $1
IFS="
"

for file in `ls -1`
do
    echo $file
	perl /Users/ide/Dropbox/inProgress/Livny-project/experiment/tensorflow/add-tags.pl $file
done