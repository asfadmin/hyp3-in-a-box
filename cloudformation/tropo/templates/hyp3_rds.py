# Converted from RDS_with_DBParameterGroup.template located at:
# http://aws.amazon.com/cloudformation/aws-cloudformation-templates/

from troposphere import Parameter, Ref
from troposphere.rds import DBInstance

from template import t

print('Adding hyp3 rds ')

t.add_description(
    "AWS CloudFormation Sample Template RDS_with_DBParameterGroup: Sample "
    "template showing how to create an Amazon RDS Database Instance with "
    "a DBParameterGroup.**WARNING** This template creates an Amazon "
    "Relational Database Service database instance. You will be billed for "
    "the AWS resources used if you create a stack from this template.")

dbuser = t.add_parameter(Parameter(
    "DBUser",
    NoEcho=False,
    Description="The database admin account username",
    Type="String",
    MinLength="1",
    MaxLength="16",
    AllowedPattern="[a-zA-Z][a-zA-Z0-9]*",
    ConstraintDescription=("must begin with a letter and contain only"
                           " alphanumeric characters.")
))

dbpassword = t.add_parameter(Parameter(
    "DBPassword",
    NoEcho=True,
    Description="The database admin account password",
    Type="String",
    MinLength="8",
    MaxLength="41",
    AllowedPattern="[a-zA-Z0-9]*",
    ConstraintDescription=("must contain only alphanumeric characters "
                           "and be from 8-41 characters in length.")
))

# Only certain versions of postgres are supported on the smaller instance types
# https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html
mydb = t.add_resource(DBInstance(
    "MyDB",
    AllocatedStorage="5",
    DBInstanceClass="db.t2.micro",
    DBName="hyp3db",
    Engine="postgres",
    EngineVersion="9.5.10",
    MasterUsername=Ref(dbuser),
    MasterUserPassword=Ref(dbpassword),
))
