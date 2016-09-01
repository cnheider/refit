#!/usr/bin/python
from __future__ import print_function

import datetime
import os

import flask
import httplib2
import oauth2client
from apiclient import discovery
from oauth2client.contrib.flask_util import UserOAuth2

from config import (DATA_SOURCE_ID_CAL1, DATA_SOURCE_ID_HR,
                    DATA_SOURCE_ID_SLEEP, DATA_SOURCE_ID_STEPS,
                    DATA_SOURCE_ID_WEIGHT_MERGE)


def datetime_to_nanoseconds(date_time):
  """Given a datetime convert it to nanoseconds since epoch.
  """
  # time_now = int(time.time()) #epoch millis
  epoch = datetime.datetime.utcfromtimestamp(0)
  return (date_time - epoch).total_seconds() * 1000 * 1000 * 1000


def get_start_and_end_timestamps():
  """Get yesterday and the day before yesterday's timestamp values.
  """
  today = datetime.date.today()
  tomorrow = datetime.date.today() + datetime.timedelta(1)
  yesterday = today - datetime.timedelta(1)
  day_before_yest = yesterday - datetime.timedelta(1)
  month_ago = today - datetime.timedelta(10)

  # Get the datetimes representing midnight
  today_datetime = datetime.datetime.combine(today, datetime.datetime.min.time())
  yest_datetime = datetime.datetime.combine(day_before_yest, datetime.datetime.min.time())
  tomorrow_datetime = datetime.datetime.combine(tomorrow, datetime.datetime.min.time())

  day_before_yest_datetime = datetime.datetime.combine(yesterday, datetime.datetime.min.time())
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
    return mean_by_day(data['point'])  # data['point'] #mean_by_day(data['point'])
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
  """Shows basic usage of the Fitness API.
  Creates a Fitness API service object and outputs a list of data points.
  """
  credentials = oauth2.credentials  # client.OAuth2Credentials.from_json(flask.session['credentials'])
  http = credentials.authorize(httplib2.Http())
  service = discovery.build('fitness', 'v1', http=http)

  # Data Source ID
  data_set_id = '{0}-{1}'.format(timestamps[0], timestamps[1])
  results = service.users().dataSources().datasets().get(userId='me',
                                                         dataSourceId=data_source_id, datasetId=data_set_id).execute()

  return results


def mean_by_day(data):
  days = dict()
  number = dict()
  means = dict()

  for entry in data:
    dt = datetime.datetime.fromtimestamp(float(entry['endTimeNanos']) / 1000.0 / 1000.0 / 1000.0)
    for value in entry['value']:
      if dt.day in days:
        number[dt.day] += 1
        days[dt.day] += value['fpVal']
      else:
        number[dt.day] = 1
        days[dt.day] = value['fpVal']

  for k, v in days.iteritems():
    means[k] = v / number[k]

  days_mean_json_list = [{'value': [{'fpVal': v}], 'endTimeNanos': '{0:.0f}'.format(datetime_to_nanoseconds(datetime.datetime.fromtimestamp(float(data[0]['endTimeNanos']) / 1000.0 / 1000.0 / 1000.0).replace(day=k))),
                          'dataTypeName': data[0]['dataTypeName']} for k, v in means.iteritems()]
  return days_mean_json_list


def aggregated_by_day(data):
  days = dict()

  for entry in data:
    dt = datetime.datetime.fromtimestamp(float(entry['endTimeNanos']) / 1000.0 / 1000.0 / 1000.0)
    for value in entry['value']:
      if dt.day in days:
        days[dt.day] += value['intVal']
      else:
        days[dt.day] = value['intVal']

  days_aggregate_json_list = [{'value': [{'intVal': v}], 'endTimeNanos': '{0:.0f}'.format(datetime_to_nanoseconds(datetime.datetime.fromtimestamp(float(data[0]['endTimeNanos']) / 1000.0 / 1000.0 / 1000.0).replace(day=k))),
                               'dataTypeName': data[0]['dataTypeName']} for k, v in days.iteritems()]
  return days_aggregate_json_list
