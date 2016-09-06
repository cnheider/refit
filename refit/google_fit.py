"""
Hsad
"""
# !/usr/bin/python

from __future__ import absolute_import, print_function, unicode_literals

import datetime

import httplib2
import pandas as pd
from apiclient import discovery

from config import (DATA_SOURCE_ID_CAL1, DATA_SOURCE_ID_HR,
                    DATA_SOURCE_ID_SLEEP, DATA_SOURCE_ID_STEPS,
                    DATA_SOURCE_ID_WEIGHT_MERGE)


def datetime_to_nanoseconds(date_time):
  """Given a datetime convert it to nanoseconds since epoch."""
  # time_now = int(time.time()) #epoch millis
  epoch = datetime.datetime.utcfromtimestamp(0)
  return (date_time - epoch).total_seconds() * 1000 * 1000 * 1000


def get_start_and_end_timestamps():
  """Get yesterday and the day before yesterday's timestamp values. """
  today = datetime.date.today()
  tomorrow = datetime.date.today() + datetime.timedelta(1)
  # yesterday = today - datetime.timedelta(1)
  # day_before_yest = yesterday - datetime.timedelta(1)
  month_ago = today - datetime.timedelta(10)

  # Get the datetimes representing midnight
  # today_datetime = datetime.datetime.combine(today, datetime.datetime.min.time())
  # yest_datetime = datetime.datetime.combine(day_before_yest, datetime.datetime.min.time())
  tomorrow_datetime = datetime.datetime.combine(tomorrow, datetime.datetime.min.time())

  # day_before_yest_datetime = datetime.datetime.combine(yesterday, datetime.datetime.min.time())
  month_ago_datetime = datetime.datetime.combine(month_ago, datetime.datetime.min.time())

  # Convert to nanoseconds since epoch
  start_time = datetime_to_nanoseconds(month_ago_datetime)
  end_time = datetime_to_nanoseconds(tomorrow_datetime)

  # Remove the digits after the decimal and store as strings
  start_time = '{0:.0f}'.format(start_time)
  end_time = '{0:.0f}'.format(end_time)

  return [start_time, end_time]


def get_steps(oauth2, timestamps=get_start_and_end_timestamps()):
  data = get_fitness_data(oauth2, timestamps, DATA_SOURCE_ID_STEPS)
  if 'point' in data:
    # aggregated_by_day2(data['point'])
    return aggregated_by_day(data['point'])  # data['point']  # aggregated_by_day(data['point'])
  else:
    return


def get_sleep(oauth2, timestamps=get_start_and_end_timestamps()):
  data = get_fitness_data(oauth2, timestamps, DATA_SOURCE_ID_SLEEP)
  if 'point' in data:
    return data['point']
  else:
    return


def get_weight(oauth2, timestamps=get_start_and_end_timestamps()):
  data = get_fitness_data(oauth2, timestamps, DATA_SOURCE_ID_WEIGHT_MERGE)
  if 'point' in data:
    return data['point']
  else:
    return


def get_hr(oauth2, timestamps=get_start_and_end_timestamps()):
  data = get_fitness_data(oauth2, timestamps, DATA_SOURCE_ID_HR)
  if 'point' in data:
    return mean_by_day(data['point'])  # data['point']  # mean_by_day(data['point'])
  else:
    return


def get_cal_burned(oauth2, timestamps=get_start_and_end_timestamps()):
  data = get_fitness_data(oauth2, timestamps, DATA_SOURCE_ID_CAL1)
  if 'point' in data:
    return data['point']
  else:
    return


def get_cal_consumed(oauth2, timestamps=get_start_and_end_timestamps()):
  data = get_fitness_data(oauth2, timestamps, DATA_SOURCE_ID_CAL1)
  if 'point' in data:
    return data['point']
  else:
    return


def get_fitness_data(oauth2, timestamps, data_source_id):
  """Shows basic usage of the Fitness API. Creates a Fitness API service object and outputs a list of data points."""
  credentials = oauth2.credentials
  http = credentials.authorize(httplib2.Http())
  service = discovery.build('fitness', 'v1', http=http)

  # Data Source ID
  data_set_id = '{0}-{1}'.format(timestamps[0], timestamps[1])
  results = service.users().dataSources().datasets().get(userId='me',
                                                         dataSourceId=data_source_id, datasetId=data_set_id).execute()

  return results


def get_fitness_data_sources_list(oauth2):
  credentials = oauth2.credentials
  http = credentials.authorize(httplib2.Http())
  service = discovery.build('fitness', 'v1', http=http)

  results = service.users().dataSources().list(userId='me').execute()

  return results


def mean_by_day(data):
  dts = list()
  values = list()
  for entry in data:
    dts.append(pd.to_datetime(float(entry['endTimeNanos']), unit="ns"))
    values.append(entry['value'][0]['fpVal'])

  entries = pd.Series(values, index=dts)
  return [{'value': [{'fpVal': v}], 'endTimeNanos': datetime_to_nanoseconds(day), 'dataTypeName': data[0]['dataTypeName']} for day, v in entries.resample('24H').mean().dropna().sort_index().iteritems()]


def aggregated_by_day(data):
  dts = list()
  values = list()
  for entry in data:
    dts.append(pd.to_datetime(float(entry['endTimeNanos']), unit="ns"))
    values.append(entry['value'][0]['intVal'])

  entries = pd.Series(values, index=dts)

  return [{'value': [{'intVal': v}], 'endTimeNanos': datetime_to_nanoseconds(day), 'dataTypeName': data[0]['dataTypeName']} for day, v in entries.resample('24H').sum().dropna().sort_index().iteritems()]
