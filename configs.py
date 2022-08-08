import os
import logging
import datetime

from dotenv import load_dotenv

load_dotenv()
formatter = '[%(asctime)s] %(levelname)8s --- %(message)s (%(filename)s:%(lineno)s)'


TOKEN = os.getenv('BOT_TOKEN')
print(type(TOKEN))

DEBUG = os.getenv('BOT_DEBUG', False)  # if DEBUG doesn't exist then .env will None variable

if not DEBUG:
    logging.basicConfig(
        filename=f'logs/bot-from-{datetime.datetime.now().date()}.log',
        filemode='w',
        format=formatter,
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.WARNING
    )
    print(DEBUG)
    import sentry_sdk
    sentry_sdk.init(
        dsn="https://47e155755171488ebf1e2f1f621d3523@o1341400.ingest.sentry.io/6631833",
    
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )
