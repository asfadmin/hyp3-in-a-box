# Converted from RDS_with_DBParameterGroup.template located at:
# http://aws.amazon.com/cloudformation/aws-cloudformation-templates/

import troposphere as ts
import troposphere.rds as rds
import troposphere.ec2 as ec2

from template import t

print('Adding hyp3 rds ')

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


def get_security_group(name: str):
    return ec2.SecurityGroupRule(
        name,
        IpProtocol="tcp",
        FromPort="5432",
        ToPort="5432",
        CidrIp="0.0.0.0/0"
    )


inrule, outrule = [
    get_security_group(n+'PostgresTcpRule') for n in ('In', 'Out')
]

security_group = t.add_resource(ec2.SecurityGroup(
    "TCPAll",
    GroupDescription="Allow for all tcp traffic through port 5432",
    VpcId=ts.Ref(vpcid_param),
    SecurityGroupIngress=[inrule],
    SecurityGroupEgress=[outrule]
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
    VPCSecurityGroups=[
        ts.Ref(security_group)
    ],
    MasterUsername=ts.Ref(dbuser),
    MasterUserPassword=ts.Ref(dbpassword),
))
