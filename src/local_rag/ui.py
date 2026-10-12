import gradio as gr
from .config import Settings
from .pipeline import answer_question


def build_ui(vectorstore, cfg: Settings) -> gr.Blocks:
    def ask(question: str, mode: str) -> str:
        if not question.strip():
            return "Bitte eine Frage eingeben."
        try:
            answer, sources = answer_question(question, mode, vectorstore, cfg)
            source_block = "\n".join(f"- {s}" for s in sources) or "- Keine"
            return f"{answer}\n\n### Quellen\n{source_block}"
        except Exception as exc:
            return f"Die Anfrage konnte nicht verarbeitet werden: {exc}"

    with gr.Blocks(title="Solid Local RAG") as demo:
        gr.Markdown("#Local LangChain RAG\nFragen an lokale PDF-, TXT- und Markdown-Dokumente.")
        question = gr.Textbox(label="Frage", lines=3)
        mode = gr.Radio(["similarity", "mmr", "threshold"], value=cfg.retriever_mode, label="Retriever-Modus")
        submit = gr.Button("Frage stellen", variant="primary")
        output = gr.Markdown()
        submit.click(ask, inputs=[question, mode], outputs=output)
    return demo
