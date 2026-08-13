import os, uuid
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)

class Payment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    idempotency_key=db.Column(db.String(255),unique=True,nullable=False)
    payment_id=db.Column(db.String(80),unique=True,nullable=False)
    amount=db.Column(db.Integer,nullable=False)
    status=db.Column(db.String(30),nullable=False,default="SUCCESS")

with app.app_context(): db.create_all()

@app.post("/")
def pay():
    key=request.headers.get("Idempotency-Key")
    data=request.get_json() or {}
    if not key: return jsonify(error="Idempotency-Key is required"),400
    existing=Payment.query.filter_by(idempotency_key=key).first()
    if existing:
        return jsonify(payment_id=existing.payment_id,status=existing.status,idempotent=True)
    amount=data.get("amount")
    if not isinstance(amount,int) or amount<=0: return jsonify(error="invalid amount"),400
    p=Payment(idempotency_key=key,payment_id="pay_"+uuid.uuid4().hex[:16],amount=amount)
    db.session.add(p); db.session.commit()
    return jsonify(payment_id=p.payment_id,status=p.status,idempotent=False),201

@app.get("/health")
def health(): return jsonify(status="healthy")

if __name__=="__main__": app.run(host="0.0.0.0",port=5000)
