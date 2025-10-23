#!/usr/bin/env python

import streamlit as st
from run_pipeline import run_pipeline, run_batch
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OUTPUTS_DIR = Path("src/barkingpig/outputs")

st.title("BarkingPig AI Content Creator")

st.markdown("Enter a topic or upload a `topics.txt` file to run your App.")

#Initialize session state to store results
if "result_text" not in st.session_state:
    st.session_state.result_text = ""

#Helper function to get snippet
def get_snippet(data, length=250):
    snippet = str(data)
    return snippet[:length] + "..." if len(snippet) > length else snippet

#---------------------
# 1) Batch Pipeline
#---------------------
uploaded_file = st.file_uploader("Upload topics.txt for batch processing", type=["txt"])
if uploaded_file is not None:
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    topics_path = upload_dir / uploaded_file.name

    with open(topics_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"{uploaded_file.name} uploaded successfully!")

    if st.button("Run Batch"):
        st.info("Running batch mode...")
        result = run_batch(str(topics_path))
        st.session_state.result_text = result

        snippet = get_snippet(result)
        st.markdown(f"**Batch Snippet:** {snippet}")

        st.text_area("Batch Results", value=result, height=300)

        st.download_button(
            label="Download Batch Results",
            data=str(result),
            file_name="batch_results.txt",
            mime="text/plain"
        )

else:
    #-------------------------
    # 2) Single Topic Pipeline
    #-------------------------
    topic = st.text_area("Enter a topic to run single pipeline", height=150)

    if st.button("Run Single Topic"):
        if topic.strip():
            st.info("Oink...")
            result = run_pipeline(topic)
            st.session_state.result_text = result

            snippet = get_snippet(result)
            st.markdown(f"**Snippet:** {snippet}")

            st.text_area("Single Topic Result", value=result, height=300)

            st.download_button(
                label="Download Single Result",
                data=str(result),
                file_name="single_result.txt",
                mime="text/plain"
            )
        else:
            st.warning("This little piggy cried Wee! Wee! Wee! all the way home.")

#-------------------
# 3) Previous Result
#-------------------
if st.session_state.result_text:
    st.text_area("Previous Result", value=st.session_state.result_text, height=300)

#-------------------
# 4) OUTPUTS BROWSER 
#-------------------
st.subheader("Generated Outputs")

if OUTPUTS_DIR.exists():
    md_files = sorted(OUTPUTS_DIR.glob("*.md"))
    if not md_files:
        st.info("No generates output files found yet.")
    else:
        for md_file in md_files:
            with st.expander(md_file.name, expanded=False):
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()

                st.markdown(content, unsafe_allow_html=True)

                st.download_button(
                    label="Download File",
                    data=content,
                    file_name=md_file.name,
                    mime="text/markdown"
                )
else:
    st.info("Outputs directory not found.")
