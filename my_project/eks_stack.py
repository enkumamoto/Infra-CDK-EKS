from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_eks as eks,
    aws_iam as iam,
    CfnOutput
)

from aws_cdk.lambda_layer_kubectl import KubectlLayer
from constructs import Construct

class EksStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cluster = eks.Cluster(self, "HelloEKS",
            vpc = vpc,
            version = eks.KubernetesVersion.V1_30,
            kubectl_layer=KubectlLayer(self, "KubectlLayer"),
            default_capacity=5,
            default_capacity_instance=ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.MICRO)
        )

        cluster.add_nodegroup_capacity("custom-node-group",
            instance_types = [ec2.InstanceType("t2.micro")],
            min_size = 4,
            disk_size = 100
        )

        CfnOutput(self, "ClusterName",
            value = cluster.cluster_name
        )

        # eks.AccessPolicy.from_access_policy_name("AmazonEKSClusterAdminPolicy",
        #     access_scope_type = eks.AccessScopeType.CLUSTER
        # )

        # eks.AccessPolicy.from_access_policy_name("AmazonEKSAdminPolicy",
        #     access_scope_type = eks.AccessScopeType.NAMESPACE,
        #     namespaces = [ "sandbox" ]
        # )

        # cluster_admin_role = iam.Role(self, "ClusterAdminRole",
        # assumed_by=iam.ArnPrincipal("arn_for_trusted_principal")
        #  )

        # eks_admin_role = iam.Role(self, "EKSAdminRole",
        #     assumed_by=iam.ArnPrincipal("arn_for_trusted_principal")
        # )

        # eks_admin_view_role = iam.Role(self, "EKSAdminViewRole",
        #     assumed_by=iam.ArnPrincipal("arn_for_trusted_principal")
        # )


        # cluster.grant_access("clusterAdminAccess", cluster_admin_role.role_arn, [
        #     eks.AccessPolicy.from_access_policy_name("AmazonEKSClusterAdminPolicy",
        #         access_scope_type=eks.AccessScopeType.CLUSTER
        #     )
        # ])
        
        # cluster.grant_access("eksAdminRoleAccess", eks_admin_role.role_arn, [
        #     eks.AccessPolicy.from_access_policy_name("AmazonEKSAdminPolicy",
        #         access_scope_type=eks.AccessScopeType.NAMESPACE,
        #         namespaces=[ "sandbox" ]
        #     )
        # ])
        
        # cluster.grant_access("eksAdminViewRoleAccess", eks_admin_view_role.role_arn, [
        #     eks.AccessPolicy.from_access_policy_name("AmazonEKSAdminViewPolicy",
        #         access_scope_type=eks.AccessScopeType.NAMESPACE,
        #         namespaces=[ "sandbox" ]
        #     )
        # ])