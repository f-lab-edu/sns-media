from confluent_kafka import Producer

producer = Producer(
    {"bootstrap.servers": "localhost:9092", "security.protocol": "PLAINTEXT"}
)


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")
