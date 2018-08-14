# hyp3_rds.py
# Rohan Weeden, William Horn
# Created: June, 2018

"""
Troposphere template responsible for generating the HyP3 database.

Example modified from:
http://aws.amazon.com/cloudformation/aws-cloudformation-templates/

Requires
~~~~~~~~
* :ref:`vpc_template`
* :ref:`db_params_template`

Resources
~~~~~~~~~

* **RDS:** PostgreSQL database for the HyP3 system
* **Security Group:** Allows all traffic on port 5432 inbound and outbound

"""

from template import t
from troposphere import GetAtt, Output, Ref, Sub, ec2, rds

from .hyp3_db_params import db_name, db_super_user, db_super_user_pass
from .hyp3_vpc import get_public_subnets, hyp3_vpc

print('  adding rds')


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
    "Hyp3TCPAll",
    GroupDescription="Allow for all tcp traffic through port 5432",
    VpcId=Ref(hyp3_vpc),
    SecurityGroupIngress=[inrule],
    SecurityGroupEgress=[outrule]
))

mydbsubnetgroup = t.add_resource(rds.DBSubnetGroup(
    "MyDBSubnetGroup",
    DBSubnetGroupDescription="Subnets available for the RDS DB Instance",
    SubnetIds=[Ref(subnet) for subnet in get_public_subnets()],
))

# Only certain versions of postgres are supported on the smaller instance types
# https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html
db = rds.DBInstance(
    "Hyp3DB",
    DBInstanceIdentifier=Sub(
        '${StackName}-hyp3-rds-instance',
        StackName=Ref('AWS::StackName')
    ),
    AllocatedStorage="5",
    DBInstanceClass="db.t2.micro",
    DBName=Ref(db_name),
    Engine="postgres",
    EngineVersion="9.5.10",
    PubliclyAccessible=True,
    VPCSecurityGroups=[Ref(security_group)],
    DBSubnetGroupName=Ref(mydbsubnetgroup),
    MasterUsername=Ref(db_super_user),
    MasterUserPassword=Ref(db_super_user_pass),
    DependsOn=hyp3_vpc,
)

hyp3_db = t.add_resource(db)

t.add_output(
    Output(
        "RdsUrl",
        Description="HyP3 Database url",
        Value=GetAtt(hyp3_db, "Endpoint.Address")
    )
)
