import os
import yaml
import argparse
import csv
from pathlib import Path
from datetime import datetime
from crewai import LLM, Agent, Task, Crew
from langchain_openai import ChatOpenAI

CONFIG_PATH = Path(__file__).parent / "config"

def load_yaml(file_name):
    with open(CONFIG_PATH / file_name, "r") as f:
        return yaml.safe_load(f)

agents_config = load_yaml("agents.yaml")
tasks_config = load_yaml("tasks.yaml")

def build_agents(topic: str):
    # Initialize real LLM object
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY")
    )

    agents = {}
    for name, conf in agents_config.items():
        agents[name] = Agent(
            role=conf["role"].format(topic=topic),
            goal=conf["goal"].format(topic=topic),
            backstory=conf["backstory"].format(topic=topic),
            llm=llm,
            verbose=True
        )

    return agents

def build_tasks(topic: str, agents, current_year: int):
    tasks = []
    for name, conf in tasks_config.items():
        tasks.append(
            Task(
                description=conf["description"].format(topic=topic, current_year=current_year),
                expected_output=conf["expected_output"].format(topic=topic),
                agent=agents[conf["agent"]],
            )
        )
    return tasks

def run_pipeline(topic: str):
    print(f"Running pipeline for topic: {topic}")
    current_year = datetime.now().year

    agents = build_agents(topic)
    tasks = build_tasks(topic, agents, current_year)

    crew = Crew(agents=list(agents.values()), tasks=tasks, verbose=True)
    final_output = crew.kickoff()
    print("\n Final Article Generated!\n")

    output_str = str(final_output)

    #Save Markdown
    out_dir = Path(__file__).parent / "outputs"
    out_dir.mkdir(exist_ok=True)
    filename = f"{topic.replace(' ', '_')}.md"
    out_file = out_dir / filename
    with open(out_file, "w") as f:
        f.write(output_str)

    #Extract H1 and meta description
    lines = output_str.splitlines()
    h1 = next((l[2:].strip() for l in lines if l.startswith("# ")), topic)
    meta_description = next((l.strip() for l in lines if l.lower().startswith("meta descripiton")), "")

    print(f"H1 Headline: {h1}")
    print(f"Meta Description: {meta_description}")
    print(f"Saved to {out_file}\n")

    return {"topic": topic, "filename": filename, "h1": h1, "meta_description": meta_description}

def run_batch(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        topics = [line.strip() for line in f if line.strip()]

    csv_records = []

    for topic in topics:
        record = run_pipeline(topic)
        csv_records.append(record)

    #Save CSV for tracking
    csv_file = Path(__file__).parent / "outputs" / "article_index.csv"
    with open(csv_file, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["topic", "filename", "h1", "meta_description"])
        writer.writeheader()
        writer.writerows(csv_records)

    print(f"CSV index saved to {csv_file}")


# --- CLI interface ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run BarkingPig pipeline")
    parser.add_argument("-t", "--topic", type=str, help="Single topic for the article (in qoutes)")
    parser.add_argument("-f", "--file", type=str, help="Path to a text file with multiple topics, one per line")
    args = parser.parse_args()

    if args.topic:
        run_pipeline(args.topic)
    elif args.file:
        run_batch(args.file)
    else:
        print("Please provide a topic with -t or a file with -f")
