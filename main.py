import os
import aiohttp
import discord
import database
import vector_db

intents = discord.Intents.default()
intents.message_content = True
intents.members = False
intents.presences = False

client = discord.Client(intents=intents)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or ""
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"


async def get_ai_response(user_message: str, conversation_history: list = None, rag_context: str = None) -> str:
    """Envia mensagem para OpenRouter com histórico de conversa e contexto RAG"""
    if not OPENROUTER_API_KEY:
        return "Erro: OPENROUTER_API_KEY não configurada. Por favor, adicione a chave nas variáveis de ambiente."
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_message = "Você é um assistente útil e amigável que responde em português. Você mantém o contexto das conversas anteriores."
    
    if rag_context:
        system_message += f"\n\nContexto relevante da base de conhecimento:\n{rag_context}"
    
    messages = [
        {
            "role": "system",
            "content": system_message
        }
    ]
    
    if conversation_history:
        messages.extend(conversation_history)
    
    messages.append({
        "role": "user",
        "content": user_message
    })
    
    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct:free",
        "messages": messages
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(OPENROUTER_BASE_URL, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    error_text = await response.text()
                    return f"Erro ao conectar com a IA (código {response.status}): {error_text}"
    except Exception as e:
        return f"Erro ao processar sua mensagem: {str(e)}"


@client.event
async def on_ready():
    database.init_database()
    vector_db.init_vector_db()
    print(f'Bot conectado como {client.user}')
    print(f'ID: {client.user.id}')
    print('------')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    is_dm = isinstance(message.channel, discord.DMChannel)
    is_mentioned = client.user in message.mentions
    
    if is_dm or is_mentioned:
        user_message = message.content.replace(f'<@{client.user.id}>', '').replace(f'<@!{client.user.id}>', '').strip()
        
        user_id = str(message.author.id)
        username = str(message.author)
        
        if user_message.lower() == '!limpar':
            database.clear_user_history(user_id)
            await message.channel.send("✅ Seu histórico de conversas foi limpo! Vamos começar uma nova conversa.")
            return
        
        if user_message.lower().startswith('!adicionar '):
            doc_text = user_message[11:].strip()
            if not doc_text:
                await message.channel.send("❌ Use: `!adicionar <texto do documento>`")
                return
            
            async with message.channel.typing():
                doc_id = await vector_db.add_document(
                    doc_text,
                    metadata={"author": username, "author_id": user_id}
                )
                
                if doc_id:
                    await message.channel.send(f"✅ Documento adicionado à base de conhecimento!\nID: `{doc_id}`")
                else:
                    await message.channel.send("❌ Erro ao adicionar documento.")
            return
        
        if user_message.lower().startswith('!buscar '):
            query = user_message[8:].strip()
            if not query:
                await message.channel.send("❌ Use: `!buscar <termo de busca>`")
                return
            
            async with message.channel.typing():
                results = await vector_db.search_similar(query, n_results=3)
                
                if results:
                    response = "🔍 **Documentos Encontrados:**\n\n"
                    for i, doc in enumerate(results, 1):
                        response += f"**{i}.** {doc['text'][:200]}{'...' if len(doc['text']) > 200 else ''}\n"
                        if doc['metadata']:
                            response += f"   📝 Autor: {doc['metadata'].get('author', 'Desconhecido')}\n"
                        response += "\n"
                    await message.channel.send(response)
                else:
                    await message.channel.send("❌ Nenhum documento encontrado.")
            return
        
        if user_message.lower() == '!rag_stats':
            doc_count = vector_db.count_documents()
            collections = vector_db.list_collections()
            
            response = f"📚 **Estatísticas do RAG:**\n"
            response += f"📄 Total de documentos: {doc_count}\n"
            response += f"📁 Coleções: {', '.join(collections) if collections else 'Nenhuma'}"
            await message.channel.send(response)
            return
        
        if user_message.lower() == '!limpar_rag':
            success = vector_db.delete_all_documents()
            if success:
                await message.channel.send("✅ Base de conhecimento limpa!")
            else:
                await message.channel.send("❌ Erro ao limpar base de conhecimento.")
            return
        
        if user_message.lower() == '!stats':
            stats = database.get_user_stats(user_id)
            if stats:
                response = f"📊 **Suas Estatísticas:**\n"
                response += f"👤 Usuário: {stats['username']}\n"
                response += f"💬 Total de mensagens: {stats['message_count']}\n"
                response += f"🕐 Última interação: {stats['last_interaction']}"
                await message.channel.send(response)
            else:
                await message.channel.send("Ainda não há estatísticas para você.")
            return
        
        if user_message.lower() == '!stats_global':
            stats = database.get_total_stats()
            response = f"📊 **Estatísticas Globais do Bot:**\n"
            response += f"👥 Total de usuários: {stats['total_users']}\n"
            response += f"💬 Total de mensagens: {stats['total_messages']}\n"
            response += f"📨 Mensagens de usuários: {stats['user_messages']}\n"
            response += f"🤖 Respostas do bot: {stats['bot_responses']}"
            await message.channel.send(response)
            return
        
        if user_message.lower() == '!ajuda':
            help_text = """
📚 **Comandos Disponíveis:**

**Conversa:**
`!limpar` - Limpa seu histórico de conversas
`!stats` - Mostra suas estatísticas pessoais
`!stats_global` - Mostra estatísticas globais do bot

**RAG (Base de Conhecimento):**
`!adicionar <texto>` - Adiciona um documento à base de conhecimento
`!buscar <termo>` - Busca documentos similares
`!rag_stats` - Mostra estatísticas da base de conhecimento
`!limpar_rag` - Limpa toda a base de conhecimento

`!ajuda` - Mostra esta mensagem

**Como usar:**
- Mencione o bot: @LeroLero sua pergunta
- Ou envie uma DM diretamente

O bot usa RAG para melhorar as respostas com informações da base de conhecimento!
            """
            await message.channel.send(help_text.strip())
            return
        
        database.add_user(user_id, username)
        
        history = database.get_conversation_history(user_id, limit=10)
        
        rag_context = None
        similar_docs = await vector_db.search_similar(user_message, n_results=2)
        if similar_docs:
            rag_context = "\n\n".join([doc['text'] for doc in similar_docs])
        
        database.save_message(user_id, "user", user_message)
        
        async with message.channel.typing():
            ai_response = await get_ai_response(user_message, history, rag_context)
            
            database.save_message(user_id, "assistant", ai_response)
            
            if len(ai_response) > 2000:
                chunks = [ai_response[i:i+2000] for i in range(0, len(ai_response), 2000)]
                for chunk in chunks:
                    await message.channel.send(chunk)
            else:
                await message.channel.send(ai_response)


try:
    token = os.getenv("TOKEN") or ""
    if token == "":
        raise Exception("Please add your TOKEN to the Secrets pane.")
    if not OPENROUTER_API_KEY:
        raise Exception("Please add your OPENROUTER_API_KEY to the Secrets pane.")
    
    client.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
