import os
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    Settings,
)
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from amr_chatbot.config import (
    DATA_DIR,
    PERSIST_DIR,
    GROQ_MODEL,
    EMBED_MODEL,
    DEFAULT_TOP_K,
)
from amr_chatbot.data import download_ecdc_report


def setup_llama_index_settings():
    """Initializes global LlamaIndex Settings for LLM and Embedding models."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set. Please check your environment or .env file.")

    Settings.llm = Groq(model=GROQ_MODEL, api_key=api_key)
    Settings.embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL)


def get_or_build_index() -> VectorStoreIndex:
    """Loads a cached VectorStoreIndex from disk or builds a new one."""
    setup_llama_index_settings()
    download_ecdc_report()

    if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR):
        print("Loading cached vector index from storage/...")
        storage_context = StorageContext.from_defaults(persist_dir=str(PERSIST_DIR))
        return load_index_from_storage(storage_context)

    print("Building vector index from documents in data/...")
    documents = SimpleDirectoryReader(str(DATA_DIR)).load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=str(PERSIST_DIR))
    print("Vector index built and persisted.")
    return index


def query_rag(index: VectorStoreIndex, question: str, top_k: int = DEFAULT_TOP_K) -> str:
    """Queries the index and formats the output with document citations."""
    query_engine = index.as_query_engine(
        similarity_top_k=top_k,
        system_prompt=(
            "You are an assistant that answers questions strictly using the "
            "provided antimicrobial resistance (AMR) surveillance documents. "
            "If the answer isn't in the documents, say you don't know rather "
            "than guessing."
        ),
    )

    response = query_engine.query(question)
    answer = str(response)

    # Source extraction (files and page numbers)
    sources = set()
    for node in getattr(response, "source_nodes", []):
        file_name = node.metadata.get("file_name", "ECDC Report")
        page_label = node.metadata.get("page_label") or node.metadata.get("page_number")
        if page_label:
            sources.add(f"{file_name} (Page {page_label})")
        else:
            sources.add(file_name)

    if sources:
        answer += "\n\n**Sources:**\n" + "\n".join(f"- {src}" for src in sorted(sources))

    return answer
