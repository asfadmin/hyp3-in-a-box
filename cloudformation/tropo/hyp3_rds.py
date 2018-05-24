# Converted from RDS_with_DBParameterGroup.template located at:
# http://aws.amazon.com/cloudformation/aws-cloudformation-templates/

# Parameter, Ref, Template
import troposphere as ts
# import DBInstance
import troposphere.rds as rds
import troposphere.ec2 as ec2
import sys


t = ts.Template()

t.add_description(
    "AWS CloudFormation Sample Template RDS_with_DBParameterGroup: Sample "
    "template showing how to create an Amazon RDS Database Instance with "
    "a DBParameterGroup.**WARNING** This template creates an Amazon "
    "Relational Database Service database instance. You will be billed for "
    "the AWS resources used if you create a stack from this template.")


dbuser = t.add_parameter(ts.Parameter(
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

dbpassword = t.add_parameter(ts.Parameter(
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

vpcid_param = t.add_parameter(ts.Parameter(
    "MyVpcId",
    Description="VpcId of your existing Virtual Private Cloud (VPC)",
    Type="String",
))

rule = ec2.SecurityGroupRule(
    IpProtocol="tcp",
    FromPort="5432",
    ToPort="5432",
    CidrIp="0.0.0.0/0"
)

t.add_resource(ec2.SecurityGroup(
    "TCPAll",
    GroupDescription="Allow for all tcp traffic through port 5432",
    VpcId=ts.Ref(vpcid_param),
    SecurityGroupEgress=[rule],
    SecurityGroupIngress=[rule]
))


# Only certain versions of postgres are supported on the smaller instance types
# https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html
mydb = t.add_resource(rds.DBInstance(
    "MyDB",
    AllocatedStorage="5",
    DBInstanceClass="db.t2.micro",
    DBName="hyp3db",
    Engine="postgres",
    EngineVersion="9.5.10",
    MasterUsername=ts.Ref(dbuser),
    MasterUserPassword=ts.Ref(dbpassword),
))

with open(sys.argv[1], 'w') as f:
    f.write(t.to_json())
