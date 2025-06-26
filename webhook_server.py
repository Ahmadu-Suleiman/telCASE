from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import json
import logging
import os

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# Path to temporary file Streamlit will read from
STATE_FILE = "case_data.json"

@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
    except Exception as e:
        logging.warning(f"Invalid JSON received: {e}")
        return JSONResponse(status_code=400, content={"message": "Invalid JSON"})

    logging.info(f"Webhook received: {data}")

    # Save the latest data to a file for Streamlit to read
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        logging.error(f"Failed to write data to file: {e}")

    return {"message": "Webhook received!"}

if __name__ == "__main__":
    logging.info("Server starting on http://localhost:8000")
    uvicorn.run("webhook_server:app", host="0.0.0.0", port=8000, reload=True)
