import threading
from django.conf import settings
from alert.tasks import process_records


ASSETS = getattr(settings, 'ASSETS')
DB_ALERT_CHECK_INTERVAL = getattr(settings, 'DB_ALERT_CHECK_INTERVAL')


class ProcessPrice:
    def __init__(self):
        self.asset_prices = {}
        self.lock = threading.Lock()
        self.execute_prices()

    def set_current_price(self, asset, price):
        self.asset_prices[asset] = price

    def execute_prices(self):
        threading.Timer(DB_ALERT_CHECK_INTERVAL, self.execute_prices).start()
        with self.lock:
            asset_prices = self.asset_prices
            self.asset_prices = {}
        print(asset_prices)
        self.call_alert_tasks(asset_prices)

    @staticmethod
    def call_alert_tasks(asset_prices):
        if not asset_prices:
            return
        process_records.delay(asset_prices)


process_price = ProcessPrice()
