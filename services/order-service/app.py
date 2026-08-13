import os, json, uuid
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from kafka import KafkaProducer

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)

producer=KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS","kafka:9092"),
    value_serializer=lambda v: json.dumps(v).encode()
)

class Order(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    order_id=db.Column(db.String(64),unique=True,nullable=False)
    user_id=db.Column(db.String(64),nullable=False)
    amount=db.Column(db.Integer,nullable=False)
    status=db.Column(db.String(40),nullable=False,default="PENDING")

with app.app_context(): db.create_all()

@app.post("/")
def create_order():
    data=request.get_json() or {}
    if not data.get("user_id") or not isinstance(data.get("amount"),int) or data["amount"]<=0:
        return jsonify(error="user_id and positive integer amount are required"),400
    oid="ORD-"+uuid.uuid4().hex[:12].upper()
    o=Order(order_id=oid,user_id=str(data["user_id"]),amount=data["amount"])
    db.session.add(o); db.session.commit()
    event={"event_id":uuid.uuid4().hex,"event_type":"ORDER_CREATED","order_id":oid,
           "user_id":str(data["user_id"]),"amount":data["amount"]}
    producer.send("order.events",event); producer.flush()
    return jsonify(order_id=oid,status=o.status),201

@app.get("/<order_id>")
def get_order(order_id):
    o=Order.query.filter_by(order_id=order_id).first()
    if not o: return jsonify(error="order not found"),404
    return jsonify(order_id=o.order_id,user_id=o.user_id,amount=o.amount,status=o.status)

@app.get("/health")
def health(): return jsonify(status="healthy")

if __name__=="__main__": app.run(host="0.0.0.0",port=5000)
