from troposphere import GetAtt, Join, Output
from troposphere import Parameter, Ref, Template
from troposphere.cloudfront import Distribution, DistributionConfig
from troposphere.cloudfront import Origin, DefaultCacheBehavior, ForwardedValues, S3Origin, CustomOrigin


t = Template()

t.add_description(
    "AWS CloudFormation Template CloudFront_S3")

s3dnsname = t.add_parameter(Parameter(
    "S3DNSNAme",
    Description="The DNS name of an existing S3 bucket to use as the "
                "Cloudfront distribution origin",
    Type="String",
))
aliascname = t.add_parameter(Parameter(
    "aliasCNAME",
    Description="Alternate Domain Names (CNAMEs)",
    Type="String",
))
# Origin names
s3origin = t.add_parameter(Parameter(
    "S3Origin",
    Type="String",
))
origin_2 = t.add_parameter(Parameter(
    "originTWO",
    Type="String",
))
origin_3 = t.add_parameter(Parameter(
    "originTHREE",
    Type="String",
))
origin_4 = t.add_parameter(Parameter(
    "originFOUR",
    Type="String",
))
origin_5 = t.add_parameter(Parameter(
    "originFIVE",
    Type="String",
))
origin_6 = t.add_parameter(Parameter(
    "originSIX",
    Type="String",
))
origin_7 = t.add_parameter(Parameter(
    "originSEVEN",
    Type="String",
))
origin_8 = t.add_parameter(Parameter(
    "originEIGHT",
    Type="String",
))
origin_9 = t.add_parameter(Parameter(
    "originNINE",
    Type="String",
))
origin_10 = t.add_parameter(Parameter(
    "originTEN",
    Type="String",
))
# DNS Names
dnsname_2 = t.add_parameter(Parameter(
    "dnsTWO",
    Type="String",
))
dnsname_3 = t.add_parameter(Parameter(
    "dnsTHREE",
    Type="String",
))
dnsname_4 = t.add_parameter(Parameter(
    "dnsFOUR",
    Type="String",
))
dnsname_5 = t.add_parameter(Parameter(
    "dnsFIVE",
    Type="String",
))
dnsname_6 = t.add_parameter(Parameter(
    "dnsSIX",
    Type="String",
))
dnsname_7 = t.add_parameter(Parameter(
    "dnsSEVEN",
    Type="String",
))
dnsname_8 = t.add_parameter(Parameter(
    "dnsEIGHT",
    Type="String",
))
dnsname_9 = t.add_parameter(Parameter(
    "dnsNINE",
    Type="String",
))
dnsname_10 = t.add_parameter(Parameter(
    "dnsTEN",
    Type="String",
))

myDistribution = t.add_resource(Distribution(
    "myDistribution",
    DistributionConfig=DistributionConfig(
        Origins=[Origin(Id=Ref(s3origin), 
                    DomainName=Ref(s3dnsname),
                    S3OriginConfig=S3Origin(OriginAccessIdentity="")),

                Origin(Id=Ref(origin_2), 
                    DomainName=Ref(dnsname_2),
                    CustomOriginConfig=CustomOrigin(
		        HTTPPort="80",
		        HTTPSPort="443",
		        OriginProtocolPolicy="http-only")),

                Origin(Id=Ref(origin_3),
                    DomainName=Ref(dnsname_3),
                    CustomOriginConfig=CustomOrigin(
                        HTTPPort="80",
                        HTTPSPort="443",
                        OriginProtocolPolicy="http-only")),

                Origin(Id=Ref(origin_4),
                    DomainName=Ref(dnsname_4),
                    CustomOriginConfig=CustomOrigin(
                        HTTPPort="80",
                        HTTPSPort="443",
                        OriginProtocolPolicy="http-only")),

                Origin(Id=Ref(origin_5),
                    DomainName=Ref(dnsname_5),
                    CustomOriginConfig=CustomOrigin(
                        HTTPPort="80",
                        HTTPSPort="443",
                        OriginProtocolPolicy="http-only")),

                Origin(Id=Ref(origin_6),
                    DomainName=Ref(dnsname_6),
                    CustomOriginConfig=CustomOrigin(
                        HTTPPort="80",
                        HTTPSPort="443",
                        OriginProtocolPolicy="http-only")),

                Origin(Id=Ref(origin_7),
                    DomainName=Ref(dnsname_7),
                    CustomOriginConfig=CustomOrigin(
                        HTTPPort="80",
                        HTTPSPort="443",
                        OriginProtocolPolicy="http-only")),

                Origin(Id=Ref(origin_8),
                    DomainName=Ref(dnsname_8),
                    CustomOriginConfig=CustomOrigin(
                        HTTPPort="80",
                        HTTPSPort="443",
                        OriginProtocolPolicy="http-only")),

                Origin(Id=Ref(origin_9),
                    DomainName=Ref(dnsname_9),
                    CustomOriginConfig=CustomOrigin(
                        HTTPPort="80",
                        HTTPSPort="443",
                        OriginProtocolPolicy="http-only")),

                Origin(Id=Ref(origin_10),
                    DomainName=Ref(dnsname_10),
                    CustomOriginConfig=CustomOrigin(
                        HTTPPort="80",
                        HTTPSPort="443",
                        OriginProtocolPolicy="http-only"))
                ],
		Aliases=[Ref(aliascname)], 


        DefaultCacheBehavior=DefaultCacheBehavior(
            TargetOriginId=Ref(s3origin),
	    ForwardedValues=ForwardedValues(
		QueryString="true"
 	    ),
            ViewerProtocolPolicy="allow-all"),
        Enabled=True
    )
))

t.add_output([
    Output("DistributionId", Value=Ref(myDistribution)),
    Output(
        "DistributionName",
        Value=Join("", ["http://", GetAtt(myDistribution, "DomainName")])),
])

print(t.to_json())
