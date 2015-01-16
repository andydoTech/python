from troposphere import GetAtt, Join, Output
from troposphere import Parameter, Ref, Template
from troposphere.cloudfront import Distribution, DistributionConfig
from troposphere.cloudfront import Origin, DefaultCacheBehavior, ForwardedValues, S3Origin, CustomOrigin


t = Template()

t.add_description(
    "AWS CloudFormation Template CloudFront_S3: Sample template ")

s3dnsname = t.add_parameter(Parameter(
    "S3DNSNAme",
    Description="The DNS name of an existing S3 bucket to use as the "
                "Cloudfront distribution origin",
    Type="String",
))

myDistribution = t.add_resource(Distribution(
    "myDistribution",
    DistributionConfig=DistributionConfig(
        Origins=[Origin(Id="myS3Origin", 
                DomainName=Ref(s3dnsname),
                S3OriginConfig=S3Origin(OriginAccessIdentity="")),

                Origin(Id="myCustomOrigin", 
                DomainName=Ref(s3dnsname),
                CustomOriginConfig=CustomOrigin(
		    HTTPPort="80",
		    HTTPSPort="443",
		    OriginProtocolPolicy="http-only"
                ))], 


        DefaultCacheBehavior=DefaultCacheBehavior(
            TargetOriginId="myS3Origin",
	    ForwardedValues=ForwardedValues(
		QueryString="false"
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
