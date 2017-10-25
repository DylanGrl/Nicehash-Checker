#!/bin/sh


#
# TO CHANGE !!!!!
# CHANGE THIS NAME IF YOU RENAME THE PYTHON SCRIPT AND THE NEW NAME DOEST CONTAIN NICEHASH
# BE SURE THAT NO OTHER SCRIPT GOT THE SAME NAME
#
SERVICE='nicehash'


if ps ax | grep -v grep | grep $SERVICE > /dev/null
then
	# IF THE SERVICE IS RUNNING WE WAIT 1H AND CHECK AGAIN
    echo "$SERVICE service running, everything is fine"
	sleep 1h
	#
	# TO CHANGE !!!!!
	# CHANGE THE LOCATION AND PUT THE LOCATION WHERE THIS SCRIPT IS
	#
	bash /location/of/checkNicehashRun.sh
else
	# IF THE SERVICE ISNT RUNNING WE LAUNCH IT AND CHECK AGAIN IN 1H
    echo "$SERVICE is not running"
    #
    # TO CHANGE !!!!! PUT HERE THE COMMANDE TO EXECUTE TO RELAUNCH THE PYTHON SCRIPT
    #
	python3 /location/of/my/script/nicehash_checker.py MY_BTC_ADRESS .... COMPLETE WITH THE PARAM YOU USE TO START THE PYTHON SCRIPT
	sleep 1h
	bash /location/of/checkNicehashRun.sh
fi
