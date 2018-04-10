#!/bin/bash
# requires aws CLI and RDS create-db-instance access
# param: dbid,  dbname, username, password
#     host gets assigned
USAGE="Usage: ${0} <DBID> <DBNAME> <USERNAME> <PASSWORD>"
# parse the parms first
DBID=$1
DBNAME=$2
DBPORT=5432
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

echo "waiting for db to be created"
DBHOST=
while [ "x$DBHOST" == "x" ]; do
    echo -n "."
    sleep 5
    DBHOST=$(aws rds describe-db-instances --db-instance-identifier $DBID --query "DBInstances[*].[Endpoint]" | grep Address | sed -e 's/^.*://' | tr -d '" ')
    #echo "DBHOST: $DBHOST"
done
echo "DBHOST: $DBHOST"

# same dir as this script
if [ "x$DBHOST" == "x" ]; then 
  echo "rollback"
  aws rds delete-db-instance --db-instance-identifier ${DBID}
  exit 2
fi

#docker run -v $SCRIPTPATH:/scripts openbridge/ob_pysh-db "export PGPASSWORD='$PASSWORD'; psql -h $DBHOST -p 5432 -U $USERNAME -d $DBNAME -f /scripts/createdb.sql"
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P)"
echo "${DBHOST}:${DBPORT}:${DBNAME}:${USERNAME}:${PASSWORD}" > ${SCRIPTPATH}/.pgpass
chmod 600 ${SCRIPTPATH}/.pgpass
docker run -v $SCRIPTPATH:/root openbridge/ob_pysh-db psql -h $DBHOST -p $DBPORT -U $USERNAME -d $DBNAME -f /root/createdb.sql
rm ${SCRIPTPATH}/.pgpass
