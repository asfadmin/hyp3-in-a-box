# Example modified from:
# https://github.com/cloudtools/troposphere/blob/master/examples/NatGateway.py

import troposphere as ts
from template import t
from troposphere import ec2

print('  adding vpc')

hyp3_vpc = t.add_resource(ec2.VPC(
    'Hyp3VPC',
    CidrBlock='10.0.0.0/16',
    InstanceTenancy='default',
    EnableDnsSupport=True,
    EnableDnsHostnames=True
))

igw = t.add_resource(ec2.InternetGateway('Hyp3InternetGateway',))

net_gw_vpc_attachment = t.add_resource(ec2.VPCGatewayAttachment(
    "Hyp3GatewayAttachment",
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
    DependsOn='Hyp3GatewayAttachment'
))


def get_az(index):
    return ts.Select(
        str(index),
        ts.GetAZs(ts.Ref('AWS::Region'))
    )


public_net_1 = t.add_resource(ec2.Subnet(
    'Hyp3PublicSubnet1',
    AvailabilityZone=get_az(0),
    CidrBlock='10.0.1.0/24',
    MapPublicIpOnLaunch=True,
    VpcId=ts.Ref(hyp3_vpc)
))

public_route_association_1 = t.add_resource(ec2.SubnetRouteTableAssociation(
    'Hyp3PublicRouteAssociation1',
    SubnetId=ts.Ref(public_net_1),
    RouteTableId=ts.Ref(public_route_table)
))

public_net_2 = t.add_resource(ec2.Subnet(
    'Hyp3PublicSubnet2',
    AvailabilityZone=get_az(1),
    CidrBlock='10.0.2.0/24',
    MapPublicIpOnLaunch=True,
    VpcId=ts.Ref(hyp3_vpc)
))

public_route_association_2 = t.add_resource(ec2.SubnetRouteTableAssociation(
    'Hyp3PublicRouteAssociation2',
    SubnetId=ts.Ref(public_net_2),
    RouteTableId=ts.Ref(public_route_table)
))


def get_public_subnets():
    return [
        public_net_1, public_net_2
    ]


private_net = t.add_resource(ec2.Subnet(
    'Hyp3PrivateSubnet',
    CidrBlock='10.0.3.0/24',
    MapPublicIpOnLaunch=False,
    VpcId=ts.Ref(hyp3_vpc)
))

private_route_association = t.add_resource(ec2.SubnetRouteTableAssociation(
    'Hyp3PrivateRouteAssociation',
    SubnetId=ts.Ref(private_net),
    RouteTableId=ts.Ref(private_route_table)
))

t.add_output(ts.Output(
    'VPCId',
    Value=ts.Ref(hyp3_vpc),
    Description='VPC Id'
))
