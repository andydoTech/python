from troposphere import Base64, Join, FindInMap, Output, GetAtt
from troposphere import Parameter, Ref, Template, UpdatePolicy
from troposphere import autoscaling, cloudformation
from troposphere.autoscaling import LaunchConfiguration
from troposphere.cloudformation import Init, InitFile
import troposphere.ec2 as ec2
from troposphere.ec2 import Instance
from troposphere.ec2 import VPC, Subnet, InternetGateway, VPCGatewayAttachment, Route, RouteTable, SubnetRouteTableAssociation
from troposphere.ec2 import NetworkAcl, NetworkAclEntry, PortRange, SubnetNetworkAclAssociation, EIP, SecurityGroup
#from troposphere.policies import CreationPolicy, ResourceSignal


t = Template()

t.add_description(
	"AWS CloudFormation Sample Template VPC_Single_Instance_In_Subnet: " 
	"Sample template showing how to create a VPC and add an EC2 instance with an Elastic IP address "
	"and a security group. **WARNING** This template creates an Amazon EC2 instance. "
	"You will be billed for the AWS resources used if you create a stack from this template.")

instancetype_param = t.add_parameter(Parameter(
	"InstanceType",
	Description="WebServer EC2 instance type",
	Type="String",
	Default="m1.small",
	AllowedValues=[ "t1.micro", "t2.micro", "t2.small", "t2.medium", "m1.small", "m1.medium", "m1.large",
                    "m1.xlarge", "m2.xlarge", "m2.2xlarge", "m2.4xlarge", "m3.medium", "m3.large", "m3.xlarge",
                    "m3.2xlarge", "c1.medium", "c1.xlarge", "c3.large", "c3.xlarge", "c3.2xlarge", "c3.4xlarge", 
                    "c3.8xlarge", "g2.2xlarge", "r3.large", "r3.xlarge", "r3.2xlarge", "r3.4xlarge", "r3.8xlarge", 
                    "i2.xlarge", "i2.2xlarge", "i2.4xlarge", "i2.8xlarge", "hi1.4xlarge", "hs1.8xlarge", "cr1.8xlarge", 
                    "cc2.8xlarge", "cg1.4xlarge" ],
    ConstraintDescription="must be a valid EC2 instance type."
))

keyname_param = t.add_parameter(Parameter(
	"KeyName",
	Description="Name of an existing EC2 KeyPair to enable SSH access to the instance",
	Type="AWS::EC2::KeyPair::KeyName",
	ConstraintDescription="must be the name of an existing KeyPair."
))

sshlocation_param = t.add_parameter(Parameter(
	"SSHLocation",
	Description="The IP address range that can be used to SSH to the EC2 instance",
	Type="String",
	MinLength="9",
	MaxLength="18",
	Default="0.0.0.0/0",
	AllowedPattern="(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})/(\\d{1,2})",
	ConstraintDescription="must be a valid IP CIDR range of the form x.x.x.x/x."
))

t.add_mapping('AWSInstanceType2Arch', {
	"t1.micro"    : { "Arch" : "PV64"   },
	"t2.micro"    : { "Arch" : "HVM64"  },
    "t2.small"    : { "Arch" : "HVM64"  },
    "t2.medium"   : { "Arch" : "HVM64"  },
    "m1.small"    : { "Arch" : "PV64"   },
    "m1.medium"   : { "Arch" : "PV64"   },
    "m1.large"    : { "Arch" : "PV64"   },
    "m1.xlarge"   : { "Arch" : "PV64"   },
    "m2.xlarge"   : { "Arch" : "PV64"   },
    "m2.2xlarge"  : { "Arch" : "PV64"   },
    "m2.4xlarge"  : { "Arch" : "PV64"   },
    "m3.medium"   : { "Arch" : "HVM64"  },
    "m3.large"    : { "Arch" : "HVM64"  },
    "m3.xlarge"   : { "Arch" : "HVM64"  },
    "m3.2xlarge"  : { "Arch" : "HVM64"  },
    "c1.medium"   : { "Arch" : "PV64"   },
    "c1.xlarge"   : { "Arch" : "PV64"   },
    "c3.large"    : { "Arch" : "HVM64"  },
    "c3.xlarge"   : { "Arch" : "HVM64"  },
    "c3.2xlarge"  : { "Arch" : "HVM64"  },
    "c3.4xlarge"  : { "Arch" : "HVM64"  },
    "c3.8xlarge"  : { "Arch" : "HVM64"  },
    "g2.2xlarge"  : { "Arch" : "HVMG2"  },
    "r3.large"    : { "Arch" : "HVM64"  },
    "r3.xlarge"   : { "Arch" : "HVM64"  },
    "r3.2xlarge"  : { "Arch" : "HVM64"  },
    "r3.4xlarge"  : { "Arch" : "HVM64"  },
    "r3.8xlarge"  : { "Arch" : "HVM64"  },
    "i2.xlarge"   : { "Arch" : "HVM64"  },
    "i2.2xlarge"  : { "Arch" : "HVM64"  },
    "i2.4xlarge"  : { "Arch" : "HVM64"  },
    "i2.8xlarge"  : { "Arch" : "HVM64"  },
    "hi1.4xlarge" : { "Arch" : "HVM64"  },
    "hs1.8xlarge" : { "Arch" : "HVM64"  },
    "cr1.8xlarge" : { "Arch" : "HVM64"  },
    "cc2.8xlarge" : { "Arch" : "HVM64"  }
})

t.add_mapping('AWSRegionArch2AMI', {
   "us-east-1"      : { "PV64" : "ami-50842d38", "HVM64" : "ami-08842d60", "HVMG2" : "ami-3a329952"  },
   "us-west-2"      : { "PV64" : "ami-af86c69f", "HVM64" : "ami-8786c6b7", "HVMG2" : "ami-47296a77"  },
   "us-west-1"      : { "PV64" : "ami-c7a8a182", "HVM64" : "ami-cfa8a18a", "HVMG2" : "ami-331b1376"  },
   "eu-west-1"      : { "PV64" : "ami-aa8f28dd", "HVM64" : "ami-748e2903", "HVMG2" : "ami-00913777"  },
   "ap-southeast-1" : { "PV64" : "ami-20e1c572", "HVM64" : "ami-d6e1c584", "HVMG2" : "ami-fabe9aa8"  },
   "ap-northeast-1" : { "PV64" : "ami-21072820", "HVM64" : "ami-35072834", "HVMG2" : "ami-5dd1ff5c"  },
   "ap-southeast-2" : { "PV64" : "ami-8b4724b1", "HVM64" : "ami-fd4724c7", "HVMG2" : "ami-e98ae9d3"  },
   "sa-east-1"      : { "PV64" : "ami-9d6cc680", "HVM64" : "ami-956cc688", "HVMG2" : "NOT_SUPPORTED" },
   "cn-north-1"     : { "PV64" : "ami-a857c591", "HVM64" : "ami-ac57c595", "HVMG2" : "NOT_SUPPORTED" },
   "eu-central-1"   : { "PV64" : "ami-a03503bd", "HVM64" : "ami-b43503a9", "HVMG2" : "ami-b03503ad"  }
})

vpc = t.add_resource(VPC(
	"VPC",
	CidrBlock="10.0.0.0/16",
	Tags=[{ "Key": "Application", "Value": { "Ref": "AWS::StackId" }}]
))

subnet = t.add_resource(Subnet(
	"Subnet",
	VpcId = Ref("VPC"),
	CidrBlock="10.0.0.0/24",
	Tags=[{ "Key": "Application", "Value": { "Ref": "AWS::StackId" }}]
))

internetgateway = t.add_resource(InternetGateway(
	"InternetGateway",
	Tags=[{ "Key": "Application", "Value": { "Ref": "AWS::StackId" }}]
))

gatewayattachment = t.add_resource(VPCGatewayAttachment(
	"AttachGateway",
	VpcId=Ref("VPC"),
	InternetGatewayId=Ref("InternetGateway")
))

routetable = t.add_resource(RouteTable(
	"RouteTable",
	VpcId=Ref("VPC"),
	Tags=[{ "Key": "Application", "Value": { "Ref": "AWS::StackId" }}]
))

route = t.add_resource(Route(
	"Route",
	DependsOn="AttachGateway",
	RouteTableId=Ref("RouteTable"),
	DestinationCidrBlock="0.0.0.0/0",
	GatewayId=Ref("InternetGateway")
))

subnetroutetableassociation = t.add_resource(SubnetRouteTableAssociation(
	"SubnetRouteTableAssociation",
	SubnetId=Ref("Subnet"),
	RouteTableId=Ref("RouteTable")
))

networkacl = t.add_resource(NetworkAcl(
	"NetworkAcl",
	VpcId=Ref("VPC"),
	Tags=[{ "Key": "Application", "Value": { "Ref": "AWS::StackId" }}]
))

inboundhttpnetworkaclentry = t.add_resource(NetworkAclEntry(
	"InboundHTTPNetworkAclEntry",
	NetworkAclId=Ref("NetworkAcl"),
	RuleNumber="100",
	Protocol="6",
	RuleAction="allow",
	Egress="false",
	CidrBlock="0.0.0.0/0",
	PortRange=PortRange(To="80", From="80")
))

inboundsshnetworkaclentry = t.add_resource(NetworkAclEntry(
	"InboundSSHNetworkAclEntry",
	NetworkAclId=Ref("NetworkAcl"),
	RuleNumber="101",
	Protocol="6",
	RuleAction="allow",
	Egress="false",
	CidrBlock="0.0.0.0/0",
	PortRange=PortRange(To="22", From="22")
))

inboundresponseportsnetworkaclentry = t.add_resource(NetworkAclEntry(
	"InboundResponsePortsNetworkAclEntry",
	NetworkAclId=Ref("NetworkAcl"),
	RuleNumber="102",
	Protocol="6",
	RuleAction="allow",
	Egress="false",
	CidrBlock="0.0.0.0/0",
	PortRange=PortRange(To="1024", From="1024")
))

outboundhttpnetworkaclentry = t.add_resource(NetworkAclEntry(
	"OutBoundHTTPNetworkAclEntry",
	NetworkAclId=Ref("NetworkAcl"),
	RuleNumber="100",
	Protocol="6",
	RuleAction="allow",
	Egress="true",
	CidrBlock="0.0.0.0/0",
	PortRange=PortRange(To="80", From="80")
))

outboundhttpsnetworkaclentry = t.add_resource(NetworkAclEntry(
	"OutBoundHTTPSNetworkAclEntry",
	NetworkAclId=Ref("NetworkAcl"),
	RuleNumber="101",
	Protocol="6",
	RuleAction="allow",
	Egress="true",
	CidrBlock="0.0.0.0/0",
	PortRange=PortRange(To="443", From="443")
))

outboundresponseportsnetworkaclentry = t.add_resource(NetworkAclEntry(
	"OutBoundResponsePortsNetworkAclEntry",
	NetworkAclId=Ref("NetworkAcl"),
	RuleNumber="102",
	Protocol="6",
	RuleAction="allow",
	Egress="true",
	CidrBlock="0.0.0.0/0",
	PortRange=PortRange(To="65535", From="1024")
))

subnetnetworkaclassociation = t.add_resource(SubnetNetworkAclAssociation(
	"SubnetNetworkAclAssociation",
	SubnetId=Ref("Subnet"),
	NetworkAclId=Ref("NetworkAcl")
))

ipaddress = t.add_resource(EIP(
	"IPAddress",
	DependsOn="AttachGateway",
	Domain="vpc",
	InstanceId=Ref("WebServerInstance")
))

instancesecuritygroup = t.add_resource(SecurityGroup(
	"InstanceSecurityGroup",
	VpcId=Ref("VPC"),
	GroupDescription="Enable SSH access via port 22",
	SecurityGroupIngress=[
		{"IpProtocol" : "tcp", "FromPort" : "22", "ToPort" : "22", "CidrIp" : { "Ref" : "SSHLocation"}},
		{ "IpProtocol" : "tcp", "FromPort" : "80", "ToPort" : "80", "CidrIp" : "0.0.0.0/0"}
	]
))


webserverinstance = t.add_resource(Instance(
	"WebServerInstance",
	InstanceType=Ref("InstanceType"),
	KeyName=Ref("KeyName"),
	ImageId=FindInMap("AWSRegionArch2AMI", Ref("AWS::Region"), FindInMap("AWSInstanceType2Arch", Ref("InstanceType"), "Arch")),
	Tags=[{ "Key": "Application", "Value": { "Ref": "AWS::StackId" }}],
	NetworkInterfaces=[
		ec2.NetworkInterfaceProperty(
			GroupSet=Ref("InstanceSecurityGroup"),
			AssociatePublicIpAddress="true",
			DeviceIndex="0",
			SubnetId=Ref("Subnet")
		)
	],
	UserData=Base64(Join('', [
		"#!/bin/bash -xe\n",
		"yum update -y aws-cfn-bootstrap\n",

		"/opt/aws/bin/cfn-init -v ",
		"   --stack ", Ref("AWS::StackName"),
		"   --resource WebServerInstance ",
		"   --region ", Ref("AWS::Region"), "\n",

		"/opt/aws/bin/cfn-signal -e $? ",
		"   --stack ", Ref("AWS::StackName"),
		"   --resource WebServerInstance ",
		"   --region ", Ref("AWS::Region"), "\n"
	])),
	CreationPolicy=CreationPolicy(
		ResourceSignal=ResourceSignal(
			Timeout="PT15M"
		)
	)
))

t.add_output([
	Output(
		"URL",
		Value=Join(" ", ["http://", GetAtt("WebServerInstance", "PublicIp")
		])
	)
])



print(t.to_json())