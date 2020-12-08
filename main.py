#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Return the status of specified AWS Services'''

import logging
import configparser

import boto3

health_client = boto3.client('health')


health_response = health_client.describe_events(filter={
    'regions': [
        ('us-east-1').strip('"')
        ],
    }
)

print(health_response)
