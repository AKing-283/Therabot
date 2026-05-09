# Therabot — AI Mental Wellness Companion

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_App-black?style=for-the-badge&logo=flask)
![MLflow](https://img.shields.io/badge/MLflow-MLOps-blue?style=for-the-badge)
![Codecov](https://img.shields.io/badge/Codecov-Test_Coverage-orange?style=for-the-badge)
![Google Gemini](https://img.shields.io/badge/Gemini-AI_Model-green?style=for-the-badge&logo=google)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

### 🚀 AI-Powered Emotional Support & Mental Wellness Platform

*An intelligent conversational assistant designed to provide empathetic interactions, emotional understanding, and mental wellness support using Generative AI + MLOps practices.*

</div>

---

# ✨ Features

## 🤖 AI Conversational Support
- Real-time AI-powered mental wellness conversations
- Context-aware empathetic responses
- Google Gemini integration
- Async chat experience without page reloads

---

## 😊 Emotion Detection System
- Detects emotional tone from user messages
- Machine Learning based classification
- Supports:
  - Anxiety
  - Stress
  - Sadness
  - Happiness
  - Neutral emotions

---

## 🆘 Crisis & Distress Detection
- Identifies harmful or distress-related messages
- Displays emergency mental health resources
- Safety-focused conversational handling

---

## 🔐 Authentication System
- User Signup/Login
- Secure session management
- Persistent user chat history

---

## 🌗 Modern UI/UX
- Fully responsive interface
- Dark/Light theme toggle
- Smooth chat interactions
- Mobile-friendly design

---

## 📚 Mental Wellness Resources
- FAQs
- Self-help resources
- Wellness guidance sections

---

# 🏗️ System Architecture

```text
User
  ↓
Flask Web Application
  ↓
AI Processing Layer
  ├── Google Gemini API
  ├── Emotion Detection Model
  └── Distress Detection Logic
  ↓
SQLite Database
  ↓
MLflow Tracking + MLOps
