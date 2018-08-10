import datetime as dt
import mock

import import_find_new

import find_new_mocks
from find_new import previous_time, environment as env

TESTING_TIME = dt.datetime(2017, 12, 6, 15, 29, 43, 79060)

env.maturity = 'test'
