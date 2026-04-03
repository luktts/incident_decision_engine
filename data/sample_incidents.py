from datetime import datetime
from domain.incident import Incident
from domain.sla import SLA


INCIDENTS = [
    Incident(
        number="INC0012345",
        short_description="VPN indisponível para usuários remotos",
        assignment_group="NOC Brasil",
        impact=1,
        urgency=2,
        opened_at=datetime(2026, 4, 1, 10, 30)
    ),
    Incident(
        number="INC0012346",
        short_description="Erro intermitente em aplicação interna",
        assignment_group="App Support",
        impact=2,
        urgency=3,
        opened_at=datetime(2026, 4, 2, 9, 10)
    ),
]

SLAS = {
    "INC0012345": SLA(
        name="Resolution SLA",
        percentage=78,
        paused=False
    ),
    "INC0012346": SLA(
        name="Resolution SLA",
        percentage=55,
        paused=False
    )
}
