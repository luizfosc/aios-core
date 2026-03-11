# Story M2 — Pipeline Core (Ensinio Prospector App)

**Epic:** Ensinio Prospector App
**PRD:** `docs/projects/ensinio-prospector-app/PRD.md` v0.2
**Status:** Done
**Criada:** 2026-03-11

---

## Objetivo

Scoring engine + dashboard com scores + preview de mensagens + Evolution API + QR code login. Ao final, o usuário vê prospects scorados, lê mensagens de outreach e conecta WhatsApp para envio.

## Acceptance Criteria

- [x] AC1: Scoring engine em TypeScript (dual axis: client x partner, 7 classificações)
- [x] AC2: Dashboard de prospects com score, classificação, temperatura e cores
- [x] AC3: Preview de mensagem de outreach ao clicar no prospect
- [x] AC4: Evolution API configurada via Docker (docker-compose.yml)
- [x] AC5: QR code login funcional — componente com QR, polling de status
- [x] AC6: Sessão WhatsApp com status (conectado/desconectado/erro)
- [x] AC7: `npm run lint`, `npm run typecheck`, `npm run build` passam sem erros

## Escopo Técnico

### 1. Scoring Engine
- Port da lógica do squad (prospect-analyst "Minerva")
- Dual scoring: client (0-10) + partner (0-10)
- 7 classificações: EMBAIXADOR, INDICADOR, PURO, ESTRATÉGICO, TÁTICO, AFILIADO, CANAL
- Temperatura: HOT (7-10), WARM (4-6), COLD (0-3)
- ICP Ensinio + red flags + bloqueadores

### 2. Dashboard com Scores
- Tabela expandida: nome, telefone, client score, partner score, classificação, temperatura
- Cores por temperatura (HOT=vermelho, WARM=laranja, COLD=azul)
- Ordenação por score dominante DESC
- Contadores por classificação

### 3. Preview de Mensagens
- Clicar no prospect abre painel lateral com mensagem gerada
- Campo de edição livre
- Botão copiar mensagem

### 4. Evolution API (Docker)
- docker-compose.yml
- Health check endpoint
- .env config

### 5. QR Code Login
- /api/whatsapp/connect → Evolution API
- Tela com QR code + status
- Polling (conectando → conectado)

## Fora do Escopo (M2)
- Envio efetivo de mensagens (M3)
- Sync GHL (M3)
- Bulk send (P1)

## File List
| Arquivo | Status |
|---------|--------|
| src/lib/scoring-engine.ts | done |
| src/lib/services/evolution-api.ts | done |
| src/components/scoring-summary.tsx | done |
| src/components/message-preview.tsx | done |
| src/components/whatsapp-connect.tsx | done |
| src/components/prospects-table.tsx | updated |
| src/components/upload-zone.tsx | updated |
| src/stores/prospects-store.ts | updated |
| src/app/page.tsx | updated |
| src/app/api/whatsapp/connect/route.ts | done |
| src/app/api/whatsapp/status/route.ts | done |
| docker-compose.yml | done |
