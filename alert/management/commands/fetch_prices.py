from django.core.management.base import BaseCommand
from alert.fetch_prices import client


class Command(BaseCommand):
    help = "Fetch prices"

    def handle(self, *args, **options):
        client()
