import json

import flask
from flask import (Flask, Response, abort, flash, g, jsonify, redirect,
                   render_template, request, session, url_for)
from oauth2client.contrib.flask_util import UserOAuth2

from config import (DEBUG, GOOGLE_FIT_SCOPES, GOOGLE_OAUTH2_CLIENT_ID,
                    GOOGLE_OAUTH2_CLIENT_SECRET, HOST, PASSWORD, PORT,
                    SECRET_KEY, USERNAME)
from google_fit import get_cal_burned, get_hr, get_sleep, get_steps, get_weight
from regression import predict, train

app = Flask(__name__)
app.config['GOOGLE_OAUTH2_CLIENT_ID'] = GOOGLE_OAUTH2_CLIENT_ID
app.config['GOOGLE_OAUTH2_CLIENT_SECRET'] = GOOGLE_OAUTH2_CLIENT_SECRET
app.config['USERNAME'] = USERNAME
app.config['PASSWORD'] = PASSWORD
oauth2 = UserOAuth2(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME']:
      error = 'Invalid username'
    elif request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid password'
    else:
      session['logged_in'] = True
      flash('You were logged in')
      return redirect(url_for('data_steps'))
  return render_template('login.html', error=error)


@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for('data_steps'))


@app.route("/data/steps")
@oauth2.required(scopes=GOOGLE_FIT_SCOPES)
def data_steps():
  return Response(json.dumps(get_steps(oauth2)), content_type="application/json")


@app.route("/data/steps/predict")
@oauth2.required(scopes=GOOGLE_FIT_SCOPES)
def data_steps_predict():
  train(get_steps(oauth2))
  return str(predict())
  # return Response(json.dumps(prediction), content_type="application/json")


@app.route("/data/sleep")
@oauth2.required(scopes=GOOGLE_FIT_SCOPES)
def data_sleep():
  return Response(json.dumps(get_sleep(oauth2)), content_type="application/json")


@app.route("/data/hr")
@oauth2.required(scopes=GOOGLE_FIT_SCOPES)
def data_hr():
  return Response(json.dumps(get_hr(oauth2)), content_type="application/json")


@app.route("/data/weight")
@oauth2.required(scopes=GOOGLE_FIT_SCOPES)
def data_weight():
  return Response(json.dumps(get_weight(oauth2)), content_type="application/json")


@app.route("/data/cal/burned")
@oauth2.required(scopes=GOOGLE_FIT_SCOPES)
def data_cal_burned():
  return Response(json.dumps(get_cal_burned(oauth2)), content_type="application/json")


@app.route("/")
@oauth2.required(scopes=GOOGLE_FIT_SCOPES)
def index():
  return render_template("index.html", google_fit_user=oauth2.email)


if __name__ == "__main__":
  app.secret_key = SECRET_KEY
  app.run(debug=DEBUG, host=HOST, port=PORT)
