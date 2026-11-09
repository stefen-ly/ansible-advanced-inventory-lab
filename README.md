# Advanced Inventory and Dynamic Configurations

Ansible AWS Mini Lab demonstrating Dynamic Inventory,
Cloud Inventory Plugins, Inventory Scripts, and Jinja2.

## Research Topics

1. Dynamic Inventory Concepts
2. Cloud Dynamic Inventory
3. Inventory Scripts
4. Jinja2 with Inventory Variables

## Architecture

AWS EC2
   |
   +-- Custom Python Inventory Script
   |
   +-- amazon.aws.aws_ec2 Plugin
   |
   v
Ansible Dynamic Inventory
   |
   v
Groups and Host Variables
   |
   v
Jinja2 Templates and Playbooks

## Lab Environment

- AWS Region: ap-southeast-1
- 3 EC2 Instances
- Ansible Controller
- Jenkins CI/CD
- Docker Web Server

## Dynamic Inventory Demo

Custom Python Script:

    ansible-inventory -i scripts/custom_inventory.py --graph

AWS EC2 Inventory Plugin:

    ansible-inventory -i inventory/lab.aws_ec2.yml --graph

## Requirements

- Ansible
- Python
- boto3
- botocore
- amazon.aws collection
- AWS IAM read permissions for EC2 discovery

## Security

This is a demonstration project.
No AWS credentials, SSH private keys, or tokens are included.
