"""Find common wasted spend: unattached EBS volumes and unassociated Elastic IPs.
Read-only: it reports, it never deletes.
"""
import argparse

import boto3


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--region", default="ap-south-1")
    args = p.parse_args()

    ec2 = boto3.client("ec2", region_name=args.region)

    volumes = ec2.describe_volumes(Filters=[{"Name": "status", "Values": ["available"]}])["Volumes"]
    total_gb = sum(v["Size"] for v in volumes)
    print(f"Unattached EBS volumes: {len(volumes)} ({total_gb} GB)")
    for v in volumes:
        print(f"  {v['VolumeId']}  {v['Size']} GB  created {v['CreateTime']:%Y-%m-%d}")

    addresses = ec2.describe_addresses()["Addresses"]
    idle = [a for a in addresses if "AssociationId" not in a]
    print(f"\nUnassociated Elastic IPs: {len(idle)}")
    for a in idle:
        print(f"  {a.get('PublicIp')}")


if __name__ == "__main__":
    main()
