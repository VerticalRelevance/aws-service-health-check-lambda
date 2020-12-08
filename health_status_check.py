#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Return the status and remedation of specified AWS Services'''

import logging
import configparser

import boto3

# Setting up logging component of lamdba script
logging.basicConfig(level=logging.INFO)

# Creates up config parser object and imports the config file
config = configparser.ConfigParser()
config.read_file(open('./aws_service_config.ini'))
logging.info("Input file loaded successfully")

# Creates boto3 health and sns client needed for script
health_client = boto3.client('health')
sns_client = boto3.client('sns')
        


def notify_service_failures(failure_dicionary):
    # Iterates over keys and values in dictionary for service level and failed service(s)
    for key, value in failure_dicionary.items():
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

notify_service_failures(detect_service_failures())


def main():
    service_failures = detect_service_failures()
    notify_service_failures(service_failures)


#if __name__ == main()

######################## END NOTIFICATION ######################## 


######################## START REMEDIATION ########################





######################## END REMEDIATION ########################