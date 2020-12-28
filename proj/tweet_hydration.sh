#!/bin/bash
start=1
end=86
extension1=".txt"
extension2=".jsonl"
file_name1="id_tweets_"
file_name2="hydrated_tweets_"
for i in $(seq  $end);
do
	if [ ${i} -lt 10 ]
	then
		echo ${file_name}0${i}${extension1}
		twarc hydrate ../${file_name1}0${extension1} > ../${file_name2}${extension2}
	else
        echo ${file_name}${i}${extension1}
		twarc hydrate ../${file_name1}${extension1} > ../${file_name2}${extension2}
	fi
done