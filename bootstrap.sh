#!/bin/bash

sudo yum -y install git POST
# to be executed as user with sudo privilege

curl --silent --location https://rpm.nodesource.com/setup_8.x | sudo bash -
sudo yum -y install nodejs

# expect error message about update at the end
sudo npm i -g serverless
sls version

echo "run 'sls config credentials --provider aws --key <publickey> --secret <privatekey>'"

echo "run 'git config --global --edit'"
echo "run 'git clone https://github.com/mcliff1/SignalBot'"


