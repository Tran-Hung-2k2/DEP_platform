import json
from pykafka import KafkaClient
import time
import random

topic_name = "alo"

client = KafkaClient(hosts="localhost:29092")
topic = client.topics[topic_name.encode()]

producer = topic.get_producer()
count = 1
while True:
    obj_ms = {
        "status": random.choice(["stop", "run", "offline", "online"]),
        "speed": random.choice(["50.55", "60", "23.335", "77", "92.54"]),
        "direction": random.choice(["41.21", "452.23", "455.22", "66.233"]),
        "longitude": random.choice(["77.5666", "88.523123", "7852.24647", "96633.66"]),
        "latitude": random.choice(["77.5666", "88.523123", "7852.24647", "96633.66"]),
        "extra_info": {"a": "b"},
        "device_id": "1111111111",
        "problem": "track_and_trace",
    }

    json_mes = json.dumps(obj_ms)
    producer.produce(json_mes.encode("utf-8"))
    print(f"Đã gửi {count}")
    count += 1
    time.sleep(0.1)
