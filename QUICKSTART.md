# 🚀 Quick Start Guide

Guia rápido para começar a usar o sistema GitHub completo que foi criado.

## ⚡ Configuração Inicial (5 minutos)

### 1. Configure as Credenciais

```bash
# Edite o arquivo .env com suas credenciais
nano .env
# ou
code .env
```

Preencha com suas chaves:
```env
TOKEN=seu_token_discord_aqui
OPENROUTER_API_KEY=sua_chave_openrouter_aqui
OPENAI_API_KEY=sua_chave_openai_aqui
```

### 2. Commit e Push para GitHub

```bash
# Adicione os novos arquivos
git add .github/ CLAUDE.md CONTRIBUTING.md PROJECT_HEALTH_REPORT.md .env.example QUICKSTART.md

# Faça o commit
git commit -m "feat: add complete GitHub system with CI/CD, CodeRabbit, and comprehensive docs

- Add CI/CD pipeline with linting, testing, and security scanning
- Add automated release workflow with semantic versioning
- Add CodeRabbit configuration for AI code reviews in Portuguese
- Add PR and issue templates
- Add comprehensive documentation (CLAUDE.md, CONTRIBUTING.md)
- Add project health report (score: 68/100)
- Add dependency monitoring and CodeQL security analysis
"

# Push para o GitHub
git push origin main
```

### 3. Verifique os Workflows

Acesse: `https://github.com/seu-usuario/ChatBOT/actions`

Você deve ver os workflows rodando:
- ✅ CI/CD Pipeline
- ✅ CodeQL Analysis

## 🎯 Criar Primeiro Release (2 minutos)

### Opção 1: Via GitHub UI (Recomendado)

1. Acesse: `https://github.com/seu-usuario/ChatBOT/actions`
2. Clique em "Release & Tag Management" no menu lateral
3. Clique em "Run workflow"
4. Escolha:
   - Branch: `main`
   - Release type: `major` (para criar v1.0.0)
5. Clique em "Run workflow"

### Opção 2: Via Git (Manual)

```bash
# Crie a tag
git tag -a v1.0.0 -m "Release v1.0.0 - Initial release with RAG chatbot"

# Push da tag
git push origin v1.0.0

# Depois crie o release manualmente no GitHub UI
```

## 🔧 Configurar GitHub Settings (5 minutos)

### 1. Branch Protection

1. Vá em: `Settings → Branches → Add rule`
2. Branch name pattern: `main`
3. Ative:
   - ✅ Require pull request before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require conversation resolution before merging
4. Salve

### 2. Habilitar Security Features

1. Vá em: `Settings → Code security and analysis`
2. Ative tudo:
   - ✅ Dependency graph
   - ✅ Dependabot alerts
   - ✅ Dependabot security updates
   - ✅ Secret scanning

### 3. Habilitar Features

1. Vá em: `Settings → General → Features`
2. Ative:
   - ✅ Issues
   - ✅ Projects (opcional)
   - ✅ Discussions (opcional)

## 🤖 Configurar CodeRabbit (Opcional - 3 minutos)

1. Acesse: https://coderabbit.ai/
2. Faça login com GitHub
3. Autorize acesso ao repositório ChatBOT
4. CodeRabbit começará a revisar PRs automaticamente

**Configuração já está pronta!** O arquivo `.github/.coderabbit.yaml` já foi criado.

## ✅ Checklist de Configuração

Use este checklist para garantir que tudo está configurado:

### Básico
- [ ] Arquivo `.env` configurado com credenciais
- [ ] `.env` está no `.gitignore` (já está ✅)
- [ ] Commit e push dos novos arquivos feito
- [ ] Workflows executando no GitHub Actions

### GitHub Settings
- [ ] Branch protection configurado em `main`
- [ ] Dependabot alerts habilitado
- [ ] Secret scanning habilitado
- [ ] CodeQL analysis executando

### Releases
- [ ] Primeiro release v1.0.0 criado
- [ ] Tag v1.0.0 existe
- [ ] Workflow de release testado

### CodeRabbit (Opcional)
- [ ] CodeRabbit instalado no repositório
- [ ] Configuração `.coderabbit.yaml` funcionando
- [ ] Primeiro PR revisado pelo CodeRabbit

## 📚 Próximos Passos

### Esta Semana
1. **Adicionar testes básicos** (Prioridade Alta)
   ```bash
   # Instalar pytest
   pip install pytest pytest-asyncio pytest-cov

   # Criar primeiro teste
   # Ver exemplos em CONTRIBUTING.md
   ```

2. **Limpar dependências duplicadas**
   ```bash
   # Remover pacotes não usados/duplicados
   pip uninstall fitz docx  # se confirmado não uso
   ```

3. **Testar o bot localmente**
   ```bash
   python main.py
   # Testar comandos no Discord
   ```

### Próximo Mês
4. Aumentar coverage de testes para 50%
5. Buscar 1-2 colaboradores
6. Criar 2-3 releases
7. Implementar monitoring básico

### 3 Meses
8. Coverage 70%+
9. 3+ colaboradores ativos
10. 5+ releases
11. Health score 80+

## 🆘 Troubleshooting

### Workflows não estão executando

**Problema**: Workflows não aparecem em Actions

**Solução**:
```bash
# Verifique se os arquivos estão no local correto
ls -la .github/workflows/

# Devem existir: ci.yml, release.yml, codeql.yml, dependency-update.yml
```

### CI está falhando

**Problema**: Linters/testes falhando

**Solução**:
```bash
# Execute localmente para ver os erros
ruff check .
black --check .
pytest

# Corrija os erros e faça novo commit
```

### Release não está criando

**Problema**: Workflow de release não funciona

**Solução**:
1. Verifique permissões em: Settings → Actions → General
2. Em "Workflow permissions", selecione "Read and write permissions"
3. Execute o workflow novamente

### CodeRabbit não está revisando

**Problema**: CodeRabbit instalado mas não faz reviews

**Solução**:
1. Verifique que `.coderabbit.yaml` existe em `.github/`
2. Faça novo commit para trigger
3. Aguarde alguns minutos (primeira vez pode demorar)

## 📖 Documentação

- **[README.md](README.md)** - Documentação do usuário
- **[CLAUDE.md](CLAUDE.md)** - Guia técnico para Claude Code
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guia para contribuidores
- **[PROJECT_HEALTH_REPORT.md](PROJECT_HEALTH_REPORT.md)** - Análise completa do projeto
- **[.github/SETUP_SUMMARY.md](.github/SETUP_SUMMARY.md)** - Resumo detalhado do setup

## 💡 Dicas

### Desenvolvimento Diário

```bash
# Antes de começar a trabalhar
git pull origin main

# Crie uma branch para sua feature
git checkout -b feature/minha-feature

# Faça suas mudanças e teste
ruff check .
black .
pytest

# Commit e push
git add .
git commit -m "feat: minha nova feature"
git push origin feature/minha-feature

# Crie PR no GitHub
# CodeRabbit vai revisar automaticamente!
```

### Comandos Úteis

```bash
# Ver saúde do projeto
cat PROJECT_HEALTH_REPORT.md

# Ver todos os workflows
gh workflow list  # requer GitHub CLI

# Ver status do último run
gh run list --limit 5

# Ver logs de um workflow
gh run view

# Criar release manualmente
gh release create v1.0.0 --generate-notes
```

## 🎉 Pronto!

Seu projeto agora está com:
- ✅ CI/CD automático
- ✅ Releases automáticas
- ✅ CodeRabbit configurado
- ✅ Security scanning
- ✅ Documentação completa

**Happy coding! 🚀**
