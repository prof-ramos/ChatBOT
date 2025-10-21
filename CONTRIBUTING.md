# Guia de Contribuição - ChatBOT Discord RAG

Obrigado por considerar contribuir com o ChatBOT! Este documento fornece diretrizes para contribuir com o projeto.

## 🚀 Como Começar

### 1. Setup do Ambiente de Desenvolvimento

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/ChatBOT.git
cd ChatBOT

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install discord.py aiohttp chromadb openai pymupdf python-docx docx2txt

# Instale ferramentas de desenvolvimento
pip install pytest pytest-asyncio pytest-cov pytest-mock
pip install ruff black isort mypy bandit
```

### 2. Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
TOKEN=seu_token_discord
OPENROUTER_API_KEY=sua_chave_openrouter
OPENAI_API_KEY=sua_chave_openai
```

### 3. Verifique se Tudo Funciona

```bash
# Execute os testes (quando disponíveis)
pytest

# Execute o linter
ruff check .

# Execute o formatador
black --check .

# Teste o bot localmente
python main.py
```

## 📋 Processo de Contribuição

### Fluxo de Trabalho

1. **Fork** o repositório
2. **Clone** seu fork localmente
3. **Crie uma branch** para sua feature/fix
4. **Faça suas mudanças** com commits descritivos
5. **Execute os testes** e linters
6. **Push** para seu fork
7. **Abra um Pull Request**

### Convenções de Branches

```
feature/nome-da-feature    # Nova funcionalidade
fix/nome-do-bug           # Correção de bug
docs/nome-da-doc          # Documentação
refactor/nome-refactor    # Refatoração
test/nome-teste           # Adição de testes
```

**Exemplo:**
```bash
git checkout -b feature/adicionar-comando-estatisticas
```

### Convenções de Commits

Seguimos o padrão [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação (sem mudança de código)
- `refactor`: Refatoração de código
- `test`: Adição/modificação de testes
- `chore`: Tarefas de manutenção

**Exemplos:**
```bash
feat(commands): add !export command to export chat history
fix(rag): resolve embedding generation error for large documents
docs(readme): update installation instructions for Windows
test(database): add tests for conversation history retrieval
refactor(vector_db): improve error handling in search_similar
```

## 🧪 Testes

### Executando Testes

```bash
# Todos os testes
pytest

# Com coverage
pytest --cov=. --cov-report=html

# Apenas um arquivo
pytest test_database.py

# Apenas um teste específico
pytest test_database.py::test_add_user
```

### Escrevendo Testes

Crie testes para toda nova funcionalidade:

```python
# test_database.py
import pytest
from database import add_user, get_user_stats

def test_add_user():
    """Testa adição de novo usuário"""
    user_id = "test_123"
    username = "TestUser"

    add_user(user_id, username)
    stats = get_user_stats(user_id)

    assert stats is not None
    assert stats["username"] == username
    assert stats["message_count"] == 0
```

**Boas práticas:**
- Use fixtures do pytest para setup/teardown
- Mocke APIs externas (Discord, OpenRouter, OpenAI)
- Teste casos de erro, não apenas happy path
- Mantenha testes rápidos (<1s cada)

## 🎨 Style Guide

### Python Code Style

Seguimos PEP 8 com algumas adaptações:

```python
# Use type hints
def get_conversation_history(user_id: str, limit: int = 10) -> List[Dict[str, str]]:
    """
    Retorna o histórico de conversas de um usuário.

    Args:
        user_id: ID do usuário Discord
        limit: Número máximo de mensagens (padrão: 10)

    Returns:
        Lista de dicionários com role e content
    """
    pass

# Use docstrings estilo Google
# Evite funções muito longas (>50 linhas)
# Prefira comprehensions quando apropriado
# Use f-strings para formatação
```

### Ferramentas Automáticas

```bash
# Formatação automática
black .

# Ordenação de imports
isort .

# Linting
ruff check .

# Type checking
mypy --ignore-missing-imports *.py
```

### Pre-commit Hooks

Configure hooks para validação automática:

```bash
# Instale pre-commit
pip install pre-commit

# Instale os hooks
pre-commit install

# Execute manualmente
pre-commit run --all-files
```

## 📝 Documentação

### README Updates

Atualize o README quando:
- Adicionar novos comandos
- Mudar configuração
- Adicionar novas dependências
- Mudar processo de instalação

### CLAUDE.md Updates

Atualize o CLAUDE.md quando:
- Modificar arquitetura
- Adicionar novos módulos
- Mudar fluxo de dados
- Adicionar patterns importantes

### Code Comments

```python
# Use comentários para explicar "por quê", não "o quê"

# ❌ Ruim
# Incrementa o contador
counter += 1

# ✅ Bom
# Incrementamos aqui porque Discord API pode enviar duplicatas
# Ver issue #123
counter += 1
```

## 🐛 Reportando Bugs

Use o template de issue para bugs:

1. Acesse [Issues](https://github.com/seu-usuario/ChatBOT/issues/new)
2. Escolha "Bug Report"
3. Preencha todas as seções
4. Adicione screenshots/logs se possível

**Informações importantes:**
- Comando exato executado
- Mensagem de erro completa
- Ambiente (Python version, OS)
- Steps para reproduzir

## 💡 Sugerindo Features

Use o template de issue para features:

1. Descreva o problema que a feature resolve
2. Explique a solução proposta
3. Considere alternativas
4. Dê exemplos de uso

## 🔍 Code Review

### Para Revisores

- ✅ Verifique que testes passam
- ✅ Revise lógica e segurança
- ✅ Confirme que segue style guide
- ✅ Teste localmente se necessário
- ✅ Seja construtivo e educado

### Para Autores

- ✅ Responda a todos os comentários
- ✅ Faça mudanças solicitadas
- ✅ Re-execute testes após mudanças
- ✅ Agradeça os revisores

## 🏗️ Áreas para Contribuir

### Alta Prioridade
- [ ] Adicionar testes (coverage atual: 0%)
- [ ] Implementar logging estruturado
- [ ] Adicionar validação de inputs
- [ ] Melhorar tratamento de erros

### Média Prioridade
- [ ] Novos comandos Discord
- [ ] Melhorias no RAG
- [ ] Performance optimization
- [ ] Documentação adicional

### Boas First Issues
- [ ] Adicionar mais tipos de arquivo ao importador
- [ ] Melhorar mensagens de erro
- [ ] Adicionar mais exemplos ao README
- [ ] Criar tests básicos

## 🎯 Diretrizes Específicas

### Adicionando Novos Comandos

1. Adicione o handler em `main.py:on_message()`
2. Implemente a lógica
3. Atualize o comando `!ajuda`
4. Adicione testes
5. Documente no README

**Exemplo:**
```python
if user_message.lower() == '!meu_comando':
    # Lógica do comando
    result = processar_comando()
    await message.channel.send(result)
    return
```

### Modificando o RAG

- Sempre teste com documentos reais
- Verifique custos de API (embeddings)
- Considere performance com muitos docs
- Documente metadados armazenados

### Trabalhando com Banco de Dados

- Use prepared statements (já fazemos)
- Sempre feche conexões
- Teste com banco limpo
- Considere migrations para mudanças

## 🔒 Segurança

### Reportando Vulnerabilidades

**NÃO** abra issues públicas para vulnerabilidades!

Use: [Security Advisories](https://github.com/seu-usuario/ChatBOT/security/advisories/new)

### Checklist de Segurança

- [ ] Nenhum secret hardcoded
- [ ] Input validation implementada
- [ ] SQL injection prevention (prepared statements)
- [ ] Rate limiting considerado
- [ ] Error messages não vazam info sensível

## 📞 Contato

- **Issues**: Para bugs e features
- **Discussions**: Para perguntas e ideias
- **Pull Requests**: Para contribuições de código

## 🙏 Reconhecimento

Todos os contribuidores serão adicionados ao README na seção Contributors.

---

**Obrigado por contribuir! 🎉**
