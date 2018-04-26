# SignalBot -  Serverless

## Purpose

Project contains `serverless.yml` file for RESTful interface to receive JSON formated data from multiple types of *sensor bots*.

The design approach is to leverage serverless technology, and template as much as possible for easy duplication. The current architecture is using a **PostgreSQL** backend database, we also include a **DynamoDB** alternative for a more scalable design.

In addition there is a *SimBot/sim.py* file which contains a simulator and *SimBot/simbot* python package folder to simululation the *sensor bots*.

**Contents**
* [Install](#install)
* [Architecture](#architecture)
* [REST API](#api)
* [CloudFormation](#cloudformation)

## Install

This is going to leverage the AWS cloud and Serverless stack.

For Serverless workstation

* Create a new Amazon Linux AMI 2016-09
* `sudo yum install -y git`
* `git clone https://github.com/mcliff1/SignalBot`
* `sudo SignalBot/bootstrap.sh`
* create an IAM user account with a Key for access to CLI (would be nice to do this with a server role, but the serverless framework uses the API Key) 
* `sls config credentials --provider aws --key <publickey> --secret <privatekey>`
* in the *SignalBot/bot* directory run `sls info` (or `sls deploy`)
 

OR you can use this [cloud formation template](https://github.com/mcliff1/aws/blob/master/cfn-ec2workstation.json)
 
## Architecture


  start with
>  /api/metrics/soil 
>  {"beg":"beg","deviceid":"3c003e000247353137323334","soilmoisture1":"3308","soilmoisture2":"3498","soilmoisture3":"1","humidity":"16.9000","tempc":"22.0000","tempf":"71.6000","volts":"4.2250","battery":"104.9375"}
  
  parameters for the PostGre SQL database string to connect too

this module will build a postgres RDS database to back end the REST API

need to run shell script to set up database initially after load (this requires docker)

## API

### call GET

 <_Additional info about the call. _>

**URI** `GET /api/metrics/<bottype>`

**Params**
* **Required (or startdate or enddate)** `deviceid=[string]`
* **Required (or deviceid or enddate)** `startdate=[string]`
* **Required (or startdate or deviceid)** `enddate=[string]`
* **Optional** `CreatedAt="YYYY-MM-DD.HH:MM:SS"` (or partial)

< _example request_ >
_GET /api/metrics/soilbot_

_GET /api/metrics/soilbot?deviceid=1231-1231-1321-as12`_
  all readings on the specified BOT in the system

_GET /api/metrics/soilbot?startdata=2017-04-24_
  all readings on everything since 4/24/2017

_GET /api/metrics/soilbot?startdata=2017-04-24.16.00.00_
  all readings on the specific bot since 4P 4/24/2017 (Local)


**Success Response**

* **Code:** 200 <br />
  **Content:** `{ id: "soil-xxxx-xxx-xxx-xxx  ",  CreatedAt: "XXX" }`


**Error Response**

* **Code:** 510 <br />
  **Content:** `{ error: "db error" }`



## call POST



**URI** `POST /api/metrics/<bottype>` 


**Data Param**

Inbound JSON data string
< _what is required for a post_ >

**Success Response**

* **Code:** 200 <br />
  **Content:** `{ error: "db error" }`


**Error Response**

* **Code:** 510 <br />
  **Content:** `{ error: "db error" }`



### TODO

* need to make the VPC subnet's dynamic or variable
* better define the GET operation (allow parameters to get data to plot)
* cloudformation or serverless project to create the postgres DB
* get the static google-charts.js to deploy on S3

## DB Tool

If you have docker installed, this is a great tool

```
docker run -it -v /home/ec2-user/SignalBot:/scripts openbridge/ob_pysh-db psql -h dbid1.cwql9pca9fko.us-west-2.rds.amazonaws.com -p 5432 -U dbuser -d dbname1
```

## Cloudformation
[Back to Top](#purpose)


<table width="100%">
  <tr><th align="left">Dynabot</th></tr>
  <tr>
    <td width="100%" valign="top">
    <p>Creates everything</p>
    <h6>Pre Requistes</h6>
    <ol>
      <li>Static Content</li>
      <li>DNS name in Route53</li>
    </ol>
    <h6>Create Details</h6>
    <ol>
      <li>creates some S3 buckets</li>
      <li>a lambda function</li>
      <li>CFN, SSL cert</li>
      <li>Route53 DNS entry</li>
    </ol>
    </td>
  </tr>
</table>

## Graph

This part is still in development, the plan is to use a *REACT* framework and *GraphQL* to be able to generate serverless graphing capabilities.  We want to see if it makes sense to expose a *GraphQL* endpoint to leverage teh Google Charts.js or Charts.js.

* [Serverless Zone](https://serverless.zone/graphql-with-the-serverless-framework-79924829a8ca)
* [Serverless.com](https://serverless.com/blog/running-scalable-reliable-graphql-endpoint-with-serverless/)

biggest struggle was I needed to install yarn and set up the json.dependencies and then run `yarn install`

to install yarn, simply type `sudo npm i yarn -g`


## Reference

* [Stelligent CFN Templats](https://github.com/stelligent/cloudformation_templates/blob/master/README.md) on GitHub


