#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Return notification of specified AWS Services'''

import logging
import configparser
import botocore.exceptions

import boto3
import time

from detect_service_failures import detect_service_failures, get_service_level

print(time.time())

# Setting up logging component of lamdba script
logging.basicConfig(level=logging.DEBUG)

# Creates up config parser object and imports the config file
config = configparser.ConfigParser()
config.read_file(open('./aws_service_config.ini'))
logging.info("Input file loaded successfully")

sns_client = boto3.client('sns')
dynamno_db_client = boto3.client('dynamodb')

# Temp - for debugging
#print(detect_service_failures()[1])

# Check DynamoDB for record of outage

def write_service_failure_event(event_failure_dictionary):
    for event in event_failure_dictionary:
        try:
            put_response = dynamno_db_client.put_item(
                    TableName='poc_aws_failure_events',
                    Item={
                        'event_arn': {'S': event_failure_dictionary[event]['arn']},
                        'service': {'S': event_failure_dictionary[event]['service']},
                        'startTime': {'S': str(event_failure_dictionary[event]['startTime'])},
                        'endTime': {'S': 'N/A'},
                        'lastUpdateTime': {'S': str(event_failure_dictionary[event]['lastUpdatedTime'])},
                        'failureNotificationStatus': {'S': 'Upcoming'},
                        'failureNotificationTimestamp': {'S': "TBD"},
                        'resolutionNotificationStatus': {'S': 'N/A'},
                        'resolutionNotificationTimestamp': {'S': 'N/A'},
                        'associatedSnsTopic': {'S':  str(get_service_level(event_failure_dictionary[event]['service'][1]))},
                        'failureEventString': {'S': str(event_failure_dictionary[event])},
                        'eventStatus': {'S': event_failure_dictionary[event]['statusCode']},
                        'eventScope': {'S': event_failure_dictionary[event]['eventScopeCode']},
                        },
                    ReturnValues='ALL_OLD',
                    ReturnConsumedCapacity='INDEXES',
                    ConditionExpression="attribute_not_exists(event_arn)",
            )
            print(put_response)
            # Call Send notification function here


        except botocore.exceptions.ClientError as e:
            # Read Event Status Code, if open and failureNotificationStatus = upcoming
                ## Update field failureNotificationStatus to sent
                ## Update failureNotificationTimeStamp to time
            # If Event Status Code closed
                # Send notification of resolution
                # Update endTime, lastUpdateTime, resolutionNotificationStatus, resolutionNotificationTimestamp, eventStatus




## Need individual, get, write and update functions

# if record already exists in dynamodb proceed to remedation script if remedation config input is not null

#print(detect_service_failures()[1])


write_service_failure_event(detect_service_failures()[1])

#print(detect_service_failures()[1]['arn:aws:health:us-east-1::event/CLOUDWATCH/AWS_CLOUDWATCH_OPERATIONAL_ISSUE/AWS_CLOUDWATCH_OPERATIONAL_ISSUE_LADUF_1606412297']['startTime'])


'''

def notify_service_failure(service_failure_dict):
    # Iterates over keys and values in dictionary for service level and failed service(s)
    for key, value in service_failure_dict.items():
        # Iterates over items in list of failed services
        for service in value:
            # Created a variable that can be used to reference sns topic arn in input config
            sns_selection = f"{key.lower()}_sns_arn"
            # Conditional to only send out notification if SNS ARN for service level isn't ""
            if (config['notifications'][sns_selection]) != '""':
                # Sends out SNS notification to all subscribers on list
                sns_response = sns_client.publish(
                            TopicArn=config['notifications'][sns_selection],
                            Message=(f"ALERT: The {key} designated service {service} is currently down"),
                            Subject=(f"ALERT: {key} Outage"),
                        )



'''