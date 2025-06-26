import streamlit as st
import json
import time
import os

st.set_page_config(page_title="Live Webhook Feed", layout="wide")

st.title("📡 Live Webhook Feed (Polling)")
st.caption("This app refreshes every 5 seconds and reads data from a shared file written by the webhook server.")

placeholder = st.empty()

# File path from the webhook server
STATE_FILE = "webhook_data.json"

# Try to read the file if it exists
if os.path.exists(STATE_FILE):
    try:
        with open(STATE_FILE, "r") as f:
            data = json.load(f)

        with placeholder.container():
            st.subheader("📥 Last Webhook Payload")
            st.json(data)

            try:
                if 'payload' in data and 'results' in data['payload']:
                    parsed = json.loads(data['payload']['results'][0]['result'])
                    st.success("🎯 Parsed Insight")
                    st.json(parsed)
            except Exception as e:
                st.warning(f"Could not parse nested result: {e}")
    except Exception as e:
        st.error(f"Error reading data file: {e}")
else:
    st.info("No webhook data file found yet.")

# Simulate refresh loop
st.write("Refreshing every 5 seconds...")
time.sleep(5)
st.rerun()
