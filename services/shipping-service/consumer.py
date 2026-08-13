import os, json
from kafka import KafkaConsumer
c=KafkaConsumer("payment.events",
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS","kafka:9092"),
    group_id="shipping-service", auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode()))
print("shipping-service started")
for msg in c:
    print("Shipping event:",msg.value)
