# FastAPI-based WebSocket and Webhook server
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse
import uvicorn
import json
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# Set to hold connected WebSocket clients
clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    logging.info(f"WebSocket connection established: {websocket.client}")
    try:
        while True:
            await websocket.receive_text()  # optional: can also be skipped if unused
    except WebSocketDisconnect:
        logging.info(f"WebSocket connection closed: {websocket.client}")
    except Exception as e:
        logging.warning(f"WebSocket error: {e}")
    finally:
        clients.discard(websocket)

@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
    except Exception as e:
        logging.warning(f"Invalid JSON received: {e}")
        return JSONResponse(status_code=400, content={"message": "Invalid JSON"})

    logging.info(f"Webhook received: {data}")

    message = json.dumps(data)
    to_remove = set()

    for client in clients:
        try:
            await client.send_text(message)
        except Exception as e:
            logging.error(f"Failed to send to client {client.client}: {e}")
            to_remove.add(client)

    clients.difference_update(to_remove)
    return {"message": "Webhook received!"}

if __name__ == "__main__":
    logging.info("Server starting on http://localhost:8000")
    uvicorn.run("webhook_server:app", host="0.0.0.0", port=8000, reload=True)
