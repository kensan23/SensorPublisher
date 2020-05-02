import boto3
import json
import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv
from sensor_data import sensor_data
load_dotenv()

def post_data(sensordata):
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    token = os.getenv("AWSSNSTOPICARN")
    sns = boto3.client('sns')
    # response = sns.publish(
    #     TopicArn=token,   
    #     Message=json.dumps(data.get_data("study")),   
    # )

try:
    data = sensor_data()
    sched = BlockingScheduler()
    sched.add_job(post_data, 'cron', minute='*/1', args=[data])
    sched.start()

except Exception as e:
    logging.exception("Error publishing data")
