import logging
import websocket
import sys

from functools import partial
from .transcription import Transcriber, LINEAR16

logging.basicConfig(level=logging.DEBUG)


def on_message(transcriber, ws, message):
    transcriber.push(message)


def on_error(ws, error):
    logging.debug(error)


def on_close(ws):
    logging.debug('closing')


def main():
    transcriber = Transcriber(language='es-ES', codec=LINEAR16, sample_rate=16000)
    transcriber.start()

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        "ws://localhost:8080/ws",
        on_message=partial(on_message, transcriber),
        on_error=on_error,
        on_close=on_close,
        subprotocols=["stream-channel"],
        header=['Channel-ID: ' + sys.argv[1]],
    )

    try:
        ws.run_forever()
    finally:
        transcriber.stop()
