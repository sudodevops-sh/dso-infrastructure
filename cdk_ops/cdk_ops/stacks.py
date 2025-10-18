from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as _s3,
    CfnOutput,
    aws_ec2 as ec2,
    # aws_sqs as sqs,
)
from constructs import Construct
import aws_cdk as cdk
import logging

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
logger = logging.getLogger()

class ArtifactBucketStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.ops_config = config["ops"]
        self.resource_config = config["resources"]

        artifact_bucket = self.create_bucket()
        CfnOutput(self, "ArtifactBucketName: ", value=artifact_bucket.bucket_name)
        CfnOutput(self, "ArtifactBucketArn: ", value=artifact_bucket.bucket_arn)


    def create_bucket(self):
        env = self.ops_config["env"]
        s3 = self.resource_config["s3"]
        
        if env == "prod":
            artifact_bucket = _s3.Bucket(self, "artifactBucket",
                                         bucket_name=s3["bucket_name"],
                                         versioned=s3["versioned"],
                                         encryption=_s3.BucketEncryption.S3_MANAGED,
                                         removal_policy=cdk.RemovalPolicy.RETAIN)
        else:
            artifact_bucket = _s3.Bucket(self, "artifactBucket",
                                         bucket_name=s3["bucket_name"],
                                         versioned=s3["versioned"])

        return artifact_bucket

class VpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, config, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.ops_config = config["ops"]
        self.resource_config = config["resources"]

        vpc = self.create_vpc()
        CfnOutput(self, "VPCId: ", value=vpc.vpc_id)

        
    def create_vpc(self):
        env = self.ops_config["env"]
        vpc_config = self.resource_config["vpc"]

        vpc = ec2.Vpc(self, "VPC",
                      ip_addresses=ec2.IpAddresses.cidr(vpc_config["cidr"]),
                      max_azs=vpc_config["max_azs"],
                      nat_gateways=vpc_config["nat_gateways"],
                      subnet_configuration=[
                          ec2.SubnetConfiguration(
                              name="Public",
                              subnet_type=ec2.SubnetType.PUBLIC,
                              cidr_mask=vpc_config["subnets"]["public"]["cidr_mask"],
                          ),
                          ec2.SubnetConfiguration(
                              name="Private",
                              subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                              cidr_mask=vpc_config["subnets"]["private"]["cidr_mask"],
                          ),
                      ],
                      )
        return vpc