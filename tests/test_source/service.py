from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def source():
    return render_template('source.html')
