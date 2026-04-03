import csv
from datetime import datetime

from domain.incident import Incident
from domain.sla import SLA


def load_servicenow_csv(csv_path: str):
    incidents = []
    slas = {}

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            incident = Incident(
                number=row["Number"],
                short_description=row["Short description"],
                assignment_group=row["Assignment group"],
                impact=int(row["Impact"]),
                urgency=int(row["Urgency"]),
                opened_at=datetime.now()
            )

            sla = SLA(
                name="Resolution SLA",
                percentage=int(row["Task SLA.Percentage"]),
                paused=row["Task SLA.Paused"].lower() == "true"
            )

            incidents.append(incident)
            slas[incident.number] = sla

    return incidents, slas
