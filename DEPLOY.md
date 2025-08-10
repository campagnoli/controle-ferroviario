# Instruções de Deploy - GitHub + Vercel

## Passo a Passo para Deploy

### 1. Preparação do Projeto

O projeto já está configurado e pronto para deploy. Certifique-se de que todos os arquivos estão presentes:

```
controle-ferroviario/
├── src/
│   ├── main.py
│   ├── routes/
│   ├── static/
│   └── models/
├── requirements.txt
├── README.md
└── venv/ (não incluir no Git)
```

### 2. Configuração do Git

```bash
# Navegue até a pasta do projeto
cd controle-ferroviario

# Inicialize o repositório Git (se ainda não foi feito)
git init

# Crie arquivo .gitignore
echo "venv/
__pycache__/
*.pyc
.env
.DS_Store
src/database/app.db" > .gitignore

# Adicione todos os arquivos
git add .

# Faça o primeiro commit
git commit -m "Aplicação de Controle Ferroviário - Versão 1.0"
```

### 3. Upload para GitHub

```bash
# Crie um repositório no GitHub (via web)
# Depois conecte o repositório local:

git remote add origin https://github.com/SEU_USUARIO/controle-ferroviario.git
git branch -M main
git push -u origin main
```

### 4. Deploy no Vercel

#### Opção A: Via Dashboard Web
1. Acesse [vercel.com](https://vercel.com)
2. Faça login com sua conta GitHub
3. Clique em "New Project"
4. Selecione o repositório `controle-ferroviario`
5. Configure as seguintes opções:
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Build Command**: `pip install -r requirements.txt`
   - **Output Directory**: `src/static`
   - **Install Command**: `pip install -r requirements.txt`

#### Opção B: Via CLI
```bash
# Instale o Vercel CLI
npm i -g vercel

# Faça login
vercel login

# Deploy
vercel

# Siga as instruções:
# - Set up and deploy? Yes
# - Which scope? (sua conta)
# - Link to existing project? No
# - Project name: controle-ferroviario
# - Directory: ./
```

### 5. Configuração Específica para Flask

Crie um arquivo `vercel.json` na raiz do projeto:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "src/main.py",
      "use": "@vercel/python"
    },
    {
      "src": "src/static/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/src/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/src/main.py"
    }
  ]
}
```

### 6. Arquivo de Configuração Python para Vercel

Crie um arquivo `api/index.py` (se necessário):

```python
from src.main import app

# Vercel precisa de uma função handler
def handler(request):
    return app(request.environ, start_response)

if __name__ == "__main__":
    app.run()
```

### 7. Variáveis de Ambiente (se necessário)

No dashboard do Vercel:
1. Vá em Settings > Environment Variables
2. Adicione as variáveis necessárias:
   - `FLASK_ENV=production`
   - `SECRET_KEY=sua_chave_secreta_aqui`

### 8. Comandos Úteis

```bash
# Atualizar o projeto
git add .
git commit -m "Atualização da aplicação"
git push

# Redeploy automático no Vercel após push

# Deploy manual no Vercel
vercel --prod
```

### 9. Verificação do Deploy

Após o deploy:
1. Acesse a URL fornecida pelo Vercel
2. Teste todas as funcionalidades:
   - Preenchimento de dados
   - Adição/remoção de trens
   - Geração de PDF
   - Geração de imagem
   - Responsividade mobile

### 10. Domínio Personalizado (Opcional)

No Vercel Dashboard:
1. Vá em Settings > Domains
2. Adicione seu domínio personalizado
3. Configure DNS conforme instruções

### 11. Monitoramento

- **Logs**: Disponíveis no dashboard do Vercel
- **Analytics**: Ative nas configurações do projeto
- **Performance**: Monitore via Vercel Analytics

### 12. Troubleshooting

#### Problemas Comuns:

**Erro de Build:**
- Verifique se `requirements.txt` está correto
- Confirme que todas as dependências estão listadas

**Erro 500:**
- Verifique logs no dashboard Vercel
- Confirme configuração do `vercel.json`

**Arquivos estáticos não carregam:**
- Verifique rotas no `vercel.json`
- Confirme estrutura de pastas

**Sessões não funcionam:**
- Configure `SECRET_KEY` nas variáveis de ambiente
- Verifique se Flask está configurado corretamente

### 13. Backup e Versionamento

```bash
# Criar tags de versão
git tag -a v1.0 -m "Versão 1.0 - Release inicial"
git push origin v1.0

# Criar branch para desenvolvimento
git checkout -b desenvolvimento
git push -u origin desenvolvimento
```

### 14. Atualizações Futuras

Para atualizações:
1. Faça as alterações no código
2. Teste localmente
3. Commit e push para GitHub
4. Deploy automático no Vercel

---

## URLs Importantes

- **Repositório GitHub**: `https://github.com/SEU_USUARIO/controle-ferroviario`
- **Aplicação Vercel**: `https://controle-ferroviario.vercel.app` (ou URL personalizada)
- **Dashboard Vercel**: `https://vercel.com/dashboard`

## Suporte

Em caso de problemas:
1. Verifique logs no Vercel
2. Consulte documentação oficial
3. Teste localmente primeiro

**Boa sorte com o deploy! 🚂**

