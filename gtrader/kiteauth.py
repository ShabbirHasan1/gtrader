import logging
import re
from gtrader.settings import KITE_API_KEY, KITE_API_SECRET
from kiteconnect import KiteConnect
from .settings import KITE_API_KEY, KITE_API_SECRET

logging.basicConfig(level=logging.DEBUG)


def refresh_access_token(request_token):
    kite = KiteConnect(api_key=KITE_API_KEY)
    data = kite.generate_session(request_token, api_secret=KITE_API_SECRET)
    return data['access_token']
