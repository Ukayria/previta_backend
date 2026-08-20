# PreVita — Prevention Before Cure

> **An AI-powered preventive healthcare platform designed to help users understand their symptoms and health risks, receive personalized health guidance, and connect with professional care.**

## 🌍 Overview

**PreVita** is a mobile-first healthcare technology platform built around the principle of **“Prevention Before Cure.”**

It combines AI-assisted symptom assessment, health-risk evaluation, and conversational AI to help users make more informed decisions about their health.

The long-term goal is to bridge the gap between **early health assessment and access to healthcare professionals**.

---

## 🎯 Problem

Many people experience health symptoms without knowing how serious they may be, what action to take, or when professional medical attention is necessary.

PreVita explores how **AI and digital health technologies can provide an accessible first layer of preventive health support while guiding users toward professional care when necessary.**

---

## 💡 How PreVita Works

Users can access different parts of the platform independently.

### 🩺 Symptom Checker

Users provide information about their symptoms, which is processed through the application's assessment and risk-evaluation workflow.

**Symptoms → Assessment → Risk Level → Health Guidance**

### 📊 Health Risk Engine

The risk engine evaluates relevant health information and assigns a corresponding risk level.

```text
Health Information
        ↓
   Risk Evaluation
        ↓
 ┌──────┼────────┐
 ▼      ▼        ▼
Low   Moderate   High
```

The risk engine is designed as a **decision-support component**, not a clinical diagnostic system.

### 🤖 LLM Health Chatbot

Users can access the AI chatbot directly without first completing the symptom checker.

The chatbot:

* Answers health-related questions
* Provides AI-assisted health information
* Can respond in the user's selected language
* Encourages users to use the symptom checker when further assessment may be appropriate
* Encourages users to seek professional medical attention when necessary

### 🌐 Multilingual Support

Users can select their preferred language, which is passed through the chatbot request flow so that the LLM can generate responses in the selected language.

### 🔐 Authentication & OTP

The backend includes user authentication and OTP verification to support secure account access.

---

# 👩🏾‍💻 My Role

## Backend Developer

I worked primarily on the **backend development of PreVita**, building several of the core services that power the application.

### Key Contributions

* **Symptom Checker** — developed backend functionality for processing user symptom information and supporting the assessment workflow.
* **Health Risk Engine** — developed the logic responsible for evaluating health information and determining risk levels.
* **LLM Chatbot** — integrated the backend with the Groq API and implemented the communication flow between users, the application, and the LLM.
* **Multilingual Chatbot** — implemented language-selection handling within the chatbot flow.
* **Authentication** — developed backend authentication functionality.
* **OTP Verification** — implemented OTP-based user verification.
* **API Development** — developed backend APIs connecting the frontend with the application's core services.

---

# 🏗️ Technology Stack

| Area           | Technologies        |
| -------------- | ------------------- |
| Backend        | Python, FastAPI     |
| AI             | LLM, Groq API       |
| Frontend       | React               |
| APIs           | REST APIs           |
| Authentication | Authentication, OTP |
| Development    | Git, GitHub         |

---

# 🔄 Architecture

```text
                         ┌───────────────┐
                         │     User      │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │ React Frontend│
                         └───────┬───────┘
                                 │
                              API Calls
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │    FastAPI Backend     │
                    │                        │
                    │ Authentication         │
                    │ OTP Verification       │
                    │ Symptom Checker        │
                    │ Risk Engine             │
                    │ LLM Integration         │
                    │ Language Handling       │
                    └───────────┬────────────┘
                                │
                       ┌────────┴────────┐
                       ▼                 ▼
                ┌────────────┐    ┌────────────┐
                │Risk Engine │    │ Groq / LLM │
                └────────────┘    └────────────┘
```

---

# 🚀 Current Status

**Live Product — Prototype / Product in Development**

### Currently functional

* ✅ Symptom Checker
* ✅ Health Risk Engine
* ✅ LLM Health Chatbot
* ✅ Multilingual chatbot interaction
* ✅ User Authentication
* ✅ OTP Verification
* ✅ Backend APIs
* ✅ AI Integration

### In development

The frontend currently includes planned healthcare-access features that are not yet fully operational:

* 🔄 Healthcare professional connection
* 🔄 Healthcare facility access
* 🔄 Appointment booking

These features will form part of the next stage of the platform after the necessary technical, clinical, privacy, and safety improvements are completed.

---

# 🗺️ Roadmap

### Healthcare Access

* [ ] Healthcare professional onboarding
* [ ] Professional profiles
* [ ] Healthcare facility integration
* [ ] Appointment scheduling
* [ ] Patient-provider communication

### Responsible Scale

* [ ] Clinical validation
* [ ] Evidence-based medical knowledge integration
* [ ] AI safety monitoring
* [ ] Privacy and data-governance improvements
* [ ] Expanded health-condition coverage

---

# 🔗 Project Links

**🌐 Live Product:** (https://previta-swart.vercel.app/)

**🎨 Frontend Repository:** `(https://github.com/Ukayria/PreVita_frontend)

---

# 👩🏾‍💻 Contributor

**Chinedu Eucharia Joseph**
*Backend Developer | AI/ML & Healthcare Technology*

**Core contributions:** Symptom Checker · Health Risk Engine · LLM Chatbot · Multilingual AI · Authentication · OTP · Backend APIs

---

## ⚕️ Disclaimer

PreVita is a healthcare technology prototype intended for informational and preventive-support purposes. It is **not a substitute for professional medical diagnosis, treatment, or emergency care**.

AI-generated information may contain errors, and the risk engine should not be interpreted as a clinical diagnosis.
