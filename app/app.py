# -*- coding: utf-8 -*-
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/procForm', methods=['POST'])
def post_action():
    id = request.form['id']
    gender = request.form['gender']
    level = request.form['level']
    rating = request.form['rating']
    return render_template("result.html", id=id, gender=gender, level=level, rating=rating)


if __name__ == '__main__':
    app.run()
