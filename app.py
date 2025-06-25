import streamlit as st
import asyncio
import websockets
import json
import threading
from streamlit.runtime.scriptrunner import add_script_run_ctx

if 'websocket_data' not in st.session_state:
    st.session_state.websocket_data = None
if 'websocket_thread' not in st.session_state:
    st.session_state.websocket_thread = None
if 'stop_websocket' not in st.session_state:
    st.session_state.stop_websocket = threading.Event()

def websocket_listener():
    uri = "ws://localhost:8000/ws"

    async def listen():
        st.session_state.stop_websocket.clear()
        try:
            async with websockets.connect(uri) as websocket:
                while not st.session_state.stop_websocket.is_set():
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                        st.session_state.websocket_data = json.loads(message)
                        st.rerun()
                    except asyncio.TimeoutError:
                        continue
                    except websockets.exceptions.ConnectionClosed:
                        print("WebSocket closed.")
                        break
        except Exception as e:
            print(f"WebSocket failed: {e}")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(listen())

@st.fragment
def display_data():
    st.header("Live Webhook Data")

    if st.session_state.websocket_data:
        st.json(st.session_state.websocket_data)
    else:
        st.info("Waiting for data from the webhook...")

    with st.expander("Debug Log"):
        st.text(json.dumps(st.session_state.websocket_data, indent=2) if st.session_state.websocket_data else "No data yet.")

st.title("Real-Time Webhook Dashboard")

# Check if the listener thread is running
is_thread_running = (
    st.session_state.websocket_thread is not None and
    st.session_state.websocket_thread.is_alive()
)

if not is_thread_running:
    if st.button("Connect to Webhook Stream"):
        st.session_state.stop_websocket.clear()
        thread = threading.Thread(target=websocket_listener)
        add_script_run_ctx(thread)
        st.session_state.websocket_thread = thread
        thread.start()
        st.success("Connected! Waiting for webhook events.")
        st.rerun()
else:
    st.success("Status: Connected to webhook stream.")

# Display the data fragment
display_data()
