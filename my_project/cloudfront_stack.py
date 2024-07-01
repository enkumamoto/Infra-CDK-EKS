from aws_cdk import (
    Stack,
    aws_cloudfront as cloudfront,
    aws_s3 as s3,
    aws_route53 as route53,
    CfnOutput
)

import aws_cdk.aws_certificatemanager as acm

from constructs import Construct

class CloudFrontStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, bucket: s3.Bucket, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.cloudfront_distribution = cloudfront.CloudFrontWebDistribution(self, "FrontendDistribution",
            origin_configs=[
                cloudfront.SourceConfiguration(
                    s3_origin_source = cloudfront.S3OriginConfig(
                        s3_bucket_source = bucket
                    ),
                    behaviors = [
                        cloudfront.Behavior(
                            is_default_behavior=True,
                        )
                    ]
                )
            ],
            error_configurations = [
                {
                    "errorCode": 403,
                    "responseCode": 200,
                    "responsePagePath": "/index.html"
                },
                {
                    "errorCode": 404,
                    "responseCode": 200,
                    "responsePagePath": "/index.html"
                }
            ]
        )

        CfnOutput(self, "DistributionId",
            value = self.cloudfront_distribution.distribution_id
        )

        cloudfront.CfnOriginAccessControl(self, "MyCfnOriginAccessControl",
                origin_access_control_config = cloudfront.CfnOriginAccessControl.OriginAccessControlConfigProperty(
                name = "frontend",
                origin_access_control_origin_type = "s3",
                signing_behavior = "always",
                signing_protocol = "sigv4",

                # the properties below are optional
                description = "teste"
                )
        )