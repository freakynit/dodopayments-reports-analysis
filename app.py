import yaml
import importlib
from typing import Dict

from utils import run_all_analyses

CONFIG_PATH = "config.yaml"

def load_config(path: str) -> Dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)

def run_report(module_name: str, csv_path: str, title: str, output: str):
    mod = importlib.import_module(f"analyzers.{module_name}")
    # convention: each module exposes Generator class
    gen_class = getattr(mod, "Generator")
    gen = gen_class(csv_path=csv_path, report_title=title)
    report_path = run_all_analyses(gen, output)
    print(f"{module_name} analysis complete. Saved to: {report_path}")

def main():
    cfg = load_config(CONFIG_PATH)
    for key, spec in cfg.get("reports", {}).items():
        run_report(spec["module"], spec["csv"], spec.get("title", key), spec["output"])

if __name__ == "__main__":
    main()
