# MAYA

MAYA - Mental Artificial Youth Assistant

• AI-enabled, voice-powered companion utilizing Cognitive Behavioral Therapy (CBT) principles for empathetic support

• Advanced Natural Language Processing (NLP) techniques, including a Llama-2 7B model fine-tuned on a mental therapy dataset for human-like conversation

• Quantization techniques applied to the LLM for efficient processing, hosted on AWS for GPU inference

• Voice input and output capabilities using ElevenLabs TTS API for human-like voice synthesis

• User-friendly and innovative frontend interface integrated with backend functionality

• Facilitation of reflective conversations with transcript documentation for user reflection

• Provision of summary notes similar to a therapist's session notes

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/piyushgaba07/MAYA
cd MAYA
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

- Copy `.env.example` to `.env`:
  ```bash
  cp .env.example .env
  ```
- Fill in your real API keys and endpoints in `.env` (do NOT commit this file):
  - `OPENAI_API_KEY`
  - `ELEVEN_API_KEY`
  - `API_URL`
  - `AUTHORIZATION`

### 5. Initialize the database

```bash
python init_db.py
```

### 6. Run the app

```bash
python app_2.py
```

---

## 📝 Notes

- If you encounter errors about missing NLTK data, run:
  ```python
  import nltk
  nltk.download('punkt')
  nltk.download('averaged_perceptron_tagger')
  ```
- For ElevenLabs and OpenAI features to work, valid API keys are required.
- For development, if `API_URL` is not set, a fallback message will be used.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

[MIT](LICENSE)
