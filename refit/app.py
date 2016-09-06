
from __future__ import absolute_import, print_function, unicode_literals

import json

from flask import Flask, Response, render_template
from flask_bower import Bower
from oauth2client.contrib.flask_util import UserOAuth2
from oauth2client.file import Storage

from config import (DEBUG, GOOGLE_FIT_SCOPES, GOOGLE_OAUTH2_CLIENT_ID,
                    GOOGLE_OAUTH2_CLIENT_SECRET, HOST, PASSWORD, PORT,
                    SECRET_KEY, USERNAME)
from google_fit import (get_cal_burned, get_fitness_data_sources_list, get_hr,
                        get_sleep, get_steps, get_weight)
from regression import predict, train

app = Flask(__name__)
app.config['GOOGLE_OAUTH2_CLIENT_ID'] = GOOGLE_OAUTH2_CLIENT_ID
app.config['GOOGLE_OAUTH2_CLIENT_SECRET'] = GOOGLE_OAUTH2_CLIENT_SECRET
app.config['USERNAME'] = USERNAME
app.config['PASSWORD'] = PASSWORD
credentials_storage = Storage('google_oauth2_credentials')
oauth2 = UserOAuth2(app, storage=credentials_storage)
Bower(app)


@app.route("/data")
@oauth2.required(scopes=GOOGLE_FIT_SCOPES)
def data_sources():
  print(get_fitness_data_sources_list(oauth2))
  return Response(json.dumps(get_fitness_data_sources_list(oauth2)), content_type="application/json")


@app.route("/data/steps")
@oauth2.required(scopes=GOOGLE_FIT_SCOPES)
def data_steps():
  return Response(json.dumps(get_steps(oauth2)), content_type="application/json")


@app.route("/data/steps/predict")
@oauth2.required(scopes=GOOGLE_FIT_SCOPES)
def data_steps_predict():
  coefs = train(get_steps(oauth2))
  return "coefficients: " + str(coefs) + ", predictions: " + str(predict())
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
  if credentials_storage.get() is None:
    credentials_storage.put(oauth2.credentials)
  return render_template("index.html", google_fit_user=oauth2.email)


if __name__ == "__main__":
  app.secret_key = SECRET_KEY
  app.run(debug=DEBUG, host=HOST, port=PORT)
