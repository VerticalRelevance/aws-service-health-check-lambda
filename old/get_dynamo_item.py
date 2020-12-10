# get dynamo item 

import boto3

dynamno_db_client = boto3.client('dynamodb')

response = dynamno_db_client.get_item(
    TableName="poc_aws_failure_events", 
    Key={
        "eventArn": {"S": "arn:aws:health:global::event/CLOUDFRONT/AWS_CLOUDFRONT_OPERATIONAL_ISSUE/AWS_CLOUDFRONT_OPERATIONAL_ISSUE_event-1606326645335"},
        "service": {"S": "CLOUDFRONT"}
        }
    )



{"eventArn": {"S": "arn:aws:health:global::event/CLOUDFRONT/AWS_CLOUDFRONT_OPERATIONAL_ISSUE/AWS_CLOUDFRONT_OPERATIONAL_ISSUE_event-1606326645335"}, "service": {"S": "CLOUDFRONT"}})
{"eventArn": {"S": event_failure_dictionary[event]['arn']} ,"service": {"S": event_failure_dictionary[event]['service']}})

print(response)
