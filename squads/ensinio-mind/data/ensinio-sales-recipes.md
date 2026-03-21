# Ensinio — Receitas de Vendas (Como Fazer Na Prática)

> Cenários operacionais comuns e como configurar cada um na plataforma.
> Para: CS guiar cliente, SDR demonstrar flexibilidade, ou cliente consultar sozinho.
> Fonte: Vídeo "Plataforma e App para Infoprodutores" — Gui Ávila (2026-03-14)

---

## Receita 1: Vender um Curso com Pagamento Único

**Cenário:** Infoprodutor quer vender um curso por R$ 497 à vista.

**Passo a passo:**
1. Criar grupo (ex: "Curso de Marketing Digital")
2. Adicionar módulos e aulas dentro do grupo
3. Grupo → Vendas → Criar Oferta
4. Tipo: **Pagamento único** → R$ 497
5. Salvar → copiar link do checkout
6. Enviar link para leads ou usar na landing page

**Resultado:** Lead acessa checkout white label (seudominio.com/payment/ID), paga e ganha acesso automático ao grupo.

---

## Receita 2: Criar Assinatura Mensal/Anual

**Cenário:** Infoprodutor quer um clube de assinatura com opções mensal e anual.

**Passo a passo:**
1. Criar grupo (ex: "Membro Platinum")
2. Grupo → Vendas → Criar Oferta
3. Tipo: **Recorrência**
4. Adicionar opções:
   - R$ 29/mês
   - R$ 180/semestre
   - R$ 290/ano
5. Cada opção vira um plano no checkout — aluno escolhe

**Resultado:** Aluno assina, tem acesso enquanto pagar. Retentativas automáticas em caso de falha.

---

## Receita 3: Pacote de Produtos (Vínculos)

**Cenário:** Infoprodutor quer vender 3 cursos juntos por um preço único.

**Passo a passo:**
1. Criar os 3 grupos individuais (Curso A, Curso B, Curso C) com conteúdo
2. Criar 1 grupo "guarda-chuva" (ex: "Pacote Completo" ou "Membro Platinum")
3. No grupo guarda-chuva → Vínculos → adicionar Curso A, Curso B e Curso C
4. Criar oferta no grupo guarda-chuva com preço do pacote
5. Opcional: adicionar aula de boas-vindas no grupo guarda-chuva

**Resultado:** Aluno compra 1 produto e ganha acesso a 4 grupos (o guarda-chuva + 3 vinculados). Conteúdos extras aparecem como "Conteúdos Extras" na aba de aulas.

**Variação Black Friday:** Criar grupo temporário "Black Friday 2026" → vincular aos cursos → criar oferta com preço promocional → desativar depois.

---

## Receita 4: Upsell Pós-Compra

**Cenário:** Após comprar o Curso A, oferecer o Curso B com desconto.

**Passo a passo:**
1. Ter Curso A e Curso B como grupos separados
2. Curso A → Vendas → Upsell
3. Selecionar o Curso B como produto de upsell
4. Escolher a oferta do Curso B (pode ser com desconto)
5. Configurar banner/descrição do upsell (texto + imagem ou vídeo)

**Resultado:** Na página de obrigado após comprar Curso A, aparece banner do Curso B. Com **1 clique, sem redigitar cartão de crédito**, aluno adiciona o Curso B. Compra instantânea — zero atrito.

---

## Receita 5: Order Bump no Checkout

**Cenário:** Oferecer e-book complementar durante o checkout do curso principal.

**Passo a passo:**
1. Criar grupo do e-book (conteúdo: PDF para download)
2. Admin Console → Vendas → Order Bump → Novo
3. Selecionar o grupo do e-book como produto do order bump
4. Definir preço do order bump
5. Escopo: **Todos os produtos**, **Grupos específicos** ou **Produtos acima de R$ X**

**Resultado:** No checkout de qualquer produto (ou dos selecionados), aparece caixinha "Adicionar e-book por + R$ 27". Aluno marca e paga junto.

**Dica do Gui:** Order Bump = complementar (algo que adiciona valor ao que já está comprando). Upsell = suplementar (próximo produto na escada de valor).

---

## Receita 6: Cupom Inteligente de Upgrade

**Cenário:** Oferecer desconto exclusivo para quem já comprou o curso iniciante fazer upgrade para o avançado.

**Passo a passo:**
1. Admin Console → Vendas → Cupons → Novo
2. Nome: "Upgrade Avançado"
3. Código: UPGRADE2026
4. Tipo de desconto: percentual (ex: 30%) ou absoluto (ex: R$ 200 off)
5. **Itens aceitos:** selecionar apenas o grupo "Curso Avançado"
6. **Permissão de uso:** "Usuários com acesso atual a" → selecionar "Curso Iniciante"
7. Configurar limite de uso e data de expiração

**Resultado:** Só quem já comprou o Curso Iniciante consegue usar o cupom UPGRADE2026. Se alguém compartilhar o código, não funciona para quem não tem o curso base.

---

## Receita 7: Cupom de Reativação de Base

**Cenário:** Reativar alunos que já tiveram acesso mas perderam (assinatura cancelada).

**Passo a passo:**
1. Admin Console → Vendas → Cupons → Novo
2. Nome: "Volta pra Casa"
3. Código: VOLTAPRACASA
4. Desconto: 50% no primeiro mês
5. **Permissão de uso:** "Usuários que já tiveram acesso no passado a" → selecionar grupo
6. Ativar cupom e enviar por e-mail/WhatsApp para a base inativa

**Resultado:** Apenas ex-alunos conseguem usar. Base ativa não consegue (evita canibalização). Reativação segmentada.

---

## Receita 8: Parcelamento Inteligente (Recuperação Automática)

**Cenário:** Lead tenta comprar por R$ 1.200, cartão recusa por limite insuficiente.

**Configuração:**
1. Admin Console → Vendas → Parcelamento Inteligente → **Manter ativo** (recomendação Gui Ávila)

**O que acontece automaticamente:**
1. Lead tenta R$ 1.200 em 12x de R$ 100 → cartão recusa (limite insuficiente para R$ 1.200)
2. Ensinio reprocessa como R$ 100/mês recorrente (consome apenas R$ 100 do limite)
3. Se ainda não tem R$ 100 → retorna ao checkout para outra opção

**Resultado:** Venda que seria perdida por limite é convertida automaticamente. Sem ação do produtor.

---

## Receita 9: Grupo Sem Aulas (Mentoria / Consultoria)

**Cenário:** Infoprodutor vende mentoria. Não tem aulas gravadas, quer apenas página de vendas bonita.

**Passo a passo:**
1. Criar grupo (ex: "Mentoria Exclusiva")
2. Configurar estampa, capa, kicker ("Mentoria Individual")
3. Grupo → Configurações → Redirecionamento externo → URL da landing page
4. Adicionar grupo como destaque na Billboard

**Resultado:** Na Billboard, o grupo aparece bonito com vídeo/imagem. Quando aluno (não logado) clica, vai para a landing page externa de vendas. Sem precisar de aulas prontas.

**Variação:** Se quer manter dentro da plataforma, criar grupo com comunidade apenas (sem aulas) para interação com mentorados.

---

## Receita 10: Múltiplas Ofertas para Mesmo Produto

**Cenário:** Mesmo curso com preços diferentes para públicos diferentes.

**Passo a passo:**
1. Grupo → Vendas → Criar Oferta (Oferta 1: R$ 497 pagamento único)
2. Criar Oferta 2: R$ 997 com bônus (vincular grupo de bônus)
3. Criar Oferta 3: 12x R$ 49/mês recorrência
4. Cada oferta gera um link de checkout diferente

**Resultado:** 3 links diferentes, cada um com preço/condição. Use links diferentes em landing pages, e-mails ou campanhas distintas.

---

## Resumo Visual: Onde Configurar Cada Coisa

| Ação | Caminho no Admin Console |
|------|------------------------|
| Criar oferta | Grupos → [seu grupo] → Vendas → Criar Oferta |
| Configurar checkout | Ofertas → [oferta] → Experiência |
| Criar cupom | Vendas → Cupons → Novo |
| Order bump | Vendas → Order Bump → Novo |
| Upsell | Grupos → [seu grupo] → Vendas → Upsell |
| Parcelamento inteligente | Vendas → Parcelamento Inteligente |
| Vínculos (pacotes) | Grupos → [seu grupo] → Vínculos |
| Ver vendas/extrato | Vendas → Extrato e Saques |
| Conta bancária | Vendas → Extrato e Saques → Cadastrar conta |

---

**Criado:** 2026-03-20
**Fonte:** Vídeo "Plataforma e App para Infoprodutores Venderem 10x Mais" — Gui Ávila (2026-03-14)
