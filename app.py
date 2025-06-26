import streamlit as st
import json
import time
import os

# --- Page Setup ---
st.set_page_config(
    page_title="telCASE",
    page_icon="case logo.png",
    menu_items={
        'Get Help': 'mailto:casebeheard@gmail.com',
        'Report a bug': 'mailto:casebeheard@gmail.com',
        'About': 'https://linktr.ee/case.be.heard'
    }
)
st.image("case logo.svg", width=50)
st.title('telCASE')
st.subheader('Voice AI–Powered Case Intake for the CASE Platform', divider='orange')
st.markdown("""
**telCASE** is a Voice AI assistant that converts every phone call into a structured case record. 
It brings together caller metadata, AI-driven transcripts, and data attributes into one seamless entry, 
eliminating manual intake and making case follow-up effortless and transparent.
""")
st.header("Live Case Generation")
st.subheader("Below is a live example of a case created from a telCASE conversation")
placeholder = st.empty()

# File path from the webhook server
STATE_FILE = "case_data.json"

# Try to read the file if it exists
if os.path.exists(STATE_FILE):
    try:
        with open(STATE_FILE, "r") as f:
            data = json.load(f)

        with placeholder.container():
            try:
                if 'payload' in data and 'results' in data['payload']:
                    case_data = json.loads(data['payload']['results'][0]['result'])
                    st.success("Parsed Insight")
                    st.markdown(f"""
                           <div style='background-color:#f9f9f9;padding:20px;border-radius:10px;border:1px solid #ddd;'>
                               <h2 style='color:#333;'>{case_data['title']}</h2>
                               <p><strong>Details:</strong> {case_data['details']}</p>
                               <p><strong>Summary:</strong> {case_data['summary']}</p>
                               <p><strong>Category:</strong> {case_data['category']}</p>
                               <p><strong>Desired Outcome:</strong> {case_data['desired_outcome']}</p>
                               <hr/>
                               <p><strong>Name:</strong> {case_data['name_of_community_member']}</p>
                               <p><strong>Address:</strong> {case_data['address_of_community_member']}</p>
                               <p><strong>Phone:</strong> {case_data['phone_number_of_community_member']}</p>
                           </div>
                       """, unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"Could not parse nested result: {e}")
    except Exception as e:
        st.error(f"Error reading data file: {e}")
else:
    st.info("No case data yet.")

# Simulate refresh loop
time.sleep(5)
st.rerun()
