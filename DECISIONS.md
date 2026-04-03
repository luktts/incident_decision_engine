# DECISIONS.md

Este documento registra as **principais decisões arquiteturais e técnicas** tomadas durante o desenvolvimento do projeto **Incident Decision Engine**.

O objetivo é deixar explícito **o raciocínio de engenharia** por trás do sistema, explicando não apenas *o que* foi feito, mas principalmente *por que* foi feito dessa maneira.

---

## Decisão 001 — Uso de CSV como origem dos dados

### Contexto
O projeto simula execução em ambiente corporativo, com restrições quanto ao uso de bibliotecas externas, credenciais e integrações diretas com sistemas produtivos.

Optou-se por usar **dados genéricos e simulados**, preservando segurança da informação.

### Decisão
Utilizar **arquivos CSV exportados manualmente** como principal fonte de dados de entrada. Visto que esse é o processo mais comum de exportação no ServiceNow quando não se pode usar bibliotecas adicionais.

### Consequências
- ✅ Nenhuma dependência externa
- ✅ Maior segurança e controle dos dados
- ✅ Fácil simulação de cenários
- ❌ Dependência de exportação manual

---

## Decisão 002 — Não recalcular SLA

### Contexto
O cálculo de SLA no ServiceNow envolve lógica complexa (pausas, contratos, exceções).

Reimplementar essa lógica aumentaria complexidade e risco.

### Decisão
Tratar o valor de SLA presente no CSV como **fonte de verdade**, não recalculando SLA internamente.

### Consequências
- ✅ Simplicidade e confiabilidade
- ✅ Alinhamento com o sistema oficial
- ❌ Dependência da correta extração dos dados

---

## Decisão 003 — Separação entre Incident e SLA no domínio

### Contexto
No ServiceNow, incidentes e SLAs residem em tabelas diferentes.

### Decisão
Modelar **Incident** e **SLA** como entidades separadas no domínio.

### Consequências
- ✅ Domínio fiel ao mundo real
- ✅ Core independente de formato de origem

---

## Decisão 004 — Motor de decisão genérico

### Contexto
Era necessário um mecanismo de decisão reutilizável, testável e explicável.

### Decisão
Implementar um **DecisionEngine** que apenas aplica políticas ordenadas sobre objetos de domínio.

### Consequências
- ✅ Engine pequeno e estável
- ✅ Regras desacopladas do código

---

## Decisão 005 — Políticas externas em JSON

### Contexto
Regras operacionais mudam com frequência e precisam ser auditáveis.

### Decisão
Externalizar políticas em arquivos **JSON**.

### Consequências
- ✅ Versionamento e clareza
- ✅ Alterações sem mexer no core

---

## Decisão 006 — Loaders como boundary de infraestrutura

### Contexto
Dados podem vir de formatos distintos (CSV genérico, CSV ServiceNow-like).

### Decisão
Criar **loaders específicos** na camada de infraestrutura e um router para seleção automática.

### Consequências
- ✅ Core protegido
- ✅ Evolução simples

---

## Decisão 007 — UI apenas como orquestração

### Contexto
Misturar regra de negócio com UI comprometeria a arquitetura.

### Decisão
Manter a UI responsável apenas por:
- seleção de arquivos
- chamada dos loaders
- execução do engine
- apresentação dos resultados

### Consequências
- ✅ Código limpo
- ✅ Fácil substituição da interface

---

## Conclusão

O arquivo **DECISIONS.md** faz parte intencional do projeto e **deve ser mantido**.