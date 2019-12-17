import os
import random
import datetime
from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.utils import secure_filename
import pandas as pd
from dialogs import dialogs

SAVE_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'saved_csv')
ENQUETE_REPEAT_TIME = 4

app = Flask(__name__)
app.secret_key = 'db295528b34367fa2a5a5ece8217b4b712136c171d8a6c1fca622151736495c0'
app.config['SAVE_FOLDER'] = SAVE_FOLDER
app.config['ENQUETE_REPEAT_TIME'] = ENQUETE_REPEAT_TIME


list_movie_ads = ['c1.gif', 'c2.gif', 'c3.gif', 'h1.gif',
                  'h2.gif', 'h3.gif', 'd1.gif', 'd2.gif', 'd3.gif']

agent_patterns = [["1_m.gif"],
                  ["2_m.gif"],
                  ["3_m.gif"],
                  ["4_m.gif"],
                  ["5_f.gif"],
                  ["6_f.gif"],
                  ["1_m.gif", "5_f.gif"],
                  ["2_m.gif", "5_f.gif"],
                  ["3_m.gif", "5_f.gif"],
                  ["4_m.gif", "5_f.gif"],
                  ["1_m.gif", "6_f.gif"],
                  ["2_m.gif", "6_f.gif"],
                  ["3_m.gif", "6_f.gif"],
                  ["4_m.gif", "6_f.gif"],
                  ["5_f.gif", "1_m.gif"],
                  ["5_f.gif", "2_m.gif"],
                  ["5_f.gif", "3_m.gif"],
                  ["5_f.gif", "4_m.gif"],
                  ["6_f.gif", "1_m.gif"],
                  ["6_f.gif", "2_m.gif"],
                  ["6_f.gif", "3_m.gif"],
                  ["6_f.gif", "4_m.gif"]]


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
    session['agent_list'] = []
    session['current_d'] = []
    return redirect(url_for('show_ad'))


@app.route('/ad')
def show_ad():
    movie_list = [m for m in range(len(list_movie_ads))
                  if m not in session['movie_list']]
    agent_list = [a for a in range(len(agent_patterns))
                  if a not in session['agent_list']]
    movie_idx = movie_list[int(random.random() * len(movie_list))]
    agent_pat = agent_list[int(random.random() * len(agent_list))]
    dialog_pat = dialogs[len(agent_patterns[agent_pat]) - 1]
    dialog = dialog_pat[int(random.random() * len(dialog_pat))]
    session['current_movie'] = movie_idx
    session['current_ag'] = agent_pat
    session['current_d'] = dialog
    return render_template("show_movie_ad.html",
                           wait_time=10,  # 秒で指定
                           img_movie=list_movie_ads[movie_idx],
                           img_ag=agent_patterns[agent_pat],
                           dialog=dialog)


@app.route('/enq')
def show_enquete():
    return render_template("enquete.html")


@app.route('/procEnq', methods=['POST'])
def proc_enquete():
    # prepare enquete result entry
    movie_idx = session['current_movie']
    agent_pat = session['current_ag']
    d = session['current_d']
    enq_entry = {
        'date': datetime.datetime.now().isoformat(),
        'user_id': session['user_id'],
        'gender': session['gender'],
        'age': session['age'],
        'idx': movie_idx,
        'pt': agent_pat,
        'dialog': d,
        'rating': int(request.form['rating']),
        'credit': int(request.form['credit']),
        'satisfy': int(request.form['satisfy'])}
    # update enquete result history
    enq_res = session['enq_res']
    enq_res.append(enq_entry)
    session['enq_res'] = enq_res
    # update movie history
    movie_list = session['movie_list']
    movie_list.append(movie_idx)
    session['movie_list'] = movie_list
    print(movie_list)
    # update agent pattern history
    ag_list = session['agent_list']
    ag_list.append(agent_pat)
    session['agent_list'] = ag_list
    print(ag_list)
    # check repeat time
    if len(movie_list) < app.config['ENQUETE_REPAET_TIME']:
        return redirect(url_for('show_ad'))
    return redirect(url_for('finish'))


@app.route('/end')
def finish():
    enq_res = session['enq_res']
    cols = {k: [d.get(k) for d in enq_res] for k in enq_res[0].keys()}
    df = pd.DataFrame(cols)
    filename = secure_filename('{}.csv'.format(enq_res[0]['user_id']))
    filepath = os.path.join(app.config['SAVE_FOLDER'], filename)
    try:
        os.makedirs(app.config['SAVE_FOLDER'])
    except FileExistsError:
        pass
    df.to_csv(filepath)
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
