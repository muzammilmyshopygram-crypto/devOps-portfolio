"""Apply a cost-saving lifecycle policy to S3 buckets.

Usage:
  python s3_lifecycle.py --bucket my-bucket --dry-run
  python s3_lifecycle.py --bucket my-bucket
"""
import argparse
import json

import boto3

RULE = {
    "ID": "cost-optimization",
    "Status": "Enabled",
    "Filter": {"Prefix": ""},
    "Transitions": [
        {"Days": 30, "StorageClass": "STANDARD_IA"},
        {"Days": 90, "StorageClass": "GLACIER"},
    ],
    "NoncurrentVersionExpiration": {"NoncurrentDays": 30},
    "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 7},
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--bucket", required=True)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    config = {"Rules": [RULE]}
    print(json.dumps(config, indent=2))
    if args.dry_run:
        print("Dry run: nothing applied.")
        return

    s3 = boto3.client("s3")
    s3.put_bucket_lifecycle_configuration(Bucket=args.bucket, LifecycleConfiguration=config)
    print(f"Lifecycle policy applied to {args.bucket}")


if __name__ == "__main__":
    main()
