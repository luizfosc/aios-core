---
id: quick-consult
title: Consulta Rápida
description: Sessão de 15 minutos para orientação inicial com um especialista.
estimated_duration: 15 min
entry_agent: lead-therapist
veto_conditions:
  - "NUNCA acionar mais de um especialista — esta é uma consulta rápida"
  - "NUNCA se aprofundar além do escopo de 15 minutos sem checkpoint de transição"
---

# Workflow: Consulta Rápida (15 min)

Fluxo para atendimentos de orientação inicial. Objetivo: 1 insight claro + 1 exercício prático. Sem aprofundamento clínico.

---

## Etapa 1 — Triagem com Sofia

**Agente:** `lead-therapist` (Sofia)

Sofia recebe o usuário com acolhimento e realiza triagem rápida:

1. Qual é o tema central que trouxe o usuário hoje?
2. Há urgência ou situação de crise envolvida?
3. O usuário quer falar sobre si mesmo, sobre o casal ou sobre a relação familiar?

Sofia seleciona **1 único especialista** com base na triagem. Critérios de seleção:

| Tema Principal | Especialista |
|----------------|-------------|
| Apego, medo de abandono, dependência emocional | Dr. John (Attachment) |
| Crise aguda, ansiedade intensa, corpo ativado | Deb Dana (Somatic) |
| Ciclos de briga com o parceiro, distância emocional | Sue Johnson (EFT) |
| Padrões de conflito recorrentes no casal | Dr. Gottman |
| Feridas de infância projetadas no parceiro | Harville (Imago) |
| Pensamentos negativos, crenças limitantes | Aaron (TCC) |
| Narrativa de sofrimento, história do relacionamento | Michael (Narrative) |
| Trauma passado afetando o presente | Bessel (Trauma) |
| Dinâmica familiar, padrões intergeracionais | Virginia (Family Systems) |
| Intimidade, desejo, sexualidade | Dr. Emily (Sexologist) |

---

## Etapa 2 — Atendimento com o Especialista

**Agente:** especialista selecionado na Etapa 1

O especialista entra com seu Voice DNA e oferece:

1. **1 perspectiva terapêutica** baseada no framework do especialista
   - Usar linguagem do framework (ex: Gottman usa "Quatro Cavaleiros", EFT usa "ciclo de interação")
   - Não usar linguagem genérica ou de autoajuda

2. **1 exercício prático** concreto e aplicável hoje
   - Exercício deve ter: duração estimada, instruções claras, o que observar

O especialista encerra e devolve para Sofia.

---

## Etapa 3 — Fechamento com Sofia

**Agente:** `lead-therapist` (Sofia)

Sofia:
1. Resume em 2-3 linhas o que foi explorado
2. Reforça o exercício prático sugerido
3. Lembra que o squad não substitui atendimento profissional presencial

---

## Checkpoint — Aprofundamento

> **Sofia pergunta ao usuário:**
>
> "Essa consulta rápida trouxe alguns pontos importantes. Você quer aprofundar com uma sessão completa? Podemos explorar o tema com mais cuidado e trazer mais de um especialista para a conversa."

- Usuário diz **sim** → iniciar workflow `full-session`
- Usuário diz **não** → encerrar com agradecimento e recomendação de terapeuta presencial
