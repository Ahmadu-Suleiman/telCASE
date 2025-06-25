from flask import Flask, request
from flask_sockets import Sockets
import json

app = Flask(__name__)
sockets = Sockets(app)

# A set to store all connected WebSocket clients
clients = set()

@sockets.route('/ws')
def socket(ws):
    """
    Handles new WebSocket connections.
    """
    clients.add(ws)
    while not ws.closed:
        # Keep the connection alive
        ws.receive()
    clients.remove(ws)

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Receives data from the webhook.
    """
    if request.method == 'POST':
        data = request.json
        print(f"Webhook received: {data}")

        # Broadcast the data to all connected WebSocket clients
        for client in clients:
            if not client.closed:
                client.send(json.dumps(data))

        return 'Webhook received!', 200

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    print("Server started on port 5000")
    server.serve_forever()