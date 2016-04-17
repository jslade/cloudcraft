#!/bin/bash

MINECRAFT_PORT=25565
MINECRAFT_SERVICE='minecraft'

function stop-server {
  echo "Here we stop the server"
  echo "We'll configure service user creds on the server"
  echo "Then use Boto to stop the instance from the hypervisor"
}

# listen for network connections on Minecraft's port.
command="lsof -iTCP:${MINECRAFT_PORT}"
count=0

while true ; do #this is so keyboard interrupts can interrupt the loop gracefully.
  while [ ${count} -lt 10 ] ; do
    echo "executing ${command}"
    conn=`$command`
    printf "The output of LSOF is:\n $conn"
    if [ -z "$conn" ] ; then
      echo "Minecraft is not running, check for SSH then shut the server"
      # If there's an established SSH connection, exit.
      # If not:
      stop-server
    fi
    echo "count is ${count}"
    if [[ $conn == *"(ESTABLISHED)"* ]] ; then
      echo "There is at least one player on the server."
      exit 0;
    fi
    echo "There are no players logged in currently"
    count=$((count+1))
    sleep 2 # Once it's done, update this to be a minute or so 
  done
done

echo "Here I should be calling the stop-server function"
stop-server
