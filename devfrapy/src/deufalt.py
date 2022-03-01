from ipaddress import IPv4Network
from typing import List

from fetcher import fetch_amzn2_latest_ami_id

# Network
DEFAULT_VPC_CIDR = IPv4Network("10.0.0.0/16")
DEFAULT_PUBLIC_SUBNET_CIDR = IPv4Network("10.0.0.0/24")
DEFAULT_PRIVATE_SUBNET_VPC_CIDR = IPv4Network("10.0.1.0/24")

# Instance
DEFAULT_AMI_ID = fetch_amzn2_latest_ami_id()
DEFAULT_INSTANCE_TYPE = "t2.micro"
DEFAULT_IAM_POLICIES: List[str] = []
DEFAULT_USERDATA = ""
