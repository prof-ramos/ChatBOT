# ChatBot Discord com OpenRouter

Bot Discord inteligente que responde usando modelos de IA através da API OpenRouter. O bot responde quando é mencionado em servidores ou quando recebe mensagens diretas (DM), **mantendo memória das conversas anteriores!**

## Funcionalidades

- ✅ Responde automaticamente quando mencionado em conversas
- ✅ Responde a mensagens diretas (DM)
- ✅ **Memória de conversas** - Lembra das últimas 10 mensagens de cada usuário
- ✅ **RAG (Retrieval-Augmented Generation)** - Busca documentos relevantes para melhorar respostas
- ✅ **Banco de dados vetorial** (ChromaDB) para armazenar e buscar documentos
- ✅ Usa modelos de IA da OpenRouter (acesso a 400+ modelos)
- ✅ Divide respostas longas automaticamente
- ✅ Mostra indicador "digitando..." enquanto processa
- ✅ **Banco de dados SQLite** para persistência de dados
- ✅ Estatísticas de uso por usuário e globais

## Comandos Disponíveis

### Conversa
- **`!ajuda`** - Mostra lista de comandos disponíveis
- **`!limpar`** - Limpa seu histórico de conversas com o bot
- **`!stats`** - Mostra suas estatísticas pessoais (total de mensagens, última interação)
- **`!stats_global`** - Mostra estatísticas globais do bot (total de usuários, mensagens)

### RAG (Base de Conhecimento)
- **`!adicionar <texto>`** - Adiciona um documento à base de conhecimento
- **`!buscar <termo>`** - Busca documentos similares na base de conhecimento
- **`!rag_stats`** - Mostra estatísticas da base de conhecimento (total de documentos)
- **`!limpar_rag`** - Limpa toda a base de conhecimento vetorial

## Configuração Necessária

### 1. Criar o Bot no Discord

1. Acesse o [Portal de Desenvolvedores do Discord](https://discord.com/developers/applications)
2. Clique em **New Application** e dê um nome ao seu bot
3. Vá na seção **Bot** no menu lateral
4. Clique em **Reset Token** para gerar um token
5. Copie o token e adicione como secret **TOKEN** no Replit

### 2. Habilitar Intents Privilegiados (IMPORTANTE)

No Portal de Desenvolvedores, na seção **Bot**:

1. Role até **Privileged Gateway Intents**
2. **ATIVE** as seguintes opções:
   - ✅ **MESSAGE CONTENT INTENT** (obrigatório para ler mensagens)
   - ✅ **SERVER MEMBERS INTENT** (opcional)
3. Clique em **Save Changes**

⚠️ **Sem esta configuração, o bot NÃO funcionará!**

### 3. Obter API Key da OpenRouter

1. Acesse [openrouter.ai/keys](https://openrouter.ai/keys)
2. Crie uma conta ou faça login
3. Clique em **Create Key**
4. Copie a chave e adicione como secret **OPENROUTER_API_KEY** no Replit

### 4. Adicionar o Bot ao Servidor

1. No Portal de Desenvolvedores, vá em **OAuth2** → **URL Generator**
2. Selecione os scopes:
   - `bot`
3. Selecione as permissões:
   - `Send Messages`
   - `Read Message History`
   - `Read Messages/View Channels`
4. Copie a URL gerada e abra no navegador
5. Selecione o servidor onde deseja adicionar o bot

## Como Usar

### Mencionar o Bot em um Canal

```
@SeuBot Olá, como você está?
@SeuBot Você lembra do que conversamos antes?
```

O bot mantém contexto das últimas 10 mensagens!

### Enviar DM (Mensagem Direta)

Envie uma mensagem direta ao bot e ele responderá automaticamente, lembrando de toda a conversa.

### Usar Comandos

```
!ajuda
!limpar
!stats
!stats_global
```

## RAG (Retrieval-Augmented Generation)

O bot utiliza **RAG** para melhorar as respostas combinando IA generativa com busca de documentos relevantes.

### Como Funciona:

1. **Adicionar documentos**: Use `!adicionar <texto>` para armazenar informações na base de conhecimento
2. **Busca automática**: Quando você faz uma pergunta, o bot busca automaticamente os 2 documentos mais relevantes
3. **Contexto enriquecido**: Os documentos encontrados são incluídos no contexto da IA para gerar respostas mais precisas
4. **Embeddings**: Usa OpenRouter API para criar representações vetoriais dos documentos

### Exemplos de Uso:

```
!adicionar A empresa XYZ foi fundada em 2020 e tem 50 funcionários.
!adicionar O produto ABC custa R$ 299,90 e tem garantia de 2 anos.

@Bot Quando a empresa XYZ foi fundada?
```

O bot vai buscar o documento relevante e responder com base nele!

## Persistência de Dados

### Banco de Dados SQLite
O bot usa **SQLite** (`bot_data.db`) para armazenar:

- **Histórico de conversas** - Últimas 10 mensagens de cada usuário
- **Informações de usuários** - ID, nome de usuário, data de cadastro
- **Estatísticas** - Contadores de mensagens e última interação

### Banco de Dados Vetorial (ChromaDB)
O bot usa **ChromaDB** (`./chroma_db/`) para armazenar:

- **Documentos embedados** - Representações vetoriais dos textos adicionados
- **Metadados** - Autor, data, e outras informações sobre os documentos
- **Índices de busca** - Para busca rápida por similaridade semântica

## Variáveis de Ambiente

Configure estas secrets no Replit:

- **TOKEN**: Token do bot Discord
- **OPENROUTER_API_KEY**: Chave de API da OpenRouter (para respostas do chat)
- **OPENAI_API_KEY**: Chave de API da OpenAI (para embeddings/RAG)

### Sobre os Embeddings

O sistema RAG usa a API da OpenAI para criar embeddings (representações vetoriais) dos documentos. O modelo padrão é `text-embedding-3-small`, que é muito econômico:

- **Custo**: ~$0.02 por 1 milhão de tokens (aproximadamente 750.000 palavras)
- **Uso típico**: Alguns centavos por mês para uso normal do bot

**Importante**: Você precisa adicionar créditos na sua conta OpenAI para usar embeddings:
1. Acesse https://platform.openai.com/settings/organization/billing
2. Adicione um método de pagamento
3. Compre créditos (mínimo $5)

## Modelo de IA Utilizado

Por padrão, o bot usa o modelo `meta-llama/llama-3.1-8b-instruct:free` (gratuito).

Você pode alterar o modelo editando a linha 46 do arquivo `main.py`:

```python
"model": "meta-llama/llama-3.1-8b-instruct:free",
```

Outros modelos disponíveis:
- `openai/gpt-4-turbo`
- `anthropic/claude-3.5-sonnet`
- `google/gemini-pro-1.5`
- `meta-llama/llama-3-70b-instruct`

Veja todos os modelos em: [openrouter.ai/models](https://openrouter.ai/models)

## Estrutura do Banco de Dados

### Tabela: users
- `user_id` (TEXT, PRIMARY KEY) - ID do usuário Discord
- `username` (TEXT) - Nome do usuário
- `created_at` (TIMESTAMP) - Data de cadastro

### Tabela: messages
- `id` (INTEGER, PRIMARY KEY) - ID da mensagem
- `user_id` (TEXT) - ID do usuário
- `role` (TEXT) - "user" ou "assistant"
- `content` (TEXT) - Conteúdo da mensagem
- `timestamp` (TIMESTAMP) - Data e hora da mensagem

### Tabela: stats
- `user_id` (TEXT, PRIMARY KEY) - ID do usuário
- `message_count` (INTEGER) - Total de mensagens enviadas
- `last_interaction` (TIMESTAMP) - Última interação com o bot

## Solução de Problemas

### Erro: PrivilegedIntentsRequired

**Causa**: O Intent MESSAGE CONTENT não está habilitado no Portal de Desenvolvedores.

**Solução**: Siga o passo 2 da configuração acima para habilitar os Intents Privilegiados.

### Erro: 429 Too Many Requests

**Causa**: Muitas requisições ao Discord em curto período.

**Solução**: Aguarde alguns minutos antes de reiniciar o bot.

### Bot não responde

Verifique:
1. ✅ Os intents estão habilitados no Portal de Desenvolvedores
2. ✅ As variáveis TOKEN e OPENROUTER_API_KEY estão configuradas
3. ✅ O bot foi adicionado ao servidor com as permissões corretas
4. ✅ O workflow "Discord Bot" está rodando (veja o console)

### Bot não lembra de conversas anteriores

- Use `!limpar` para resetar seu histórico se algo der errado
- O bot mantém apenas as últimas 10 mensagens por usuário
- O histórico é específico de cada usuário (conversas em DM e menções são tratadas juntas)

## Tecnologias

- Python 3.10
- discord.py 2.6.4
- aiohttp 3.13.1
- SQLite3 (built-in)
- OpenRouter API

## Script de Importação em Massa

Para adicionar vários documentos de uma vez, use o script importador:

```bash
python import_documents.py <diretório>
```

**Exemplo**:
```bash
# Importar todos os PDFs e DOCXs de uma pasta
python import_documents.py ./meus_documentos
```

O script processa automaticamente todos os arquivos PDF, DOCX e DOC do diretório, extrai o texto e adiciona ao banco vetorial.

📖 **[Ver documentação completa do importador](README_IMPORTADOR.md)**

## Arquitetura

- `main.py` - Lógica principal do bot Discord e integração com OpenRouter
- `database.py` - Funções para gerenciar o banco de dados SQLite
- `vector_db.py` - Funções para gerenciar o banco vetorial (ChromaDB + embeddings)
- `import_documents.py` - Script para importar documentos em massa
- `bot_data.db` - Arquivo do banco de dados SQLite (criado automaticamente)
- `chroma_db/` - Diretório do banco vetorial ChromaDB (criado automaticamente)

## Licença

Este é um projeto de código aberto para fins educacionais.
