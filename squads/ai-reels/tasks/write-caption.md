# Task: Write Caption

**Agente:** @script-director
**Fase:** 6 (Caption Instagram)
**Gate:** QG-AR-6

## Objetivo

Escrever caption Instagram (texto + hashtags + CTA) alinhada com Voice DNA.

## Input

- `script`: Roteiro original (fase 2)
- `reel_file`: Reel editado (fase 5)
- `topic`: Tema do reel
- `cta_goal`: Objetivo do CTA

## Processo

1. Assistir o reel editado para contexto visual
2. Escrever caption em tom Voice DNA (guardrail: voice-dna.md)
3. Incluir CTA específico (não genérico)
4. Selecionar hashtags nichadas (não genéricas)
5. Validar contra guardrail AI writing

## Estrutura da Caption

```
[Abertura — gancho textual alinhado com o hook do reel]

[Corpo — 2-4 linhas expandindo o insight]

[CTA — chamada específica para ação]

[Hashtags — 5-10 nichadas]
```

## Output

```yaml
caption:
  text: "..."
  cta: "..."
  hashtags: ["#tag1", "#tag2", "..."]
  voice_dna_score: X/10
  ai_guardrail_score: X/10
```

## Quality Gate QG-AR-6

| Critério | Obrigatório |
|----------|-------------|
| Voice DNA pass (score >= 8/10) | SIM |
| CTA específico (não genérico) | SIM |
| Guardrail AI writing 10/10 | SIM |
| Hashtags nichadas (não #reels #viral) | SIM |
| Tom consistente com o reel | SIM |

## Veto Conditions

- Caption sem CTA → **BLOQUEAR** (adicionar CTA)
- Tom não alinhado com Voice DNA → **REESCREVER** consultando voice-dna.md
- Hashtags genéricas (#reels, #viral, #fyp) → **SUBSTITUIR** por nichadas
- Score guardrail AI < 10/10 → **REESCREVER** até passar
- Caption > 2200 caracteres (limite Instagram) → **CORTAR**
