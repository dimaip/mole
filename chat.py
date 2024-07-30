from setup import vector_store, storage_context
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings

index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store, embed_model=Settings.embed_model, storage_context=storage_context
)

agent = index.as_chat_engine()

while True:
    text_input = input("Пользователь: ")
    if text_input == "exit":
        break
    response = agent.chat(text_input)
    print(f"Бот: {response}")
