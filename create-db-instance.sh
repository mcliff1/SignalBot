#!/bin/bash
# requires aws CLI and RDS create-db-instance access
# param: dbid,  dbname, username, password
#     host gets assigned
USAGE="Usage: ${0} <DBID> <DBNAME> <USERNAME> <PASSWORD>"
# parse the parms first
DBID=$1
DBNAME=$2
USERNAME=$3
PASSWORD=$4
if [ "x$PASSWORD" == "x" ]; then
  echo $USAGE
  exit 1
fi

echo "create instance id : $DBID, Name: $DBNAME, USerName: $USERNAME, and PAssword: $PASSWORD"

aws rds create-db-instance \
  --db-name ${DBNAME} \
  --db-instance-identifier ${DBID} \
  --allocated-storage 5 \
  --db-instance-class db.t2.micro \
  --engine postgres \
  --master-username ${USERNAME} \
  --master-user-password ${PASSWORD} \
  --backup-retention-period 3 \
  --no-publicly-accessible 

