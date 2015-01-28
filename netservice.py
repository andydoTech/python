from troposphere import Parameter, Output, Ref, Template
from troposphere.s3 import Bucket, AuthenticatedRead
from troposphere.sqs import Queue
from troposphere.dynamodb import (Key, AttributeDefinition, ProvisionedThroughput, Projection)
from troposphere.dynamodb import Table, GlobalSecondaryIndex
t = Template()

t.add_description(
    "AWS .NET services Cloudformation template"
)

readunits = t.add_parameter(Parameter(
    "ReadCapacityUnits",
    Description="Provisioned read throughput",
    Type="Number",
    Default="10",
    MinValue="5",
    MaxValue="10000",
    ConstraintDescription="should be between 5 and 10000"
))

writeunits = t.add_parameter(Parameter(
    "WriteCapacityUnits",
    Description="Provisioned write throughput",
    Type="Number",
    Default="5",
    MinValue="5",
    MaxValue="10000",
    ConstraintDescription="should be between 5 and 10000"
))

tableIndexName = t.add_parameter(Parameter(
    "TableIndexName",
    Description="Table: Primary Key Field",
    Type="String",
    Default="id",
    AllowedPattern="[a-zA-Z0-9]*",
    MinLength="1",
    MaxLength="2048",
    ConstraintDescription="must contain only alphanumberic characters"
))

tableIndexDataType = t.add_parameter(Parameter(
    "TableIndexDataType",
    Description=" Table: Primary Key Data Type",
    Type="String",
    Default="S",
    AllowedPattern="[S|N|B]",
    MinLength="1",
    MaxLength="1",
    ConstraintDescription="S for string data, N for numeric data, or B for "
                          "binary data"
))

secondaryIndexHashName = t.add_parameter(Parameter(
    "SecondaryIndexHashName",
    Description="Secondary Index: Primary Key Field",
    Type="String",
    Default="tokenType",
    AllowedPattern="[a-zA-Z0-9]*",
    MinLength="1",
    MaxLength="2048",
    ConstraintDescription="must contain only alphanumberic characters"
))

secondaryIndexHashDataType = t.add_parameter(Parameter(
    "SecondaryIndexHashDataType",
    Description="Secondary Index: Primary Key Data Type",
    Type="String",
    Default="S",
    AllowedPattern="[S|N|B]",
    MinLength="1",
    MaxLength="1",
    ConstraintDescription="S for string data, N for numeric data, or B for "
                          "binary data"
))

secondaryIndexRangeName = t.add_parameter(Parameter(
    "refreshSecondaryIndexRangeName",
    Description="Secondary Index: Range Key Field",
    Type="String",
    Default="tokenUpdatedTime",
    AllowedPattern="[a-zA-Z0-9]*",
    MinLength="1",
    MaxLength="2048",
    ConstraintDescription="must contain only alphanumberic characters"
))

secondaryIndexRangeDataType = t.add_parameter(Parameter(
    "SecondaryIndexRangeDataType",
    Description="Secondary Index: Range Key Data Type",
    Type="String",
    Default="S",
    AllowedPattern="[S|N|B]",
    MinLength="1",
    MaxLength="1",
    ConstraintDescription="S for string data, N for numeric data, or B for "
                          "binary data"
))

s3bucket = t.add_resource(Bucket("netBinaryBucket", AccessControl=AuthenticatedRead))
t.add_output(Output(
    "BucketName",
    Value=Ref(s3bucket),
    Description="Name of S3 NET build bucket"
))

netqueue = t.add_resource(Queue("NetQueue"))
t.add_output(Output(
    "QueueURL",
    Value=Ref(netqueue),
    Description="Name of NET queue"
))

GSITable = t.add_resource(Table(
    "GSITable",
    AttributeDefinitions=[
        AttributeDefinition(Ref(tableIndexName), Ref(tableIndexDataType)),
        AttributeDefinition(Ref(secondaryIndexHashName),
                            Ref(secondaryIndexHashDataType)),
        AttributeDefinition(Ref(secondaryIndexRangeName),
                            Ref(secondaryIndexRangeDataType))
    ],
    KeySchema=[
        Key(Ref(tableIndexName), "HASH")
    ],
    ProvisionedThroughput=ProvisionedThroughput(
        Ref(readunits),
        Ref(writeunits)
    ),
    GlobalSecondaryIndexes=[
        GlobalSecondaryIndex(
            "SecondaryIndex",
            [
                Key(Ref(secondaryIndexHashName), "HASH"),
                Key(Ref(secondaryIndexRangeName), "RANGE")
            ],
            Projection("ALL"),
            ProvisionedThroughput(
                Ref(readunits),
                Ref(writeunits)
            )
        )
    ]
))

t.add_output(Output(
    "GSITable",
    Value=Ref(GSITable),
    Description="Table with a Global Secondary Index",
))

print(t.to_json())

