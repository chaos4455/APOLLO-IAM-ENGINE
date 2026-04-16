from datetime import datetime
import json, yaml, os


def _log_dir(fmt: str) -> str:
    d = os.path.join("logs", fmt)
    os.makedirs(d, exist_ok=True)
    return d


def append_json_log(entry: dict):
    path = os.path.join(_log_dir("json"), "apollo_iam.json")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")


def append_yaml_log(entry: dict):
    path = os.path.join(_log_dir("yaml"), "apollo_iam.yaml")
    with open(path, "a", encoding="utf-8") as f:
        yaml.dump([entry], f, allow_unicode=True, default_flow_style=False)


def append_md_log(entry: dict):
    path = os.path.join(_log_dir("md"), "apollo_iam.md")
    ts = entry.get("timestamp", datetime.utcnow().isoformat())
    level = entry.get("level", "INFO")
    msg = entry.get("message", "")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"| {ts} | {level} | {msg} |\n")
