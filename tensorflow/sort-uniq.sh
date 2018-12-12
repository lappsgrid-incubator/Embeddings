#! /bin/sh

cd $1
IFS="
"

for file in `ls -1`
do
   echo $file
   sort $file | uniq -c | sort -r > ../sorted/$file
done