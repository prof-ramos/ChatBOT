import os
import chromadb
from typing import List, Dict, Optional
import uuid
from openai import AsyncOpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or ""
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL") or "text-embedding-3-small"
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "rag_collection"

client = chromadb.PersistentClient(path=CHROMA_PATH)
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


async def get_embedding(text: str) -> List[float]:
    """Obtém embedding de um texto usando OpenAI"""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY não configurada")
    
    if not openai_client:
        raise Exception("Cliente OpenAI não inicializado")
    
    try:
        response = await openai_client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        raise Exception(f"Erro ao gerar embedding: {e}")


def init_vector_db():
    """Inicializa o banco de dados vetorial"""
    try:
        collections = client.list_collections()
        print(f"✅ Banco vetorial inicializado. Coleções: {len(collections)}")
        return True
    except Exception as e:
        print(f"Erro ao inicializar banco vetorial: {e}")
        return False


def get_or_create_collection(name: str = COLLECTION_NAME):
    """Obtém ou cria uma coleção no ChromaDB"""
    try:
        return client.get_or_create_collection(
            name=name,
            metadata={"description": "Documentos do bot Discord"}
        )
    except Exception as e:
        print(f"Erro ao criar/obter coleção: {e}")
        return None


async def add_document(text: str, metadata: Dict = None, collection_name: str = COLLECTION_NAME) -> Optional[str]:
    """Adiciona um documento ao banco vetorial"""
    try:
        collection = get_or_create_collection(collection_name)
        if not collection:
            return None
        
        embedding = await get_embedding(text)
        
        doc_id = str(uuid.uuid4())
        
        if metadata is None:
            metadata = {}
        
        collection.add(
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )
        
        return doc_id
    except Exception as e:
        print(f"Erro ao adicionar documento: {e}")
        return None


async def search_similar(query: str, n_results: int = 3, collection_name: str = COLLECTION_NAME) -> List[Dict]:
    """Busca documentos similares a uma query"""
    try:
        collection = get_or_create_collection(collection_name)
        if not collection:
            return []
        
        query_embedding = await get_embedding(query)
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        documents = []
        if results and results['documents'] and len(results['documents']) > 0:
            for i, doc in enumerate(results['documents'][0]):
                doc_data = {
                    "text": doc,
                    "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                    "distance": results['distances'][0][i] if results['distances'] else None
                }
                documents.append(doc_data)
        
        return documents
    except Exception as e:
        print(f"Erro ao buscar documentos: {e}")
        return []


def count_documents(collection_name: str = COLLECTION_NAME) -> int:
    """Retorna o número de documentos na coleção"""
    try:
        collection = get_or_create_collection(collection_name)
        if not collection:
            return 0
        return collection.count()
    except Exception as e:
        print(f"Erro ao contar documentos: {e}")
        return 0


def delete_all_documents(collection_name: str = COLLECTION_NAME) -> bool:
    """Deleta todos os documentos de uma coleção"""
    try:
        client.delete_collection(collection_name)
        print(f"✅ Coleção '{collection_name}' deletada")
        return True
    except Exception as e:
        print(f"Erro ao deletar coleção: {e}")
        return False


def list_collections() -> List[str]:
    """Lista todas as coleções"""
    try:
        collections = client.list_collections()
        return [col.name for col in collections]
    except Exception as e:
        print(f"Erro ao listar coleções: {e}")
        return []
