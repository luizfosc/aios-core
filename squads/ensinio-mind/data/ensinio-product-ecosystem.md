# Ensinio — Ecossistema de Produtos

> Source of Truth para todos os squads ensinio-*
> Atualizado: 2026-03-20
> Fontes: ensinio.com, Pitch Deck 2026, [Vídeo Setup Completo — Gui Ávila (2026-03-14)](https://www.youtube.com/watch?v=FXtV6uQomUQ)

---

## Visão Geral do Ecossistema

A Ensinio entrega uma solução de ponta a ponta que permite o infoprodutor subir seu conteúdo, definir sua oferta e gerir seu público sem ter que se preocupar com integrações.

| Produto | Categoria | Descrição |
|---------|-----------|-----------|
| **Ensinio Club** | Área de Membros | Distribua conteúdo para seus membros em sua própria Netflix |
| **Ensinio Pay** | Checkout | Checkout 100% integrado — transforme cliques em vendas |
| **Ensinio Stream** | Vídeo On Demand | Hospedagem de vídeo própria, sem depender de YouTube/Vimeo |
| **Ensinio AI** | Agentes de IA | Agentes que vendem, atendem, qualificam leads 24/7 |
| **Ensinio Engage** | Comunidades | Comunidades segmentadas por nicho/tema |
| **Ensinio Chat** | Atendimento Omnichannel | Em breve — atendimento centralizado multi-canal |

---

## Ensinio Club — Área de Membros

**Proposta:** "Sua plataforma estilo Netflix"

### Conceitos fundamentais:
- **Billboard** — Vitrine/tela inicial da plataforma (URL: /browse). Onde o aluno vê todos os conteúdos ao entrar.
- **Grupos** — Unidade fundamental ("tijolos que constroem a casa"). Tudo é grupo: curso, mentoria, comunidade, e-book, assinatura. Cada grupo pode conter aulas, comunidade, ou ambos. Grupos não precisam aparecer na Billboard — podem ser "invisíveis" (ex: bônus, conteúdo vinculado). Sem imagem de capa, o grupo exibe uma cor padrão automática (trocável).
- **Admin Console** — Painel de gestão. Acessível por usuários com permissão admin. Alunos não veem. Atalho: dentro de qualquer grupo, admins veem um botão "Gerenciar" direto na interface (sem precisar voltar ao Admin Console).
- **Seletor de grupo** — Dentro de um grupo, existe um seletor no header para alternar entre grupos sem voltar à Billboard.
- **Trilhas** — Sequência ordenada de grupos. Disponível apenas nos planos pagos.

### Billboard — Estrutura:
- **Destaques iniciais** — Área nobre no topo. Carrossel de grupos em destaque com vídeo de fundo + estampa + kicker + subtítulo. Se apenas 1 destaque, não exibe setas de navegação. **Limitação atual:** destaques só suportam grupos (trilhas como destaque = roadmap futuro). Quando o vídeo de destaque termina, faz transição automática para a imagem estática configurada — por isso ter ambos (vídeo + imagem).
- **Sessões** — Faixas horizontais estilo Netflix. Tipos: grupos, grupos em alta, grupos em destaque, módulos, aulas mais assistidas, trilhas. Cada sessão com título, subtítulo e capas verticais ou horizontais.
- **Cache de Billboard** — Alterações na billboard demoram ~1 minuto para refletir (cache de performance). Não é instantâneo.

### Features principais:
- **Billboard customizável** — Vitrine que valoriza a marca de todas as formas
- **Sliders modernos** — Organização em sliders que emulam ambiente de streaming
- **Capas verticais e horizontais** — Diferentes tipos de sliders para trilhas e cursos
- **Identidade visual 100%** — Liberdade máxima para expressar identidade visual
- **Feed central** — Rede social própria onde alunos ficam a par de tudo
- **Comunidades segmentadas** — Múltiplas comunidades por grupos ou temas
- **Aulas e módulos** — Jornada clara para que o aluno siga as aulas na ordem correta
- **Envio de tarefas** — Alunos enviam arquivos e anotações para correção manual
- **Quizzes** — Testes rápidos nas próprias aulas que estão assistindo
- **Transmissão ao vivo** — Sem sair da plataforma, com DVR ativo e gravações automáticas
- **Anamnese** — Pesquisa de perfil com pesos configuráveis → direcionamento automático para trilha
- **Analytics de performance** — Dados precisos para refinar conteúdo e aumentar retenção

### Layouts de aula (pré-definições de conteúdo):
- **Imersivo** (padrão) — Módulos abertos com aulas visíveis lado a lado. Ideal para poucos conteúdos.
- **Seriado** — Mostra capas dos módulos primeiro; ao clicar, abre aulas do módulo (estilo Netflix: temporadas → episódios). Ideal para muitas aulas.
- **Sequencial** — Módulos na direita com aulas empilhadas abaixo. Ideal para cursos extensos com muitas aulas.

### Identidade visual do grupo:
- **Estampa** — Logomarca/identidade do grupo (600x240px). Substitui o título em texto por uma imagem estilizada na interface. Sem estampa = puxa título em texto (fica feio).
- **Capa vertical** — Imagem 9:12 para sessões com capas verticais na Billboard
- **Capa horizontal** — Imagem 16:9 para sessões horizontais na Billboard
- **Capa imersiva** — Background da aba de aulas dentro do grupo (usar versão da capa SEM textos para evitar poluição visual)
- **Capa da comunidade** — Banner retangular exibido no topo da comunidade do grupo
- **Kicker** — Texto curto exibido acima do subtítulo na Billboard e na página de vendas (ex: "Curso + Comunidade")
- Todas as artes suportam versão desktop e versão mobile separada (se não enviar mobile, puxa a de desktop)

### Vínculos entre grupos (pacotes):
- Um grupo pode vincular a outros grupos — quem compra o grupo principal ganha acesso aos vinculados
- Uso típico: criar grupo "Membro Platinum" como assinatura → vincular a múltiplos cursos
- Uso Black Friday: grupo temporário com vínculos → pacote especial sem duplicar conteúdo
- Conteúdos extras vinculados aparecem na aba de aulas do grupo principal, abaixo dos módulos

### Drip Content (liberação programada):
- Liberar aulas a conta-gotas para evitar consumo rápido e pedido de reembolso
- Configurável por aula/módulo: imediatamente, após X dias, ou em data específica
- Estratégia comum: liberar bônus apenas após período de garantia (ex: 15 dias)

### Avaliação personalizada (tarefas):
- Habilite por aula quando quiser receber um Envio de Tarefa
- Aluno pode enviar texto por escrito e anexos de arquivos
- Correção com nota e feedbacks
- Desfazer envio e permitir nova tentativa
- Central de Tarefas para acompanhar todos os envios
- Impedimento de conclusão até que a tarefa seja enviada
- Prazo de conclusão definível
- Aulas fora do prazo indicadas com atraso

### Pesquisa de satisfação (CSAT por aula):
- Formato configurável: **emoji**, **estrela** ou **números**
- Pode ser **obrigatória**: aluno só avança para a próxima aula se avaliar a aula atual
- Resultados visíveis no dashboard de dados (média por aula, total de avaliações)

### Comentários por aula:
- **Comentário público** — visível para todos os membros do grupo (NÃO é público para o mundo, apenas para quem comprou o grupo)
- **Comentário privado** — somente aluno + professor
- Ambos configuráveis (permitir/desativar por grupo)

### Quizzes:
- Reutilize perguntas em diferentes aulas
- Respostas corretas para correção automática
- Data e horário para liberação de resultados
- Explicação para contextualizar o aluno
- Múltipla escolha e múltipla seleção
- Conferência individual de cada resposta
- Impedimento de conclusão até que quiz seja respondido

---

## Ensinio Pay — Checkout Integrado

**Proposta:** "Transforme cliques em vendas com seu checkout 100% integrado"

### Checkout transparente:
- Venda sem direcionar alunos para fora da plataforma
- 100% integrado ao ambiente da área de membros
- Meios de pagamento: **Pix, Cartão de crédito, Boleto**
- Totalmente personalizável: one-page ou multi-steps (layout configurável por oferta)
- Campos personalizados
- White label completo: URL = seudominio.com/payment/ID (sem menção à Ensinio)
- Cor do botão customizável (match com brand)
- Banners customizáveis: imagem em cima e embaixo, versão desktop e mobile separadas
- Página de obrigado: padrão Ensinio, URL externa ou página customizada
- Campo de endereço: ativável/desativável (ativado reduz reembolso, desativado reduz atrito)
- Checkout em etapas: captura lead mesmo se não comprar (dados para recuperação de carrinho)

### Assinaturas:
- **Retentativas automáticas** — Múltiplas tentativas de renovação em 25 dias
- **Cobranças otimizadas** — Análise de horários mais vantajosos por banco emissor
- **Alertas de renovação** — Notificação até regularizar
- **Troca de meio de pagamento** — Aluno troca a qualquer momento dentro da área
- **Cancelamento controlado** — Todos passam pelo produtor para reverter churn
- **Reembolso por garantia** — Aprovação automática dentro do prazo estabelecido

### Cross Sell:
- **Venda Mais** — Mais dinheiro com os mesmos leads
- **Order Bump** — Oferta complementar durante checkout
- **Upsell** — Oferta pós-compra para aumentar ticket. **1 clique sem redigitar cartão** — aluno adiciona segundo produto instantaneamente na página de obrigado.
- **Split de pagamento** — Divisão de receita entre co-produtores/afiliados (mencionado no admin console, detalhes sob demanda)

### Recuperador de Vendas (Parcelamento Inteligente):
Fluxo automático quando cartão é recusado por limite insuficiente:
1. Lead inicia compra (ex: R$ 1.200 em 12x de R$ 100)
2. Compra negada por limite insuficiente (valor total)
3. **Parcelamento Inteligente ativa**: cobrança reprocessada como parcelas recorrentes (12x R$ 100 recorrente, consumindo apenas R$ 100 do limite)
4. Se ainda não há limite para R$ 100 → comprador retorna ao checkout e escolhe outras opções
5. Resultado: **venda realizada** que seria perdida

### Cupons Inteligentes:
- Leads retornantes (condições exclusivas)
- Base ativa (inside sales com restrições)
- Descontos absoluto e percentual
- Desconto percentual máximo (limite para evitar burla)
- Valor mínimo para desconto
- Autorização por produto (itens aceitos: grupos específicos)
- Limites de uso individual e total + quantidade de resgate
- Autorização por lead
- **Permissão de uso avançada:**
  - Qualquer pessoa
  - Usuários específicos (selecionar manualmente)
  - Usuários com acesso atual a determinado grupo
  - Usuários que já tiveram acesso no passado (reativação de base!)
- Data de expiração configurável
- Liga/desliga independente (preparar cupom sem publicar)
- Caso de uso poderoso: "Upgrade para avançado" — cupom exclusivo para quem já comprou o produto inicial

---

## Ensinio Stream — Vídeo On Demand

- Hospedagem própria de vídeos
- Sem depender de YouTube, Vimeo ou provedores externos
- Biblioteca centralizada para upload e organização
- Associação direta a aulas
- Traga vídeos da biblioteca atual ou use Ensinio Stream

---

## Ensinio AI — Agentes de Inteligência Artificial

**Proposta:** "Crie agentes de IA que trabalham para você 24/7"

### Tipos de agente:
- **Agente de Vendas (SDR)** — Conversa com compradores, responde dúvidas, quebra objeções, agenda chamada ou realiza a venda na hora
- **Agente Tutor** — Responde dúvidas dos alunos sobre conteúdo, aulas e assuntos técnicos. Reduz volume de tickets de suporte e necessidade de monitores/tutores humanos.
- **Agente Customizado** — Determine o DNA do agente: diretrizes, tom de voz, código de conduta

### Capacidades:
- Estabelecer tom de voz e objetivos
- Tirar dúvidas e quebrar objeções (com playbook configurável)
- Qualificar leads automaticamente
- Converter leads em vendas (consulta produtos disponíveis, cupons e preços nativamente)
- Agendar reuniões (verifica disponibilidade automaticamente via Google Agenda)
- Follow-ups automáticos — quando lead para de responder, agente retoma contato
- Painel de followups com explicação da IA sobre motivo de cada followup + opção de cancelar
- Habilidades liga/desliga: vendas, reunião, etc. — cada habilidade ativável/desativável por chave
- Base de conhecimento conectável (interna ou via ClickUp)
- Conexão WhatsApp via QR code (mesmo app que o produtor já usa)
- Histórico de conversas visível no admin console

### Visão estratégica (Gui Ávila):
- "A visão é que a Ensinio seja uma plataforma estruturada com base em agentes de IA para ajudar no seu negócio"
- Agentes para: tirar dúvida, fazer venda, ajudar cliente a dar o próximo passo na escada de valor

### Em breve (Ensinio AI roadmap):
- Análise de imagens e áudios (compreensão multimodal)
- Web scraping (agente aprende de páginas e conteúdos da web)
- Guardrails (filtragem e análise de segurança das respostas)
- Mais canais (widget Landing Page, Instagram, Messenger, Telegram, WhatsApp Oficial)
- Métricas e analytics (acompanhamento em tempo real)
- Social selling via Instagram

---

## Ensinio Engage — Comunidades

- Comunidades segmentadas por nichos diferentes em um só lugar
- Feed central de interações
- "É como ter sua própria rede social"
- Publicações, comentários, reações
- Rankings de gamificação integrados

### Comunidade dentro do grupo:
- Cada grupo criado já vem com comunidade (pode desativar se quiser)
- Página inicial do grupo configurável: comunidade, aulas, primeira aula, ou última aula assistida
- Comentários podem ser feitos dentro da aula OU na comunidade do grupo — ambos aparecem no feed

### Feed central:
- URL: /feed — centraliza atividades de múltiplas comunidades
- Publicações no feed podem ter título e imagem de banner (diferencial vs comunidade do grupo)
- Permissão de acesso ao feed: todos os usuários OU membros de grupos específicos
- Conteúdo segmentado: post feito na comunidade do grupo X só aparece para quem tem acesso ao grupo X, mesmo com feed público
- Feed tem sessões customizáveis (como a Billboard): destaques, produtos, sessões personalizadas
- Perfil do usuário no feed: foto, capa, resumo de curtidas/publicações, gamificação, aulas em andamento

### Moderação de comentários:
- Central de comentários no admin console (grupos e recursos → comentários)
- Comentários revisados e não revisados
- Possível excluir, responder, ver módulo/aula de origem

---

## Gamificação — Motor de Retenção

**Proposta:** "Transforme cada interação em uma experiência envolvente"

### Sistema de pontuação flexível:
| Ação | Limite Diário | Moeda | Pontos |
|------|---------------|-------|--------|
| Realizar login | 1 | 0 | 1 |
| Reagir a publicação | 1 | 0 | 1 |
| Comentar em postagem | 1 | 0 | 1 |
| Comentar em aula | 1 | 0 | 1 |
| Fazer comentário particular | 1 | 0 | 1 |

### Gamificação — Dois níveis:
- **Nível de plataforma** (recomendado) — Gatilhos, níveis e recompensas que valem para toda a plataforma. Mais fácil de gerenciar.
- **Nível de grupo** (legado) — Gamificação específica por grupo. Mais trabalhoso, pois precisa configurar em cada grupo.
- Recomendação Gui Ávila: usar gamificação a nível da plataforma, não a nível do grupo.

### Efeito posse (psicologia social):
- Gamificação gera "efeito posse" — quando o aluno acumula pontos, moedas, selos, ele não quer abrir mão
- Resultado: mais engajamento, menos churn, mais recompra, mais LTV
- Referência: livro "Shortcuts" do Gui Ávila

### Loja de Recompensas:
- Reivindique recompensas com Coins (moedas acumuladas via gatilhos)
- Prêmios definidos pelo produtor: desde matrículas em grupos até prêmios físicos (bonés, squeezes, canecas, camisetas)
- Cada recompensa: título, imagem, custo em moedas, data de expiração, quantidade em estoque, limite por usuário
- Recompensas podem ser restritas a membros de grupos específicos
- Histórico de resgate completo com controle de logística para prêmios físicos (**sem integração nativa com correio/shipping** — logística de entrega é responsabilidade do produtor)
- Pode ativar/desativar a loja independente dos gatilhos (preparar sem publicar)
- Alunos engajados permanecem mais tempo e se tornam promotores da marca

### Níveis de gamificação:
- Exemplo de estrutura: Iniciante (2pts) → Bronze (50) → Prata (100) → Ouro (200) → Esmeralda (400) → Safira → Rubi → Diamante (1000)
- Nomes customizáveis por nicho (ex: para finanças, "Nível Warren Buffett")
- Selos visuais por nível (upload próprio ou opções prontas)
- Notificação + confetes na tela ao subir de nível

### Rankings:
- Rankings diários dos alunos
- Ranking geral ativável (aparece como opção na Billboard)
- Competição saudável fomenta engajamento
- Pontuação por XP (experiência)

---

## Ensinio Chat — Atendimento Omnichannel (Em breve)

- Atendimento centralizado multi-canal
- Status: em desenvolvimento

---

## Analytics e Métricas

### Dashboard de dados (admin console → dados):
- **Métricas de aproveitamento:** taxa de conclusão, quizzes, tarefas, feedbacks por aula
- **Satisfação do cliente:** notas CSAT por aula (ex: 1000+ avaliações, média 4.8)
- **Estatísticas de uso:** período de acesso, horário do dia, filtro por grupo
- **Aulas mais acessadas** e desempenho acima/abaixo da média
- **Engajamento:** usuários mais engajados, participação na comunidade
- **Gamificação:** ranking de pontos, participação
- **Assinaturas:** métricas de recorrência
- Tudo filtrável por grupo específico

### Insight prático (Gui Ávila):
- "Métrica não é para ser chata e inútil — é para te dar insights diretos e feedbacks para melhorar"
- Exemplo: aula com nota baixa → investigar se está muito longa ou muito difícil

---

## Aparência e Design

### Logomarca e Favicon:
- Logo para modo claro e modo escuro (separadas)
- Isotipo (símbolo da marca) usado como favicon no navegador
- Favicon: puxar do isotipo (recomendado) ou upload personalizado

### Modo claro/escuro:
- Plataforma suporta ambos os modos
- Configurável: só escuro, só claro, escuro por padrão com claro opcional
- Recomendação Gui Ávila: escuro por padrão — "mais sofisticado, dá ideia de streaming/Netflix"

### Menu customizado:
- Itens de menu no header da plataforma (ex: Início, YouTube, Ensinio)
- Cada item: URL externa ou página interna (grupo, Billboard, etc.)
- Muitos itens → gera menu "mais" automaticamente
- Mobile: menu colapsa em barra inferior estilo app
- Totalmente personalizável pelo admin

---

## Features Transversais

| Feature | Disponível em |
|---------|---------------|
| White Label completo | Todos os planos (esconder marca no Professional+) |
| App mobile próprio | Business+ (em breve) |
| Domínio customizado | Todos |
| SSO (Google, Microsoft, Okta) | Enterprise |
| API REST pública | Enterprise |
| 38 Webhooks (6 classes) | Todos |
| Integrações checkout externo | Professional+ (Hotmart, Kiwify, Monetizze, etc.) |
| Pixel Facebook Ads | Todos |
| SCORM 1.2 e 2004 | Enterprise |
| Organizações multi-tenant | Enterprise |
| 5 Dashboards analíticos | Business+ |
| Campanhas de email | Todos |
| DRM Social (marca d'água) | Todos |
| Certificados com QR Code | Todos |
| NF-e via Notazz | Todos |
