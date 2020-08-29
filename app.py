import boto3
import json
import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from dotenv import load_dotenv
from sensor_data import sensor_data
from tenacity import *

load_dotenv()
LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
FORMAT = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
logging.basicConfig(level = LOGLEVEL, format = FORMAT)
LOCATION = "StudyNorth"
_COUNTS = {'exception_count': 0 }


def my_listener(event):
    if event.exception:
        if _COUNTS['exception_count'] >= 5:
            sched.shutdown()
        _COUNTS['exception_count'] +=  1

@retry(wait=wait_random_exponential(multiplier=1, max=60), stop=stop_after_attempt(2))
def post_data(sensordata):
    ssm = boto3.client('ssm')
    arn = ssm.get_parameter(Name='/Roomdata/RoomDataTopicArn')["Parameter"]["ARN"]
    sns = boto3.client('sns')
    publish_data = data.get_data()
    publish_data.update({'locationId' : LOCATION})
    response = sns.publish(
        TopicArn=arn,   
        Message=json.dumps(publish_data),   
    )
    logging.info(json.dumps(publish_data))
    _COUNTS['exception_count'] = 0

if __name__ == '__main__':
    try:
        data = sensor_data()
        sched = BlockingScheduler()
        logging.info('Starting logging')
        sched.add_job(post_data, 'cron', minute='*/1', args=[data])
        sched.add_listener(my_listener, EVENT_JOB_ERROR)
        sched.start()

    except Exception as e:
        logging.exception('Error publishing data')
