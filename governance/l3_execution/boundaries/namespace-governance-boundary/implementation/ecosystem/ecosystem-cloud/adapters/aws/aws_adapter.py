#!/usr/bin/env python3
"""
AWS Cloud Adapter Implementation
Semantic Anchor: CLOUDPROVIDERABSTRACTION.AWS

Implements Cross-Cloud contracts for AWS services.
"""

import boto3
from typing import Dict, List, Optional, BinaryIO
from datetime import datetime
import hashlib


class AWSStorageAdapter:
    """AWS S3 Adapter implementing CrossCloudStorage contract"""

    def __init__(self, region: str = "us-east-1"):
        self.s3_client = boto3.client("s3", region_name=region)
        self.s3_resource = boto3.resource("s3", region_name=region)
        self.region = region
        self.adapter_name = "AWS-S3"

    def upload_object(
        self,
        bucket: str,
        key: str,
        data: bytes,
        content_type: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Dict:
        """
        Upload object to S3 bucket

        Implements: upload_object capability
        Contract: storage/v1/storage_contract.yaml
        """
        try:
            extra_args = {}
            if content_type:
                extra_args["ContentType"] = content_type
            if metadata:
                extra_args["Metadata"] = metadata

            result = self.s3_client.put_object(
                Bucket=bucket, Key=key, Body=data, **extra_args
            )

            return {
                "success": True,
                "object_url": f"s3://{bucket}/{key}",
                "version_id": result.get("VersionId", ""),
                "size_bytes": len(data),
                "etag": result["ETag"].replace('"', ""),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_code": getattr(e, "response", {})
                .get("Error", {})
                .get("Code", "Unknown"),
            }

    def download_object(
        self, bucket: str, key: str, version_id: Optional[str] = None
    ) -> Dict:
        """
        Download object from S3 bucket

        Implements: download_object capability
        Contract: storage/v1/storage_contract.yaml
        """
        try:
            extra_args = {}
            if version_id:
                extra_args["VersionId"] = version_id

            response = self.s3_client.get_object(Bucket=bucket, Key=key, **extra_args)

            data = response["Body"].read()

            return {
                "success": True,
                "data": data,
                "content_type": response.get("ContentType", "application/octet-stream"),
                "metadata": response.get("Metadata", {}),
                "size_bytes": len(data),
                "last_modified": response["LastModified"],
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_code": getattr(e, "response", {})
                .get("Error", {})
                .get("Code", "Unknown"),
            }

    def delete_object(
        self, bucket: str, key: str, version_id: Optional[str] = None
    ) -> Dict:
        """
        Delete object from S3 bucket

        Implements: delete_object capability
        Contract: storage/v1/storage_contract.yaml
        """
        try:
            extra_args = {}
            if version_id:
                extra_args["VersionId"] = version_id

            self.s3_client.delete_object(Bucket=bucket, Key=key, **extra_args)

            return {"success": True}
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_code": getattr(e, "response", {})
                .get("Error", {})
                .get("Code", "Unknown"),
            }

    def list_objects(
        self,
        bucket: str,
        prefix: Optional[str] = None,
        max_keys: int = 1000,
        continuation_token: Optional[str] = None,
    ) -> Dict:
        """
        List objects in S3 bucket

        Implements: list_objects capability
        Contract: storage/v1/storage_contract.yaml
        """
        try:
            extra_args = {"MaxKeys": max_keys}
            if prefix:
                extra_args["Prefix"] = prefix
            if continuation_token:
                extra_args["ContinuationToken"] = continuation_token

            response = self.s3_client.list_objects_v2(Bucket=bucket, **extra_args)

            objects = []
            if "Contents" in response:
                for obj in response["Contents"]:
                    objects.append(
                        {
                            "key": obj["Key"],
                            "size_bytes": obj["Size"],
                            "last_modified": obj["LastModified"],
                            "etag": obj["ETag"].replace('"', ""),
                            "storage_class": obj.get("StorageClass", "STANDARD"),
                            "version_id": obj.get("VersionId", ""),
                        }
                    )

            return {
                "success": True,
                "objects": objects,
                "next_continuation_token": response.get("NextContinuationToken", ""),
                "is_truncated": response.get("IsTruncated", False),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_code": getattr(e, "response", {})
                .get("Error", {})
                .get("Code", "Unknown"),
            }


class AWSComputeAdapter:
    """AWS EC2 Adapter implementing CrossCloudCompute contract"""

    def __init__(self, region: str = "us-east-1"):
        self.ec2_client = boto3.client("ec2", region_name=region)
        self.ec2_resource = boto3.resource("ec2", region_name=region)
        self.region = region
        self.adapter_name = "AWS-EC2"

    def create_vm(
        self,
        instance_type: str,
        image_id: str,
        region: Optional[str] = None,
        availability_zone: Optional[str] = None,
        subnet_id: Optional[str] = None,
        security_groups: Optional[List[str]] = None,
        user_data: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        volume_size_gb: int = 20,
        volume_type: str = "gp2",
    ) -> Dict:
        """
        Create EC2 instance

        Implements: create_vm capability
        Contract: compute/v1/compute_contract.yaml
        """
        try:
            block_device_mappings = [
                {
                    "DeviceName": "/dev/sda1",
                    "Ebs": {
                        "VolumeSize": volume_size_gb,
                        "VolumeType": volume_type,
                        "DeleteOnTermination": True,
                    },
                }
            ]

            run_kwargs = {
                "ImageId": image_id,
                "InstanceType": instance_type,
                "BlockDeviceMappings": block_device_mappings,
                "MinCount": 1,
                "MaxCount": 1,
            }

            if availability_zone:
                run_kwargs["Placement"] = {"AvailabilityZone": availability_zone}
            if subnet_id:
                run_kwargs["SubnetId"] = subnet_id
            if security_groups:
                run_kwargs["SecurityGroupIds"] = security_groups
            if user_data:
                import base64

                run_kwargs["UserData"] = base64.b64encode(user_data.encode()).decode()
            if tags:
                tag_list = [{"Key": k, "Value": v} for k, v in tags.items()]
                run_kwargs["TagSpecifications"] = [
                    {"ResourceType": "instance", "Tags": tag_list}
                ]

            response = self.ec2_client.run_instances(**run_kwargs)
            instance = response["Instances"][0]

            instance_id = instance["InstanceId"]

            # Wait for instance to be running
            self.ec2_resource.Instance(instance_id).wait_until_running()

            instance = self.ec2_resource.Instance(instance_id)

            return {
                "success": True,
                "instance_id": instance_id,
                "public_ip": instance.public_ip_address or "",
                "private_ip": instance.private_ip_address or "",
                "status": instance.state["Name"],
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_code": getattr(e, "response", {})
                .get("Error", {})
                .get("Code", "Unknown"),
            }

    def delete_vm(self, instance_id: str, force: bool = False) -> Dict:
        """
        Delete EC2 instance

        Implements: delete_vm capability
        Contract: compute/v1/compute_contract.yaml
        """
        try:
            self.ec2_client.terminate_instances(InstanceIds=[instance_id])
            return {"success": True}
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_code": getattr(e, "response", {})
                .get("Error", {})
                .get("Code", "Unknown"),
            }

    def get_vm_status(self, instance_id: str) -> Dict:
        """
        Get EC2 instance status

        Implements: get_vm_status capability
        Contract: compute/v1/compute_contract.yaml
        """
        try:
            instance = self.ec2_resource.Instance(instance_id)
            instance.reload()

            return {
                "success": True,
                "status": instance.state["Name"],
                "state": instance.state["Name"],
                "uptime_seconds": int(
                    (
                        datetime.now(instance.launch_time.tzinfo) - instance.launch_time
                    ).total_seconds()
                ),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_code": getattr(e, "response", {})
                .get("Error", {})
                .get("Code", "Unknown"),
            }


class AWSQueueAdapter:
    """AWS SQS Adapter implementing CrossCloudQueue contract"""

    def __init__(self, region: str = "us-east-1"):
        self.sqs_client = boto3.client("sqs", region_name=region)
        self.region = region
        self.adapter_name = "AWS-SQS"

    def create_queue(
        self,
        queue_name: str,
        visibility_timeout_seconds: int = 30,
        message_retention_seconds: int = 345600,
        tags: Optional[Dict[str, str]] = None,
    ) -> Dict:
        """
        Create SQS queue

        Implements: create_queue capability
        Contract: queue/v1/queue_contract.yaml
        """
        try:
            attributes = {
                "VisibilityTimeout": str(visibility_timeout_seconds),
                "MessageRetentionPeriod": str(message_retention_seconds),
            }

            create_kwargs = {"QueueName": queue_name, "Attributes": attributes}
            if tags:
                create_kwargs["tags"] = tags

            response = self.sqs_client.create_queue(**create_kwargs)

            return {
                "success": True,
                "queue_url": response["QueueUrl"],
                "queue_arn": response["Attributes"]["QueueArn"],
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_code": getattr(e, "response", {})
                .get("Error", {})
                .get("Code", "Unknown"),
            }


class AWSSecretsAdapter:
    """AWS Secrets Manager Adapter implementing CrossCloudSecrets contract"""

    def __init__(self, region: str = "us-east-1"):
        self.secrets_client = boto3.client("secretsmanager", region_name=region)
        self.region = region
        self.adapter_name = "AWS-SecretsManager"

    def create_secret(
        self,
        secret_name: str,
        secret_value: str,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        kms_key_id: Optional[str] = None,
    ) -> Dict:
        """
        Create secret in AWS Secrets Manager

        Implements: create_secret capability
        Contract: secrets/v1/secrets_contract.yaml
        """
        try:
            create_kwargs = {"Name": secret_name, "SecretString": secret_value}
            if description:
                create_kwargs["Description"] = description
            if tags:
                tag_list = [{"Key": k, "Value": v} for k, v in tags.items()]
                create_kwargs["Tags"] = tag_list
            if kms_key_id:
                create_kwargs["KmsKeyId"] = kms_key_id

            response = self.secrets_client.create_secret(**create_kwargs)

            return {
                "success": True,
                "secret_arn": response["ARN"],
                "version_id": response["VersionId"],
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_code": getattr(e, "response", {})
                .get("Error", {})
                .get("Code", "Unknown"),
            }


class AWSLoggingAdapter:
    """AWS CloudWatch Logs Adapter implementing CrossCloudLogging contract"""

    def __init__(self, region: str = "us-east-1"):
        self.logs_client = boto3.client("logs", region_name=region)
        self.region = region
        self.adapter_name = "AWS-CloudWatchLogs"

    def create_log_group(
        self,
        log_group_name: str,
        retention_in_days: Optional[int] = None,
        tags: Optional[Dict[str, str]] = None,
    ) -> Dict:
        """
        Create CloudWatch Logs log group

        Implements: create_log_group capability
        Contract: logging/v1/logging_contract.yaml
        """
        try:
            self.logs_client.create_log_group(logGroupName=log_group_name)

            if retention_in_days:
                self.logs_client.put_retention_policy(
                    logGroupName=log_group_name, retentionInDays=retention_in_days
                )

            if tags:
                self.logs_client.tag_log_group(logGroupName=log_group_name, tags=tags)

            return {
                "success": True,
                "log_group_arn": f"arn:aws:logs:{self.region}:*:log-group:{log_group_name}",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_code": getattr(e, "response", {})
                .get("Error", {})
                .get("Code", "Unknown"),
            }


def get_adapter(service_type: str, region: str = "us-east-1"):
    """
    Factory function to get AWS adapter for specific service

    Args:
        service_type: Type of service (storage, compute, queue, secrets, logging)
        region: AWS region

    Returns:
        Adapter instance for the specified service
    """
    adapters = {
        "storage": AWSStorageAdapter,
        "compute": AWSComputeAdapter,
        "queue": AWSQueueAdapter,
        "secrets": AWSSecretsAdapter,
        "logging": AWSLoggingAdapter,
    }

    adapter_class = adapters.get(service_type)
    if not adapter_class:
        raise ValueError(f"Unknown service type: {service_type}")

    return adapter_class(region=region)
