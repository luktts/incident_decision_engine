import csv

from infrastructure.csv_loader import load_incidents_from_csv
from infrastructure.servicenow_csv_loader import load_servicenow_csv


def load_incidents(csv_path: str):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []

    if "Task SLA.Percentage" in headers:
        return load_servicenow_csv(csv_path)

    return load_incidents_from_csv(csv_path)