from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def source():
    return render_template('source.html')


@app.route('/article/<int:article_id>')
def article(article_id):
    return render_template(f'article{article_id}.html')
