#!/bin/bash

passwd=test

if [[ -z $1 ]]; then
	echo admin!
	rabbitmqctl add_user admin admin
	rabbitmqctl set_user_tags admin administrator
	rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"
	rabbitmqctl set_topic_permissions -p / admin amq.topic ".*" ".*"
	exit 0
fi

while [ $# -gt 0 ]; do
	case "$1" in
		* )
		rabbitmqctl add_user $1 $passwd
		rabbitmqctl set_permissions -p / $1 ".*" ".*" ".*"
		rabbitmqctl set_topic_permissions -p / $1 amq.topic ".*" ".*"
		;;
	esac
	shift
done


