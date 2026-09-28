import gradio as gr
from amr_chatbot.config import DEFAULT_TOP_K, EXAMPLE_QUESTIONS
from amr_chatbot.engine import get_or_build_index, query_rag


def create_ui():
    """Builds and returns the Gradio web interface."""
    index = get_or_build_index()

    theme = gr.themes.Soft(
        primary_hue="teal",
        secondary_hue="cyan",
        neutral_hue="slate",
    ).set(
        body_background_fill="linear-gradient(135deg, #e0f7fa 0%, #f1f8e9 100%)",
        button_primary_background_fill="#00897b",
        button_primary_background_fill_hover="#00695c",
    )

    css = """
    #header {
        background: linear-gradient(90deg, #00695c, #26a69a);
        color: white;
        padding: 16px 24px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        gap: 16px;
    }
    #header h1 { margin: 0; font-size: 1.6rem; color: white; }
    #header p  { margin: 0; opacity: 0.9; }
    #header img { height: 64px; border-radius: 8px; }
    """

    BANNER_IMG = "https://images.unsplash.com/photo-1583912267550-d974311a9a6e?w=200"
    USER_AVATAR = "https://cdn-icons-png.flaticon.com/512/1077/1077114.png"
    BOT_AVATAR = "https://cdn-icons-png.flaticon.com/512/4712/4712027.png"

    with gr.Blocks(title="AMR Surveillance Chatbot") as demo:
        gr.HTML(
            f"""
