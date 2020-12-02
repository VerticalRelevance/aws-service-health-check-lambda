#!/usr/bin/env python
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

# Detection Functionality

def detect_service_failures():
    ### Need to run as root account for this to work
    #health_response = health_client.describe_events_for_organization()

    # Get recent health events that are open for account lambda resides in

####### PRODUCTION CODE SNIPIT BELOW #######
    # health_response = health_client.describe_events(filter={
    #     'regions': [
    #         (config['default']['region']).strip('"')
    #         ],
    #     'eventStatusCodes': [
    #         'open'
    #     ],
    #     }
    # )

####### NOT PRODUCTION - Pulls ALL Events, not just open events. Replace after testing ########
    health_response = health_client.describe_events(filter={
        'regions': [
            (config['default']['region']).strip('"')
            ],
        }
    )

    logging.info("Successfully checked for failed services")

    # Creating empty list to store possible failed services in

    if len(health_response['events']) == 0:
        logging.info("There are no current AWS Health Events - EXITING")
        return
    else:
        logging.info("There are AWS health events affecting your account")

        # Creating a dictionary object that stores the differnet service level and failed serivce
        failure_dict = dict()

        for i, event in enumerate(health_response['events']):
            # Check platinum specified services for failures
            if event['service'] in config['default']['platinum_services'].split(","):
                logging.info((f"{event['service']} is a platinum service and has degraded health"))
                failure_dict.setdefault("Platinum", []).append(event['service'])
            # Check gold specified services for failures
            if event['service'] in config['default']['gold_services'].split(","):
                logging.info((f"{event['service']} is a gold service and has degraded health"))
                failure_dict.setdefault("Gold", []).append(event['service'])
            ## Check silver specified services for failures
            if event['service'] in config['default']['silver_services'].split(","):
                logging.info((f"{event['service']} is a silver service and has degraded health"))
                failure_dict.setdefault("Silver", []).append(event['service'])


        logging.info("Successfully returned dictionary with failed services")

        # Returns failed items to a dict that can be passed into notify function
        return failure_dict
        


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

######################## END NOTIFICATION ######################## 


######################## START REMEDIATION ########################





######################## END REMEDIATION ########################