"""
Discord bot command handlers.
"""
from typing import Optional

import discord

from ..database.sqlite_db import db
# from ..rag.vector_store import vector_store  # Temporarily disabled


class CommandHandler:
    """Handler for bot commands"""

    @staticmethod
    async def handle_help(message: discord.Message):
        """Handle !ajuda command"""
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
- Mencione o bot: @SeuBot sua pergunta
- Ou envie uma DM diretamente

O bot usa RAG para melhorar as respostas com informações da base de conhecimento!
        """
        await message.channel.send(help_text.strip())

    @staticmethod
    async def handle_clear_history(message: discord.Message):
        """Handle !limpar command"""
        user_id = str(message.author.id)
        db.clear_user_history(user_id)
        await message.channel.send(
            "✅ Seu histórico de conversas foi limpo! Vamos começar uma nova conversa."
        )

    @staticmethod
    async def handle_stats(message: discord.Message):
        """Handle !stats command"""
        user_id = str(message.author.id)
        stats = db.get_user_stats(user_id)

        if stats:
            response = f"📊 **Suas Estatísticas:**\n"
            response += f"👤 Usuário: {stats['username']}\n"
            response += f"💬 Total de mensagens: {stats['message_count']}\n"
            response += f"🕐 Última interação: {stats['last_interaction']}"
            await message.channel.send(response)
        else:
            await message.channel.send("Ainda não há estatísticas para você.")

    @staticmethod
    async def handle_global_stats(message: discord.Message):
        """Handle !stats_global command"""
        stats = db.get_total_stats()
        response = f"📊 **Estatísticas Globais do Bot:**\n"
        response += f"👥 Total de usuários: {stats['total_users']}\n"
        response += f"💬 Total de mensagens: {stats['total_messages']}\n"
        response += f"📨 Mensagens de usuários: {stats['user_messages']}\n"
        response += f"🤖 Respostas do bot: {stats['bot_responses']}"
        await message.channel.send(response)

    @staticmethod
    async def handle_add_document(message: discord.Message, doc_text: str):
        """Handle !adicionar command"""
        if not doc_text:
            await message.channel.send("❌ Use: `!adicionar <texto do documento>`")
            return

        user_id = str(message.author.id)
        username = str(message.author)

        async with message.channel.typing():
            # doc_id = await vector_store.add_document(  # Temporarily disabled
            #     doc_text,
            #     metadata={"author": username, "author_id": user_id}
            # )

            # if doc_id:
            #     await message.channel.send(
            #         f"✅ Documento adicionado à base de conhecimento!\nID: `{doc_id}`"
            #     )
            # else:
            await message.channel.send("❌ RAG temporariamente desabilitado devido a problemas de dependências.")

    @staticmethod
    async def handle_search_documents(message: discord.Message, query: str):
        """Handle !buscar command"""
        if not query:
            await message.channel.send("❌ Use: `!buscar <termo de busca>`")
            return

        async with message.channel.typing():
            # results = await vector_store.search_similar(query, n_results=3)  # Temporarily disabled

            # if results:
            #     response = "🔍 **Documentos Encontrados:**\n\n"
            #     for i, doc in enumerate(results, 1):
            #         text_preview = doc['text'][:200]
            #         if len(doc['text']) > 200:
            #             text_preview += '...'
            #         response += f"**{i}.** {text_preview}\n\n"
            #     await message.channel.send(response)
            # else:
            await message.channel.send("❌ RAG temporariamente desabilitado devido a problemas de dependências.")

    @staticmethod
    async def handle_rag_stats(message: discord.Message):
        """Handle !rag_stats command"""
        # doc_count = vector_store.count_documents()  # Temporarily disabled
        # collections = vector_store.list_collections()  # Temporarily disabled

        response = f"📚 **Estatísticas do RAG:**\n"
        response += f"📄 RAG temporariamente desabilitado devido a problemas de dependências\n"
        response += f"📁 Coleções: Indisponível"
        await message.channel.send(response)

    @staticmethod
    async def handle_clear_rag(message: discord.Message):
        """Handle !limpar_rag command"""
        # success = vector_store.delete_all_documents()  # Temporarily disabled
        # if success:
        #     await message.channel.send("✅ Base de conhecimento limpa!")
        # else:
        await message.channel.send("❌ RAG temporariamente desabilitado devido a problemas de dependências.")


command_handler = CommandHandler()
