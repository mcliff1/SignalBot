# SignalBot -  Serverless
Project contains `serverless.yml` file for RESTful interface to receive JSON formated data from multiple types of *sensor bots*.

The design approach is to leverage serverless technology, and template as much as possible for easy duplication. The current architecture is using a **PostgreSQL** backend database, but we expect to leverage **DynamoDB** as an alternative for a more scalable design.

In addition there is a *sim.py* file which contains a python object model to simululation the *sensor bots*.

## Architecture
This is going to leverage the AWS cloud and Serverless stack.

For Serverless workstation

* Create a new Amazon Linux AMI 2016-09
* `sudo yum install -y git`
* `git clone https://github.com/mcliff1/SignalBot`
* `sudo SignalBot/bootstrap.sh`
* create an IAM user account with a Key for access to CLI (would be nice to do this with a server role, but the serverless framework uses the API Key) 
* `sls config credentials --provider aws --key <publickey> --secret <privatekey>`
* in the *SignalBot/bot* directory run `sls info` (or `sls deploy`)
  
  start with
>  /api/metrics/soil 
>  {"beg":"beg","deviceid":"3c003e000247353137323334","soilmoisture1":"3308","soilmoisture2":"3498","soilmoisture3":"1","humidity":"16.9000","tempc":"22.0000","tempf":"71.6000","volts":"4.2250","battery":"104.9375"}
  
  parameters for the PostGre SQL database string to connect too

### TODO

* need to make the VPC subnet's dynamic or variable
* better define the GET operation (allow parameters to get data to plot)

## DB Tool

If you have docker installed, this is a great tool

```
docker run -it -v /home/ec2-user/SignalBot:/scripts openbridge/ob_pysh-db psql -h dbid1.cwql9pca9fko.us-west-2.rds.amazonaws.com -p 5432 -U dbuser -d dbname1
```

## Graph

This part is still in development, the plan is to use a *REACT* frameweok and *GraphQL* to be able to generate serverless graphing capabilities.

* [Serverless Zone](https://serverless.zone/graphql-with-the-serverless-framework-79924829a8ca)
* [Serverless.com](https://serverless.com/blog/running-scalable-reliable-graphql-endpoint-with-serverless/)

biggest struggle was I needed to install yarn and set up the json.dependencies and then run `yarn install`

to install yarn, simply type `sudo npm i yarn -g`

