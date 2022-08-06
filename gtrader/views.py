import json
import csv
import re
from django.http import HttpResponse
from .kiteauth import refresh_access_token
from .models import Auth, Instruments
from .settings import KITE_API_KEY
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from kiteconnect import KiteConnect
from io import StringIO
from .strategy import shooting_star, engulfing_pattern, support_resistence

kite = KiteConnect(api_key=KITE_API_KEY)


def index():
    return HttpResponse("Hello, world. Welcome to Gtrader.")


def token(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        request_token = data['request_token']
        try:
            access_token = refresh_access_token(request_token)
        except Exception as e:
            print("Error {0}".format(str(e.args[0])).encode("utf-8"))
            return json.dumps({"Error": str(e.args[0]).encode("utf-8")})
        auth_obj = Auth.objects.get(api_key=KITE_API_KEY)
        auth_obj.access_token = access_token
        auth_obj.save()

        return json.dumps({"status": 200})


def instruments(request):
    if request.method == "POST":
        auth_obj = Auth.objects.get(api_key=KITE_API_KEY)
        kite.set_access_token(auth_obj.access_token)
        instruments = kite.instruments(exchange='NSE')
        for instrument in instruments:
            try:
                if instrument['instrument_type'] == 'EQ':
                    print(instrument)
                    expiry = instrument['expiry']
                    Instruments.objects.update_or_create(
                        trading_symbol=instrument['tradingsymbol'],
                        exchange=instrument['exchange'],
                        defaults=dict(trading_symbol=instrument['tradingsymbol'],
                                      exchange=instrument['exchange'],
                                      exchange_token=instrument['exchange_token'],
                                      instrument_token=instrument['instrument_token'],
                                      name=instrument['name'],
                                      last_price=instrument['last_price'],
                                      expiry=None if expiry else expiry,
                                      strike=instrument['strike'],
                                      tick_size=instrument['tick_size'],
                                      lot_size=instrument['lot_size'],
                                      instrument_type=instrument['instrument_type'],
                                      segment=instrument['segment']))
            except Exception as e:
                print(e)
        return json.dumps({"status": 200})


def signal(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        symbol = data['symbol']
        # shooting_star.shooting_star(symbol)
        # engulfing_pattern.engulfing_pattern(symbol)
        support_resistence.support_resistance(symbol)
    return HttpResponse("Hello, world. Welcome to Gtrader.")
