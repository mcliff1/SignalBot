#!/bin/bash
# requires aws CLI and RDS create-db-instance access
# param: dbid,  dbname, username, password
#     host gets assigned
USAGE="Usage: ${0} <DBID> <DBNAME> <USERNAME> <PASSWORD> <DBHOST>"
# parse the parms first
DBID=$1
DBNAME=$2
DBPORT=5432
USERNAME=$3
PASSWORD=$4
DBHOST=$5
if [ "x$DBHOST" == "x" ]; then
  echo $USAGE
  exit 1
fi

#echo "create instance id : $DBID, Name: $DBNAME, USerName: $USERNAME, and PAssword: $PASSWORD"

# this is done in cloud formation
#3aws rds create-db-instance \
#  --db-name ${DBNAME} \
#  --db-instance-identifier ${DBID} \
#  --allocated-storage 5 \
#  --db-instance-class db.t2.micro \
#  --engine postgres \
#  --master-username ${USERNAME} \
#  --master-user-password ${PASSWORD} \
#  --backup-retention-period 3 \
#  --no-publicly-accessible

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P)"
echo "${DBHOST}:${DBPORT}:${DBNAME}:${USERNAME}:${PASSWORD}" > ${SCRIPTPATH}/.pgpass
chmod 600 ${SCRIPTPATH}/.pgpass
docker run -v $SCRIPTPATH:/root openbridge/ob_pysh-db psql -h $DBHOST -p $DBPORT -U $USERNAME -d $DBNAME -f /root/createdb.sql
rm ${SCRIPTPATH}/.pgpass
