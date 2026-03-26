# Task: Create Hook

**Agente:** @hook-architect
**Fase:** 1 (Hook)
**Gate:** QG-AR-1

## Objetivo

Criar hook magnético para os primeiros 3 segundos do reel usando uma das 7 fórmulas comprovadas.

## Input

- `topic`: Tema/assunto do reel
- `pain_point` (opcional): Dor específica do público
- `cta_goal` (opcional): Objetivo do CTA

## Processo

1. Analisar o tema e identificar o trigger psicológico mais forte
2. Gerar 5 variações usando fórmulas diferentes (7Fs, Hormozi, Kane)
3. Pontuar cada hook (curiosity gap + viabilidade visual + trigger strength)
4. Selecionar o melhor e justificar

## Output

```yaml
selected_hook: "..."
formula_used: "..."
trigger_type: "..."
retention_strategy: "..."
score: X/10
alternatives:
  - hook: "..."
    score: X/10
```

## Quality Gate QG-AR-1

| Critério | Obrigatório |
|----------|-------------|
| Score >= 8/10 | SIM |
| Curiosity gap presente | SIM |
| Fórmula comprovada identificável | SIM |
| Dados verificados (se usar números) | SIM |
| Viável em vídeo (não apenas texto) | SIM |

## Veto Conditions

- Hook sem fórmula comprovada → **VETO** (regenerar com fórmula explícita)
- Dados não verificáveis no hook → **VETO** (remover dado ou verificar fonte)
- Hook que só funciona em texto (não visual) → **VETO** (reformular para vídeo)
- Nenhuma das 5 variações com score >= 8/10 → **ESCALAR** para Chief
