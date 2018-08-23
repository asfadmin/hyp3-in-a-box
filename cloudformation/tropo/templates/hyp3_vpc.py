# hyp3_vpc.py
# William Horn
# Created: June 2018

"""
Troposphere template responsible for generating the VPC which the HyP3 system
operates in.

Example modified from:
https://github.com/cloudtools/troposphere/blob/master/examples/NatGateway.py

Resources
~~~~~~~~~

* **VPC:** The VPC which all other HyP3 infrastructure is connected to
* **Internet Gateway:** Enables internet traffic to and from the public subnets
* **Route Tables:**

  * Public
  * Private

* **Subnets:**

  * Public net 1 in availability zone 'a'
  * Public net 2 in availability zone 'b'
  * Private net


"""

from template import t
from troposphere import GetAZs, Output, Ref, Select, Tags, ec2, Parameter

print('  adding vpc')

hyp3_vpc = t.add_resource(ec2.VPC(
    'HyP3VPC',
    CidrBlock='10.0.0.0/16',
    InstanceTenancy='default',
    EnableDnsSupport=True,
    EnableDnsHostnames=True,
    Tags=Tags(
        Name="HyP3 VPC"
    )
))

igw = t.add_resource(ec2.InternetGateway('HyP3InternetGateway',))

net_gw_vpc_attachment = t.add_resource(ec2.VPCGatewayAttachment(
    "HyP3GatewayAttachment",
    VpcId=Ref(hyp3_vpc),
    InternetGatewayId=Ref(igw),
))


public_route_table = t.add_resource(ec2.RouteTable(
    'HyP3PublicRouteTable',
    VpcId=Ref(hyp3_vpc),
))

private_route_table = t.add_resource(ec2.RouteTable(
    'HyP3PrivateRouteTable',
    VpcId=Ref(hyp3_vpc),
))

default_public_route = t.add_resource(ec2.Route(
    'HyP3PublicDefaultRoute',
    RouteTableId=Ref(public_route_table),
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=Ref(igw),
    DependsOn=net_gw_vpc_attachment
))


def get_az(index):
    return Select(
        str(index),
        GetAZs(Ref('AWS::Region'))
    )


public_net_1 = t.add_resource(ec2.Subnet(
    'HyP3PublicSubnet1',
    AvailabilityZone=get_az(0),
    CidrBlock='10.0.1.0/24',
    MapPublicIpOnLaunch=True,
    VpcId=Ref(hyp3_vpc)
))

public_route_association_1 = t.add_resource(ec2.SubnetRouteTableAssociation(
    'HyP3PublicRouteAssociation1',
    SubnetId=Ref(public_net_1),
    RouteTableId=Ref(public_route_table)
))

public_net_2 = t.add_resource(ec2.Subnet(
    'HyP3PublicSubnet2',
    AvailabilityZone=get_az(1),
    CidrBlock='10.0.2.0/24',
    MapPublicIpOnLaunch=True,
    VpcId=Ref(hyp3_vpc)
))

public_route_association_2 = t.add_resource(ec2.SubnetRouteTableAssociation(
    'HyP3PublicRouteAssociation2',
    SubnetId=Ref(public_net_2),
    RouteTableId=Ref(public_route_table)
))


def get_public_subnets():
    return [
        public_net_1, public_net_2
    ]


restricted_subnet = t.add_resource(ec2.Subnet(
    'HyP3RestrictedSubnet',
    AvailabilityZone=get_az(2),
    CidrBlock='10.0.4.0/24',
    MapPublicIpOnLaunch=True,
    VpcId=Ref(hyp3_vpc)
))

restricted_subnet_route_association = t.add_resource(
    ec2.SubnetRouteTableAssociation(
        'HyP3PrivateRouteAssociation',
        SubnetId=Ref(restricted_subnet),
        RouteTableId=Ref(public_route_table)
    )
)


local_cidr_range = t.add_parameter(Parameter(
    "ApiCidrRange",
    Description=("The IP range the hyp3 stack will be accessible from. "
                 "Default is to allow traffic from anywhere."),
    Type="String",
    Default="0.0.0.0/0",
    AllowedPattern=r"((\d{1,3})\.){3}\d{1,3}/\d{1,2}",
    ConstraintDescription="Valid CIDR IP range"
))

local_network_acl = t.add_resource(ec2.NetworkAcl(
    'LocalNetworkAcl',
    VpcId=Ref(hyp3_vpc)
))

local_acl_entry = t.add_resource(ec2.NetworkAclEntry(
    'LocalAclEntry',
    NetworkAclId=Ref(local_network_acl),
    CidrBlock=Ref(local_cidr_range),
    Protocol=-1,
    RuleAction="allow",
    RuleNumber=100,
    Egress=False
))

restricted_subnet_acl_association = t.add_resource(
    ec2.SubnetNetworkAclAssociation(
        "RestrictedSubnetAclAssociation",
        SubnetId=Ref(restricted_subnet),
        NetworkAclId=Ref(local_network_acl)
    )
)

t.add_output(Output(
    'VPCId',
    Value=Ref(hyp3_vpc),
    Description='VPC Id'
))
