"""Report IAM users without MFA and access keys older than N days."""
import argparse
from datetime import datetime, timezone

import boto3


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--max-key-age", type=int, default=90)
    args = p.parse_args()

    iam = boto3.client("iam")
    now = datetime.now(timezone.utc)
    findings = 0

    for page in iam.get_paginator("list_users").paginate():
        for user in page["Users"]:
            name = user["UserName"]

            if not iam.list_mfa_devices(UserName=name)["MFADevices"]:
                print(f"[NO MFA]    {name}")
                findings += 1

            for key in iam.list_access_keys(UserName=name)["AccessKeyMetadata"]:
                age = (now - key["CreateDate"]).days
                if key["Status"] == "Active" and age > args.max_key_age:
                    print(f"[OLD KEY]   {name} key {key['AccessKeyId']} is {age} days old")
                    findings += 1

    print(f"\n{findings} finding(s)")


if __name__ == "__main__":
    main()
