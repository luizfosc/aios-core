Ao receber este comando, siga EXATAMENTE estes passos:

1. **Gere o pulse** rodando `node scripts/generate-project-pulse.js` via Bash

   - Se o usuário pediu `--dry-run`, rode com essa flag para apenas visualizar
   - Caso contrário, rode com as env vars:
     ```
     BOT_API_URL=http://178.156.242.82:3000 SYNC_API_KEY=bf3baae3852e6668855840f50164b383faf4aae4f018b47a69cf713d5316bb55 node scripts/generate-project-pulse.js
     ```

2. **Confirme ao usuário** com o resultado:
   - Quantos projetos foram escaneados
   - Se o envio foi bem-sucedido ou falhou
   - Se `--dry-run`, mostre o resumo compacto do output

3. **Notas:**
   - Este comando substitui o antigo `/sync-projects` (que usava Google Docs)
   - O bot recebe os dados via `POST /api/projects/sync` e injeta no contexto do LLM
   - Recomendado rodar 1x por semana ou após criar/modificar projetos significativos
   - Use `--dry-run` para verificar o que será enviado antes de sincronizar
