
import troposphere as ts
import troposphere.ec2 as ec2

from template import t

"""
AWS CloudFormation Sample Template NatGateway: Sample template showing
how to create a public NAT gateway.
**WARNING** This template creates an Amazon NAT gateway.
You will be billed for the AWS resources used if you create
a stack from this template.
"""


hyp3_vpc = t.add_resource(ec2.VPC(
    'Hyp3VPC',
    CidrBlock='10.0.0.0/16',
    InstanceTenancy='default'
))

igw = t.add_resource(ec2.InternetGateway('Hyp3InternetGateway',))

net_gw_vpc_attachment = t.add_resource(ec2.VPCGatewayAttachment(
    "Hyp3NatAttachment",
    VpcId=ts.Ref(hyp3_vpc),
    InternetGatewayId=ts.Ref(igw),
))

public_route_table = t.add_resource(ec2.RouteTable(
    'Hyp3PublicRouteTable',
    VpcId=ts.Ref(hyp3_vpc),
))

private_route_table = t.add_resource(ec2.RouteTable(
    'Hyp3PrivateRouteTable',
    VpcId=ts.Ref(hyp3_vpc),
))

default_public_route = t.add_resource(ec2.Route(
    'Hyp3PublicDefaultRoute',
    RouteTableId=ts.Ref(public_route_table),
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=ts.Ref(igw),
))

public_net_1 = t.add_resource(ec2.Subnet(
    'Hyp3PublicSubnet1',
    AvailabilityZone='us-west-1',
    CidrBlock='10.0.1.0/24',
    MapPublicIpOnLaunch=True,
    VpcId=ts.Ref(hyp3_vpc)
))

public_route_association_1 = t.add_resource(ec2.SubnetRouteTableAssociation(
    'Hyp3PublicRouteAssociation1',
    SubnetId=ts.Ref(public_net_1),
    RouteTableId=ts.Ref(public_route_table),
))

public_net_2 = t.add_resource(ec2.Subnet(
    'Hyp3PublicSubnet2',
    AvailabilityZone='us-west-2',
    CidrBlock='10.0.1.0/24',
    MapPublicIpOnLaunch=True,
    VpcId=ts.Ref(hyp3_vpc)
))

public_route_association_2 = t.add_resource(ec2.SubnetRouteTableAssociation(
    'Hyp3PublicRouteAssociation2',
    SubnetId=ts.Ref(public_net_2),
    RouteTableId=ts.Ref(public_route_table),
))

private_net = t.add_resource(ec2.Subnet(
    'Hyp3PrivateSubnet',
    CidrBlock='10.0.2.0/24',
    MapPublicIpOnLaunch=False,
    VpcId=ts.Ref(hyp3_vpc)
))

private_route_association = t.add_resource(ec2.SubnetRouteTableAssociation(
    'Hyp3PrivateRouteAssociation',
    SubnetId=ts.Ref(private_net),
    RouteTableId=ts.Ref(private_route_table),
))

t.add_output(ts.Output(
    'VPCId',
    Value=ts.Ref(hyp3_vpc),
    Description='VPC Id'
))
