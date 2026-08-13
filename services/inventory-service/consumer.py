import os, json
from kafka import KafkaConsumer

c=KafkaConsumer("order.events",
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS","kafka:9092"),
    group_id="inventory-service",
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode()))
print("inventory-service started")
for msg in c:
    event=msg.value
    if event.get("event_type")=="ORDER_CREATED":
        print("Inventory reservation requested:",event["order_id"])
