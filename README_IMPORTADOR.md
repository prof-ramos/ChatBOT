# Script Importador de Documentos

Este script permite importar documentos em massa (PDF, DOCX, DOC) para o banco vetorial do bot Discord, facilitando a criação de uma base de conhecimento.

## Uso

```bash
python import_documents.py <diretório>
```

## Exemplos

```bash
# Importar todos os documentos de uma pasta
python import_documents.py ./meus_documentos

# Importar documentos de um caminho absoluto
python import_documents.py /home/user/arquivos_empresa
```

## Formatos Suportados

- ✅ **PDF** (.pdf) - Extração de texto usando PyMuPDF
- ✅ **DOCX** (.docx) - Documentos Word modernos usando python-docx
- ✅ **DOC** (.doc) - Documentos Word antigos (conversão limitada)

## Como Funciona

1. **Busca arquivos**: Varre o diretório procurando arquivos .pdf, .docx e .doc
2. **Extrai texto**: Processa cada arquivo extraindo todo o texto
3. **Cria embeddings**: Usa a API OpenAI para gerar representações vetoriais
4. **Armazena no ChromaDB**: Salva os documentos no banco vetorial para busca

## Metadados Armazenados

Para cada documento, o script salva:

- `filename` - Nome do arquivo
- `filepath` - Caminho completo do arquivo
- `filetype` - Tipo de arquivo (.pdf, .docx, .doc)
- `imported_at` - Data e hora da importação
- `word_count` - Número de palavras extraídas
- `char_count` - Número de caracteres extraídos

## Requisitos

### 1. Chave da API OpenAI

Você precisa ter uma chave da OpenAI configurada nos Secrets do Replit:

- **OPENAI_API_KEY**: Sua chave de API
- A conta precisa ter créditos disponíveis (mínimo $5)

### 2. Bibliotecas Python

As seguintes bibliotecas são instaladas automaticamente:

- `pymupdf` - Processamento de PDFs
- `python-docx` - Processamento de DOCX
- `docx2txt` - Processamento alternativo de DOCX/DOC
- `chromadb` - Banco de dados vetorial
- `openai` - API de embeddings

## Saída Esperada

```
============================================================
📚 IMPORTADOR DE DOCUMENTOS - Bot Discord RAG
============================================================

🔧 Inicializando banco vetorial...
✅ Banco vetorial inicializado. Coleções: 1

🔍 Procurando documentos em: /caminho/para/documentos
📚 Encontrados 5 documento(s)
============================================================

📄 Processando: relatorio.pdf
   📊 Texto extraído: 1523 palavras, 9845 caracteres
   ✅ Adicionado ao banco vetorial!

📄 Processando: manual.docx
   📊 Texto extraído: 3421 palavras, 21032 caracteres
   ✅ Adicionado ao banco vetorial!

📄 Processando: procedimentos.pdf
   📊 Texto extraído: 892 palavras, 5634 caracteres
   ✅ Adicionado ao banco vetorial!

============================================================

📊 Resumo da importação:
   ✅ Sucesso: 3 documento(s)
   ❌ Falhas: 0 documento(s)
   📦 Total: 3 arquivo(s) processados

💾 Total de documentos no banco vetorial: 3

✅ Importação concluída!
============================================================
```

## Erros Comuns

### Erro: OPENAI_API_KEY não configurada

**Causa**: A chave da API não foi adicionada aos Secrets.

**Solução**: 
1. Vá em Secrets (🔒) no painel do Replit
2. Adicione `OPENAI_API_KEY` com sua chave da OpenAI

### Erro: 429 - Quota Exceeded

**Causa**: Sua conta OpenAI não tem créditos suficientes.

**Solução**:
1. Acesse https://platform.openai.com/settings/organization/billing
2. Adicione créditos à sua conta (mínimo $5)

### Erro ao ler arquivo DOC

**Causa**: Arquivos .doc antigos (formato binário) têm suporte limitado.

**Solução**:
1. Converta o arquivo .doc para .docx usando Microsoft Word ou LibreOffice
2. Ou use um conversor online: https://www.zamzar.com/convert/doc-to-docx/

### Nenhum texto extraído

**Causa**: O arquivo pode estar vazio, corrompido ou ser uma imagem escaneada.

**Solução**:
- Para PDFs escaneados, você precisaria de OCR (reconhecimento óptico de caracteres)
- Verifique se o arquivo abre normalmente em um leitor de PDF/Word

## Custos

O custo para processar documentos depende do tamanho:

| Documentos | Palavras | Custo Aprox. |
|------------|----------|--------------|
| 10 PDFs pequenos | ~5.000 | $0.0001 |
| 50 PDFs médios | ~50.000 | $0.001 |
| 100 documentos grandes | ~200.000 | $0.005 |

**Modelo usado**: `text-embedding-3-small` (~$0.02 por 1M tokens)

## Dicas de Uso

### 1. Organize seus documentos

```
meus_documentos/
├── manuais/
│   ├── manual_produto.pdf
│   └── guia_usuario.docx
├── politicas/
│   ├── politica_privacidade.pdf
│   └── termos_uso.pdf
└── tutoriais/
    └── como_usar.docx
```

Importe cada pasta separadamente para melhor organização.

### 2. Nomes de arquivo descritivos

Use nomes claros e descritivos para seus arquivos:
- ✅ `manual_instalacao_produto_xyz.pdf`
- ❌ `documento1.pdf`

### 3. Verifique antes de importar

Execute o script primeiro para ver quantos documentos serão processados antes de confirmar.

### 4. Monitore o banco vetorial

Use o comando `!rag_stats` no Discord para ver quantos documentos foram adicionados.

## Próximos Passos

Após importar os documentos:

1. **Teste a busca**: Use `!buscar <termo>` no Discord para verificar se os documentos foram indexados
2. **Faça perguntas**: Mencione o bot e faça perguntas relacionadas aos documentos importados
3. **Verifique relevância**: O bot automaticamente busca os 2 documentos mais relevantes para cada pergunta

## Arquivo de Exemplo

Foi criado um diretório `documentos_exemplo/` com um PDF de teste. Você pode usá-lo para testar o script:

```bash
python import_documents.py documentos_exemplo
```
