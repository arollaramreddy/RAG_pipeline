"""
app.py  —  Gradio web UI for the ASU Career Services RAG pipeline

Run:
    python app.py
Then open http://localhost:7860
"""

import gradio as gr

from generation import generate, TOP_K


def handle_query(question: str):
    if not question.strip():
        return "", ""

    result = generate(question)

    # ── Retrieved context panel ───────────────────────────────────────────────
    # Show rank, similarity, source file, and a short preview for each chunk
    context_lines = []
    for chunk in result["chunks"]:
        preview = chunk["text"][:300].replace("\n", " ")
        context_lines.append(
            f"[{chunk['rank']}] {chunk['source']}  "
            f"(similarity: {chunk['similarity']:.4f})\n"
            f"{preview}{'…' if len(chunk['text']) > 300 else ''}"
        )
    context_text = "\n\n".join(context_lines)

    return result["answer"], context_text


# ── UI layout ─────────────────────────────────────────────────────────────────
with gr.Blocks(title="ASU Career Services Q&A") as demo:
    gr.Markdown(
        "## ASU Career Services Q&A\n"
        "Ask questions about ASU career fairs, internships, on-campus jobs, "
        "Handshake, and more. Answers are grounded in real student discussions."
    )

    with gr.Row():
        inp = gr.Textbox(
            label="Your question",
            placeholder="e.g. What do students say about ASU career fairs?",
            lines=2,
            scale=5,
        )
        btn = gr.Button("Ask", variant="primary", scale=1)

    answer_box = gr.Textbox(label="Answer", lines=12, buttons=["copy"])

    with gr.Accordion("Retrieved context", open=False):
        context_box = gr.Textbox(
            label=f"Top {TOP_K} chunks used to generate the answer",
            lines=15,
            buttons=["copy"],
        )

    btn.click(handle_query, inputs=inp, outputs=[answer_box, context_box])
    inp.submit(handle_query, inputs=inp, outputs=[answer_box, context_box])


if __name__ == "__main__":
    demo.launch()
