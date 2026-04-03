import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

from infrastructure.csv_router import load_incidents
from infrastructure.decision_exporter import (
    export_decisions_to_csv,
    export_decisions_to_json
)
from engine.decision_engine import DecisionEngine
from engine.policy_loader import load_policies


class IncidentDecisionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Incident Decision Engine")

        self.csv_path = None
        self.decisions = []

        # Inicializa engine e políticas (uma única vez)
        self.policies = load_policies("policies/policies.json")
        self.engine = DecisionEngine(self.policies)

        self.build_ui()

    # ==================================================
    # UI BUILD
    # ==================================================
    def build_ui(self):
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)

        # Ações principais
        tk.Button(main_frame, text="Selecionar CSV", command=self.select_csv)\
          .pack(fill="x", pady=4)

        tk.Button(main_frame, text="Processar Incidentes", command=self.process_incidents)\
          .pack(fill="x", pady=4)

        tk.Button(main_frame, text="Exportar Decisões (CSV)", command=self.export_decisions_csv)\
          .pack(fill="x", pady=4)

        tk.Button(main_frame, text="Exportar Decisões (JSON)", command=self.export_decisions_json)\
          .pack(fill="x", pady=4)

        # --------------------------------------------------
        # Filtros
        # --------------------------------------------------
        filter_frame = tk.Frame(main_frame)
        filter_frame.pack(fill="x", pady=8)

        tk.Label(filter_frame, text="Filtrar prioridade:").pack(side="left")

        self.priority_filter = ttk.Combobox(
            filter_frame,
            values=["Todos", "high", "normal", "low"],
            state="readonly",
            width=10
        )
        self.priority_filter.set("Todos")
        self.priority_filter.pack(side="left", padx=5)

        tk.Label(filter_frame, text="Filtrar equipe:").pack(side="left", padx=(10, 0))

        self.group_filter = ttk.Combobox(
            filter_frame,
            values=["Todos"],
            state="readonly",
            width=20
        )
        self.group_filter.set("Todos")
        self.group_filter.pack(side="left", padx=5)

        tk.Label(filter_frame, text="Filtrar policy:").pack(side="left", padx=(10, 0))

        self.policy_filter = ttk.Combobox(
            filter_frame,
            values=["Todos"],
            state="readonly",
            width=30
        )
        self.policy_filter.set("Todos")
        self.policy_filter.pack(side="left", padx=5)

        tk.Button(filter_frame, text="Aplicar Filtro", command=self.apply_filters)\
          .pack(side="left", padx=10)

        # --------------------------------------------------
        # Tabela com Scrollbar
        # --------------------------------------------------
        table_frame = tk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True, pady=10)

        columns = ("incident", "priority", "group", "policy", "actions")

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.tree.heading("incident", text="Incident")
        self.tree.heading("priority", text="Priority")
        self.tree.heading("group", text="Equipe")
        self.tree.heading("policy", text="Policy")
        self.tree.heading("actions", text="Actions")

        self.tree.column("incident", width=120)
        self.tree.column("priority", width=80)
        self.tree.column("group", width=160)
        self.tree.column("policy", width=220)
        self.tree.column("actions", width=420)

        v_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        h_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

    # ==================================================
    # CALLBACKS
    # ==================================================
    def select_csv(self):
        self.csv_path = filedialog.askopenfilename(
            title="Selecione o CSV",
            filetypes=[("CSV Files", "*.csv")]
        )

        if self.csv_path:
            messagebox.showinfo("Arquivo selecionado", self.csv_path)

    def process_incidents(self):
        if not self.csv_path:
            messagebox.showwarning("Aviso", "Selecione um CSV primeiro.")
            return

        self.decisions = []
        self.clear_table()

        try:
            incidents, slas = load_incidents(self.csv_path)
        except Exception as e:
            messagebox.showerror("Erro ao processar CSV", str(e))
            return

        for incident in incidents:
            sla = slas.get(incident.number)
            decision = self.engine.evaluate(incident, sla)
            self.decisions.append(decision)

        self.update_filters()
        self.render_table(self.decisions)

    # ==================================================
    # FILTROS
    # ==================================================
    def update_filters(self):
        policies = sorted({d.policy_applied for d in self.decisions})
        groups = sorted({d.assignment_group for d in self.decisions})

        self.policy_filter["values"] = ["Todos"] + policies
        self.group_filter["values"] = ["Todos"] + groups

        self.policy_filter.set("Todos")
        self.group_filter.set("Todos")

    def apply_filters(self):
        priority = self.priority_filter.get()
        policy = self.policy_filter.get()
        group = self.group_filter.get()

        filtered = []

        for d in self.decisions:
            if priority != "Todos" and d.priority != priority:
                continue
            if policy != "Todos" and d.policy_applied != policy:
                continue
            if group != "Todos" and d.assignment_group != group:
                continue
            filtered.append(d)

        self.render_table(filtered)

    # ==================================================
    # TABELA
    # ==================================================
    def clear_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def render_table(self, decisions):
        self.clear_table()
        for d in decisions:
            self.tree.insert(
                "",
                "end",
                values=(
                    d.incident_number,
                    d.priority,
                    d.assignment_group,
                    d.policy_applied,
                    "; ".join(d.actions)
                )
            )

    # ==================================================
    # EXPORTAÇÃO
    # ==================================================
    def export_decisions_csv(self):
        if not self.decisions:
            messagebox.showwarning("Aviso", "Nada para exportar.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )

        if path:
            export_decisions_to_csv(self.decisions, path)
            messagebox.showinfo("Sucesso", "CSV exportado com sucesso.")

    def export_decisions_json(self):
        if not self.decisions:
            messagebox.showwarning("Aviso", "Nada para exportar.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")]
        )

        if path:
            export_decisions_to_json(self.decisions, path)
            messagebox.showinfo("Sucesso", "JSON exportado com sucesso.")