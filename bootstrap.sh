#!/bin/bash
#
#  this script can be run on a EC2 instance to load and enable the serverless python environmnet
# to be executed as user with sudo privilege
#
#  expect that we have already cloned this file could be pulled from
# wget https://raw.githubusercontent.com/mcliff1/SignalBot/master/bootstrap.sh
#echo "run 'git clone https://github.com/mcliff1/SignalBot'"

sudo yum -y install git docker tmux

# ensures we install 
curl --silent --location https://rpm.nodesource.com/setup_8.x | sudo bash -
sudo yum -y install nodejs

# expect error message about update at the end
sudo npm i -g serverless
sudo npm i -g yarn
#sls version

sudo pip install numpy
sudo pip install psycogpg2
sudo pip install plyint

echo "run 'sls config credentials --provider aws --key <publickey> --secret <privatekey>'"

echo "run 'git config --global --edit'"


