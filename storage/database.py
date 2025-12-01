# Collection management for Qdrant vector database with hybrid search and reranking
# Querying

from qdrant_client import QdrantClient
from fastembed import SparseTextEmbedding, TextEmbedding, LateInteractionTextEmbedding
from sentence_transformers import CrossEncoder
from config.agent_config import QDRANT_API, QDRANT_URL, COLLECTION_NAME
        
class QdrantRAG:
    def __init__(self):
        # ---- Qdrant ----
        self.client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API)

        # ---- Embedding models ----
        self.sparse_embedding_model = SparseTextEmbedding("Qdrant/bm25")
        self.late_interaction_embedding_model = LateInteractionTextEmbedding("colbert-ir/colbertv2.0")
        self.dense_embedding_model = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")
        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        self.chunk_size = 650
        self.overlap = 100
        
    # ---------------------------------------------------------
    # Build Collection
    # ---------------------------------------------------------
    def build_collection(self, file_paths = ["/Manufacturing_Intro.txt"]):
        from qdrant_client.models import (
            VectorParams, Distance, SparseVectorParams,
            MultiVectorConfig, MultiVectorComparator, PointStruct, Modifier
        )
        from langchain_core.documents import Document
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        import pdfplumber
        print("Building Qdrant collection...")
        if COLLECTION_NAME in [c.name for c in self.client.get_collections().collections]:
            return "Collection already exists."

        docs_list = []

        # --- Load files ---
        for file_path in file_paths:
            if file_path.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    docs_list.append(Document(page_content=f.read(), metadata={"source": file_path}))

        # --- Split ---
        splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.overlap)
        chunks = splitter.split_documents(docs_list)

        # --- Create collection ----
        self.client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config={
                "dense": VectorParams(size=384, distance=Distance.COSINE),
                "late": VectorParams(
                    size=self.late_interaction_embedding_model.embedding_size,
                    distance=Distance.COSINE,
                    multivector_config=MultiVectorConfig(comparator=MultiVectorComparator.MAX_SIM),
                ),
            },
            sparse_vectors_config={"sparse": SparseVectorParams(modifier=Modifier.IDF)},
        )
        
        self.client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="source",
            field_type="keyword"
        )

        # --- Embedding ---
        dense = list(self.dense_embedding_model.embed([c.page_content for c in chunks]))
        sparse = list(self.sparse_embedding_model.embed([c.page_content for c in chunks]))
        late = list(self.late_interaction_embedding_model.embed([c.page_content for c in chunks]))

        # --- Upload ---
        points = []
        for idx, chunk in enumerate(chunks):
            points.append(
                PointStruct(
                    id=idx,
                    vector={
                        "dense": dense[idx],
                        "sparse": sparse[idx].as_object(),
                        "late": late[idx],
                    },
                    payload={"text": chunk.page_content, "source": chunk.metadata.get("source")},
                )
            )

        self.client.upsert(collection_name=COLLECTION_NAME, points=points)

    # ---------------------------------------------------------
    # Search Query
    # ---------------------------------------------------------
    def search(self, query_text, file_name, top_k=4):
        from qdrant_client.models import Prefetch, SparseVector

        dense_q = next(self.dense_embedding_model.query_embed(query_text))
        sparse_q = next(self.sparse_embedding_model.query_embed(query_text))
        late_q = next(self.late_interaction_embedding_model.query_embed(query_text))

        prefetch = [
        Prefetch(
            query=dense_q,
            using="dense",
            limit=top_k * 5,
            filter={
                "must": [
                    {"key": "source", "match": {"value": file_name}}
                ]
            } 
        ),
        Prefetch(
            query=SparseVector(**sparse_q.as_object()),
            using="sparse",
            limit=top_k * 5,
            filter={
                "must": [
                    {"key": "source", "match": {"value": file_name}}
                ]
            }
        )
    ]

        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            prefetch=prefetch,
            query=late_q,
            using="late",
            with_payload=True,
            limit=top_k
        )

        # Extract text
        output = []
        if hasattr(results, "points"):
            for pt in results.points:
                if pt.payload and "text" in pt.payload:
                    output.append(pt.payload["text"])

        return output

    def remove_collection(self, name):
        self.client.delete_collection(collection_name=name)
        
        
        