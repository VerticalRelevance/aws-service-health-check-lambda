
#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Remediate specified AWS Services'''

import logging
import configparser
import botocore.exceptions

import boto3
import time

from detect_service_failures import detect_service_failures, get_service_level
from notify_service_failures import write_service_failure_event

# Setting up logging component of lamdba script
logging.basicConfig(level=logging.INFO)

# Creates up config parser object and imports the config file
config = configparser.ConfigParser()
config.read_file(open('./aws_service_config.ini'))
logging.info("Input file loaded successfully")


# Creates boto3 health needed for script
health_client = boto3.client('health')
dynamno_db_client = boto3.client('dynamodb')

''' 
This script is intended to be customized based on individual use cases for how to handle certain service outages.
Below I've included a sample function that checks if an issue is open and it pertains to a select service.
If so, it executes the code below and also updates the dynamodb table to indicate that the remediation has been triggered
'''

def remediate_SERVICE(event_failure_dictionary):
    for event in event_failure_dictionary:
        if event_failure_dictionary[event]['statusCode'] == "open" and event_failure_dictionary[event]['statusCode'] == SERVICE:
            pass
            # Custom Remedation Code Here
            # Insert custom remediation code here
                # Some examples include
                    # Calling a custom lambda remediation
                    # Kicking off a codepipeline / step function 

            # Inputs remediation action into DynamoDB for associated eventARN
            update_item_response = dynamno_db_client.update_item(
                    TableName=config['default']['dynamodb_table_name'],
                    Key={
                        'eventArn': {'S': event['arn']},
                        'service': {'S': event['service']},
                    },
                    ReturnValues= 'ALL_NEW',
                    ReturnConsumedCapacity='INDEXES',
                    UpdateExpression='SET remediationActionStatus = :updatedRemediationActionStatus, remediationActionTimestamp = :updatedRemediationActionTimestamp',
                    ConditionExpression = "remediationActionStatus = :remediationActionStatus",
                    ## Conditional for status code = open and failureNotificationStatus and failureNotificationTimestamp
                    ExpressionAttributeValues={
                        ":remediationActionStatus": {'S': 'N/A'},
                        ":updatedRemediationActionStatus": {'S': 'Triggered'},
                        ":updatedRemediationActionTimestamp": {'S': str(time.time())},
                    },
            )
            



remediate_SERVICE(detect_service_failures()[1])