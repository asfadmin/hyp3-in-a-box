# hyp3_keypairname_param.py
# Rohan Weeden
# Created: June 21, 2018

"""
Troposphere template parameter for the KeyPair to use on all EC2 instances.
"""

from template import t
from troposphere import Parameter

keyname = t.add_parameter(Parameter(
    "KeyPairName",
    Description="Name of an existing EC2 KeyPair to enable SSH access to "
                "EC2 instances",
    Type="AWS::EC2::KeyPair::KeyName",
    ConstraintDescription="must be the name of an existing EC2 KeyPair."
))
