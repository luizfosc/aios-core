---
name: design-system-forge
description: Orchestrates design system extraction, elevation, and build from any website
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Agent]
version: "1.0.0"
category: design
requires: aios
quest-pack: design-system-forge
---

# Design System Forge

Skill orquestradora do Quest Pack "Design System Forge". Transforma qualquer site em um design system premium com componentes prontos.

**Filosofia:** Extraia o DNA. Eleve o design. Entregue arte.

## Como Funciona

Esta skill NÃO duplica ferramentas existentes. Ela orquestra:

| Ferramenta | Onde vive | O que faz |
|---|---|---|
| `dissect-artifact.cjs` | `squads/design/scripts/` | Motor Playwright: extrai CSS computado, keyframes, media queries, componentes |
| `design-system-extractor` | `skills/design-system-extractor/` | Geração de token templates TypeScript |
| `smart-browser-playwright` | `tools/smart-browser-playwright/` | Automação de browser para scraping |
| `/design` squad | `squads/design/` | Brad Frost (tokens), Dan Mall (elevação), Dave Malouf (a11y) |
| `dembrandt` | CLI global (npm) | Extração rápida de tokens (DTCG JSON) |

## Scripts CLI (lib/)

Cada script preenche um gap específico. Todos são CLI-first, zero dependências extras.

### Extração (World 1)

```bash
# Wrapper do dissect-artifact.cjs — redireciona output pra design-system/
node ~/aios-core/skills/design-system-forge/lib/dissect.mjs <url> --name <name> [--mobile] [--split-animations]

# Simula :hover, :focus, :active e captura diffs de computed style
node ~/aios-core/skills/design-system-forge/lib/extract-states.mjs <url> --name <name>

# Toggle prefers-color-scheme: dark e re-extrai cores/custom properties
node ~/aios-core/skills/design-system-forge/lib/extract-dark-mode.mjs <url> --name <name>
```

### Referências (World 2)

```bash
# Scraping de referências premium com recipes pré-built
node ~/aios-core/skills/design-system-forge/lib/scrape-references.mjs --source awwwards
node ~/aios-core/skills/design-system-forge/lib/scrape-references.mjs --source 21st
node ~/aios-core/skills/design-system-forge/lib/scrape-references.mjs --source <name> --url <url>
```

### Tokens (World 3)

```bash
# Merge dembrandt + dissect outputs, deduplica cores, separa light/dark
node ~/aios-core/skills/design-system-forge/lib/consolidate-tokens.mjs \
  --dembrandt ./dembrandt-output.json \
  --dissect ./design-system/tokens.yaml \
  [--dark ./design-system/tokens/dark-tokens.yaml]

# Gera tailwind.config.forge.ts + tokens.css
node ~/aios-core/skills/design-system-forge/lib/generate-tailwind.mjs \
  --input ./design-system/tokens/consolidated.yaml \
  [--css-only] [--animations]
```

### QA (World 5)

```bash
# Compara screenshots original vs redesign, calcula % diferença
node ~/aios-core/skills/design-system-forge/lib/visual-diff.mjs \
  --original ./design-system/screenshots/original.png \
  --redesign ./screenshots/redesign.png
```

## Command Map

Cada quest item tem um comando CLI mapeado em `resources/command-map.yaml`. Agentes DEVEM consultar esse arquivo para saber exatamente o que executar em cada missão.

## Fluxo de Agentes

| World | Agentes | Squads |
|---|---|---|
| 0 - Laboratório | @dev, @devops, user | — |
| 1 - Espião | @dev, @ux | — |
| 2 - Biblioteca | @analyst, @dev, @ux | — |
| 3 - Alquimista | @architect, @dev | /design (Brad Frost) |
| 4 - Forja | @dev, @ux | /design (Dave Malouf) |
| 5 - Arena | @dev, @qa | /design (Dan Mall, Dave Malouf) |
| 6 - Deploy | @dev, @devops, @qa | — |
| 7 - Evolução | @dev, @devops, @ux, @qa | — |

## Output Esperado

Após completar a quest, o projeto terá:

```
{projeto}/
├── design-system/
│   ├── tokens/
│   │   ├── consolidated.yaml      # Tokens unificados (light + dark)
│   │   ├── dark-tokens.yaml       # Tokens dark mode
│   │   └── primitives/semantic/   # Hierarquia Brad Frost
│   ├── patterns/
│   │   ├── hero-sections/         # Patterns por categoria
│   │   ├── animations/
│   │   ├── micro-interactions/
│   │   └── INDEX.md               # Índice navegável
│   ├── anti-patterns/             # O que NÃO fazer
│   ├── screenshots/
│   │   ├── screenshot-desktop.png # Original capturado
│   │   ├── screenshot-mobile.png
│   │   └── comparison.png         # Visual diff
│   ├── states/
│   │   └── interactions.json      # Hover/focus/active diffs
│   ├── components/
│   │   └── component-catalog.md   # Catálogo visual
│   ├── references/
│   │   ├── awwwards.json          # Referências scrapadas
│   │   └── 21st.json
│   ├── extracted-css.json         # CSS completo extraído
│   ├── dom-tree.json              # DOM com computed styles
│   ├── animations.json            # Keyframes separados
│   ├── effects.json               # Transitions/transforms
│   ├── DECISIONS.md               # Decisões de design
│   ├── README.md                  # Guia de uso
│   └── INDEX.md                   # Índice geral
├── tailwind.config.forge.ts       # Config gerado
├── tokens.css                     # CSS custom properties
└── src/components/                # Componentes React/Shadcn
    ├── atoms/
    ├── molecules/
    └── organisms/
```
