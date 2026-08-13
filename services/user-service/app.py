import os, jwt
from datetime import datetime, timedelta, timezone
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)
SECRET=os.getenv("JWT_SECRET","change-me")

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(120),nullable=False)
    email=db.Column(db.String(255),unique=True,nullable=False)
    password_hash=db.Column(db.String(255),nullable=False)

with app.app_context(): db.create_all()

@app.get("/")
def root(): return jsonify(service="user-service")

@app.post("/register")
def register():
    data=request.get_json() or {}
    if not data.get("name") or not data.get("email") or not data.get("password"):
        return jsonify(error="name, email and password are required"),400
    if User.query.filter_by(email=data["email"]).first():
        return jsonify(error="email already registered"),409
    u=User(name=data["name"],email=data["email"],
           password_hash=generate_password_hash(data["password"]))
    db.session.add(u); db.session.commit()
    return jsonify(id=u.id,name=u.name,email=u.email),201

@app.post("/login")
def login():
    data=request.get_json() or {}
    u=User.query.filter_by(email=data.get("email")).first()
    if not u or not check_password_hash(u.password_hash,data.get("password","")):
        return jsonify(error="invalid credentials"),401
    token=jwt.encode({"sub":u.id,"exp":datetime.now(timezone.utc)+timedelta(hours=2)},SECRET,algorithm="HS256")
    return jsonify(access_token=token)

@app.get("/health")
def health(): return jsonify(status="healthy")

if __name__=="__main__": app.run(host="0.0.0.0",port=5000)
