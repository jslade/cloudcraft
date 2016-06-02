#!/bin/bash

MINECRAFT_PORT=25565
MINECRAFT_SERVICE='minecraft'

function stop-server {
  echo "Users logged on to the server are: `users`"
  echo "Stopping the server at `date`"
  instance=`aws ec2 describe-instances --filters Name=tag:role,Values=minecraft --query Reservations[].Instances[].[InstanceId] | grep -o '".*"' | sed 's/"//g'`
  aws ec2 stop-instances --instance-ids $instance
}

# listen for network connections on Minecraft's port.
counter=0

while [[ "${counter}" -lt 10 ]] ; do
  command="/usr/sbin/ss -t sport == ${MINECRAFT_PORT}"
  conn=`$command`
  echo ${conn}
  if [[ ${conn} == *"ESTAB"* ]] ; then
    echo "Minecraft is running"
    exit 0
  else
    echo "conn is $conn"
    echo "Minecraft has no connected users at `date`, now let's check for logged in users."
  fi

  sessions=`users`
  echo "Logged in users at `date` are: $sessions"

  if [ "${sessions}" == '' ] ; then
    counter=$((counter+1))
    echo "Count is now $counter"
  else
    echo "Someone's logged in, sleeping."
    exit 0
  fi

  sleep 60

done

if [ "${counter}" -ge "10" ]
then
  echo "Shutting down now at `date`"
  stop-server;
fi
