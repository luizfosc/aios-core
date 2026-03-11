# Story M1 — Fundação (Ensinio Prospector App)

**Epic:** Ensinio Prospector App
**PRD:** `docs/projects/ensinio-prospector-app/PRD.md` v0.2
**Status:** In Progress
**Criada:** 2026-03-11

---

## Objetivo

Setup completo do projeto + upload de chat ZIP + parse de mensagens. Ao final, o usuário faz upload de um ZIP exportado do WhatsApp e vê a lista de prospects extraídos.

## Acceptance Criteria

- [x] AC1: Projeto Next.js 15 (App Router) + Tailwind + shadcn/ui + Zustand criado em `~/CODE/Projects/ensinio-prospector-app/`
- [x] AC2: Schema Supabase criado (migration SQL) com 7 tabelas
- [x] AC3: Upload de arquivo ZIP funcional (drag & drop + botão)
- [x] AC4: Parser de chat WhatsApp — extrai mensagens, participantes, telefones do ZIP
- [x] AC5: Enriquecimento de telefones via Claude Code (upload de imagens ao agente)
- [x] AC6: Dashboard básico — lista prospects com nome, telefone, total de mensagens
- [x] AC7: `npm run lint`, `npm run typecheck`, `npm run build` passam sem erros
- [x] AC8: Tag GHL configurada como "Leads Fosc" na tabela `settings` (seed)

## Fluxo Correto (atualizado)

```
Upload ZIP → Parse mensagens → Enriquecimento de telefones (imagens) → Dashboard
                                                                           ↓
                                                              (M2: Scoring + Outreach)
                                                                           ↓
                                                              (M3: WhatsApp login + Envio + GHL)
```

**WhatsApp Web (Evolution API) = só para ENVIO (M3), não para extração.**

## Escopo Técnico

### 1. Setup do Projeto (DONE)
- Next.js 15 com App Router, TypeScript, Tailwind
- shadcn/ui, Zustand, @supabase/supabase-js
- Path alias `@/` configurado
- Estrutura de pastas:
  ```
  src/
  ├── app/           # Pages (App Router)
  ├── components/    # UI components
  ├── lib/           # Services, utils
  ├── stores/        # Zustand stores
  └── types/         # TypeScript types
  ```

### 2. Supabase Schema
- Criar tabelas conforme PRD seção 5.5
- RLS policies básicas (MVP interno — permissivo)
- Seed: settings com valores default (tag "Leads Fosc")

### 3. Upload ZIP + Parse
- Tela de upload (drag & drop) para arquivo ZIP
- Parser: extrai _chat.txt do ZIP
- Regex para extrair: data, hora, remetente, mensagem, telefone (quando disponível)
- Salvar contatos e mensagens no Supabase

### 4. Enriquecimento de Telefones
- Área para upload de imagens/screenshots de grupos do WhatsApp
- Extrair números de telefone das imagens (OCR ou manual)
- Matching nome ↔ telefone e persistir no Supabase

### 5. Dashboard Básico
- Lista de prospects: nome, telefone, mensagens
- Indicador de telefone (tem / não tem)

## Fora do Escopo (M1)
- Scoring (M2)
- Geração de outreach (M2)
- Evolution API / QR code login (M3)
- Envio de mensagens (M3)
- Integração GHL (M3)

## File List
<!-- Manter atualizada conforme implementação -->
| Arquivo | Status |
|---------|--------|
| package.json | done |
| tsconfig.json | done |
| .env.local.example | done |
| src/app/page.tsx | done |
| src/lib/utils.ts | done |
| src/lib/supabase.ts | done |
| src/lib/chat-parser.ts | done |
| src/lib/zip-extractor.ts | done |
| src/types/database.ts | done |
| src/stores/prospects-store.ts | done |
| src/components/ui/button.tsx | done |
| src/components/upload-zone.tsx | done |
| src/components/prospects-table.tsx | done |
| supabase/migrations/001_initial_schema.sql | done |

## Dependências
- Node.js 20+
- Conta Supabase (free tier)

## Notas
- Auth: config local (MVP interno, D7 do PRD)
- Tag GHL "Leads Fosc" (D8 do PRD)
- ZIP não contém todos os telefones → enriquecimento via imagens
- Evolution API movida para M3 (não necessária em M1)
