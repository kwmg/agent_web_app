# -*- coding: utf-8 -*-
import random
from flask import Flask, render_template, request

app = Flask(__name__)


comedy_movie_ads = ['c1.gif', 'c2.gif', 'c3.gif']


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/show/comedy')
def show_page():
    idx = int(random.random() * len(comedy_movie_ads))
    return render_template("show_movie_ad.html",
                           target_page="/enq/comedy/{}".format(idx),
                           img_file=comedy_movie_ads[idx])


@app.route('/enq/comedy/<movie_idx>')
def show_enquete(movie_idx):
    return render_template("enquete.html", movie_idx=movie_idx)


@app.route('/procForm', methods=['POST'])
def post_action():
    id = request.form['id']
    gender = request.form['gender']
    level = request.form['level']
    rating = request.form['rating']
    return render_template("result.html", id=id, gender=gender, level=level, rating=rating)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)
