from troposphere import Base64, FindInMap, GetAtt
from troposphere import Parameter, Output, Ref, Template
import troposphere.ec2 as ec2

t = Template()

keyname_param = t.add_parameter(Parameter(
    "KeyName",
    Description="EC2 KeyPair to enable SSH access to the instance",
    Type="String",
))
repo_param = t.add_parameter(Parameter(
    "GitRepo",
    Description="Git repository",
    Type="String",
))
branch_param = t.add_parameter(Parameter(
    "GitBranch",
    Description="Git branch",
    Type="String",
))
environment_param = t.add_parameter(Parameter(
    "Environment",
    Description="Environment",
    Type="String",
))
tier_param = t.add_parameter(Parameter(
    "Tier",
    Description="Tier",
    Type="String",
))
service_registry_param = t.add_parameter(Parameter(
    "ServiceRegistry",
    Description="Service registry",
    Type="String",
))
version_param = t.add_parameter(Parameter(
    "Version",
    Description="Version",
    Type="String",
))
port_param = t.add_parameter(Parameter(
    "port",
    Description="Port",
    Type="String",
))
amiid_param = t.add_parameter(Parameter(
    "amiid",
    Description="AMI ID",
    Type="String",
))
instance_size_param = t.add_parameter(Parameter(
    "instancesize",
    Description="Size of an instance",
    Type="String",
))
igw_param = t.add_parameter(Parameter(
    "igw",
    Description="Internet gateway",
    Type="String",
))
subnet_block_param = t.add_parameter(Parameter(
   "subnetblock",
    Description="Subnet block",
    Type="String",
))
vpcid_parameter = t.add_parameter(Parameter(
    "vpcid",
    Description="VPC Id",
    Type="String",
))


print(t.to_json())
