# AWS Training


### Area
 Frankfurt (EU-Central-1). This is the one we want to use for our training. Also the one we have permission to use.

 ### Least Privileged --> Minimum access given to users

 ### EC2 Homepage

 Elastic Compute Cloud (EC2) is a web service that provides resizable compute capacity in the cloud. It allows users to run virtual servers, known as instances, in a secure and scalable environment.

 It is infrastucture as a service (IaaS) that enables users to deploy and manage applications without the need to invest in physical hardware.

 ### SSH
 An SSH (Secure Shell) key pair is a set of cryptographic keys used for secure access to remote servers. It consists of a public key and a private key. The public key is stored on the server, while the private key remains with the user. When connecting to the server, the SSH protocol uses these keys to authenticate the user and establish a secure connection.

 ### 1. New Key Pair
 To create a new key pair in AWS, follow these steps:
  1. Log in to the AWS Management Console.
  2. Navigate to the EC2 service.
  3. In the left-hand menu, click on "Key Pairs" under the "Network & Security" section.
  4. Click on the "Create Key Pair" button.
  5. Provide a name for the key pair and select the desired key pair type (RSA or ED25519).
  Naming convention:  `se-yourname-key-pair`

  key pair type: RSA (2048 bits) or ED25519 (recommended for better security)
  preivously created key pairs cannot be downloaded again, so make sure to save the private key file (.pem) in a secure location. Public key ends in .pub and private key has no extension. Here we get AWS to make it. Use a OpenSSSH client.

  RSA.pem

get agreen bar saying "succesfully created key pair" and download the private key file (.pem) to your local machine. Make sure to store it securely, as it will be required for SSH access to your EC2 instances.

### Once Dowloaded

Move .pem file to users .ssh file but with the cut function or in the terminal use the mv command to move the file to the .ssh directory. For example, if your username is "user" and the .pem file is named "se-yourname-key-pair.pem", you would run the following command:

```bash
mv se-yourname-key-pair.pem ~/.ssh/
``` 
### Intiating a connection 

To initiate a connection to your EC2 instance using the SSH key pair, follow these steps:
1. Open a terminal on your local machine.
2. Navigate to the directory where your private key file (.pem) is located. If you followed the previous step, it should be in the `~/.ssh/` directory.
3. launch instance on AWS and choose aws image using ubuntu
4. Choose ubuntu 24.04 LTS (HVM), SSD Volume Type
5. Choose instance type: t3.micro (free tier eligible), this is because by design nothing we are doing requires much processing power. t3 micro requires 2cpus and 1gb ram. This is more than enough for our training. Notice the price per hour is $0.0104, which is very cheap. If you are using a different instance type, the price may vary.
6. key pair: choose your previously created key pair (se-yourname-key-pair)
7. Network settings: This si the tricky bit. Keep it as simple as possible for now. We dont want it to be called "launch wizard 33". Click on edit button, dopnt worry about vpc, subnet, availability and auto assign public IP enabled. I called my group name "se-harry-basic-sg". 
Description: lazy and just copy group name.
7. Rules: Type: SSH Port 22, PRtoocol: TCP, SourceType: Anywhere, info  - cant change this, but it is ok for now. We will change it later to be more secure. You wouldnt do this in the real world  - but in training. Note: MYIP does clock my real ip address.
8. Add another security rule: Type: custom: port 80. Source Type: Anywhere.
9. Leave storage as is and laucnh should go green. The id it produces is a link which is a summary page for that particular resource. 
10. Connect to the instance (using my linux shell)
 make sure the permission is changed using chmod 400 "key.pem". Then past the command into a terminal in your .ssh file. ssh -i "se-yourname-key-pair.pem" ubuntu@ec2-xx-xx-xx-xx.compute.amazonaws.com. Every space is like a new argument.
    - ssh - use ssh
    - -i - specify the identity file (private key)
    - "se-yourname-key-pair.pem" - the private key file
    - ubuntu@ec2-xx-xx-xx-xx.compute.amazonaws.com - the EC2 instance address (if your not in the directory use the path to the .pem file). 

10. Are you sure you want to contonue connecting  - the computer here is trying to protect us saying you connecirtng to a server that we dont know about are you sure you want to connect. Type yes and hit enter. This will add the server to your known hosts file. You should now be connected to your EC2 instance via SSH.


## Getting started with AWS Linux

`sudo apt update` - updates the package lists for upgrades and new package installations.

