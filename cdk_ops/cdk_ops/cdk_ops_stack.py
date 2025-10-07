from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as s3
    # aws_sqs as sqs,
)
from constructs import Construct

class CdkOpsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, id="app-bucket", bucket_name="app-bucket",
                           block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                           versioned=False)
