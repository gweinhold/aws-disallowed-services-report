import boto3
import datetime

#Reference https://github.com/hjacobs/aws-cost-and-usage-report

#How far back to query Cost Explorer for usage?
days_back = 30

#Use names as they're output from Cost Explorer.  Might need to run this a few times to get names correct.  i.e., "ECR" is "Amazon EC2 Container Registry (ECR)"
allowed_services = ['AWS X-Ray', 'Amazon Glacier', 'AWS Systems Manager', 'Amazon Simple Notification Service', 'AWS CloudTrail', 'Amazon EC2 Container Registry (ECR)', 'Amazon Relational Database Service', 'AWS Amplify', 'Amazon Route 53', 'AWS Budgets', 'Amazon Managed Streaming for Apache Kafka', 'Amazon Simple Email Service', 'Amazon Simple Queue Service', 'AWS Secrets Manager', 'Amazon Simple Storage Service']

#Use profile name stored in ~/.aws/credentials
session = boto3.session.Session(profile_name='default')

#Use us-east-1 as that's where billing is stored
client = session.client('ce', 'us-east-1')

def get_services_used_by_account(days_back):
    now = datetime.datetime.utcnow()
    start = (now - datetime.timedelta(days=days_back)).strftime('%Y-%m-%d')
    end = now.strftime('%Y-%m-%d')

    results = []

    token = None
    while True:
        if token:
            kwargs = {'NextPageToken': token}
        else:
            kwargs = {}
        data = client.get_cost_and_usage(TimePeriod={'Start': start, 'End':  end}, Granularity='MONTHLY', Metrics=['UnblendedCost'], GroupBy=[{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}, {'Type': 'DIMENSION', 'Key': 'SERVICE'}], **kwargs)
        results += data['ResultsByTime']
        token = data.get('NextPageToken')
        if not token:
            break

    services_used_by_account = {}

    for result_by_time in results:
        for group in result_by_time['Groups']:

            try:
                services_used_by_account[group['Keys'][0]].add(group['Keys'][1])
            except KeyError:
                services_used_by_account[group['Keys'][0]] = {group['Keys'][1]}

    return services_used_by_account

def get_disallowed_services(services_used, allowed_services):
    disallowed_services_by_account = {}

    for account, services in services_used.items():
        for service in services:
            if service not in allowed_services:
                try:
                    disallowed_services_by_account[account].add(service)
                except KeyError:
                    disallowed_services_by_account[account] = {service}

    return disallowed_services_by_account

def print_disallowed_services(disallowed_services_by_account):
    print('\t'.join(['LinkedAccount', 'Service']))

    for account, services in disallowed_services_by_account.items():
        for service in services:
            print(f"{account}\t{service}")

def main():
    services_used = get_services_used_by_account(days_back)
    disallowed_services = get_disallowed_services(services_used, allowed_services)
    print_disallowed_services(disallowed_services)

main()
