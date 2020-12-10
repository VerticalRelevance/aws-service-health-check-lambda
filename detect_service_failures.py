
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Return the status of specified AWS Services'''



import logging
import configparser

import json # for testing purposes only to read in test file

import boto3

# Setting up logging component of lamdba script
logging.basicConfig(level=logging.WARNING)

# Creates up config parser object and imports the config file
config = configparser.ConfigParser()
config.read_file(open('./aws_service_config.ini'))
logging.info("Input file loaded successfully")


# Creates boto3 health needed for script
health_client = boto3.client('health')

def get_service_level(service):
    if service in config['default']['platinum_services'].split(","):
        return("Platinum",config['notifications']['platinum_sns_arn'])
    if service in config['default']['gold_services'].split(","):
        return("Gold",config['notifications']['silver_sns_arn'])
    if service in config['default']['silver_services'].split(","):
        return("Silver",config['notifications']['silver_sns_arn'])

# Detection Functionality


#### FOR TESTING ONLY - READING IN FILE FOR SAMPLE EVENTS ####
with open('test_health_events_payload.json') as f:
  health_response = json.load(f)

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
    # health_response = health_client.describe_events(filter={
    #     'regions': [
    #         (config['default']['region']).strip('"')
    #         ],
    #     }
    # )

    logging.info("Successfully checked for failed services")

    # Creating empty list to store possible failed services in
    if len(health_response['events']) == 0:
        logging.info("There are no current AWS Health Events - EXITING")
        return
    else:
        logging.info("There are AWS health events affecting your account")

        # Creating a dictionary object that stores the differnet service level and failed serivce
        service_failure_dict = dict()

        # Creating a dictionary object that stores the full failure event inside
        event_failure_dict = dict()

        for i, event in enumerate(health_response['events']):
            try:
            # Check platinum specified services for failures
                if get_service_level(event['service'])[0] == "Platinum":
                    logging.info((f"{event['service']} is a platinum service and has degraded health"))
                    service_failure_dict.setdefault("Platinum", []).append(event['service'])
                    event_failure_dict[event['arn']] = event
                # Check gold specified services for failures
                if  get_service_level(event['service'])[0] == "Gold":
                    logging.info((f"{event['service']} is a gold service and has degraded health"))
                    service_failure_dict.setdefault("Gold", []).append(event['service'])
                    event_failure_dict[event['arn']] = event
                ## Check silver specified services for failures
                if  get_service_level(event['service'])[0] == "Silver":
                    logging.info((f"{event['service']} is a silver service and has degraded health"))
                    service_failure_dict.setdefault("Silver", []).append(event['service'])
                    event_failure_dict[event['arn']] = event

                logging.info("Successfully returned dictionary with failed services")
            except TypeError as NotCriticalService:
                ## Add Info type to logger saying that Service X is not a critical service
                pass
        # Returns failed items and events to a dict that can be passed into notify function
        return (service_failure_dict, event_failure_dict)
        

detect_service_failures()