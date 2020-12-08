## DynamoDB Test

import boto3
import botocore.exceptions
import logging

dynamnodb_client = boto3.client('dynamodb')

## If request == open
  


put_response = dynamnodb_client.put_item(
            TableName='poc_aws_failure_events',
            Item={
                'event_arn': {'S': 'arn:aws:health:us-east-1::event/EC2/AWS_EC2_OPERATIONAL_ISSUE/AWS_EC2_OPERATIONAL_ISSUE_VKTXI_EXAMPLE124'},
                'service': {'S': 'EC2'},
                'startTime': {'S': '1587462325.096'},
                'endTime': {'S': '1587464204.774'},
                'lastUpdateTime': {'S': '1587464204.865'},
                'failureNotificationStatus': {'S': 'sent'},
                'failureNotificationTimestamp': {'S': '1587462325.096'},
                'resolutionNotificationStatus': {'S': 'sent'},
                'resolutionNotificationTimestamp': {'S': '1587464204.774'},
                'associatedSnsTopic': {'S': ''},
                'failureEventString': {'S': '"arn":"arn:aws:health:us-east-1::event/CLOUDWATCH/AWS_CLOUDWATCH_OPERATIONAL_ISSUE/AWS_CLOUDWATCH_OPERATIONAL_ISSUE_event-1606317831882","service":"CLOUDWATCH","eventTypeCode":"AWS_CLOUDWATCH_OPERATIONAL_ISSUE","eventTypeCategory":"issue","region":"us-east-1","startTime":1606316400.0,"endTime":1606373818.0,"lastUpdatedTime":1606373894.864,"statusCode":"closed","eventScopeCode":"PUBLIC"}'},
                'eventStatus': {'S': 'open'},
                'eventScope': {'S': 'PUBLIC'},
                },
            ReturnValues='ALL_OLD',
            ReturnConsumedCapacity='INDEXES',
            ConditionExpression="eventStatus = :test_eventStatus",
            ExpressionAttributeValues={
                 ":test_eventStatus": {"S": 'open'},
                # If above line contains "S": 'open' - I expect the item to be written to the table
                # If above line is changed to "S": 'closed' - I expect there to be a conditional request failed

                # Currently, regardless of whether it is set to open or closed, the condition request fails.

            },
)
print(put_response)


  #"ConditionExpression": "aggregateId <> :id and streamRevision <> :rev and #name <> :name and context <> :ctx",
  #"ExpressionAttributeValues": {
  #   ":id": { "S": "id" },


# except botocore.exceptions.ClientError as e:
#     print("This value is already in the table and cannot be added again")
#     if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
#         pass
        ## Insert logic that checks if the event status is set to closed and attempt to write object 
        # (only select fields) if event status did not match the event status from the latest API call


                # Need conditional to see 
                #ConditionExpression='attribute_not_exists(event_arn) OR ((attribute_exists(event_arn) AND eventStatus != "closed")',
                #ConditionExpression='attribute_not_exists(event_arn)',
                #ConditionExpression='attribute_not_exists(event_arn) OR ((attribute_exists(event_arn) AND (eventStatus <> :v_eventStatus))', 
                #ExpressionAttributeValues={':v_eventStatus': {'S': 'open'}},

                #(attribute_exists(event_arn AND
                ### Need to call notification script


#response_get = dynamnodb_client.get_item(
#         TableName='poc_aws_failure_events',
#         Key={
#         'event_arn': { 'S': 'arn:aws:health:us-east-1::event/EC2/AWS_EC2_OPERATIONAL_ISSUE/AWS_EC2_OPERATIONAL_ISSUE_VKTXI_EXAMPLE111'},
#         'service': {'S': 'EC2'},
#         }
# )
