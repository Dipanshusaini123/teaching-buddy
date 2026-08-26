# 🧑‍🏫 Teaching Buddy

**Teaching Buddy** is an AI-powered learning assistant designed to help students learn through interactive conversations.

Unlike a basic chatbot, Teaching Buddy maintains conversation context and uses **short-term memory + long-term summarized memory** to provide a more continuous and personalized learning experience.

🌐 **Live Demo:** [Add your Streamlit deployment link]

---

## ✨ Features

* 🤖 **AI-powered teaching assistant**

  * Ask questions and get explanations in a conversational format.
  * Learn concepts step-by-step.

* 🧠 **Conversation Memory**

  * Maintains recent conversation history.
  * Creates a summarized long-term memory of important information from previous interactions.

* 📚 **Personalized Learning**

  * Remembers useful learning preferences and context.
  * Can adapt explanations based on previous conversations.

* 💬 **Conversational Context**

  * Understands previous messages instead of treating every question independently.

* 🔄 **Memory Management**

  * Uses a recent conversation buffer for short-term context.
  * Uses summarized information for long-term memory.

* 🌐 **Deployed Online**

  * The application is deployed using Streamlit and can be accessed through the web instead of running only on a local PC.

---

## 🧠 How Memory Works

Teaching Buddy uses two levels of memory:

### 1. Recent Conversation Buffer

The chatbot keeps a limited number of recent messages in short-term memory.

This allows the model to understand the immediate context of the conversation without sending the entire conversation history every time.

```text
User → Message
        ↓
Recent Conversation Buffer
        ↓
      LLM
        ↓
AI Response
```

### 2. Long-Term Memory

Important information from the conversation is summarized and stored as long-term memory.

For example, the system may remember that a user:

* Is learning programming
* Prefers step-by-step explanations
* Is interested in C++
* Likes practical examples

Instead of keeping every message forever, the system stores a **compact summary of important information**.

```text
Long Conversation
       ↓
   Summarization
       ↓
Long-Term Memory
       ↓
Future Conversations
```

This approach helps control the amount of context sent to the LLM while still maintaining useful information about the learner.

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │       User          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Streamlit UI      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Conversation Memory │
                    └───────┬─────┬───────┘
                            │     │
                ┌───────────┘     └────────────┐
                ▼                              ▼
       Recent Conversation              Long-Term Memory
            Buffer                       (Summary)
                │                              │
                └──────────────┬───────────────┘
                               ▼
                    ┌─────────────────────┐
                    │     Groq LLM        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    AI Response      │
                    └─────────────────────┘
```

---

## 🛠️ Tech Stack

| Technology       | Purpose                                 |
| ---------------- | --------------------------------------- |
| **Python**       | Application development                 |
| **Streamlit**    | Web interface and deployment            |
| **LangChain**    | LLM application framework               |
| **Groq**         | LLM inference                           |
| **dotenv**       | Local environment variable management   |
| **Git & GitHub** | Version control and source code hosting |

---

## 📂 Project Structure

```text
teaching-buddy/
│
├── coreui.py
├── requirements.txt
├── .gitignore
└── README.md
```

> The project structure may change as new features are added.

---

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Dipanshusaini123/teaching-buddy.git
cd teaching-buddy
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project directory:

```env
GROQ_API_KEY=your_api_key_here
```

**Never commit your `.env` file or API keys to GitHub.**

Make sure `.env` is included in `.gitignore`.

### 5. Run the application

```bash
streamlit run coreui.py
```

The application will open in your browser.

---

## ☁️ Deployment

Teaching Buddy is deployed using **Streamlit**.

For deployment, the API key should be stored securely using Streamlit's secrets management rather than committing it to the repository.

Example:

```toml
GROQ_API_KEY = "your_api_key_here"
```

The secret should be configured through the deployment platform's settings.

---

## 🔐 Security

API keys and other sensitive credentials should **never** be committed to GitHub.

For local development:

```text
.env
```

should be included in `.gitignore`.

For deployment, use the platform's secure secrets management.

---

## 📸 Application

### Teaching Buddy

The application provides a conversational interface where users can ask questions and receive explanations.

### Memory System

Teaching Buddy includes both:

* **Long-term memory**
* **Recent conversation buffer**

This allows the application to maintain useful context without continuously sending the entire conversation history to the LLM.

---

## 🎯 What I Learned

Building Teaching Buddy helped me understand several important concepts in AI application development:

* How to integrate an LLM into a real application
* Working with LangChain
* Managing conversation history
* Implementing short-term and long-term memory
* Using summarization to control context size
* Managing API keys securely
* Using Git and GitHub
* Deploying a Streamlit application
* Debugging deployment-specific problems
* Taking an AI application from **local development to a publicly accessible application**

One of the biggest lessons was that building an AI application is not just about calling an LLM. **The engineering around the model—memory, context management, security, UI, and deployment—is equally important.**

---

## 🔮 Future Improvements

Some features I would like to explore in future versions:

* 📌 Persistent memory across sessions
* 👤 User accounts and personalized profiles
* 📊 Learning progress tracking
* 📝 Automatic quizzes and exercises
* 🎯 Personalized study plans
* 📚 Document/PDF-based learning
* 🔎 Retrieval-Augmented Generation (RAG)
* 🗃️ Vector database integration
* 🎤 Voice-based interaction

---

## 👨‍💻 Author

**Dipanshu Saini**

GitHub: [@Dipanshusaini123](https://github.com/Dipanshusaini123)

---

⭐ If you find this project interesting, consider giving the repository a star!

**Teaching Buddy — from a local Python project to a deployed AI learning assistant. 🚀**
