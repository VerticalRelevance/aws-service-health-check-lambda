
#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Remediate specified AWS Services'''

import logging
import configparser

import boto3

# Setting up logging component of lamdba script
logging.basicConfig(level=logging.INFO)

# Creates up config parser object and imports the config file
config = configparser.ConfigParser()
config.read_file(open('./aws_service_config.ini'))
logging.info("Input file loaded successfully")


# Creates boto3 health needed for script
health_client = boto3.client('health')