# 🎙️ Recaply

### AI Meeting Intelligence — Turn long conversations into clear, actionable insights.

Recaply is an AI-powered meeting and video analysis assistant that transforms long conversations into structured, useful information.

Instead of manually going through an hour-long meeting or video, Recaply processes the content and generates:

**Transcripts · Summaries · Action Items · Key Decisions · Open Questions · AI-powered Q&A**

Built with **Python, Streamlit, Whisper, Groq, LangChain, ChromaDB, and Hugging Face embeddings**, Recaply combines speech recognition, LLM-based analysis, and Retrieval-Augmented Generation (RAG) into one streamlined application.

---

## ✨ Why Recaply?

Long meetings contain a lot of information — but finding the important parts shouldn't take as long as attending the meeting.

Recaply helps answer:

- 📝 What was discussed?
- 🎯 What are the important takeaways?
- ✅ What actions need to be taken?
- 💡 What decisions were made?
- ❓ What questions remain unanswered?
- 🔎 Can I ask questions about the meeting later?

### The result

> **From conversation → to structured intelligence.**

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🎥 **YouTube Processing** | Analyze audio from YouTube videos |
| 📁 **File Upload** | Process local audio/video files |
| 🎙️ **AI Transcription** | Transcribe speech using OpenAI Whisper |
| 🌐 **Multilingual Support** | English and Hindi/Hinglish processing |
| 🧠 **AI Summarization** | Generate concise meeting summaries |
| ✅ **Action Items** | Extract tasks and follow-ups |
| 🎯 **Key Decisions** | Identify important decisions |
| ❓ **Open Questions** | Extract unresolved questions |
| 🔎 **RAG Q&A** | Ask questions about the processed meeting |
| 📚 **Vector Search** | Store transcript knowledge using ChromaDB |
| 📄 **PDF Export** | Export analysis as PDF |
| 📝 **TXT Export** | Export analysis as text |
| 🎨 **Premium UI** | Modern Streamlit interface |

---

## 🧠 How It Works

```text
                 ┌──────────────────────┐
                 │    YouTube / File    │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Audio Processing   │
                 │     yt-dlp / FFmpeg  │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Audio Chunking     │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Whisper Speech     │
                 │     Recognition      │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     Transcript       │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │      Groq LLM        │
                 │   Content Analysis   │
                 └──────────┬───────────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
        ┌─────────┐   ┌──────────┐   ┌───────────┐
        │ Summary │   │ Action   │   │ Decisions │
        │         │   │ Items    │   │           │
        └─────────┘   └──────────┘   └───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Embeddings + ChromaDB│
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │       RAG Q&A        │
                 │  Ask the meeting     │
                 └──────────────────────┘
```

---

## 🏗️ Architecture

### 1. Input Layer

Users can provide:

- YouTube URLs
- Local audio files
- Local video files

### 2. Audio Processing

**yt-dlp** handles YouTube audio extraction while **FFmpeg** and **pydub** handle audio conversion and processing.

Audio is converted into a format suitable for speech recognition and divided into manageable chunks.

### 3. Speech Recognition

Recaply uses **OpenAI Whisper** for local speech-to-text transcription.

The current implementation uses the Whisper `small` model.

### 4. AI Analysis

The transcript is processed using a **Groq-hosted LLM** through LangChain.

The system extracts:

- Meeting summary
- Action items
- Key decisions
- Open questions

### 5. Knowledge Retrieval

The transcript is converted into embeddings and stored in **ChromaDB**.

This enables Retrieval-Augmented Generation (RAG), allowing users to ask questions about the processed meeting.

### 6. Presentation & Export

The results are presented through a Streamlit interface with options to export the analysis as:

- PDF
- TXT

---

## 🛠️ Tech Stack

### Frontend / UI

- **Streamlit**
- Custom CSS
- Responsive interface

### AI / Machine Learning

- **OpenAI Whisper** — speech recognition
- **Groq** — LLM inference
- **LangChain** — LLM orchestration
- **Hugging Face** — embeddings

### Retrieval

- **ChromaDB**
- **LangChain Chroma**

### Audio / Video

- **yt-dlp**
- **FFmpeg**
- **pydub**

### Development

- **Python**
- **python-dotenv**
- **Git / GitHub**

---

## 📂 Project Structure

```text
Recaply/
│
├── app.py
│
├── core/
│   ├── transcriber.py
│   ├── extractor.py
│   ├── summarizer.py
│   ├── rag_engine.py
│   └── vector_store.py
│
├── utils/
│   └── audio_processor.py
│
├── .streamlit/
│   └── config.toml
│
├── requirements.txt
├── packages.txt
├── .gitignore
├── .env
└── README.md
```

> `.env`, generated audio, vector databases, and other local/generated files should remain excluded from version control.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Aditya-Kurlekar/Recaply.git
cd Recaply
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

#### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Install FFmpeg

Recaply requires **FFmpeg** for audio and video processing.

Verify your installation:

```bash
ffmpeg -version
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
SARVAM_API_KEY=your_sarvam_api_key
```

### ⚠️ Important

Never commit your `.env` file or expose your API keys publicly.

---

## ▶️ Run Recaply

Activate your virtual environment and run:

```bash
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

---

## 💬 RAG Q&A

After processing a meeting, Recaply builds a searchable knowledge base from the transcript.

You can ask questions such as:

```text
What were the main decisions made?

What tasks were assigned?

What did the team discuss about the project deadline?

What problems were mentioned during the meeting?

Who was responsible for the next steps?
```

The system retrieves relevant transcript context before generating an answer.

---

## 🌍 Multilingual Processing

### 🇬🇧 English

English audio is processed using local Whisper transcription.

### 🇮🇳 Hindi / Hinglish

Hindi and Hinglish audio can be processed through the integrated multilingual speech-to-text workflow.

The resulting transcript can then be analyzed for summaries, decisions, action items, and questions.

---

## 📤 Export

Recaply supports exporting generated meeting intelligence.

### TXT

Useful for:

- Notes
- Documentation
- Sharing
- Further processing

### PDF

Useful for:

- Meeting reports
- Documentation
- Professional sharing
- Archiving

---

## ⚡ Processing Pipeline

Recaply is designed to handle longer meetings by:

- Splitting audio into chunks
- Processing transcription incrementally
- Separating AI extraction tasks
- Creating embeddings for transcript retrieval

Processing time depends on:

- Audio/video duration
- Whisper model
- CPU/GPU performance
- Internet connection
- LLM/API response time

---

## 🔒 Security

Recaply keeps sensitive configuration outside the source code.

API keys are stored in:

```text
.env
```

and should be excluded from Git using `.gitignore`.

Generated local data such as:

```text
downloads/
downloades/
vector_db/
```

should also remain excluded from version control.

---

## 🎯 Use Cases

### 🧑‍💼 Meetings

Turn lengthy meetings into concise reports.

### 🎓 Lectures

Extract important concepts and ask questions about recorded lectures.

### 📞 Interviews

Review interview recordings and identify key discussion points.

### 📺 Educational Videos

Convert long-form videos into structured notes.

### 👥 Team Discussions

Track decisions, tasks, and unresolved questions.

### 📝 Research

Search through long conversations without manually reviewing the entire transcript.

---

## 🧪 Project Status

### 🟢 Local Version — Working

The current local version supports:

- ✅ YouTube audio processing
- ✅ Local file processing
- ✅ Whisper transcription
- ✅ Groq-based analysis
- ✅ Transcript embeddings
- ✅ ChromaDB vector storage
- ✅ RAG-based Q&A
- ✅ Streamlit interface
- ✅ PDF/TXT exports
- ✅ English and Hindi/Hinglish workflows

---

## 🔮 Future Improvements

- [ ] Speaker diarization
- [ ] Automatic speaker identification
- [ ] Timestamp-based transcript navigation
- [ ] Improved multilingual support
- [ ] Topic detection
- [ ] Sentiment analysis
- [ ] Calendar and meeting integrations
- [ ] Persistent meeting history
- [ ] User authentication
- [ ] Cloud deployment

---

## 📸 Screenshots

You can add screenshots of the application here:

```markdown
![Recaply Dashboard](screenshots/dashboard.png)

![Meeting Analysis](screenshots/analysis.png)

![RAG Q&A](screenshots/qa.png)
```

Adding real screenshots of your application will make the repository more visually appealing and easier to understand.

---

## 👨‍💻 Author

### Aditya Kurlekar

**B.Tech Computer Science & Engineering**

Interested in:

**Data Analytics · Data Science · Artificial Intelligence · Machine Learning**

### Connect

🔗 **LinkedIn:** [Aditya Kurlekar](https://www.linkedin.com/in/aditya-kurlekar)

🐙 **GitHub:** [Aditya-Kurlekar](https://github.com/Aditya-Kurlekar)

---

## ⭐ Support

If you find Recaply useful or interesting, consider giving the repository a ⭐ on GitHub.

---

<div align="center">

## 🎙️ Recaply

### Every conversation. One clear picture.

**Built with Python · AI · RAG · Streamlit**

</div>
