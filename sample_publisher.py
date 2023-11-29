from google.cloud import pubsub_v1
import time
from dotenv import load_dotenv
import os

load_dotenv()

project_id = os.environ['GCP_PROJECT_ID']
topic_id = os.environ['GCP_PUBSUB_TOPIC_ID']

def publish_messages():
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    
    for n in range(1, 10):
        data_str = f"Message number {n}"
        # Data must be a bytestring
        data = data_str.encode("utf-8")
        # # When you publish a message, the client returns a future.
        future = publisher.publish(topic_path, data)
        time.sleep(3)
        print(future.result())
        
    print(f"Published messages to {topic_path}.")

