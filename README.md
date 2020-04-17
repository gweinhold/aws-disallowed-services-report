# aws-disallowed-services-report
Simple script to compare services used against an allow list from Cost Explorer data.  Run using profile of master (payer) account.  Will print TSV report of services by account that aren't on list of allowed services.

Usage:
```python
pip3 install boto3
python services-disallowed.py > results.tsv
```

Example output:
AccountName | LinkedAccount | Service
--- | --- | ---
Account1 | 012345678901	| AmazonCloudWatch
Account1 | 012345678901	| AWS Step Functions
Account1 | 012345678901	| Amazon EC2 Container Service
Account2 | 567890123456	| AWS Key Management Service
Account2 | 567890123456	| Amazon GuardDuty
Account2 | 567890123456	| Amazon Kinesis
