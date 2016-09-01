import datetime

import numpy as np
from sklearn import linear_model

regr = linear_model.LinearRegression()


def train(data):
  days = dict()
  for entry in data:
    dt = datetime.datetime.fromtimestamp(float(entry['endTimeNanos']) / 1000.0 / 1000.0 / 1000.0)
    for value in entry['value']:
      if dt.day in days:
        days[dt.day] += value['intVal']
      else:
        days[dt.day] = value['intVal']

  datearray = np.array(days.keys())
  print(datearray)
  print(days.values())

  regr.fit(datearray.reshape(datearray.shape[0], 1), days.values())

  print(regr.coef_)


def predict():
  return regr.predict(np.array([[datetime.datetime.now().day]]))
