#!/bin/bash

room="w323"
room="wg06"
room="w115"
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
		ssh -oStrictHostKeyChecking=no -oConnectTimeout=1 -oBatchMode=yes $host "killall maya.bin -9; killall prman -9; pkill -9 -t -t pts/0; pkill -9 -t pts/1; pkill -9 -t pts/2; pkill -9 -t pts/3; pkill -9 -t pts/4; pkill -9 -t pts/4; pkill -9 -t pts/5; pkill -9 -t pts/6; pkill -9 -t pts/7; pkill -9 -t pts/8; pkill -9 -t pts/9"
	else
		echo "$host doesn't exist :c"
	fi
done
