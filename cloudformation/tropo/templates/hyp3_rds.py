# Example modified from:
# http://aws.amazon.com/cloudformation/aws-cloudformation-templates/

from troposphere import GetAtt, Output, Ref, ec2, rds, Parameter

from template import t
from environment import environment

from .hyp3_vpc import get_public_subnets, hyp3_vpc
from .hyp3_db_params import db_super_user_pass, db_super_user, db_name


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
    DependsOn=('Hyp3VPC'),
)

if environment.use_name_parameters:
    db_instance_name = t.add_parameter(Parameter(
        "Hyp3DBInstanceId",
        Description="The name of the rds instance within aws.",
        Type="String"
    ))

    db.DBInstanceIdentifier = Ref(db_instance_name)

hyp3_db = t.add_resource(db)

t.add_output(
    Output(
        "RdsUrl",
        Description="HyP3 Database url",
        Value=GetAtt(hyp3_db, "Endpoint.Address")
    )
)
