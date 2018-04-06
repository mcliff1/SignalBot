# SignalBot -  Serverless
Repository for project to build deployable units that can send information back to a central server via standard format (json post)


This is going to leverage the AWS cloud and Serverless stack.

For Serverless workstation

* Create a Amazon Linux AMI 2016-09, with the bootstrap.sh from this repository  (`node -v` *8.11.1*; and npm -v 5.6.0)
* git clone this folder and cd into signal bot
  - use https://  and `git config --global --edit`  first
* create an IAM user account with a Key for access to CLI  (NOTE: can I do this with server role instead?)
* `sls config credentials --provider aws --key <publickey> --secret <privatekey>`
* `sls deploy`
  
  start with
>  /api/metrics/soil 
>  {"beg":"beg","deviceid":"3c003e000247353137323334","soilmoisture1":"3308","soilmoisture2":"3498","soilmoisture3":"1","humidity":"16.9000","tempc":"22.0000","tempf":"71.6000","volts":"4.2250","battery":"104.9375"}
  
  parameters for the PostGre SQL database string to connect too
 

## Graph

attempting to get GraphQL to do the work for me.

* [Serverless Zone](https://serverless.zone/graphql-with-the-serverless-framework-79924829a8ca)
* [Serverless.com](https://serverless.com/blog/running-scalable-reliable-graphql-endpoint-with-serverless/)

biggest struggle was I needed to install yarn and set up the json.dependencies and then run `yarn install`

to install yarn, simply type `sudo npm i yarn -g`

