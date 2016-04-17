#!/usr/bin/python

# This script requires the Python library Boto3 to be present on your system.
# Run `pip install boto3` or download from here: http://aws.amazon.com/sdk-for-python/ 

# User relevant defaults follow below 
minecraftClient = "/usr/local/Minecraft.jar" # The path to your Minecraft client. 
minecraftPort = 25565 # Port that Minecraft is running on. This is the default.

import boto3
import socket
import time
from contextlib import closing
from subprocess import call

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

def startServer(instance):
  print "Starting instance"
  instance.start()
  waiter = client.get_waiter('instance_running')
  print "Waiting for instance state to change to running"
  waiter.wait(InstanceIds=[instance.id])
  checkSocket(instance.public_ip_address, minecraftPort)

def launchMinecraft():
  call(["java", "-jar", minecraftClient])

def fetchServerState():
  print "Fetching information on the Minecraft server..."
  instances = ec2.instances.filter(
    Filters=[{'Name': 'tag:role', 'Values': ['minecraft']}]
  )
  id = []
  for instance in instances:
    id.append(instance)
  if len(id) != 1:
  	print "You have %d Minecraft servers, so I don't know which you want to connect to." % len(id)
  	print "This is confusing, so I'm I'm stopping now."
  else:
    return id

def checkSocket(host, port):
  print "Checking state of port %d on host %s host" % (port, host)
  with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
    if sock.connect_ex((host, port)) == 0:
      print "Port is open, launching Minecraft client"
      launchMinecraft()
    else:
      count = 0
      while (count < 12):
      	print "Port shut, waiting 10 seconds."
      	count = count + 1
     	time.sleep(10)
      	print "Trying again: we've tried %d times so far." % count
      	if sock.connect_ex((host, port)) == 0:
          print "Port is open, launching Minecraft client"
          launchMinecraft()
      if (sock.connect_ex((host, 22)) == 0):
      	print "Minecraft's not running but ssh is up. Go check out what's up w/ your server."
      else:
      	print "Welp, something's not right there. Go check out what's up w/ your server"

print "This script checks if the Minecraft server is running, and starts it if needed!"
instance = fetchServerState()[0]

print "The instance's current state is %s" % instance.state['Name']

if (instance.state['Name'] == 'stopped'):
  startServer(instance)
elif instance.state['Name'] in [ 'shutting-down', 'stopping' ]:
  waiter = client.get_waiter('instance_stopped')
  print "Instance is mid-state change; waiting for it to stabilise."
  waiter.wait(InstanceIds=[instance.id])
  startServer(instance)
else:
  checkSocket(instance.public_ip_address, minecraftPort)
