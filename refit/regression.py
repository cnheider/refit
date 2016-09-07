from __future__ import absolute_import, print_function, unicode_literals

import datetime

import numpy as np
import pandas as pd
from sklearn import linear_model

regr = linear_model.LinearRegression()


def train(data):
  dts = list()
  values = list()
  for entry in data:
    dts.append(pd.to_datetime(float(entry['endTimeNanos']), unit="ns"))
    values.append(entry['value'][0]['intVal'])

  entries = pd.Series(values, index=dts)

  entries_sorted_and_resampled = entries.resample('24H').mean().dropna().sort_index()
  dates = entries_sorted_and_resampled.keys().date.reshape(-1, 1)
  ordinals = [d.toordinal() for d in dates.flatten()]

  regr.fit(np.array(ordinals).reshape(-1, 1),
           np.array(entries_sorted_and_resampled.values).reshape(-1, 1))

  return regr.coef_


def predict_now_and_tommorow():
  return regr.predict(np.array([[datetime.datetime.now().toordinal()], [(datetime.date.today() + datetime.timedelta(1)).toordinal()]]))


def predict(date):
  return regr.predict(np.array([[date]]))
