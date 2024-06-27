#!/usr/bin/env python3
import aws_cdk as cdk
from my_project.vpc_stack import VpcStack
from my_project.eks_stack import EksStack
from my_project.s3_stack import S3Stack
from my_project.cloudfront_stack import CloudFrontStack
from my_project.rds_stack import PostgresqlDBStack

import os

app = cdk.App()

vpc_stack = VpcStack(app, "VpcStack")

eks_stack = EksStack(app, "EksStack", vpc = vpc_stack.vpc)

s3_stack = S3Stack(app, "S3Stack")

cloudfront_stack = CloudFrontStack(app, "CloudFrontStack", bucket = s3_stack.bucket)

rds_stack = PostgresqlDBStack(app, "PostgresqlDBStack", vpc = vpc_stack.vpc)

app.synth()