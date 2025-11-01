from flask import Flask
from threading import Thread
import time

app = Flask('')

@app.route('/')
def home():
    return "🤖 Bot Discord está online 24/7 no Replit!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()
    