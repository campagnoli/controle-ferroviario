# Controle Ferroviário - Passagem de Serviço

Aplicação web para controle e acompanhamento de produção ferroviária por turno, desenvolvida especificamente para controladores de pátio e terminais.

## Funcionalidades

### ✅ Implementadas
- **Informações do Turno**: Registro de agente, data, feriado e turno
- **Tabela de Trens**: Controle completo com todos os campos solicitados:
  - Nº, TREM, ORIG, PART, DEST, CHEG
  - PART REAL, STATUS DE PARTIDA, CHEG REAL, STATUS DE CHEGADA
  - OBSERVAÇÕES
- **Cálculo Automático de Status**: Baseado nos horários programados vs reais
- **Gráficos em Tempo Real**: Visualização do status de circulação
- **Estatísticas**: Contadores por status (Atrasado, OnTime, Para Circular, Circulando, Extra)
- **Exportação PDF**: Relatório completo para anexo em e-mail
- **Exportação Imagem**: Resumo visual para corpo de e-mail
- **Interface Responsiva**: Funciona em desktop e mobile

### 🎯 Status dos Trens
- **🟢 OnTime**: Tolerância de até 5 minutos
- **🔴 Atrasado**: Mais de 5 minutos de atraso
- **🟡 Para Circular**: Aguardando partida
- **🔵 Circulando**: Em movimento
- **⚫ Extra**: Outros status

## Como Usar

### 1. Preenchimento das Informações do Turno
- **Agente**: Nome do controlador responsável
- **Dia**: Data do turno (preenchida automaticamente)
- **Feriado**: Sim/Não
- **Turno**: Dia/Manhã/Tarde/Noite

### 2. Registro dos Trens
- Preencha os dados de cada trem nas colunas correspondentes
- Os horários devem ser no formato HH:MM (24h)
- O status é calculado automaticamente ao preencher horários reais
- Use o campo "Observações" para anotações importantes

### 3. Gerenciamento da Tabela
- **Adicionar Trem**: Clique no botão para adicionar nova linha
- **Remover Trem**: Use o botão "Remover" na linha correspondente
- **Limpar Dados**: Remove todos os dados (use com cuidado!)

### 4. Exportação de Relatórios
- **Gerar PDF**: Cria relatório completo para anexar em e-mails
- **Gerar Imagem**: Cria resumo visual para corpo de e-mail
- **Salvar Dados**: Força o salvamento dos dados atuais

## Instalação e Execução

### Pré-requisitos
- Python 3.11+
- pip (gerenciador de pacotes Python)

### Instalação
```bash
# Clone ou baixe o projeto
cd controle-ferroviario

# Ative o ambiente virtual
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### Execução Local
```bash
# Ative o ambiente virtual
source venv/bin/activate

# Execute a aplicação
python src/main.py
```

A aplicação estará disponível em: `http://localhost:5001`

### Deploy no Vercel
1. Faça upload do projeto para o GitHub
2. Conecte o repositório ao Vercel
3. Configure as variáveis de ambiente se necessário
4. Deploy automático será realizado

## Estrutura do Projeto

```
controle-ferroviario/
├── src/
│   ├── main.py              # Arquivo principal do Flask
│   ├── routes/
│   │   ├── trens.py         # Rotas para gerenciamento de trens
│   │   └── relatorios.py    # Rotas para geração de relatórios
│   └── static/
│       ├── index.html       # Interface principal
│       ├── styles.css       # Estilos da aplicação
│       └── script.js        # Lógica JavaScript
├── requirements.txt         # Dependências Python
└── README.md               # Esta documentação
```

## Tecnologias Utilizadas

### Backend
- **Flask**: Framework web Python
- **ReportLab**: Geração de PDFs
- **Matplotlib**: Geração de gráficos e imagens
- **Flask-CORS**: Suporte a requisições cross-origin

### Frontend
- **HTML5/CSS3**: Estrutura e estilização
- **JavaScript**: Lógica da aplicação
- **Chart.js**: Gráficos interativos

### Armazenamento
- **Sessão Flask**: Dados temporários (sem banco de dados)
- **Memória**: Dados não persistem entre reinicializações

## Características Técnicas

### Responsividade
- Layout adaptável para desktop e mobile
- Tabela com scroll horizontal em telas pequenas
- Interface otimizada para touch

### Performance
- Carregamento rápido
- Atualizações em tempo real
- Cálculos automáticos de status

### Usabilidade
- Interface intuitiva similar à planilha original
- Cores padronizadas para status
- Feedback visual para ações do usuário

## Suporte e Manutenção

### Logs
- Logs do servidor disponíveis no console
- Erros JavaScript visíveis no console do navegador

### Backup
- Dados são temporários (sessão)
- Use "Gerar PDF" para backup permanente
- Considere implementar banco de dados para versões futuras

## Próximas Versões (Sugestões)

### 🔄 Melhorias Futuras
- **Banco de Dados**: Persistência de dados históricos
- **Autenticação**: Login de usuários
- **Relatórios Históricos**: Consulta de turnos anteriores
- **Notificações**: Alertas para atrasos
- **API REST**: Integração com outros sistemas
- **Backup Automático**: Salvamento periódico

### 📱 Mobile App
- Aplicativo nativo para smartphones
- Sincronização com versão web
- Notificações push

## Contato e Suporte

Para dúvidas, sugestões ou problemas:
- Documente o erro com screenshot
- Inclua informações do navegador
- Descreva os passos para reproduzir o problema

---

**Desenvolvido especificamente para controladores ferroviários**  
*Versão 1.0 - Agosto 2025*

