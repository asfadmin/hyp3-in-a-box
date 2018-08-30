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

* **Subnets:**

  * Public net 1 in availability zone 'a'
  * Public net 2 in availability zone 'b'
  * Restricted Subnet

* **NetworkACL:** Control traffic for the restricted subnet

"""

from template import t
from troposphere import (
    GetAZs, Output, Ref, Select,
    Tags, ec2, Parameter, GetAtt
)

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
    CidrBlock='10.0.6.0/24',
    AvailabilityZone=get_az(0),
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
    CidrBlock='10.0.5.0/24',
    AvailabilityZone=get_az(1),
    MapPublicIpOnLaunch=True,
    VpcId=Ref(hyp3_vpc)
))

public_route_association_2 = t.add_resource(ec2.SubnetRouteTableAssociation(
    'HyP3PublicRouteAssociation2',
    SubnetId=Ref(public_net_2),
    RouteTableId=Ref(public_route_table)
))

public_net_3 = t.add_resource(ec2.Subnet(
    'HyP3PublicSubnet3',
    CidrBlock='10.0.3.0/24',
    AvailabilityZone=get_az(2),
    MapPublicIpOnLaunch=True,
    VpcId=Ref(hyp3_vpc)
))

public_route_association_3 = t.add_resource(
    ec2.SubnetRouteTableAssociation(
        'HyP3PrivateRouteAssociation',
        SubnetId=Ref(public_net_3),
        RouteTableId=Ref(public_route_table)
    )
)


def get_public_subnets():
    return [
        public_net_1, public_net_2, public_net_3
    ]


t.add_output(Output(
    'VPCId',
    Value=Ref(hyp3_vpc),
    Description='VPC Id'
))
