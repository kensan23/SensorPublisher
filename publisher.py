import boto3
import json
import os
from dotenv import load_dotenv
load_dotenv()

sns = boto3.client('sns')

response = sns.publish(
    TopicArn='',   
    Message='Hello world',   
)
