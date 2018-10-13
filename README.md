# SignalBot -  Cloud based RESTful API

This project provides mutliple implementations of a RESTful API to process JSON formatted data from simulated *sensor bots*.

The design approach is to leverage *CloudFormation* and *serverless* templates for easy duplication. The implementations will use both a **PostgreSQL** backend database, we also include a **DynamoDB** alternative for a more scalable design.

The *simulator/sim.py* provides a simulator which will publish events either to **HTTP POST** or direct to file system. *simulator/signalbot.py* is a python object model for the *bots*.

In addition the *pyapi.py* utility can maintain a list of endpoints for POST/GET operations, the *swagger* file [swagger.yaml](https://github.com/mcliff1/SignalBot/raw/master/swagger.yaml) is availble for the *OpenAPI 2.0* standard.


TODO - make a cloud formation stack that takes a RDS snapshot as input
builds the right DB target;  for the purpose of being able to have a code source (GitHub or CodeCommit) be able to trigger builds from a specific branch.


### Contents
* [Architecture](#architecture)
* [REST API](#api)
* [Code](#code)
* [Install](#install)
* [References](#references)



## Architecture
[back to top](#purpose)

There are four basic components to the Architecture
* Foundational components - Hosted Zone, and SSL certs must be set up (Route53, and Certificate Manager) independent of any AWS templates or configuration
* Framework components - S3 buckets, Cloud Resources (SNS, Parameter Manager) generated for each environment with *bot-cfn-base.json* template
* API Layer - Lambda/API Gateway configuration providing REST interface
* Persistence Layer - A DynamoDB and a PostgreSQL RDS implementation are provided



As of June 2018, the foundational components will have a recurring cost of *$0.50* a month for running a hosted zone in Route53, all other costs are withing the AWS Free Tier.  Beyond the free tier the expenses for the DynamoDB are the lowest, and based on transactional volume (you should be able to get *o(10^6)* transactions for under a dollar).  The *RDS* expense will be driven off the footprint of the server.

DynamoDB is not intended for a long-term store of the data, it does serve all the needs for a fully functional and scalable run-time API. For a future state we would like to include *AWS IOT* as an alternative to *HTTP POST* to the API.

### Static Content Presentation

Both implementations utilize *S3* and *CloudFront* to present the *REACT* based UI.

The **static** folder contains *NodeJS* files for the *REACT* framework to provide static graphs and interface to the API.


### PostgreSQL RDS backed API

This implementation is provided, to help bridge the user to a serverless model. There are many reasons why a relational database may be needed for reporting or archive that the DynamoDB solution would need to supplement.



### DynamoDB backed API


The DynamoDB implementation is truly serverless, the user does NOT need to have a VPC defined to use this.

The Lambda function connects to a DynamoDB table, the REST interface does not change.




## API
[back to top](#purpose)

Open this link with
 swagger UI -
 [swagger.yaml](https://github.com/mcliff1/SignalBot/raw/master/swagger.yaml)





 ## Code
 [back to top](#purpose)

Explain layout of code.

Use 'develop', 'test', and 'master' branch to reflect environments.





 ## Install
 [back to top](#purpose)

The install path depends on the API implementation, there are several common steps.

### Prerequistes

Before running any scripts of utilities in this repository, there must be an AWS account, with a hosted zone and two SSL certs created in the *us-east-1* region. Two **A** record will be created.

* a Hosted Zone must exist in the AWS account
* SSL certs for the web host and the api need to be created in the us-east-1 Zone

### Common Framework

This cloud formation template takes the DNS, host, and cert information and creates a stack that is leveraged by the *serverless* templates.  The [bot-cfn-base.json](https://github.com/mcliff1/SignalBot/blob/master/bot-cfn-base.json) template creates the following resources

Currently the serverless.yml is hardcoded to look for **botbase**

* *SNS* Topic for stack related events
* *Cognito* User Pool
* *S3* Bucket to perform automated builds
* *S3* Bucket to host static web Content
* *CloudFront* distribution
* *Route53* DNS Entries for Web
* Stores key parameters in the *Parameter Store*
* *CodeBuild* project is set up with GitHub source (which docker image to build with and how to set environment variables)

You can run the Cloud Formation templates either from a CLI, or the AWS console.

### SLS Workstation to deploy Static code and serverless


In order to deplpy the Serverless code, we need to set up a SLS workstation, there is a template that does this
Next, create a SLS workstation, and deploy the serverless components (the workstation is created because need to run the *NodeJS* commands and need appropriate system permissions).


Can I do all this with a docker image instead?


Use the Cloud Formation template from *mcliff1/aws* [ec2-slsworkstation](https://github.com/mcliff1/aws/blob/master/ec2-slsworkstation.json)

Then create a *IAM* role we will need to install using the right script. **TODO** we need to clean up thse permissions scripts, there is a different set for deploying static content, api level, and the different DBs.;
the EC2 create should take as optional input a *stack* name that was used as a base;  this sets  a parameter in *SSM* called `/{stackname}/iamEc2Role`


TODO - this should create the IAM role necessary


Log into the server; pull the code from GitHub and deploy
* `git config --global --edit`  to set up GIT credentials
* `git clone https://github.com/mcliff1/SignalBot`


### Run Static Web Deploy

`./deploy-web.sh` run from the SLS server will do everything necessary (in *us-west-2*)

Then sync the build directory to the S3 bucket for the web (which can be gotten from *SSM*)

AWS *CodeBuild* is set up as part of the template, by default it is connected to [this](https://github.com/mcliff1/SignalBot.git) GitHub repository.



### Deploy DyanmodDB backend

If you choose the *RDS* option, skip this section.

Here is it different based on the implementation, for Dynabot
* `cd SignalBot/dynabot`
* `sls deploy --region us-west-2` (or whatever region you are running in, the EC2 instance has no default)

This has the basestack name hard coded as **botbase**.


This creates the Lambda function, API gateway, API DNS name, and DynamoDB table.



### RDS backed API

If you choose the *DynamoDB* option, skip this section

The simplify implementation we will leverage the CloudFormation templates in the [mcliff1/aws](https://github.com/mcliff1/aws) repository.

You can either set up the RDS database from a snapshot or build from source. In either case you will need to run either *rds-postgres.json* or *rds-postgres-snapshot.json* template. These require that a *mcliff1/aws/vpc.json* stack has already created. The RDS will be non-publicly accessible and created in the private subnets of the VPC, a DB workstation or Bastion host will be required to directly access. The output parameters *dbname*, *dbuser*, and  *db_endpoint* can be queried from either stack (**TODO this isn't done yet**)


```
% git clone https://github.com/mcliff1/SignalBot
% docker run -it -v /home/ec2-user/SignalBot:/scripts openbridge/ob_pysh-db psql \
-h <db-endpoint-url> \
-p 5432 -U dbuser -d dbname1 -f /scripts/createdb.sql
```


This pulls the **SignalBot** repository locally (all we need is the create script) and runs a docker utility to load the database.

### RDS DB Workstation

These only apply for the RDS solution, and will create a EC2 instance that you can use to connect to or bridge to the RDS instance of PostgreSQL.  It is NOT necessary to build this server to run the solution. The RDS server is created in a private VPC subnet with no access to the public internet.

For now use the *mcliff1/aws/bastion.json* script.

Use the bastion host template in *mcliff1/aws* and then run the following; enter the DB password at the prompt (in the future once the bastion.json settles down we can branch that and make this one-stop, along with some prebuilt utilities that know the location of the DB, they are available from CloudFormation).




### Stacks
[back to top](#purpose)

In order to run these serverless stacks you need to create a [SLS Workstation](#SLS_Workstation).

<table width="100%">
  <tr><th align="left">CFN Foundation</th></tr>
  <tr width="100%">
    <td width="100%" valign="top">
    <p>Creates static resources for managing the stack, and sets parameters for other stacks</p>
    <h6>Prerequistes</h6>
    <ol>
      <li>SSL certs created for API and Web interface in us-east-1</li>
      <li>Hosted Zonein Route53</li>
    </ol>
    <h6>Parameters</h6>
    <ol>
      <li>Stack Name - calling stacks default to botbase</li>
      <li>Domain Name - must have hosted zone in route 53</li>
      <li>Hostnames for the Web and API Interface - should match the SSL cert name that was created</li>
      <li>ARN for the 2 SSL certificates created as prerequistes (to match the hostnames)</li>
      <li>GitHub Source - for the static content, not currently used</li>
      <li>SNS Topic - used for notifications related to this stack</li>
    </ol>
    <h6>Create Details</h6>
    <ol>
      <li>creates S3 bucket for web and build</li>
      <li>CFN Distribution</li>
      <li>Route53 DNS entry</li>
      <li>Cognito User Pool</li>
      <li>SSM Parameters used by  the SLS stack and EC2 stacks</li>
    </ol>
    </td>
  </tr>
</table>


<table width="100%">
  <tr><th align="left">Dynabot (SLS)</th></tr>
  <tr width="100%">
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



## References
[back to top](#purpose)

* [Stelligent CFN Templats](https://github.com/stelligent/cloudformation_templates/blob/master/README.md) on GitHub
* [Serverless Zone](https://serverless.zone/graphql-with-the-serverless-framework-79924829a8ca)
* [Serverless.com](https://serverless.com/blog/running-scalable-reliable-graphql-endpoint-with-serverless/)
