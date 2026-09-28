# 🧫 AMR Surveillance Chatbot

A retrieval-augmented generation (RAG) chatbot that answers questions about antimicrobial resistance (AMR) in Europe. Answers are grounded in the ECDC *Antimicrobial resistance in the EU/EEA (EARS-Net): Annual Epidemiological Report 2024*, and the bot says it doesn't know when the report doesn't contain the answer.

<!-- Add a screenshot: save it as docs/screenshot.png, then uncomment the next line -->
<!-- ![App screenshot](docs/screenshot.png) -->

## ✨ Features

- Question answering over the ECDC EARS-Net report, with source file and page shown under every answer
- Adjustable **Top K** slider to control how many report passages the LLM receives
- Grounded prompt: the model is told to answer only from the retrieved context
- Vector index is built once and cached in `storage/`, so later starts are fast
- Custom teal Gradio interface

## ⚙️ How it works

```
ECDC PDF  ->  chunks + embeddings (BAAI/bge-small-en-v1.5)  ->  vector index (storage/)
                                                                      |
question  ->  retrieve top K chunks  ->  Groq LLM (openai/gpt-oss-20b)  ->  answer + sources
```

Built with [LlamaIndex](https://www.llamaindex.ai/), [Groq](https://groq.com/), [Hugging Face embeddings](https://huggingface.co/BAAI/bge-small-en-v1.5) and [Gradio](https://gradio.app/).

## 🚀 Quick start

You need Python 3.10+ and a free [Groq API key](https://console.groq.com/keys).

```bash
git clone https://github.com/<your-username>/amr-surveillance-chatbot.git
cd amr-surveillance-chatbot

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # then edit .env and add GROQ_API_KEY
python app.py
```

Open the local URL that Gradio prints. On the first run the app downloads the ECDC PDF into `data/` and builds the index, which takes a few minutes.

### ☁️ Google Colab

Add `GROQ_API_KEY` (and optionally `HF_TOKEN`) under **Secrets**, then:

```python
import os
from google.colab import userdata
os.environ["GROQ_API_KEY"] = userdata.get("GROQ_API_KEY")

!pip install -q -r requirements.txt
!python app.py
```

Use the public `gradio.live` link that appears in the output.

## 🔧 Configuration

Everything lives in `amr_chatbot/config.py`:

| Setting | Default | Notes |
|---|---|---|
| `GROQ_MODEL` | `openai/gpt-oss-20b` | Can also be set with the `GROQ_MODEL` environment variable |
| `EMBED_MODEL` | `BAAI/bge-small-en-v1.5` | If you change it, delete `storage/` so the index is rebuilt |
| `DEFAULT_TOP_K` | `3` | Slider range is 1 to 5 |

To use your own documents, put PDFs in `data/`, delete `storage/`, and restart.

## 📁 Project structure

```
amr-surveillance-chatbot/
├── app.py                 # entry point
├── amr_chatbot/
│   ├── config.py          # settings, paths, example questions
│   ├── data.py            # downloads the ECDC report
│   ├── engine.py          # index building/loading and question answering
│   └── ui.py              # Gradio interface
├── requirements.txt
├── .env.example
└── docs/                  # screenshots
```

## 🛠️ Troubleshooting

- **`GROQ_API_KEY is not set`**: create `.env` from `.env.example`, or set the variable in your environment.
- **Odd answers after changing the embedding model**: delete `storage/` and restart.
- **`huggingface_hub` version conflicts (seen on Colab)**: run `pip install huggingface_hub==0.34.4`.
- **Theme or CSS errors**: this project targets Gradio 6, where `theme` and `css` are passed to `launch()`. On Gradio 5 or older they go to `gr.Blocks(...)` instead.

## ⚠️ Limitations

- Knowledge is limited to the loaded report; it does not have newer data unless you add documents.
- Charts and tables in the PDF are read as text, so numeric answers from tables should be checked against the source page.
- This is a research and learning tool, not medical advice.

## 📄 Data source

European Centre for Disease Prevention and Control (ECDC), *Antimicrobial resistance in the EU/EEA (EARS-Net) – Annual Epidemiological Report 2024*. The PDF is downloaded from ECDC at run time and is not redistributed in this repository. Please follow ECDC's reuse terms.

