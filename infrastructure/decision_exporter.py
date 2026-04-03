import csv
import json

def export_decisions_to_csv(decisions, output_path):
    """
    Exporta uma lista de Decision para um CSV.
    """

    with open(output_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Header
        writer.writerow([
            "Incident",
            "Priority",
            "Policy Applied",
            "Actions"
        ])

        # Rows
        for decision in decisions:
            writer.writerow([
                decision.incident_number,
                decision.priority,
                decision.policy_applied,
                "; ".join(decision.actions)
            ])

def export_decisions_to_json(decisions, output_path):
    """
    Exporta uma lista de Decision para JSON.
    """

    data = []

    for decision in decisions:
        data.append({
            "incident": decision.incident_number,
            "priority": decision.priority,
            "policy_applied": decision.policy_applied,
            "actions": decision.actions
        })

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)