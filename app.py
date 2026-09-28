import os
from amr_chatbot.ui import create_ui

if __name__ == "__main__":
    demo, theme, css = create_ui()
    # Gradio 6 configuration passing theme and css directly into launch()
    demo.launch(
        theme=theme,
        css=css,
        share=False,
        debug=True,
    )
