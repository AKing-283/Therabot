<div align="center">
 🧠 Therabot — AI Mental Wellness Companion

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?style=for-the-badge&logo=flask)
![Gemini](https://img.shields.io/badge/Google-Gemini-orange?style=for-the-badge&logo=google)
![MLflow](https://img.shields.io/badge/MLflow-MLOps-blue?style=for-the-badge&logo=mlflow)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue?style=for-the-badge&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

<h3>🚀 AI-Powered Emotional Support & Mental Wellness Platform</h3>

<p>
An intelligent conversational assistant designed to provide empathetic interactions,
emotional understanding, and mental wellness support using
<b>Generative AI + MLOps practices</b>.
</p>

</div>

---

# 🌟 Overview

**Therabot** is an AI-powered mental wellness companion that provides emotionally aware conversations using **Google Gemini**, **Machine Learning**, and **MLOps workflows**.

The platform can:

- Detect emotions from user messages
- Generate empathetic AI responses
- Identify distress-related conversations
- Maintain contextual chat history
- Provide mental wellness support resources

---

# ✨ Features

## 🤖 AI Conversational Support

- Real-time AI wellness conversations
- Context-aware empathetic replies
- Google Gemini integration
- Async chat experience
- Human-like responses

---

## 😊 Emotion Detection System

ML-powered emotional classification system.

### Supported Emotions

- 😟 Anxiety
- 😔 Sadness
- 😫 Stress
- 😄 Happiness
- 😐 Neutral

---

## 🆘 Crisis & Distress Detection

Safety-focused conversational handling.

### Includes

- Distress keyword detection
- Harmful message identification
- Emergency wellness prompts
- Safe response handling

---

## 🔐 Authentication System

- User Signup/Login
- Secure sessions
- Persistent chat history
- User-specific conversations

---

## 🌗 Modern UI/UX

- Fully responsive interface
- Dark/Light theme toggle
- Smooth chat animations
- Mobile-friendly design

---

## 📚 Mental Wellness Resources

- FAQs section
- Self-help resources
- Wellness guidance
- Mental health support links

---

# 🏗️ System Architecture

```text
                ┌────────────────────┐
                │       User         │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Flask Web App      │
                └─────────┬──────────┘
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
 ┌────────────────┐ ┌──────────────┐ ┌────────────────┐
 │ Gemini API     │ │ Emotion ML   │ │ Distress Logic │
 │ AI Responses   │ │ Classification│ │ Safety System │
 └────────────────┘ └──────────────┘ └────────────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ SQLite Database    │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ MLflow Tracking    │
                │ + MLOps Pipeline   │
                └────────────────────┘
```

---

# 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Backend | Python, Flask |
| AI | Google Gemini API |
| Machine Learning | Scikit-learn |
| MLOps | MLflow |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| Authentication | Flask Sessions |
| Deployment | Docker, Render, AWS |

---

# 📂 Project Structure

```bash
Therabot/
│
├── app/
│   ├── routes/
│   ├── templates/
│   ├── static/
│   ├── models/
│   └── utils/
│
├── mlops/
│   ├── train.py
│   ├── evaluate.py
│   └── mlruns/
│
├── data/
├── requirements.txt
├── Dockerfile
├── render.yaml
├── app.py
└── README.md
```

---

# ⚡ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/therabot.git
cd therabot
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key
SECRET_KEY=your_secret_key
```

---

## 5️⃣ Run Application

```bash
python app.py
```

Application runs on:

```bash
http://127.0.0.1:5000
```

---

# 🐳 Docker Deployment

## Build Docker Image

```bash
docker build -t therabot .
```

## Run Container

```bash
docker run -p 5000:5000 therabot
```

---

# ☁️ Render Deployment

## Example `render.yaml`

```yaml
services:
  - type: web
    name: therabot
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn app:app"
    envVars:
      - key: GEMINI_API_KEY
        sync: false
      - key: SECRET_KEY
        sync: false
```

---

# 📊 MLflow Integration

Therabot uses **MLflow** for:

- Experiment tracking
- Model versioning
- Metrics logging
- Performance monitoring

## Start MLflow UI

```bash
mlflow ui
```

Open:

```bash
http://127.0.0.1:5000
```

---

# 🧪 Model Training

## Train Emotion Detection Model

```bash
python mlops/train.py
```

## Evaluate Model

```bash
python mlops/evaluate.py
```

---

# 🔒 Security & Safety

Therabot is built with user safety in mind.

### Safety Features

- Distress detection
- Crisis-sensitive prompts
- Safe conversational boundaries
- Session protection
- Secure authentication

> ⚠️ Disclaimer:
> Therabot is not a replacement for professional mental health care or emergency medical services.

---

# 📸 UI Preview

## 💬 AI Chat Interface

![Chat UI](https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=1200&auto=format&fit=crop)

---

## 🌗 Responsive Dashboard

![Dashboard](https://images.unsplash.com/photo-1498050108023-c5249f4df085?q=80&w=1200&auto=format&fit=crop)

---

## 🧠 Emotion Detection System

![Emotion AI](https://images.unsplash.com/photo-1504384308090-c894fdcc538d?q=80&w=1200&auto=format&fit=crop)

---

# 🚀 Future Improvements

- Voice-based conversations
- Multi-language support
- Therapist recommendations
- AI journaling assistant
- Emotion analytics dashboard
- PostgreSQL integration
- Cloud-native deployment

---

# 🤝 Contributing

Contributions are welcome!

## Steps

```bash
# Fork repository

# Create branch
git checkout -b feature-name

# Commit changes
git commit -m "Added new feature"

# Push branch
git push origin feature-name
```

Then create a Pull Request 🚀

---

# 📄 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Author

## Puspak Dakkata

Final Year Computer Science Student  
AI/ML • MLOps • Flask • Generative AI

---

<div align="center">

## ⭐ If you like this project, give it a star!

Built with ❤️ using Flask, Gemini & Machine Learning

</div>
