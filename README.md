# Cloudcraft

This is a simple set of tools for managing a Minecraft server hosted on AWS.

It requires: Python 2, Boto3 with credentials configured, and permission to start and stop ec2 instances on the target AWS account.

## Usage

Both the startup and the shutdown script need to be run on computers with AWS credentials configured. Don't use the root credentials here - make a new user account to do the automated shutdown of the server, with minimal privileges. The `minecraft-admins.json` policy attached will let the user start and stop only ec2 instances tagged with 'role: minecraft'.

## Configuring the server

Here are roughly the steps to take. In this guide, I'm installing Minecraft to run as a service user called minecraft, because it's both more secure and more convenient:

- Spin up a Linux ec2 instance with a securitygroup that allows SSH (TCP port 22) and Minecraft traffic (25565 by default) from your IP address and that of any friends
- SSH in, create a `minecraft` user, and install Minecraft (or Forge) as that user.
- Configure Minecraft to start on boot (see: http://minecraft.gamepedia.com/Tutorials/Server_startup_script)
- Install the AWS commandline tools. `sudo yum install awscli` as the ec2-user.
- `sudo su` to the minecraft user and run `aws ec2 describe-instances` it'll and walk through the steps of adding credentials.
- Save the shutdown-if-idle.sh script to the server and mark it as executable (chmod 744 shutdown-if-idle.sh)
- Add that to the Minecraft users's crontab with `crontab -e`.

Further to that, you can install an FTP client like vsftpd to make the process of importing or backing up worlds much more convenient. Invaluable if you're playing modded Minecraft!

## Configuring your client

Once you've got the server running you're mostly done. The client-side config is just a Python script starts the server and boots the Minecraft jar you specify. 

To start the server, it'll need the boto3 Python library, and credentials configured.

Install the Python package manager 'pip' for your operating system of choice, and then run `pip install boto3` with appropriate permissions.

Then just update these values as appropriate for your computer:

```
# User relevant defaults follow below
minecraftClient = "/usr/local/Minecraft.jar" # The path to your Minecraft client.
minecraftPort = 25565 # Port that Minecraft is running on. This is the default.
```

Have fun!
