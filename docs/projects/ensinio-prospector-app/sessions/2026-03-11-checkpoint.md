# Session 2026-03-11

## Projeto
- **Nome:** Ensinio Prospector App
- **INDEX.md:** `docs/projects/ensinio-prospector-app/INDEX.md`

## O que foi feito

### PRD + Decisões
- PRD v0.2 atualizado: fluxo ZIP upload (não API), WhatsApp só para envio
- Tag GHL definida: "Leads Fosc"
- 12 decisões tomadas (D1-D12), 0 em aberto

### M1 — Fundação (8/8 ACs Done)
- Next.js 15 + Tailwind + shadcn/ui + Zustand + Supabase client
- Schema Supabase: 7 tabelas + seed "Leads Fosc" (migration SQL)
- Chat parser WhatsApp (3 formatos: android_br, ios_br, android_en)
- ZIP extractor + upload zone (drag & drop)
- Dashboard de prospects + multi-grupo

### M2 — Pipeline Core (7/7 ACs Done)
- Scoring engine TypeScript (dual axis: client x partner, 7 classificações, 3 temperaturas)
- Dashboard com scores, badges coloridos, temperatura
- Message preview com edição, cópia e link WhatsApp direto
- Evolution API service layer + docker-compose.yml
- WhatsApp connect (QR code + polling de status)
- API routes: /api/whatsapp/connect e /api/whatsapp/status

### VK Talks — Dados Processados
- 80 membros, 50 telefones resolvidos via screenshots
- 28 prospects scorados (dual axis)
- 28 mensagens de outreach personalizadas
- Top 3: Victória Rammé (9/8), Luanna Pace (8/7), Valeria Santos (8/7)

## Agente/Squad em uso
@dev (implementação) + scoring manual via Claude Code

## Arquivos para contexto (próximo Claude DEVE ler)
- `docs/projects/ensinio-prospector-app/INDEX.md`
- `docs/projects/ensinio-prospector-app/PRD.md`
- `docs/stories/active/story-m2-pipeline-core.md`
- `squads/ensinio-whatsapp-prospector/data/outputs/vk-talks/scoring-results.md`
- `squads/ensinio-whatsapp-prospector/data/outputs/vk-talks/outreach-messages.md`

## Decisões tomadas
- D1-D7: Stack, WhatsApp, GHL, deploy, AI, auth (sessão anterior)
- D8: Tag GHL = "Leads Fosc"
- D9: Extração via ZIP (não via Evolution API) — WhatsApp Web só para envio
- D10: Enriquecimento de telefones via Claude Code (screenshots → OCR manual)
- D11: Dashboard separado por grupo (cada ZIP = grupo distinto)
- D12: Evolution API movida de M1 para M3

## Commits no app (~/CODE/Projects/ensinio-prospector-app/)
- `a09192f` feat: add ZIP upload, chat parser, prospects dashboard and Supabase schema [M1]
- `9ac8a7e` feat: add multi-group support with group selector [M1]
- `86e9c8a` feat: add scoring engine, message preview, WhatsApp connect and Evolution API [M2]

## Próximo passo exato
M3: Envio direto via Evolution API + integração GHL
1. Subir Evolution API Docker local (`docker compose up -d`)
2. Testar QR code real no app (`npm run dev` → conectar WhatsApp)
3. Implementar envio efetivo via API route /api/whatsapp/send
4. Integrar GHL: criar contato pós-envio com tag "Leads Fosc"
5. Tracking de status (draft → sent → synced)

## Arquivos modificados não commitados
- `docs/projects/ensinio-prospector-app/INDEX.md` (atualizado neste checkpoint)
- `docs/projects/ACTIVE.md` (atualizado)
- `.aios/session.json` (auto)
