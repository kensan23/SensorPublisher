import boto3
import json
import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv
from sensor_data import sensor_data
load_dotenv()
LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
FORMAT = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
logging.basicConfig(level = LOGLEVEL, format = FORMAT)
LOCATION = "Location"

def post_data(sensordata):
    token = os.getenv("AWSSNSTOPICARN")
    sns = boto3.client('sns')
    publish_data = data.get_data()
    publish_data.update({'locationId' : LOCATION})
    response = sns.publish(
        TopicArn=token,   
        Message=json.dumps(publish_data),   
    )

try:
    data = sensor_data()
    sched = BlockingScheduler()
    logging.info('Starting logging')
    sched.add_job(post_data, 'cron', minute='*/1', args=[data])
    sched.start()

except Exception as e:
    logging.exception('Error publishing data')
