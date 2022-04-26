from flask import Flask
from honkai3 import config

app = Flask(__name__,template_folder='../templates')
app.config.from_object(config)

@app.route('/')
def index():
    pass