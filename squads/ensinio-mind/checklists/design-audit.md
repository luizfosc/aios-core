# Checklist: Auditoria Visual da Plataforma (7 Dicas do Gui)

> As 7 dicas de design do Gui Ávila para sua plataforma ficar "lindona".
> Use para: auditar plataforma de cliente, CS revisar antes de go-live, ou cliente conferir sozinho.
> Fonte: Vídeo "Plataforma e App para Infoprodutores" — Gui Ávila (2026-03-14), parte 10.

---

## Dica 1: Logomarca e Favicon

- [ ] Logo para **modo escuro** enviada (Admin Console → Configurações → Aparência)
- [ ] Logo para **modo claro** enviada (se modo claro estiver ativo)
- [ ] **Isotipo** (símbolo da marca) enviado — vira favicon no navegador
- [ ] Favicon configurado para puxar do isotipo (recomendado) ou upload personalizado
- [ ] Modo de cor padrão definido: **escuro** (recomendado — "mais sofisticado, dá ideia de Netflix/streaming")

**Teste:** Abrir a plataforma no navegador → ícone da aba mostra o isotipo, não o ícone genérico.

---

## Dica 2: Vídeo de Background na Billboard

- [ ] Pelo menos 1 grupo em destaque tem **vídeo de fundo** configurado
- [ ] Vídeo é curto (poucos segundos) e faz transição suave para imagem estática
- [ ] Imagem de fallback configurada (aparece após o vídeo terminar)
- [ ] Vídeo enviado via Ensinio Stream ou YouTube

**Onde configurar:** Grupo → Configurações → Página Principal → Vídeo de destaque

**Teste:** Entrar na Billboard → vídeo toca automaticamente → transiciona para imagem. Se não tem vídeo, pelo menos tem imagem de fundo (não a cor padrão).

---

## Dica 3: Estampa em Todos os Grupos

- [ ] **Todo grupo** tem estampa configurada (600x240px)
- [ ] Nenhum grupo mostra título em texto puro na interface (sinal de estampa faltando)
- [ ] Estampa aparece na aba de aulas dentro do grupo
- [ ] Estampa aparece na Billboard nos destaques

**Sem estampa = puxa título em texto = fica feio.** Essa é a diferença mais impactante entre plataforma amadora e profissional.

**Onde configurar:** Grupo → Configurações → Identidade Visual → Estampa

**Teste:** Entrar no grupo → aba aulas → em vez de "Grupo Teste" em texto, aparece a logomarca visual do produto.

---

## Dica 4: Sessões e Trilhas na Billboard

- [ ] Billboard tem pelo menos **2 sessões** além dos destaques
- [ ] Cada sessão tem título e subtítulo descritivos
- [ ] Mix de orientações: pelo menos 1 sessão com **capas verticais** e 1 com **capas horizontais**
- [ ] Sessões reordenadas por prioridade (conteúdo principal primeiro)
- [ ] (Planos pagos) Pelo menos 1 trilha como sessão na Billboard

**Tipos de sessão disponíveis:** Grupos (manual), Grupos em alta (automático), Módulos, Aulas mais assistidas, Trilhas.

**Teste:** Navegar a Billboard de cima a baixo → variedade visual, não tudo igual.

---

## Dica 5: Layout de Aulas Dentro do Grupo

- [ ] Layout escolhido de acordo com volume de conteúdo:
  - **Imersivo** (padrão) → para poucos módulos/aulas (mostra tudo aberto)
  - **Seriado** → para muitas aulas (mostra módulos primeiro, clica para abrir)
  - **Sequencial** → para cursos extensos (lista vertical)
- [ ] Se layout seriado: cada módulo tem **capa própria** (se não tem, puxa a do grupo)
- [ ] Capa imersiva configurada (background da aba de aulas — versão da arte SEM textos)

**Erro comum:** Usar layout imersivo com 50+ aulas → aluno toma susto com a quantidade.

**Onde configurar:** Grupo → Conteúdos → Pré-definições de Conteúdos

**Teste:** Entrar no grupo como aluno → a primeira impressão é organizada, não assustadora.

---

## Dica 6: Artes para Desktop E Mobile

- [ ] Billboard: imagem de destaque tem versão **desktop** e **mobile** (se necessário)
- [ ] Grupo: capa da comunidade tem versão **desktop** e **mobile** (se necessário)
- [ ] Grupo: capa imersiva renderiza bem em tela pequena

**Regra:** Se não enviar versão mobile, a Ensinio puxa a de desktop. Geralmente funciona, mas se a imagem corta mal no celular, envie uma versão específica.

**Onde configurar:** Em cada lugar que aceita upload de imagem, a Ensinio oferece campo para desktop e campo para dispositivos móveis.

**Teste:** Abrir a plataforma no celular (ou diminuir a janela do navegador) → imagens não cortam texto, não ficam estranhas.

---

## Dica 7: Menu Customizado

- [ ] Menu tem pelo menos **2-3 itens** relevantes (ex: Início, YouTube, Contato)
- [ ] Itens linkam para: URL externa (canal YouTube, site), página interna (grupo, Billboard), ou ambos
- [ ] Itens ordenados por prioridade (mais importante à esquerda)
- [ ] Não tem itens demais (muitos itens → gera menu "mais" que esconde conteúdo)
- [ ] Menu mobile: colapsa em barra inferior estilo app (automático, mas verificar se itens fazem sentido)

**Onde configurar:** Admin Console → Configurações → Menus

**Teste:** Navegar pelo header → links funcionam. Diminuir janela → menu mobile aparece limpo.

---

## Score de Auditoria

| Critério | Status | Impacto |
|----------|--------|---------|
| Logo + Favicon | ⬜ | Alto — primeira impressão profissional |
| Vídeo de background | ⬜ | Alto — sofisticação imediata |
| Estampa em todos os grupos | ⬜ | **Crítico** — maior diferença amador vs profissional |
| Sessões variadas na Billboard | ⬜ | Médio — riqueza visual |
| Layout de aulas adequado | ⬜ | Médio — UX do aluno |
| Artes desktop + mobile | ⬜ | Médio — experiência mobile |
| Menu customizado | ⬜ | Baixo — polimento final |

### Classificação
- **7/7:** Plataforma premium, pronta para go-live
- **5-6/7:** Boa, mas falta polimento
- **3-4/7:** Funcional, mas amadora visualmente
- **0-2/7:** Precisa de atenção urgente antes de mostrar para alunos

---

**Criado:** 2026-03-20
**Fonte:** Vídeo "Plataforma e App para Infoprodutores Venderem 10x Mais" — Gui Ávila (2026-03-14)
