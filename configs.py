import os
import logging

import sentry_sdk
import datetime

from dotenv import load_dotenv

load_dotenv()
formatter = '[%(asctime)s] %(levelname)8s --- %(message)s (%(filename)s:%(lineno)s)'


TOKEN = os.getenv('BOT_TOKEN')

DEBUG = os.getenv('BOT_DEBUG', False)  # if DEBUG doesn't exist then .env will None variable

SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

SMS_SECRET_KEY = os.getenv('SMS_SECRET_KEY')

if not DEBUG:
    logging.basicConfig(
        filename=f'logs/bot-from-{datetime.datetime.now().date()}.log',
        filemode='w',
        format=formatter,
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.WARNING
    )
    sentry_sdk.init(
        dsn="https://aef700f7d45c44cd8b043231c030ea6e@o1341400.ingest.sentry.io/4504875616305152",
    
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )