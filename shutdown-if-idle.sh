#!/bin/bash

MINECRAFT_PORT=25565
MINECRAFT_SERVICE='minecraft'

function stop-server {
  echo "Here we stop the server"
  echo "We'll configure service user creds on the server"
  echo "Then use Boto to stop the instance from the hypervisor"
}

# listen for network connections on Minecraft's port.
command="ss -t sport == ${MINECRAFT_PORT}"
counter=0

while [[ "${counter}" -lt 10 ]] ; do
  conn=`$command`

  if [[ ${conn} == *"ESTAB"* ]] ; then
    echo "Minecraft is running"
    exit 0
  else
    echo "Minecraft has no connected users, now let's check for logged in users."
  fi

  sessions=`users`
  echo "Logged in users are: $sessions"

  if [ "${sessions}" == '' ] ; then
    counter=$((counter+1))
    echo "Count is now $counter"
  else
    echo "Someone's logged in, sleeping."
    exit 0
  fi

  sleep 180

done

instance=`aws ec2 describe-instances --filters Name=tag:role,Values=minecraft --query Reservations[].Instances[].[InstanceId] | grep -o '".*"' | sed 's/"//g'`
aws ec2 stop-instances --instance-ids $instance
