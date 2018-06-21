"""
Troposphere template responsible for adding parameters for entering
data base credentials.
"""

from troposphere import Parameter

from template import t


db_user = t.add_parameter(Parameter(
    "Hyp3DBUser",
    NoEcho=False,
    Description="The database admin account username",
    Type="String",
    MinLength="1",
    MaxLength="16",
    AllowedPattern="[a-zA-Z][a-zA-Z0-9]*",
    ConstraintDescription=("must begin with a letter and contain only"
                           " alphanumeric characters.")
))

db_pass = t.add_parameter(Parameter(
    "Hyp3DBPassword",
    NoEcho=True,
    Description="The database admin account password",
    Type="String",
    MinLength="8",
    MaxLength="41",
    AllowedPattern="[a-zA-Z0-9]*",
    ConstraintDescription=("must contain only alphanumeric characters "
                           "and be from 8-41 characters in length.")
))


db_name = t.add_parameter(Parameter(
    "Hyp3DBName",
    NoEcho=True,
    Description="The name of the database",
    Type="String",
    MinLength="1",
    MaxLength="41",
    AllowedPattern="[a-zA-Z0-9]*",
    ConstraintDescription=("must contain only alphanumeric characters "
                           "and be from 8-41 characters in length.")
))
