# Task: Create Script

```yaml
task:
  name: create-script
  display_name: Create Playwright/Stagehand Script
  executor: agent
  elicit: true
  workflow: wf-create-script.yaml

description: |
  Cria um script Playwright/Stagehand completo de forma guiada.
  O usuário descreve o que quer, o squad navega o site e gera o script.

input:
  required:
    - url: "URL do site alvo"
    - objective: "O que o script deve fazer"
  optional:
    - auth: "Credenciais se necessário (via .env)"
    - output_format: "JSON, CSV, file download"
    - recurrence: "one-time ou scheduled"

elicitation:
  format: "numbered_options"
  questions:
    - question: "Qual a URL do site?"
      type: "text"
      validation: "Must be valid URL"

    - question: "O que você quer fazer?"
      type: "choice"
      options:
        1: "Extrair dados (preços, contatos, listings)"
        2: "Preencher formulários"
        3: "Navegar e fazer ações (clicks, downloads)"
        4: "Login + ação dentro de área logada"
        5: "Outro (descreva)"

    - question: "Precisa de login?"
      type: "choice"
      options:
        1: "Não"
        2: "Sim, email + senha"
        3: "Sim, OAuth (Google, GitHub, etc)"
        4: "Sim, outro método"

    - question: "Frequência?"
      type: "choice"
      options:
        1: "Uma vez só"
        2: "Diário"
        3: "Semanal"
        4: "Sob demanda"

output:
  files:
    - "output/scripts/{task-name}.js - Script executável"
    - "output/scripts/{task-name}-output.json - Output de exemplo"
  documentation:
    - "Como rodar: node output/scripts/{task-name}.js"
    - "Flags: --headed, --headless, --model"

completion_criteria:
  - "Script roda sem erros"
  - "Output corresponde à expectativa"
  - "Tem error handling (timeout, element not found)"
  - "É auto-contido (um arquivo, sem deps extras)"
  - "Passou nos testes do script-tester-validator"

veto_conditions:
  - "URL inválida ou inacessível"
  - "Site requer CAPTCHA que não pode ser contornado"
  - "Credenciais necessárias mas não fornecidas"
  - "Objetivo viola termos de serviço do site"
```
