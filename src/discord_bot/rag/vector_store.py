"""
Vector database management using ChromaDB and OpenAI embeddings.
"""
import uuid
from typing import List, Dict, Optional

import chromadb
from openai import AsyncOpenAI

from ..config.settings import settings


class VectorStore:
    """ChromaDB vector store manager with OpenAI embeddings"""

    def __init__(
        self,
        chroma_path: str = None,
        collection_name: str = None,
        openai_api_key: str = None
    ):
        self.chroma_path = chroma_path or settings.CHROMA_DB_PATH
        self.collection_name = collection_name or settings.CHROMA_COLLECTION_NAME

        self.client = chromadb.PersistentClient(path=self.chroma_path)

        api_key = openai_api_key or settings.OPENAI_API_KEY
        self.openai_client = AsyncOpenAI(api_key=api_key) if api_key else None

    async def get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using OpenAI"""
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not configured")

        if not self.openai_client:
            raise Exception("OpenAI client not initialized")

        try:
            response = await self.openai_client.embeddings.create(
                model=settings.EMBEDDING_MODEL,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Error generating embedding: {e}")

    def init_vector_db(self):
        """Initialize the vector database"""
        try:
            collections = self.client.list_collections()
            print(f"✅ Vector database initialized. Collections: {len(collections)}")
            return True
        except Exception as e:
            print(f"Error initializing vector database: {e}")
            return False

    def get_or_create_collection(self, name: str = None):
        """Get or create a collection in ChromaDB"""
        collection_name = name or self.collection_name

        try:
            return self.client.get_or_create_collection(
                name=collection_name,
                metadata={"description": "Discord bot knowledge base"}
            )
        except Exception as e:
            print(f"Error creating/getting collection: {e}")
            return None

    async def add_document(
        self,
        text: str,
        metadata: Dict = None,
        collection_name: str = None
    ) -> Optional[str]:
        """Add a document to the vector database"""
        try:
            collection = self.get_or_create_collection(collection_name)
            if not collection:
                return None

            embedding = await self.get_embedding(text)

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
            print(f"Error adding document: {e}")
            return None

    async def search_similar(
        self,
        query: str,
        n_results: int = None,
        collection_name: str = None
    ) -> List[Dict]:
        """Search for similar documents"""
        if n_results is None:
            n_results = settings.RAG_SEARCH_RESULTS

        try:
            collection = self.get_or_create_collection(collection_name)
            if not collection:
                return []

            query_embedding = await self.get_embedding(query)

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
            print(f"Error searching documents: {e}")
            return []

    def count_documents(self, collection_name: str = None) -> int:
        """Count documents in collection"""
        try:
            collection = self.get_or_create_collection(collection_name)
            if not collection:
                return 0
            return collection.count()
        except Exception as e:
            print(f"Error counting documents: {e}")
            return 0

    def delete_all_documents(self, collection_name: str = None) -> bool:
        """Delete all documents from a collection"""
        collection_name = collection_name or self.collection_name

        try:
            self.client.delete_collection(collection_name)
            print(f"✅ Collection '{collection_name}' deleted")
            return True
        except Exception as e:
            print(f"Error deleting collection: {e}")
            return False

    def list_collections(self) -> List[str]:
        """List all collections"""
        try:
            collections = self.client.list_collections()
            return [col.name for col in collections]
        except Exception as e:
            print(f"Error listing collections: {e}")
            return []


# Singleton instance
vector_store = VectorStore()
