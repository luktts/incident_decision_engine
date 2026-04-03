import csv
from datetime import datetime

from domain.incident import Incident
from domain.sla import SLA


def load_incidents_from_csv(csv_path: str):
    incidents = []
    slas = {}

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            incident = Incident(
                number=row["number"],
                short_description=row["short_description"],
                assignment_group=row["assignment_group"],
                impact=int(row["impact"]),
                urgency=int(row["urgency"]),
                opened_at=datetime.now()  # simulando
            )

            sla = SLA(
                name="Resolution SLA",
                percentage=int(row["sla_percentage"]),
                paused=row["sla_paused"].lower() == "true"
            )

            incidents.append(incident)
            slas[incident.number] = sla

    return incidents, slas