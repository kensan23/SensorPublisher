import json
import os
# from dotenv import load_dotenv
# load_dotenv()
from sensordata import sensor_data

data = sensor_data()
try:
    while True:
        print(data.get_data("testRoom"))
except KeyboardInterrupt:
    print('interrupted!')



# sns = boto3.client('sns')

# response = sns.publish(
#     TopicArn='',   
#     Message='Hello world',   
# )
