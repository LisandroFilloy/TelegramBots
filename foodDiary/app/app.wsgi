#! /usr/bin/python3.8

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/bots/TelegramBots/foodDiary/app'

from app import app as application
application.secret_key = 'abc123'

