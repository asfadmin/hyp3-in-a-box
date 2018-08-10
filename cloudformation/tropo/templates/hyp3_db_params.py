"""
Troposphere template responsible for adding parameters for entering database
credentials.
"""

from template import t
from troposphere import Parameter

from . import utils

hyp3_db = Parameter(
    "{}Hyp3DBHostUrl".format(utils.get_param_prefix()),
    Description="The host url for an existing hyp3 database",
    Type="String",
)

db_super_user = t.add_parameter(Parameter(
    "{}Hyp3DBSuperUser".format(utils.get_param_prefix()),
    Description="The database admin account username",
    Type="String",
    MinLength="1",
    MaxLength="16",
    Default="hyp3dbrootuser",
    AllowedPattern="[a-zA-Z][a-zA-Z0-9]*",
    ConstraintDescription=("must begin with a letter and contain only"
                           " alphanumeric characters.")
))

db_super_user_pass = t.add_parameter(Parameter(
    "{}Hyp3DBSuperUserPassword".format(utils.get_param_prefix()),
    NoEcho=True,
    Description="The database admin account password",
    Type="String",
    MinLength="8",
    MaxLength="41",
    AllowedPattern="[a-zA-Z0-9]*",
    ConstraintDescription=("must contain only alphanumeric characters "
                           "and be from 8-41 characters in length.")
))

db_user = t.add_parameter(Parameter(
    "{}Hyp3DBUser".format(utils.get_param_prefix()),
    Description="The database low privilege account username",
    Type="String",
    MinLength="1",
    MaxLength="16",
    Default="hyp3dbuser",
    AllowedPattern="[a-zA-Z][a-zA-Z0-9]*",
    ConstraintDescription=("must begin with a letter and contain only"
                           " alphanumeric characters.")
))

db_pass = t.add_parameter(Parameter(
    "{}Hyp3DBUserPassword".format(utils.get_param_prefix()),
    NoEcho=True,
    Description="The database low privelege account password",
    Type="String",
    MinLength="8",
    MaxLength="41",
    AllowedPattern="[a-zA-Z0-9]*",
    ConstraintDescription=("must contain only alphanumeric characters "
                           "and be from 8-41 characters in length.")
))


db_name = t.add_parameter(Parameter(
    "{}Hyp3DBName".format(utils.get_param_prefix()),
    Description="The name of the database",
    Default="hyp3db",
    Type="String",
    MinLength="1",
    MaxLength="41",
    AllowedPattern="[a-zA-Z0-9]*",
    ConstraintDescription=("must contain only alphanumeric characters "
                           "and be from 8-41 characters in length.")
))
