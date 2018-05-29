# SignalBot -  Serverless

## Purpose

Project provides multiple implementations of a RESTful API to process JSON formatted data from multiple types of *sensor bots*.

The design approach is to leverage *CloudFormation* and *serverless* templates for easy duplication. The implementations will use both a **PostgreSQL** backend database, we also include a **DynamoDB** alternative for a more scalable design.

In addition the *pyapi.py* utility can maintain a list of endpoints for POST/GET operations, and there is a *simulator/sim.py* file which contains a simulator and *simulator/signalbot.py* is a python package folder to generate client traffic the *sensor bots*.

### Contents
* [Architecture](#architecture)
* [REACT](#REACT)
* [REST API](#api)
* [GraphQL](#graphql)
* [Install](#install--set-up-workstation)
* [References](#references)



## Architecture
[back to top](#purpose)

Each implementation is utilizing API Gateway and Lambda,  if provided in the configuration we will apply a custom URL in front of the API Gateway.


### PostgreSQL RDS implementation

This implementation is provided, to help bridge the user to a serverless model. There are many reasons why a relational database may be needed for reporting or archive that the DynamoDB solution would need to supplement.

The simplify implementation we will leverage the CloudFormation templates in the [mcliff1/aws](https://github.com/mcliff1/aws) repository.

### DynamoDB implementation


The DynamoDB implementation is truly serverless, the user does NOT need to have a VPC defined to use this.

The Lambda function connects to a DynamoDB table, the REST interface does not change.


## REACT

The **static** folder contains *NodeJS* files for the *REACT* framework to provide static graphs and interface to the API.


## API
[back to top](#purpose)

Example
>  POST /api/metrics/soil
>
> {"beg":"beg","deviceid":"3c003e000247353137323334","soilmoisture1":"3308","soilmoisture2":"3498","soilmoisture3":"1","humidity":"16.9000","tempc":"22.0000","tempf":"71.6000","volts":"4.2250","battery":"104.9375"}


#### GET

No parameters, returns count, and information about most recent add; deviceid and startdate parameters can be provided for filtering, there is no way in the API to get list of deviceid's.

**URI** `GET /api/metrics/<bottype>`

**Params**
* `deviceid=[string]` - returns all information about designated bot
* Both `deviceid` and `startdate` - returns information since date for specified bot

**example request**
_GET /api/metrics/soilbot_
**Content:** `{ 'count': xxx, 'deviceid' : 'xxxx-xxx-xxx-xxx', 'CreatedAt': 'XXX' }`

_GET /api/metrics/soilbot?deviceid=1231-1231-1321-as12`_
  all readings on the specified BOT in the system

_GET /api/metrics/soilbot?startdate=2018-05-02&deviceid=1231-1231-123-1230_
  all readings on the specific bot since 5/2/2018


**Success Response**

* **Code:** 200 <br />


**Error Response**

* **Code:** 510 <br />
  **Content:** `{ error: "db error" }`



#### POST



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




## Install / Set Up Workstation
[back to top](#purpose)

  You can run the Cloud Formation templates either from a CLI, or the AWS console.

 Prerequistes
 * create ACM (in us-east-1) for both the web and api
 * domainname must exist in hosted Zone

Run the [bot-cfn-base.json](https://github.com/mcliff1/SignalBot/blob/master/bot-cfn-base.json) template (ideally from the console); this will create S3 buckets, Cognito Pool, and set some properties in *SSM* that the serverless files will expect to use.

Next, create a SLS workstation, and deploy the serverless components (the workstation is created because need to run the *NodeJS* commands and need appropriate system permissions)





### SLS Workstation
  This server will be able to deploy SLS scripts.

Use the Cloud Formation template from *mcliff1/aws* [ec2-slsworkstation](https://github.com/mcliff1/aws/blob/master/ec2-slsworkstation.json)


OLD Steps
  These steps will bootstrap an EC2 instance (TODO - replace with CFN template)
  * Create a new Amazon Linux AMI 2016-09
  * `sudo yum install -y git`
  * `git clone https://github.com/mcliff1/SignalBot`
  * `sudo SignalBot/bootstrap.sh`
  * `git config --global --edit` to set GIT credentials
  * TODO - do we have the IAM role set up?
  * in the *SignalBot/bot* directory run `sls info` (or `sls deploy`)




### RDS DB Workstation

These only apply for the RDS solution, and will create a EC2 instance that you can use to connect to or bridge to the RDS instance of PostgreSQL.

For now use the *mcliff1/aws/bastion.json* script.

Use the bastion host template in *mcliff1/aws* and then run the following; enter the DB password at the prompt (in the future once the bastion.json settles down we can branch that and make this one-stop, along with some prebuilt utilities that know the location of the DB, they are available from CloudFormation).



### RDS build

You can either set up the RDS database from a snapshot or build from source. In either case you will need to run either *rds-postgres.json* or *rds-postgres-snapshot.json* template. These require that a *mcliff1/aws/vpc.json* stack has already created. The RDS will be non-publicly accessible and created in the private subnets of the VPC, a DB workstation or Bastion host will be required to directly access. The output parameters *dbname*, *dbuser*, and  *db_endpoint* can be queried from either stack (**TODO this isn't done yet**)


```
% git clone https://github.com/mcliff1/SignalBot
% docker run -it -v /home/ec2-user/SignalBot:/scripts openbridge/ob_pysh-db psql \
-h <db-endpoint-url> \
-p 5432 -U dbuser -d dbname1 -f /scripts/createdb.sql
```


This pulls the **SignalBot** repository locally (all we need is the create script) and runs a docker utility to load the database.




### Stacks
[back to top](#purpose)

In order to run these serverless stacks you need to create a [SLS Workstation](#SLS_Workstation).

<table width="100%">
  <tr><th align="left">Dynabot (SLS)</th></tr>
  <tr>
    <td width="100%" valign="top">
    <p>Creates everything</p>
    <h6>Prerequistes</h6>
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

<table width="100%">
  <tr><th align="left">Bot (SLS)</th></tr>
  <tr>
    <td width="100%" valign="top">
    <p>Creates everything</p>
    <h6>Prerequistes</h6>
    <ol>
      <li><a href="#RDS_build">rds build</a></li>
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
    <h6>Post Steps</h6>
    <ol>
    <li>Set RDS parameters on Lambda function</li>
    </ol>
    </td>
  </tr>
</table>


### TODO

* need to make the VPC subnet's dynamic or variable
* better define the GET operation (allow parameters to get data to plot)
* cloudformation or serverless project to create the postgres DB
* get the static google-charts.js to deploy on S3
* should we also back this to S3 (we could put some version control on there and a Lambda trigger) (for DyanmoDB)
* parameters for the PostGre SQL database string to connect too



## GraphQL
[back to top](#purpose)

This part is still in development, the plan is to use a *REACT* framework and *GraphQL* to be able to generate serverless graphing capabilities.  We want to see if it makes sense to expose a *GraphQL* endpoint to leverage teh Google Charts.js or Charts.js.



biggest struggle was I needed to install yarn and set up the json.dependencies and then run `yarn install`

to install yarn, simply type `sudo npm i yarn -g`





## References
[back to top](#purpose)

* [Stelligent CFN Templats](https://github.com/stelligent/cloudformation_templates/blob/master/README.md) on GitHub
* [Serverless Zone](https://serverless.zone/graphql-with-the-serverless-framework-79924829a8ca)
* [Serverless.com](https://serverless.com/blog/running-scalable-reliable-graphql-endpoint-with-serverless/)
