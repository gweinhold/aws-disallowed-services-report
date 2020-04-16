# aws-disallowed-services-report
Simple script to compare services used against an allow list from Cost Explorer data.  Run using profile of master (payer) account.  Will print TSV report of services by account that aren't on list of allowed services.

Usage:
```python
pip3 install boto3
python services-disallowed.py >> results.tsv
```

Example output:
LinkedAccount | Service
--- | ---
012345678901	| AmazonCloudWatch
012345678901	| AWS Step Functions
012345678901	| Amazon EC2 Container Service
567890123456	| AWS Key Management Service
567890123456	| Amazon GuardDuty
567890123456	| Amazon Kinesis
