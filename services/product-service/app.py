import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)

class Product(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    price=db.Column(db.Integer,nullable=False)
    stock=db.Column(db.Integer,nullable=False,default=0)

with app.app_context():
    db.create_all()
    if Product.query.count()==0:
        db.session.add_all([
            Product(name="Running Shoes",price=4999,stock=25),
            Product(name="Training Shoes",price=3999,stock=40)
        ])
        db.session.commit()

@app.get("/")
def products():
    return jsonify([{"id":p.id,"name":p.name,"price":p.price,"stock":p.stock}
                    for p in Product.query.all()])

@app.post("/")
def create():
    data=request.get_json() or {}
    if not data.get("name") or not isinstance(data.get("price"),int):
        return jsonify(error="name and integer price are required"),400
    p=Product(name=data["name"],price=data["price"],stock=int(data.get("stock",0)))
    db.session.add(p); db.session.commit()
    return jsonify(id=p.id,name=p.name,price=p.price,stock=p.stock),201

@app.get("/health")
def health(): return jsonify(status="healthy")

if __name__=="__main__": app.run(host="0.0.0.0",port=5000)
