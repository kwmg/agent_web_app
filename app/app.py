import random
from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'db295528b34367fa2a5a5ece8217b4b712136c171d8a6c1fca622151736495c0'

REPEAT_NUM = 4

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


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        return redirect(url_for('index'))
    session['user_id'] = request.form['user_id']
    session['gender'] = request.form['gender']
    session['age'] = request.form['age']
    session['enq_res'] = []
    session['movie_list'] = []
    return redirect(url_for('show_ad'))


@app.route('/ad')
def show_ad():
    movie_list = list(range(len(list_movie_ads)))
    dup = list(set(movie_list) & set(session['movie_list']))
    for d in dup:
        movie_list.remove(d)
    idx = movie_list[int(random.random() * len(movie_list))]
    session['current_movie'] = idx
    return render_template("show_movie_ad.html",
                           wait_time=5,  # 秒で指定
                           img_file=list_movie_ads[idx])


@app.route('/enq')
def show_enquete():
    return render_template("enquete.html")


@app.route('/procEnq', methods=['POST'])
def proc_enquete():
    movie_idx = session['current_movie']
    enq_entry = {'idx': movie_idx, 'rating': int(request.form['rating'])}
    enq_res = session['enq_res']
    enq_res.append(enq_entry)
    session['enq_res'] = enq_res
    movie_list = session['movie_list']
    movie_list.append(movie_idx)
    session['movie_list'] = movie_list
    print(movie_list)
    if len(movie_list) < REPEAT_NUM:
        return redirect(url_for('show_ad'))
    return redirect(url_for('finish'))


@app.route('/end')
def finish():
    return '''
<html>
<head></head>
<body>
  <h1>ご協力ありがとうございました</h1>
</body>
</html>
'''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)
