from typing import List

import boto3

from exceptions import DevfraError


def fetch_latest_ami_id(filters: List, owners: List[str]) -> str:
    client = boto3.client("ec2")
    response = client.describe_images(Filters=filters, Owners=owners)

    images = response["Images"]
    if len(images) == 0:
        raise DevfraError("Got no images.")

    latest_id = get_latest_id(images)
    return latest_id


def get_latest_id(images: List) -> str:
    latest_image = sorted(images, key=lambda x: x["CreationDate"], reverse=True)[0]
    return latest_image["ImageId"]


def fetch_amzn2_latest_ami_id() -> str:
    filters = [
        {"Name": "name", "Values": ["amzn2-ami-hvm-2.0.*-x86_64-gp2"]},
        {"Name": "root-device-type", "Values": ["ebs"]},
        {"Name": "virtualization-type", "Values": ["hvm"]},
    ]
    return fetch_latest_ami_id(filters, ["amazon"])


def fetch_ubuntu2004_latest_ami_id() -> str:
    filters = [
        {"Name": "name", "Values": ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]},
        {"Name": "virtualization-type", "Values": ["hvm"]},
    ]
    return fetch_latest_ami_id(filters, ["099720109477"])
