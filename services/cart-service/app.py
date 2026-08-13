import os, json
from flask import Flask, request, jsonify
import redis

app=Flask(__name__)
r=redis.from_url(os.getenv("REDIS_URL","redis://redis:6379/0"),decode_responses=True)

@app.get("/")
def get_cart():
    user=request.headers.get("X-User-ID","guest")
    return jsonify(json.loads(r.get(f"cart:{user}") or '{"items":[]}'))

@app.post("/items")
def add_item():
    data=request.get_json() or {}
    user=request.headers.get("X-User-ID","guest")
    key=f"cart:{user}"
    cart=json.loads(r.get(key) or '{"items":[]}')
    cart["items"].append({"product_id":data.get("product_id"),"quantity":data.get("quantity",1)})
    r.set(key,json.dumps(cart),ex=86400)
    return jsonify(cart)

@app.delete("/")
def clear_cart():
    user=request.headers.get("X-User-ID","guest")
    r.delete(f"cart:{user}")
    return jsonify(message="cart cleared")

@app.get("/health")
def health(): return jsonify(status="healthy")

if __name__=="__main__": app.run(host="0.0.0.0",port=5000)
