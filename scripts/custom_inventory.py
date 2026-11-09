#!/usr/bin/env python3
import argparse
import json
import re
import sys

import boto3
from botocore.exceptions import BotoCoreError, ClientError

REGION = "ap-southeast-1"
PROJECT = "ansible-mini"


def safe_group(value):
    return re.sub(r"[^A-Za-z0-9_]", "_", value)


def build_inventory():
    ec2 = boto3.client("ec2", region_name=REGION)

    inventory = {
        "_meta": {"hostvars": {}},
        "aws_ec2": {"hosts": []},
    }

    pages = ec2.get_paginator("describe_instances").paginate(
        Filters=[
            {"Name": "instance-state-name", "Values": ["running"]},
            {"Name": "tag:Project", "Values": [PROJECT]},
        ]
    )

    for page in pages:
        for reservation in page["Reservations"]:
            for instance in reservation["Instances"]:
                hostname = instance["InstanceId"]

                tags = {
                    tag["Key"]: tag["Value"]
                    for tag in instance.get("Tags", [])
                }

                role = tags.get("Role", "unknown")
                environment = tags.get("Environment", "unknown")

                inventory["aws_ec2"]["hosts"].append(hostname)

                groups = [
                    f"role_{safe_group(role)}",
                    f"env_{safe_group(environment)}",
                    f"project_{safe_group(PROJECT)}",
                ]

                for group in groups:
                    inventory.setdefault(group, {"hosts": []})
                    inventory[group]["hosts"].append(hostname)

                inventory["_meta"]["hostvars"][hostname] = {
                    "ansible_host": instance.get("PrivateIpAddress"),
                    "ansible_user": "ubuntu",
                    "instance_id": hostname,
                    "instance_type": instance["InstanceType"],
                    "private_ip_address": instance.get("PrivateIpAddress"),
                    "ec2_tags": tags,
                    "role": role,
                    "deployment_env": environment,
                }

    return inventory


def main():
    parser = argparse.ArgumentParser()
    args_group = parser.add_mutually_exclusive_group(required=True)

    args_group.add_argument("--list", action="store_true")
    args_group.add_argument("--host")

    args = parser.parse_args()

    try:
        inventory = build_inventory()

        if args.list:
            result = inventory
        else:
            result = inventory["_meta"]["hostvars"].get(
                args.host, {}
            )

        print(json.dumps(result, indent=2))

    except (BotoCoreError, ClientError) as error:
        print(f"AWS Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
