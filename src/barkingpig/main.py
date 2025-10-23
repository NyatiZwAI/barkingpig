#!/usr/bin/env python

from pathlib import Path
from .run_pipeline import run_pipeline, run_batch

def run():
    topics_file = Path(__file__).parent / "topics.txt"

    if topics_file.exists() and topics_file.stat().st.size > 0:
        print(f"Found topics.txt, running batch mode...")
        return run_batch(str(topics_file))
    else:
        default_topic = "Moving the masses, Web3 technology in Sub Saharan Africa"
        print(f"topics.txt not found or empty. Running default topic: {default_topic}")
        return run_pipeline(default_topic)
