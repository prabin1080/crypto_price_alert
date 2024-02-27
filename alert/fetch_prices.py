import asyncio
import json
import websockets
from django.conf import settings
from alert.process_prices import process_price


END_POINT = 'wss://stream.binance.com:9443/ws'

ASSETS = getattr(settings, 'ASSETS')


config_message = json.dumps({'method': 'SUBSCRIBE', 'params': [asset.lower()+'@ticker' for asset in ASSETS], 'id': 1})


def handle_message(message):
    message = json.loads(message)
    if 's' in message:
        process_price.set_current_price(message['s'], message['c'])
    else:
        print(message)


async def _client(uri):
    async for websocket in websockets.connect(uri):
        await websocket.send(config_message)
        try:
            async for message in websocket:
                handle_message(message)
                await asyncio.sleep(1)

        except websockets.ConnectionClosed:
            print('closed connection')
            continue


def client():
    asyncio.run(_client(END_POINT))
