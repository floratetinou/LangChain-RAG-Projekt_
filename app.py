from src.local_rag.config import settings
from src.local_rag.ui import build_ui
from src.local_rag.vectorstore import open_vectorstore

if __name__ == "__main__":
    store = open_vectorstore(settings)
    ui = build_ui(store, settings)
    ui.launch(server_name=settings.gradio_host, server_port=settings.gradio_port)
