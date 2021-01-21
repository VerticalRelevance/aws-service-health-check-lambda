#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Return notification of specified AWS Services'''

import logging
import configparser
import botocore.exceptions

import boto3
import time

from detect_service_failures import detect_service_failures, get_service_level

# Setting up logging component of lambda script
logging.basicConfig(level=logging.DEBUG)

# Creates up config parser object and imports the config file
config = configparser.ConfigParser()
config.read_file(open('./aws_service_config.ini'))
logging.info("Input file loaded successfully")

sns_client = boto3.client('sns')
dynamno_db_client = boto3.client('dynamodb')


# Check DynamoDB for record of outage

# If outage, check if ARN exists in Dynamo. If it exists, don't write. If it doesn't exist, write it.
def write_service_failure_event(event_failure_dictionary):
    for event in event_failure_dictionary:
        try:
            if event_failure_dictionary[event]['statusCode'] == "open":
                dynamo_put_response = dynamno_db_client.put_item(
                    TableName= config['default']['dynamodb_table_name'],
                    Item={
                        'eventArn': {'S': event_failure_dictionary[event]['arn']},
                        'service': {'S': event_failure_dictionary[event]['service']},
                        'serviceLevel': {'S': get_service_level(event_failure_dictionary[event]['service'])[0]},
                        'outageStartTime': {'S': str(event_failure_dictionary[event]['startTime'])},
                        'entryTime': {'S': str(time.time())},
                        'outageEndTime': {'S': 'N/A'},
                        'lastUpdateTime': {'S': str(event_failure_dictionary[event]['lastUpdatedTime'])},
                        'failureNotificationStatus': {'S': 'Upcoming'},
                        'failureNotificationTimestamp': {'S': "TBD"},
                        'resolutionNotificationStatus': {'S': 'N/A'},
                        'resolutionNotificationTimestamp': {'S': 'N/A'},
                        'associatedSnsTopic': {'S':  str(get_service_level(event_failure_dictionary[event]['service'])[1])},
                        'failureEventString': {'S': str(event_failure_dictionary[event])},
                        'eventStatus': {'S': event_failure_dictionary[event]['statusCode']},
                        'remediationActionStatus': {'S': 'N/A'},
                        'remediationActionTimestamp': {'S': 'N/A'},
                        },
                    ReturnValues='ALL_OLD',
                    ReturnConsumedCapacity='INDEXES',
                    ConditionExpression="attribute_not_exists(eventArn)",
                )
                
                # Calls function right after sending notification so record can be updated
                event_open_update_notification(event_failure_dictionary[event])
            
            # Checks if event has been closed since last run, if so, it calls the event closed function and sends notification
            if event_failure_dictionary[event]['statusCode'] == "closed":
                closed_response = dynamno_db_client.get_item(
                    TableName=config['default']['dynamodb_table_name'], 
                    Key={
                        "eventArn": {"S": event_failure_dictionary[event]['arn']},
                        "service": {"S": event_failure_dictionary[event]['service']}
                        },
                    )
                if 'Item' in closed_response and "'resolutionNotificationStatus': {'S': 'Sent'}" not in str(closed_response['Item']):
                    event_closed(event_failure_dictionary[event])

        except botocore.exceptions.ClientError as e:
            pass

def event_open_update_notification(event):
    if event['statusCode'] == "open":
        try:
            send_event_open_notification(event)
            update_item_response = dynamno_db_client.update_item(
                TableName=config['default']['dynamodb_table_name'],
                Key={
                    'eventArn': {'S': event['arn']},
                    'service': {'S': event['service']},
                },
                ReturnValues= 'ALL_NEW',
                ReturnConsumedCapacity='INDEXES',
                UpdateExpression='SET failureNotificationStatus = :updatedfailureNotificationStatus, failureNotificationTimestamp = :updatedfailureNotificationTimestamp',
                ConditionExpression = "eventStatus = :eventStatus AND failureNotificationStatus = :failureNotificationStatus AND failureNotificationTimestamp = :failureNotificationTimestamp",
                ## Conditional for status code = open and failureNotificationStatus and failureNotificationTimestamp
                ExpressionAttributeValues={
                    ":failureNotificationStatus": {'S': 'Upcoming'},
                    ":failureNotificationTimestamp": {'S': 'TBD'},
                    ":updatedfailureNotificationStatus": {'S': 'Sent'},
                    ":updatedfailureNotificationTimestamp": {'S': str(time.time())},
                    ":eventStatus": {'S': 'open'},
                },
            ),
        except botocore.exceptions.ClientError as e:
            pass
                            

def event_closed(event):
    try:
        send_event_closed_notification(event)
        close_item_response = dynamno_db_client.update_item(
            TableName=config['default']['dynamodb_table_name'],
            Key={
                'eventArn': {'S': event['arn']},
                'service': {'S': event['service']},
            },
            ReturnValues= 'ALL_NEW',
            ReturnConsumedCapacity='INDEXES',
            ConditionExpression = "eventStatus = :eventStatus",
            UpdateExpression='SET lastUpdateTime = :updatedLastUpdateTime, resolutionNotificationStatus = :updatedresolutionNotificationStatus, resolutionNotificationTimestamp = :updatedresolutionNotificationTimestamp, eventStatus = :updatedEventStatus, outageEndTime = :updatedEndTime',
            ## Conditional for status code = open (needs to be updated to closed) 
            ExpressionAttributeValues={
                ":updatedEndTime": {'S': str(event['endTime'])},
                ":updatedLastUpdateTime": {'S': str(event['lastUpdatedTime'])},
                ":updatedresolutionNotificationStatus": {'S': 'Sent'},
                ":updatedresolutionNotificationTimestamp": {'S': str(time.time())},
                ":eventStatus": {'S': 'open'},
                ":updatedEventStatus": {'S': 'closed'},
            },
        ),
    except botocore.exceptions.ClientError as e:
        pass

def send_event_open_notification(event):
    # Created a variable that can be used to reference sns topic arn in input config
    sns_selection = get_service_level(event['service'])[1]
    service_level = get_service_level(event['service'])[0]
    # Conditional to only send out notification if SNS ARN for service level isn't ""
    if sns_selection != '""':
        # Sends out SNS notification to all subscribers on list
        sns_open_response = sns_client.publish(
                    TopicArn=sns_selection,
                    Message=(f"ALERT: The {service_level} designated service {event['service']} is currently down.\n\nEvent ARN: {event['arn']}"),
                    Subject=(f"ALERT: {service_level} {event['service']} Outage"),
                )

def send_event_closed_notification(event):
    # Created a variable that can be used to reference sns topic arn in input config
    sns_selection = get_service_level(event['service'])[1]
    service_level = get_service_level(event['service'])[0]
    # Conditional to only send out notification if SNS ARN for service level isn't ""
    if sns_selection != '""':
        # Sends out SNS notification to all subscribers on list
        sns_closed_response = sns_client.publish(
                    TopicArn=sns_selection,
                    Message=(f"ALERT: The {service_level} designated service {event['service']} has been resolved!\n\nEvent ARN: {event['arn']}"),
                    Subject=(f"ALERT: {service_level} {event['service']} Resolved"),
                )

write_service_failure_event(detect_service_failures()[1])