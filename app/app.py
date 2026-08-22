from fastapi import FastAPI
import pymysql
from datetime import datetime
import os

app = FastAPI()

def get_db():
    conn = pymysql.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root"),
        database=os.getenv("DB_NAME", "mydb")
    )
    return conn


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api")
def root():
    return {"message": "API is working"}


@app.get("/api/items")
def get_items():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    conn.close()
    return items


@app.post("/api/items/{name}")
def add_item(name: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO items (name, created_at) VALUES (%s, %s)",
        (name, datetime.now())
    )
    conn.commit()
    conn.close()
    return {"message": "Item added", "name": name}
