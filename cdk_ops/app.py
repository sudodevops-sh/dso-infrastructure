#!/usr/bin/env python3
import os
import yaml
import aws_cdk as cdk

from cdk_ops.stacks import ArtifactBucketStack, VpcStack

app = cdk.App()

env = app.node.try_get_context("env")
if env is None:
    raise ValueError("Please specify an environment using -c env=<dev|prod>")

config_path = os.path.join("configs", f"ops-{env}.yaml")
with open(config_path, "r") as f:
    config = yaml.safe_load(f)

stack_name = f"{env}-stack"
env=cdk.Environment(account=config["ops"]["aws_account"],region=config["ops"]["aws_region"])
ArtifactBucketStack(app, f"{stack_name}-artifact-bucket",
                    config=config,
                    env=env)

VpcStack(app, f"{stack_name}-vpc",
         config=config,
         env=env)

app.synth()
