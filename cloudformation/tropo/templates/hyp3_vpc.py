
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

public_net = t.add_resource(ec2.Subnet(
    'Hyp3PublicSubnet',
    CidrBlock='10.0.1.0/24',
    MapPublicIpOnLaunch=True,
    VpcId=ts.Ref(hyp3_vpc),
))

private_net = t.add_resource(ec2.Subnet(
    'Hyp3PrivateSubnet',
    CidrBlock='10.0.2.0/24',
    MapPublicIpOnLaunch=False,
    VpcId=ts.Ref(hyp3_vpc),
))

igw = t.add_resource(ec2.InternetGateway('Hyp3InternetGateway',))

net_gw_vpc_attachment = t.add_resource(ec2.VPCGatewayAttachment(
    "Hyp3NatAttachment",
    VpcId=ts.Ref(hyp3_vpc),
    InternetGatewayId=ts.Ref(igw),
))

private_route_table = t.add_resource(ec2.RouteTable(
    'Hyp3PrivateRouteTable',
    VpcId=ts.Ref(hyp3_vpc),
))

public_route_table = t.add_resource(ec2.RouteTable(
    'Hyp3PublicRouteTable',
    VpcId=ts.Ref(hyp3_vpc),
))

public_route_association = t.add_resource(ec2.SubnetRouteTableAssociation(
    'Hyp3PublicRouteAssociation',
    SubnetId=ts.Ref(public_net),
    RouteTableId=ts.Ref(public_route_table),
))

default_public_route = t.add_resource(ec2.Route(
    'Hyp3PublicDefaultRoute',
    RouteTableId=ts.Ref(public_route_table),
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=ts.Ref(igw),
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

print(t.to_json())
