# AWS Automation with Python (Boto3)

Small CLI scripts for common AWS housekeeping: cost reduction, IAM hygiene and waste detection.

| Script | What it does |
|---|---|
| `s3_lifecycle.py` | Applies a lifecycle policy (Standard-IA at 30 days, Glacier at 90, cleans old versions and failed uploads). Has `--dry-run`. |
| `iam_audit.py` | Lists IAM users without MFA and access keys older than 90 days. |
| `cost_report.py` | Read-only report of unattached EBS volumes and unused Elastic IPs. |

## Setup
```bash
pip install -r requirements.txt
aws configure            # or use an IAM role / SSO
python s3_lifecycle.py --bucket my-bucket --dry-run
python iam_audit.py
python cost_report.py --region ap-south-1
```

## Permissions
Use least privilege. Each script needs only: `s3:PutLifecycleConfiguration`; `iam:ListUsers`, `iam:ListMFADevices`, `iam:ListAccessKeys`; `ec2:DescribeVolumes`, `ec2:DescribeAddresses`.

## Safety
The scripts either have a dry-run mode or only read. Test on a non-production bucket or account first.
