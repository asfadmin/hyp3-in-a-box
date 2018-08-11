"""
Troposphere template responsible for earthdata credentials

Resources
~~~~~~~~~

* **SSM Parameter:** Store earthdata credentials as json string

"""

from troposphere import Parameter, Ref, Sub
from troposphere.ssm import Parameter as SSMParameter

from template import t


earthdata_username = t.add_parameter(Parameter(
    "EarthdataUsername",
    Description="Username for Earthdata account HyP3 should use",
    Type="String",
))

earthdata_password = t.add_parameter(Parameter(
    "EarthdataPassword",
    NoEcho=True,
    Description="Password for Earthdata account HyP3 should use",
    Type="String"
))


ssm_earthdata_creds = t.add_resource(SSMParameter(
    "Hyp3SSMParameterEarthdataCreds",
    Name=Sub(
        "/${StackName}/EarthdataCredentials",
        StackName=Ref("AWS::StackName")
    ),
    Type="String",
    Value=Sub(
        '{"username": ${Username}, "password": "${Password}"}',
        Username=Ref(earthdata_username),
        Password=Ref(earthdata_password)
    )
))
