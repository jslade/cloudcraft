#!/usr/bin/python

# This script requires the Python library Boto3 to be present on your system.
# Run `pip install boto3` or download from here: http://aws.amazon.com/sdk-for-python/ 

# User relevant defaults follow below 
minecraftClient = "/usr/local/Minecraft.jar" # The path to your Minecraft client. 
minecraftPort = 25565

import boto3
import socket
from contextlib import closing
from subprocess import call
from pprint import pprint 

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')


def startServer(instance):
  print "Starting instance"
  instance.start()
  waiter = client.get_waiter('instance_running')
  print "Waiting for instance state to change to running"
  waiter.wait(instance.id)
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
  	print "You have %d Minecraft servers. This is confusing. I'm stopping now." % len(id)
  else:
    return id

def checkSocket(host, port):
  print "Checking state of port %d on host %s host" % (port, host)
  with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
    if sock.connect_ex((host, port)) == 0:
      print "Port is open, launching Minecraft client"
      launchMinecraft()
    else:
      print "Port is not open"
      # retry loop here

# def retryloop(attempts, timeout):
#     starttime = time.time()
#     success = set()
#     for i in range(attempts): 
#         success.add(True)
#         yield success.clear
#         if success:
#             return
#         if time.time() > starttime + timeout:
#             break
#     raise RetryError

print "This script checks if the Minecraft server is running, and starts it if needed!"
instance = fetchServerState()[0]

print "The instance's current state is %s" % instance.state['Name']

if instance.state['Name'] != 'running':
  startServer(instance)
else:
  checkSocket(instance.public_ip_address, minecraftPort)