from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as _s3,
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

        if config["ops"]["env"] == "prod":
            artifact_bucket = _s3.Bucket(self, "artifactBucket",
                                         bucket_name=config["resources"]["s3"]["bucket_name"],
                                         versioned=config["resources"]["s3"]["versioned"],
                                         encryption=_s3.BucketEncryption.S3_MANAGED,
                                         removal_policy=cdk.RemovalPolicy.RETAIN)
        else:
            artifact_bucket = _s3.Bucket(self, "artifactBucket",
                                         bucket_name=config["resources"]["s3"]["bucket_name"],
                                         versioned=False)