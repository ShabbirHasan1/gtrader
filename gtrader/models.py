from decimal import Decimal
from django.db import models


class Auth(models.Model):
    api_key = models.CharField(
        max_length=100, null=False, blank=False, primary_key=True)
    api_secret = models.CharField(max_length=100, null=False, blank=False)
    access_token = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.api_key


class Instruments(models.Model):
    exchange_token = models.IntegerField(null=False)
    instrument_token = models.IntegerField(null=False)
    trading_symbol = models.CharField(max_length=255, null=False)
    name = models.CharField(max_length=255, null=False)
    last_price = models.DecimalField(
        max_digits=20, decimal_places=2, default=Decimal(0.00))
    expiry = models.DateField(max_length=255, null=True, blank=True)
    strike = models.DecimalField(
        max_digits=20, decimal_places=2, default=Decimal(0.00))
    tick_size = models.IntegerField(null=False)
    lot_size = models.IntegerField(null=False)
    instrument_type = models.CharField(max_length=100, null=False)
    segment = models.CharField(max_length=100, null=False)
    exchange = models.CharField(max_length=100, null=False)

    class Meta:
        unique_together = ('trading_symbol', 'exchange')


class HistoricalDataManager(models.Manager):
    def get_stock_historical_data(self, symbol):
        historical_data = list(self.filter(trading_symbol=symbol).values(
            'trading_symbol', 'open_price', 'high_price', 'low_price', 'close_price', 'volume', 'date'))
        return historical_data


class HistoricalData(models.Model):
    trading_symbol = models.CharField(max_length=255, null=False)
    exchange = models.CharField(max_length=100, null=False)
    date = models.CharField(max_length=100, null=False, blank=False)
    open_price = models.DecimalField(
        max_digits=20, decimal_places=2, default=Decimal(0.00))
    high_price = models.DecimalField(
        max_digits=20, decimal_places=2, default=Decimal(0.00))
    low_price = models.DecimalField(
        max_digits=20, decimal_places=2, default=Decimal(0.00))
    close_price = models.DecimalField(
        max_digits=20, decimal_places=2, default=Decimal(0.00))
    volume = models.IntegerField(null=False, blank=False)
    historical_manager = HistoricalDataManager()
