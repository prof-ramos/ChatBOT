# Relatório de Problema: Sistema RAG Desabilitado

## 📋 Resumo Executivo

O sistema RAG (Retrieval-Augmented Generation) do chatbot Discord foi temporariamente desabilitado devido a conflitos de dependências entre ChromaDB e Python 3.14. O bot está funcionando normalmente para conversas básicas, mas sem a capacidade de buscar em documentos armazenados.

## 🔍 Detalhes do Problema

### Contexto
- **Data de identificação**: 21 de outubro de 2025
- **Ambiente**: Python 3.14.0, macOS
- **Componente afetado**: Sistema RAG (ChromaDB + OpenAI embeddings)
- **Impacto**: Funcionalidades de busca em documentos desabilitadas

### Sintomas Observados

1. **Erro de instalação**: `ModuleNotFoundError: No module named 'chromadb'`
2. **Conflitos de dependências**: Múltiplas versões do ChromaDB testadas falharam
3. **Dependência faltante**: `pulsar-client` não disponível para Python 3.14
4. **Degradação funcional**: Bot opera sem RAG, apenas conversas básicas

### Tentativas de Resolução

#### 1. Instalação Direta
```bash
pip install chromadb
# Resultado: Conflitos de resolução de dependências
```

#### 2. Versões Específicas
```bash
pip install chromadb==0.4.24  # Falhou: pulsar-client não encontrado
pip install chromadb==0.3.29  # Instalado, mas dependências incompatíveis
```

#### 3. Dependências Manuais
```bash
pip install overrides requests fastapi uvicorn posthog
# Resultado: ChromaDB ainda sem dependências críticas
```

#### 4. Modificação do Código
- Comentadas todas as referências ao `vector_store`
- Sistema RAG completamente desabilitado
- Bot funcionando com funcionalidades básicas

## 🛠️ Análise Técnica

### Dependências Problemáticas

| Dependência | Status | Problema |
|-------------|--------|----------|
| `chromadb` | ❌ | Conflitos de versão |
| `pulsar-client` | ❌ | Não disponível para Python 3.14 |
| `hnswlib` | ⚠️ | Instalado, mas incompatível |
| `chroma-hnswlib` | ❌ | Falha na compilação |

### Impacto no Sistema

#### Funcionalidades Afetadas
- ❌ `!adicionar` - Adicionar documentos à base de conhecimento
- ❌ `!buscar` - Buscar documentos relevantes
- ❌ `!rag_stats` - Estatísticas do RAG
- ❌ `!limpar_rag` - Limpar base de conhecimento
- ❌ Busca automática de contexto em conversas

#### Funcionalidades Operacionais
- ✅ Conversas com IA via OpenRouter
- ✅ Histórico de conversas (SQLite)
- ✅ Comandos básicos (!ajuda, !stats, !limpar)
- ✅ Sistema de logging implementado

## 📊 Métricas de Impacto

### Antes do Problema
- **Conversas**: Com contexto RAG (2 documentos relevantes)
- **Precisão**: Alta (contexto relevante injetado)
- **Funcionalidades**: 100% operacionais

### Após Desabilitação
- **Conversas**: Sem contexto RAG (apenas histórico)
- **Precisão**: Média (baseado apenas em histórico)
- **Funcionalidades**: 60% operacionais

## 🔧 Soluções Propostas

### Solução 1: Downgrade do Python (Recomendada)
```bash
# Usar Python 3.11 ou 3.12
pyenv install 3.11.9
pyenv local 3.11.9
pip install chromadb==0.4.18
```

**Vantagens:**
- Compatibilidade garantida
- Todas as funcionalidades RAG
- Melhor performance

**Desvantagens:**
- Requer mudança de versão Python
- Possível impacto em outros projetos

### Solução 2: Docker (Alternativa Segura)
```bash
docker build -t discord-bot-rag .
docker-compose up -d
```

**Vantagens:**
- Ambiente isolado
- Versão Python controlada
- Fácil deployment

**Desvantagens:**
- Overhead de container
- Curva de aprendizado Docker

### Solução 3: Alternativa ao ChromaDB
- **Pinecone**: Serviço gerenciado
- **Weaviate**: Base vetorial alternativa
- **FAISS**: Biblioteca mais leve
- **Qdrant**: Alternativa open-source

**Vantagens:**
- Melhor compatibilidade
- Possível melhor performance

**Desvantagens:**
- Requer refatoração do código
- Mudança de arquitetura

### Solução 4: RAG Temporário Desabilitado (Atual)
- Manter bot funcional
- Implementar logging detalhado
- Planejar migração futura

## 📈 Plano de Ação Recomendado

### Fase 1: Estabilização (Imediata)
1. ✅ Implementar sistema de logging abrangente
2. ✅ Documentar problema completamente
3. ✅ Manter bot operacional com funcionalidades básicas

### Fase 2: Resolução (Curto Prazo - 1 semana)
1. Escolher solução (Docker ou downgrade Python)
2. Implementar solução escolhida
3. Testar funcionalidades RAG
4. Reabilitar comandos desabilitados

### Fase 3: Otimização (Médio Prazo)
1. Considerar alternativas ao ChromaDB se necessário
2. Implementar métricas de performance
3. Melhorar tratamento de erros

## 📋 Logs de Erro

### Log Principal
```
[2025-10-21 09:01:59] [INFO    ] discord.client: logging in using static token
[2025-10-21 09:02:00] [INFO    ] discord.gateway: Connected to Gateway
[2025-10-21 09:02:00] [WARNING ] discord_bot: RAG system temporarily disabled due to ChromaDB dependency issues
```

### Erros de Dependência
```
ERROR: Could not find a version that satisfies the requirement pulsar-client>=3.1.0
ERROR: No matching distribution found for pulsar-client
ModuleNotFoundError: No module named 'chromadb'
```

## 🎯 Conclusão

O problema do RAG representa uma degradação temporária das funcionalidades, mas não impede o funcionamento básico do bot. A solução mais adequada seria utilizar Docker para garantir um ambiente controlado e compatível, permitindo a reabilitação completa do sistema RAG sem impactar outros projetos Python no sistema.

**Status**: Sistema RAG desabilitado, bot operacional com funcionalidades básicas.
**Prioridade**: Alta - afetando experiência do usuário.
**Prazo estimado para resolução**: 1 semana.