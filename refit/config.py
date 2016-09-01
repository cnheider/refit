#!/usr/bin/python
import os
import uuid

DEBUG = True
GOOGLE_OAUTH2_CLIENT_ID = os.environ.get('GOOGLE_OAUTH2_CLIENT_ID', 'not found')
AUTH_URI = os.environ.get('AUTH_URI', 'not found')
TOKEN_URI = os.environ.get('TOKEN_URI', 'not found')
GOOGLE_OAUTH2_CLIENT_SECRET = os.environ.get('GOOGLE_OAUTH2_CLIENT_SECRET', 'not found')
REDIRECT_URIS = os.environ.get('REDIRECT_URIS', 'not found')
JAVASCRIPT_ORIGINS = os.environ.get('JAVASCRIPT_ORIGINS', 'not found')
APPLICATION_NAME = os.environ.get('APP_NAME', 'refit')
USERNAME = os.environ.get('USERNAME', 'admin')
PASSWORD = os.environ.get('PASSWORD', 'admin')
SECRET_KEY = os.environ.get('SECRET_KEY', str(uuid.uuid4()))
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', 5000))
GOOGLE_FIT_SCOPES = ['https://www.googleapis.com/auth/fitness.body.read',
                     'https://www.googleapis.com/auth/fitness.activity.read', 'https://www.googleapis.com/auth/fitness.activity.read', 'https://www.googleapis.com/auth/drive.metadata.readonly']
DATA_SOURCE_ID_CAL1 = 'derived:com.google.calories.bmr:com.google.android.gms:from_height&weight'
DATA_SOURCE_ID_CAL2 = 'derived:com.google.calories.bmr:com.google.android.gms:merged'
DATA_SOURCE_ID_STEPS = 'derived:com.google.step_count.delta:com.google.android.gms:estimated_steps'
DATA_SOURCE_ID_WEIGHT_USER_INPUT = 'raw:com.google.height:com.google.android.apps.fitness:user_input'
DATA_SOURCE_ID_HR = 'derived:com.google.heart_rate.bpm:com.google.android.gms:merge_heart_rate_bpm'
DATA_SOURCE_ID_SLEEP = 'raw:com.google.activity.segment:com.mc.miband1:'
DATA_SOURCE_ID_WEIGHT_MERGE = 'derived:com.google.weight:com.google.android.gms:merge_weight'
