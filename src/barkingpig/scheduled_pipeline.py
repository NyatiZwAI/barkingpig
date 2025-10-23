import schedule
import time
from pathlib import Path
from run_pipeline import run_batch, run_pipeline
from social_posting import post_to_social_media

TOPIC_FILE = Path(__file__).parent / "topics.txt"

def job():
    print("Running weekly BarkingPig article pipeline...")

    if TOPIC_FILE.exists():
        with open(TOPIC_FILE, "r") as f:
            topics = [line.strip() for line in f if line.strip()]

        csv_records = []

        for topic in topics:
            record = run_pipeline(topic)
            csv_records.append(record)
            #Auto post to social media
            post_to_social_media(record)

        #Save CSV for SEO tracking
        cvs_file = Path(__file__).parent / "outputs" / "article_index.csv"
        import csv
        with open(csv_file, "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, filenames=["topic", "filename", "h1", "meta_description"])
            writer.writeheader()
            write.writerows(csv_records)

        print(f"CSV index saved to {csv_file}")

    else:
        print(f"Topic file not found: {TOPIC_FILE}")

#Schedule weekly job (every Mon at 09:00AM)
#schedule.every().monday.at("09:00").do(job)
#
#while True:
#    schedule.run_pending()
#    time.sleep(60)
