# 🤖 What This Project Does  
An end-to-end **AI-powered meeting assistant** that automates your post-meeting workflow:

#### 🎙️ Automatic Speech Transcription  
Upload `.mp3` or `.wav` audio files, and the system uses **OpenAI Whisper** to transcribe them into readable text — no manual note-taking needed.

#### 🧠 Smart Summarization with GPT-4o  
The transcript is summarized using **Azure OpenAI's GPT-4o**, producing:

- 🔹 A concise abstract  
- 🔹 Key discussion points  
- 🔹 Early action items  

Perfect for catching up without reading the entire transcript.

#### ✅ Action Item Extraction (Who, What, When)  
Using GPT-4o’s language understanding, the assistant extracts structured tasks with:

- 📌 Task description  
- 👤 Assigned person  
- 🗓️ Deadline (converted to ISO 8601)

#### 📅 Seamless Google Calendar Integration  
Tasks are scheduled to **Google Calendar** using the API, automatically creating:

- 📝 Event title & description  
- 🕘 Start & end times  
- 📅 Accurate due dates based on parsed natural language

#### 🌐 Beautiful Web Interface (Streamlit)  
Everything is bundled into a clean, intuitive **Streamlit UI** where users can:

- 🔼 Upload audio or transcript  
- 📄 View real-time summaries  
- 🧾 Extract action items  
- 📆 Schedule all tasks in one click


## 📸 Screenshots

![image](https://github.com/user-attachments/assets/f7337ff9-0a9d-49d1-bbfb-d87415c0b243)
![image](https://github.com/user-attachments/assets/bd185b1c-a6a0-4abf-a3e7-dc9107af3e92)
![image](https://github.com/user-attachments/assets/cef1c805-df1e-4640-94b6-4bd9e8a3482d)

---

## 🛠️ Features

| Feature                          | Description                                               |
|----------------------------------|-----------------------------------------------------------|
| 🔊 Audio Upload                  | Upload `.mp3` or `.wav` files and transcribe via Whisper  |
| 📝 Transcript Paste or Upload    | Paste or upload `.txt` or `.srt` transcript files         |
| 💡 GPT‑4o Summarizer            | Uses Azure OpenAI to summarize and extract tasks          |
| 📌 Action Item Extraction        | Assigns tasks to people with deadlines                    |
| 📅 Google Calendar Integration   | Adds tasks as events to Google Calendar                   |

---

## ⚙️ Tech Stack

- **Frontend**: Streamlit  
- **ASR (Speech-to-Text)**: OpenAI Whisper  
- **LLM**: GPT‑4o via Azure OpenAI  
- **Task Extraction**: GPT with ISO-enforced due dates  
- **Scheduling**: Google Calendar API  
- **Utilities**: Python, `dateparser`, `python-pptx`, `google-api-python-client`

---

## 🚀 Setup Instructions

### ✅ 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/meeting-agent.git
cd meeting-agent
```

### ✅ 2. Create and Activate Virtual Environment

```bash
python -m venv env
# For Windows:
env\Scripts\activate
# For macOS/Linux:
source env/bin/activate
```

### ✅ 3. Install Requirements

```bash
pip install -r requirements.txt
```

### ✅ 4. Azure OpenAI API Setup

Open `streamlit_app.py` and `summarizer.py` and replace this block:

```python
openai.api_type = "azure"
openai.api_base = "https://YOUR_ENDPOINT.openai.azure.com/"
openai.api_version = "2024-12-01-preview"
openai.api_key = "YOUR_API_KEY"
deployment_name = "YOUR_DEPLOYMENT_NAME"
```

**NOTE** :🔐 You can also load these from a `.env` file (recommended for production).

---
### ✅ 5. Google Calendar API Setup
---

#### a. Go to https://console.cloud.google.com/

- Create a new project  
- Enable **Google Calendar API**

#### b. Create OAuth Credentials

- Go to **APIs & Services → Credentials → + Create Credentials**
- Choose **OAuth Client ID → Desktop App**
- Download `credentials.json`

#### c. File Placement & Purpose

| File             | Location         | Purpose                                                 |
|------------------|------------------|---------------------------------------------------------|
| `credentials.json` | Project root    | Google OAuth credentials for calendar access            |
| `token.pickle`     | Auto-created    | Stores access token after login to avoid re-authentication |

### 📂 Directory structure:

```
/project-root
│
├── credentials.json         # ← Required before first run
├── token.pickle             # ← Auto-generated after login
├── streamlit_app.py
├── summarizer.py
├── calendar_integartion.py
├── transcript_parser.py
├── requirements.txt
└── audio/                   # (Optional) where audio files are saved
```

 **NOTE: **  🔒 Do not share `credentials.json` or `token.pickle` publicly.
 
---

### ▶️ Running the App

```bash
streamlit run streamlit_app.py
```

---


### ✅ How It Works (End-to-End)

- Upload an audio file or transcript  
- Whisper transcribes audio (if any)  
- GPT-4o generates a summary and action items  
- Action items use GPT-generated ISO 8601 dates (YYYY-MM-DD)  
- Items are pushed to your Google Calendar via API  

---

### 🔐 Environment Variables (optional via `.env`)

```ini
OPENAI_API_KEY=your-azure-api-key
OPENAI_API_BASE=https://your-endpoint.openai.azure.com/
DEPLOYMENT_NAME=mindcraft-gpt4o
```

> Use `python-dotenv` to load these automatically in your script.

---

### 📦 Future Enhancements

- 📤 Export summary + action items as PDF  
- 🔔 Email or Slack notifications per task  
- 📊 Visual Gantt-style task timelines  
- 🌐 Deploy to Streamlit Cloud or Render  
- 🧠 Meeting search & archive feature  

---

### 📄 License

MIT License — Free to use with attribution

---

### 🙋‍♂️ Author

**Sparsh Sinha**  
B.Tech, IIIT Lucknow  
📧 sparshsinha11@gmail.com
🔗 https://linkedin.com/in/sparshsinha  
🔗 https://github.com/yourusername
