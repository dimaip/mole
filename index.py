from setup import vector_store, storage_context
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader(input_dir="scrape/kp-f.ru", recursive=True, required_exts=[".pdf", ".txt"]).load_data()

index = VectorStoreIndex(
    nodes=documents,
    vector_store=vector_store,
    embed_model=Settings.embed_model,
    storage_context=storage_context,
    show_progress=True,
)

