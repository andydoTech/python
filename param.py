from troposphere import Base64, FindInMap, GetAtt, Select, GetAZs, Join
from troposphere import Parameter, Output, Ref, Template, Tags, Condition, Equals
from troposphere.s3 import Bucket, AuthenticatedRead
from troposphere.dynamodb import (Key, AttributeDefinition, ProvisionedThroughput)
from troposphere.dynamodb import Table
from troposphere.sqs import Queue
from troposphere.autoscaling import Metadata
from troposphere.ec2 import PortRange, NetworkAcl, Route, \
    VPCGatewayAttachment, SubnetRouteTableAssociation, Subnet, RouteTable, \
    VPC, NetworkInterfaceProperty, NetworkAclEntry, \
    SubnetNetworkAclAssociation, EIP, Instance, InternetGateway, \
    SecurityGroupRule, SecurityGroup
from troposphere.elasticloadbalancing import LoadBalancer
from troposphere.autoscaling import AutoScalingGroup, LaunchConfiguration
import troposphere.elasticloadbalancing as elb
from troposphere.policies import UpdatePolicy, AutoScalingRollingUpdate
import troposphere.ec2 as ec2

t = Template()
t.add_mapping('RegionMap', {
    "us-east-1": {"AMI": "ami-c4fe9aac"},
    "us-west-1": {"AMI": "ami-cfa5b68a"},
    "us-west-2": {"AMI": "ami-29d18719"},
})
conditions = {
    "NoKeyPair": Equals(
        Ref("KeyPair"),
        "None"
    ), 
}
LBSecurityGroup = t.add_parameter(Parameter(
    "LBSecurityGroup",
    Type="String",
    Description="Load Balancer Security group for NET instances",
))
ScaleCapacity = t.add_parameter(Parameter(
    "ScaleCapacity",
    Default="1",
    Type="String",
    Description="Number of NET servers to run",
))
EC2keyname = t.add_parameter(Parameter(
    "KeyName",
    Description="EC2 KeyPair to enable SSH access to the instance",
    Type="String",
))
Repo = t.add_parameter(Parameter(
    "GitRepo",
    Description="Git repository",
    Type="String",
))
Branch = t.add_parameter(Parameter(
    "GitBranch",
    Description="Git branch",
    Type="String",
))
EnvType = t.add_parameter(Parameter(
    "EnvType",
    Description="The environment being deployed into",
    Type="String",
))
Tier = t.add_parameter(Parameter(
    "Tier",
    Description="Tier",
    Type="String",
))
ServiceRegistry = t.add_parameter(Parameter(
    "ServiceRegistry",
    Description="Service registry",
    Type="String",
))
Version = t.add_parameter(Parameter(
    "Version",
    Description="Version",
    Type="String",
))
Port = t.add_parameter(Parameter(
    "port",
    Description="Port",
    Type="String",
))
AmiId = t.add_parameter(Parameter(
    "AmiId",
    Description="The AMI id for the api instance",
    Type="String",
))
InstanceSize = t.add_parameter(Parameter(
    "instancesize",
    Description="Size of an instance",
    Type="String",
))
IGW = t.add_parameter(Parameter(
    "IGW",
    Description="Internet gateway",
    Type="String",
))
SubnetBlocks = t.add_parameter(Parameter(
   "SubnetBlocks",
    Description="API CIDR blocks",
    Type="CommaDelimitedList",
    Default="10.0.10.0/24, 10.0.11.0/24, 10.0.12.0/24",
))
VPC = t.add_parameter(Parameter(
    "VPC",
    Description="VPC Id",
    Type="String",
))
hashkeyname = t.add_parameter(Parameter(
    "HasKeyElementName",
    Description="HasType PrimaryKey Name",
    Type="String",
    AllowedPattern="[a-zA-z0-9]*",
    MinLength="1",
    MaxLength="2048",
    ConstraintDescription="must contain only alphanumberic characters",
))
hashkeytype = t.add_parameter(Parameter(
    "HasKeyElementType",
    Description="HashType PrimaryKey Type",
    Type="String",
    Default="S",
    AllowedPattern="[S|N]",
    MinLength="1",
    MaxLength="1",
    ConstraintDescription="must be either S or N",
))
readunits = t.add_parameter(Parameter(
    "ReadCapacityUnits",
    Description="Provisioned read throughput",
    Type="Number",
    Default="5",
    MinValue="5",
    MaxValue="10000",
    ConstraintDescription="should be between 5 and 10000"
))

writeunits = t.add_parameter(Parameter(
    "WriteCapacityUnits",
    Description="Provisioned write throughput",
    Type="Number",
    Default="10",
    MinValue="5",
    MaxValue="10000",
    ConstraintDescription="should be between 5 and 10000"
))
ec2InstanceType = t.add_parameter(Parameter(
    "NetInstanceType",
    Description="NET EC2 instance type",
    Type="String",
    Default="m1.medium",
    AllowedValues=[
        't1.micro',
        't2.micro', 't2.small', 't2.medium',
        'm1.small', 'm1.medium', 'm1.large', 'm1.xlarge',
        'm2.xlarge', 'm2.2xlarge', 'm2.4xlarge',
        'm3.medium', 'm3.large', 'm3.xlarge', 'm3.2xlarge',
        'c1.medium', 'c1.xlarge',
        'c3.large', 'c3.xlarge', 'c3.2xlarge', 'c3.4xlarge', 'c3.8xlarge',
        'g2.2xlarge',
        'r3.large', 'r3.xlarge', 'r3.2xlarge', 'r3.4xlarge', 'r3.8xlarge',
        'i2.xlarge', 'i2.2xlarge', 'i2.4xlarge', 'i2.8xlarge',
        'hi1.4xlarge',
        'hs1.8xlarge',
        'cr1.8xlarge',
        'cc2.8xlarge',
        'cg1.4xlarge',
    ],
    ConstraintDescription="must be a valid EC2 instance type.",
))

netServerCapacity = t.add_parameter(Parameter(
   "NETServerCapacity",
    Default="2",
    Description="The initial number of NETServer instances",
    Type="Number",
    MinValue="1",
    MaxValue="2",
    ConstraintDescription="Must be between 1 and 2 EC2 instances.",
))

################ Resources #######################
s3bucket = t.add_resource(Bucket(
    "S3Bucket",
    AccessControl=AuthenticatedRead,
))
dynamoConfigDB = t.add_resource(Table(
    "DynamoConfigTable",
    AttributeDefinitions=[
        AttributeDefinition(Ref(hashkeyname), Ref(hashkeytype)),
    ],
    KeySchema=[
        Key(Ref(hashkeyname), "HASH")
    ],
    ProvisionedThroughput=ProvisionedThroughput(
        Ref(readunits),
        Ref(writeunits)
    )
))
loggingQueue = t.add_resource(Queue(
    "LoggingQueue"
))

PrivateSubnetA = t.add_resource(
    Subnet(
        "PrivateSubnetA",
        CidrBlock=(Select("0", Ref(SubnetBlocks))),
        AvailabilityZone=(Select("0", GetAZs(Ref("AWS::Region")))),
        VpcId=Ref(VPC),
        Tags=Tags(
            Name=(Join(" ", [Ref(EnvType), "Subnet A"])),
        )
    )
)
PrivateSubnetB = t.add_resource(
    Subnet(
        "PrivateSubnetB",
        CidrBlock=(Select("1", Ref(SubnetBlocks))),
        AvailabilityZone=(Select("1", GetAZs(Ref("AWS::Region")))),
        VpcId=Ref(VPC),
        Tags=Tags(
            Name=(Join(" ", [Ref(EnvType), "Subnet B"])),
        )
    )
)
PrivateSubnetC = t.add_resource(
    Subnet(
        "PrivateSubnetC",
        CidrBlock=(Select("2", Ref(SubnetBlocks))),
        AvailabilityZone=(Select("2", GetAZs(Ref("AWS::Region")))),
        VpcId=Ref(VPC),
        Tags=Tags(
            Name=(Join(" ", [Ref(EnvType), "Subnet C"])),
        )
    )
)
PrivateIGW = t.add_resource(InternetGateway(
    "PrivateIGW",
    Tags=[{"Key": "Service", "Value": {"Ref": "AWS::StackId"}}]
))
GatewayAttachment = t.add_resource(VPCGatewayAttachment(
    "AttachGateway",
    VpcId=Ref("VPC"),
    InternetGatewayId=Ref("PrivateIGW"),
))
PrivateACL = t.add_resource(NetworkAcl(
    "PrivateACL",
    VpcId=Ref("VPC"),
))
PrivateRouteTable = t.add_resource(RouteTable(
    "PrivateRouteTable",
    VpcId=Ref("VPC"),
))
PrivateELB = t.add_resource(LoadBalancer(
    "PrivateELB",
    Subnets = [Ref("PrivateSubnetA"), Ref("PrivateSubnetB"), Ref("PrivateSubnetC")],
    CrossZone = True,
    Scheme = "internal",
    SecurityGroups = Ref("LBSecurityGroup"),
    HealthCheck=elb.HealthCheck(
        Target="HTTP:80/",
        HealthyThreshold="5",
        UnhealthyThreshold="2",
        Interval="20",
        Timeout="15",
    ),
    Listeners=[
        elb.Listener(
            LoadBalancerPort="80",
            InstancePort="80",
            Protocol="HTTP",
            InstanceProtocol="HTTP",
        )
    ]
))











print(t.to_json())
