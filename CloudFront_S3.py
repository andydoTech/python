from troposphere import GetAtt, Join, Output
from troposphere import Parameter, Ref, Template
from troposphere.cloudfront import Distribution, DistributionConfig
from troposphere.cloudfront import Origin, DefaultCacheBehavior, ForwardedValues, S3Origin, CustomOrigin, CacheBehavior


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
origin_account = t.add_parameter(Parameter(
    "originACCOUNT",
    Type="String",
))
origin_report = t.add_parameter(Parameter(
    "originREPORT",
    Type="String",
))
origin_alerts = t.add_parameter(Parameter(
    "originALERTS",
    Type="String",
))
origin_benefits = t.add_parameter(Parameter(
    "originBENEFITS",
    Type="String",
))
origin_enrollment = t.add_parameter(Parameter(
    "originENROLLMENT",
    Type="String",
))
origin_fulfillment = t.add_parameter(Parameter(
    "originFULFILLMENT",
    Type="String",
))
origin_offers = t.add_parameter(Parameter(
    "originOFFERS",
    Type="String",
))
origin_profile = t.add_parameter(Parameter(
    "originPROFILE",
    Type="String",
))
origin_registration = t.add_parameter(Parameter(
    "originREGISTRATION",
    Type="String",
))
# DNS Names
dns_account = t.add_parameter(Parameter(
    "dnsACCOUNT",
    Type="String",
))
dns_report = t.add_parameter(Parameter(
    "dnsREPORT",
    Type="String",
))
dns_alerts = t.add_parameter(Parameter(
    "dnsALERTS",
    Type="String",
))
dns_benefits = t.add_parameter(Parameter(
    "dnsBENEFITS",
    Type="String",
))
dns_enrollment = t.add_parameter(Parameter(
    "dnsENROLLMENT",
    Type="String",
))
dns_fulfillment = t.add_parameter(Parameter(
    "dnsFULFILLMENT",
    Type="String",
))
dns_offers = t.add_parameter(Parameter(
    "dnsOFFERS",
    Type="String",
))
dns_profile = t.add_parameter(Parameter(
    "dnsPROFILE",
    Type="String",
))
dns_registration = t.add_parameter(Parameter(
    "dnsREGISTRATION",
    Type="String",
))
# Behaviors
behavior_account = t.add_parameter(Parameter(
    "behaviorACCOUNT",
    Type="String",
))
behavior_report = t.add_parameter(Parameter(
    "behaviorREPORT",
    Type="String",
))
behavior_alerts = t.add_parameter(Parameter(
    "behaviorALERTS",
    Type="String",
))
behavior_benefits = t.add_parameter(Parameter(
    "behaviorBENEFITS",
    Type="String",
))
behavior_enrollment = t.add_parameter(Parameter(
    "behaviorENROLLMENT",
    Type="String",
))
behavior_fulfillment = t.add_parameter(Parameter(
    "behaviorFULFILLMENT",
    Type="String",
))
behavior_offers = t.add_parameter(Parameter(
    "behaviorOFFERS",
    Type="String",
))
behavior_profile = t.add_parameter(Parameter(
    "behaviorPROFILE",
    Type="String",
))
behavior_registration = t.add_parameter(Parameter(
    "behaviorREGISTRATION",
    Type="String",
))


myDistribution = t.add_resource(Distribution(
    "myDistribution",
    DistributionConfig=DistributionConfig(
        Origins=[Origin(Id=Ref(s3origin), 
                    DomainName=Ref(s3dnsname),
                    S3OriginConfig=S3Origin(OriginAccessIdentity="")),

                Origin(Id=Ref(origin_account), 
                    DomainName=Ref(dns_account),
                    CustomOriginConfig=CustomOrigin(
		        HTTPPort="80",
		        HTTPSPort="443",
		        OriginProtocolPolicy="http-only")),

                Origin(Id=Ref(origin_report),
                    DomainName=Ref(dns_report),
                    CustomOriginConfig=CustomOrigin(
                        HTTPPort="80",
                        HTTPSPort="443",
                        OriginProtocolPolicy="http-only")),

                Origin(Id=Ref(origin_alerts),
                    DomainName=Ref(dns_alerts),
                    CustomOriginConfig=CustomOrigin(
                        HTTPPort="80",
                        HTTPSPort="443",
                        OriginProtocolPolicy="http-only")),

                Origin(Id=Ref(origin_benefits),
                    DomainName=Ref(dns_benefits),
                    CustomOriginConfig=CustomOrigin(
                        HTTPPort="80",
                        HTTPSPort="443",
                        OriginProtocolPolicy="http-only")),

                Origin(Id=Ref(origin_enrollment),
                    DomainName=Ref(dns_enrollment),
                    CustomOriginConfig=CustomOrigin(
                        HTTPPort="80",
                        HTTPSPort="443",
                        OriginProtocolPolicy="http-only")),

                Origin(Id=Ref(origin_fulfillment),
                    DomainName=Ref(dns_fulfillment),
                    CustomOriginConfig=CustomOrigin(
                        HTTPPort="80",
                        HTTPSPort="443",
                        OriginProtocolPolicy="http-only")),

                Origin(Id=Ref(origin_offers),
                    DomainName=Ref(dns_offers),
                    CustomOriginConfig=CustomOrigin(
                        HTTPPort="80",
                        HTTPSPort="443",
                        OriginProtocolPolicy="http-only")),

                Origin(Id=Ref(origin_profile),
                    DomainName=Ref(dns_profile),
                    CustomOriginConfig=CustomOrigin(
                        HTTPPort="80",
                        HTTPSPort="443",
                        OriginProtocolPolicy="http-only")),

                Origin(Id=Ref(origin_registration),
                    DomainName=Ref(dns_registration),
                    CustomOriginConfig=CustomOrigin(
                        HTTPPort="80",
                        HTTPSPort="443",
                        OriginProtocolPolicy="http-only"))
                ],
		Aliases=[Ref(aliascname)], 

                CacheBehaviors=(
                    [CacheBehavior(
                        PathPattern=Ref(behavior_account),
                        TargetOriginId=Ref(origin_account),
                        ViewerProtocolPolicy="allow-all",
                        ForwardedValues=ForwardedValues(
                        QueryString="true")
                    ),
                    CacheBehavior(
                        PathPattern=Ref(behavior_report),
                        TargetOriginId=Ref(origin_report),
                        ViewerProtocolPolicy="allow-all",
                        ForwardedValues=ForwardedValues(
                        QueryString="true")
                    ),
                    CacheBehavior(
                        PathPattern=Ref(behavior_alerts),
                        TargetOriginId=Ref(origin_alerts),
                        ViewerProtocolPolicy="allow-all",
                        ForwardedValues=ForwardedValues(
                        QueryString="true")
                    ),
                    CacheBehavior(
                        PathPattern=Ref(behavior_benefits),
                        TargetOriginId=Ref(origin_benefits),
                        ViewerProtocolPolicy="allow-all",
                        ForwardedValues=ForwardedValues(
                        QueryString="true")
                    ),
                    CacheBehavior(
                        PathPattern=Ref(behavior_enrollment),
                        TargetOriginId=Ref(origin_enrollment),
                        ViewerProtocolPolicy="allow-all",
                        ForwardedValues=ForwardedValues(
                        QueryString="true")
                    ),
                    CacheBehavior(
                        PathPattern=Ref(behavior_fulfillment),
                        TargetOriginId=Ref(origin_fulfillment),
                        ViewerProtocolPolicy="allow-all",
                        ForwardedValues=ForwardedValues(
                        QueryString="true")
                    ),
                    CacheBehavior(
                        PathPattern=Ref(behavior_offers),
                        TargetOriginId=Ref(origin_offers),
                        ViewerProtocolPolicy="allow-all",
                        ForwardedValues=ForwardedValues(
                        QueryString="true")
                    ),
                    CacheBehavior(
                        PathPattern=Ref(behavior_profile),
                        TargetOriginId=Ref(origin_profile),
                        ViewerProtocolPolicy="allow-all",
                        ForwardedValues=ForwardedValues(
                        QueryString="true")
                    ),
                    CacheBehavior(
                        PathPattern=Ref(behavior_registration),
                        TargetOriginId=Ref(origin_registration),
                        ViewerProtocolPolicy="allow-all",
                        ForwardedValues=ForwardedValues(
                        QueryString="true")
                    )]
                ),

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
