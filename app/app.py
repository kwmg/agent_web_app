import random
from flask import Flask, render_template, request

app = Flask(__name__)


list_movie_ads = ['c1.gif', 'c2.gif', 'c3.gif', 'h1.gif',
                  'h2.gif', 'h3.gif', 'd1.gif', 'd2.gif', 'd3.gif']

dialogs = [{"settokusha": "星3つの映画です", "hisettokusha": "　"},
           {"settokusha": "これは見るべきですよ", "hisettokusha": "なぜおすすめなんですか"},
           {"settokusha": "foo", "hisettokusha": "hee"}]

patterns = [{"settokusha": "1_m.gif", "hisettokusha": "user"},
            {"settokusha": "2_m.gif", "hisettokusha": "user"},
            {"settokusha": "3_m.gif", "hisettokusha": "user"},
            {"settokusha": "4_m.gif", "hisettokusha": "user"},
            {"settokusha": "5_f.gif", "hisettokusha": "user"},
            {"settokusha": "6_f.gif", "hisettokusha": "user"},
            {"settokusha": "1_m.gif", "hisettokusha": "5_f.gif"},
            {"settokusha": "2_m.gif", "hisettokusha": "5_f.gif"},
            {"settokusha": "3_m.gif", "hisettokusha": "5_f.gif"},
            {"settokusha": "4_m.gif", "hisettokusha": "5_f.gif"},
            {"settokusha": "1_m.gif", "hisettokusha": "6_f.gif"},
            {"settokusha": "2_m.gif", "hisettokusha": "6_f.gif"},
            {"settokusha": "3_m.gif", "hisettokusha": "6_f.gif"},
            {"settokusha": "4_m.gif", "hisettokusha": "6_f.gif"},
            {"settokusha": "5_f.gif", "hisettokusha": "1_m.gif"},
            {"settokusha": "5_f.gif", "hisettokusha": "2_m.gif"},
            {"settokusha": "5_f.gif", "hisettokusha": "3_m.gif"},
            {"settokusha": "5_f.gif", "hisettokusha": "4_m.gif"},
            {"settokusha": "6_f.gif", "hisettokusha": "1_m.gif"},
            {"settokusha": "6_f.gif", "hisettokusha": "2_m.gif"},
            {"settokusha": "6_f.gif", "hisettokusha": "3_m.gif"},
            {"settokusha": "6_f.gif", "hisettokusha": "4_m.gif"}]


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/show/movie')
def show_page():

    idx = int(random.random() * len(list_movie_ads))
    return render_template("show_movie_ad.html",
                           target_page="/enq/movie/{}".format(idx),
                           img_file=list_movie_ads[idx])


@app.route('/enq/movie/<movie_idx>')
def show_enquete(movie_idx):
    return render_template("enquete.html", movie_idx=movie_idx)


@app.route('/procForm', methods=['POST'])
def post_action():
    id = request.form['id']
    gender = request.form['gender']
    level = request.form['level']
    return render_template("result.html", id=id, gender=gender, level=level)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)
