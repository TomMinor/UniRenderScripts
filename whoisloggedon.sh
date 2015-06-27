#!/bin/bash

room="$1"

for i in {0..70}
do
	currentNumber=$i
	host=$(printf "%s%.2d" $room $currentNumber)	
	getent hosts $host >/dev/null 2>/dev/null
	returnCode=$?

	if [ $returnCode -eq 0 ]
	then
		echo "$host exists"
		ssh -oStrictHostKeyChecking=no -oConnectTimeout=1 -oBatchMode=yes $host "echo ----------\$(hostname)----------; w "
	else
		echo "$host doesn't exist :c"
	fi
done
