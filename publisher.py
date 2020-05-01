import boto3
import json
import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv
from sensordata import sensor_data

try:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv()
    #token = os.getenv("AWSSNSTOPICARN")
    data = sensor_data()
    #sns = boto3.client('sns')

    # response = sns.publish(
    #     TopicArn=token,   
    #     Message=json.dumps(data.get_data("study")),   
    # )
    print(data.get_data("study"))
    sched = BlockingScheduler()
    sched.add_job(job_function, 'cron', second='*/5')
    sched.start()

except Exception as e:
    logging.exception("Error publishing data")
