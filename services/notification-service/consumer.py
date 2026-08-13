import os, json
from kafka import KafkaConsumer
c=KafkaConsumer("order.events","payment.events",
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS","kafka:9092"),
    group_id="notification-service", auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode()))
print("notification-service started")
for msg in c:
    print("NOTIFICATION:",msg.value)
