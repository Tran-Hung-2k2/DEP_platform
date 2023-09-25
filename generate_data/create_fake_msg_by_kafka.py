from confluent_kafka import Producer
import json
import random
import time

# Kafka configuration
kafka_config = {
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'django-server',
    'auto.offset.reset': 'earliest'
}

# Kafka topic
topic = "TrackAndTrace"

# Create a Kafka producer instance
producer = Producer(kafka_config)

# Send 1000 random messages
for i in range(1000):
    # Generate random data for each message
    sample_data = {
        'device_id': f'device_{random.randint(1, 100)}',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'status': random.choice(['OK', 'Error']),
        'speed': random.uniform(0, 100),
        'direction': random.choice(['N', 'S', 'E', 'W']),
        'longitude': random.uniform(-180, 180),
        'latitude': random.uniform(-90, 90),
        'extra_info': {
            'random_key1': random.randint(1, 100),
            'random_key2': random.uniform(0, 1),
            'random_key3': random.choice(['A', 'B', 'C']),
        }
    }

    # Serialize the random data to JSON
    message_value = json.dumps(sample_data)

    # Send the data to the Kafka topic
    producer.produce(topic, key=None, value=message_value)

# Wait for any outstanding messages to be delivered
producer.flush()
