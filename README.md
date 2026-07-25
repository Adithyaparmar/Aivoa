# AIVOA – AI Assisted Pharmaceutical Complaint Management System

## Overview

This project was developed as part of the AIVOA Full Stack Developer Assessment.
The goal was to build an AI-powered complaint management system that helps pharmaceutical quality teams process customer complaints more efficiently. Instead of manually filling out complaint forms, users can simply paste complaint text (or upload a document), and the system automatically extracts the important information using an AI workflow.
The extracted data is then validated, stored in a PostgreSQL database, and displayed in the complaint form for further review.
---

## Features
- Extracts complaint information using AI
- Automatically fills the complaint form
- Stores complaint records in PostgreSQL
- LangGraph-based AI workflow
- FastAPI REST backend
- React + Redux frontend
- Modern and responsive user interface

---

## Tech Stack

### Frontend
- React
- Redux Toolkit
- JavaScript
- Vite
- Axios

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic

### AI
- LangGraph
- Groq API
- Llama 3.3 70B Versatile
- Structured JSON Output

---
## How It Works
1. The user pastes complaint text into the application.
2. React sends the complaint to the FastAPI backend.
3. LangGraph starts the AI workflow.
4. Groq extracts structured complaint information.
5. The extracted data is validated.
6. The complaint is stored in PostgreSQL.
7. The frontend automatically updates the complaint form.

---

## Information Extracted

The AI extracts fields including:
- Complaint Source
- Customer Name
- Product Name
- Product Strength
- Batch / Lot Number
- Manufacturing Date
- Expiry Date
- Quantity Affected
- Complaint Type
- Complaint Description
- Complaint Date

---

## Project Structure

```
Aivoa
│
├── aivoa-frontend
│
├── aivoa-backend
│   ├── app
│   ├── alembic
│   └── requirements.txt
│
└── README.md
```

---

## API Endpoints

### Process Complaint

```
POST /api/complaints/process
```

Accepts complaint text, runs the AI workflow, and returns structured complaint data.

---

### AI Chat

```
POST /api/chat
```

Provides AI-generated responses related to the complaint.

---

## Running the Project

### Backend

```bash
cd aivoa-backend

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

### Frontend

```bash
cd aivoa-frontend

npm install

npm run dev
```

---

## Environment Variables

Create a `.env` file inside the backend directory.

```env
DATABASE_URL=postgresql://username:password@localhost:5432/aivoa

GROQ_API_KEY=your_api_key
```

---

## Why I Chose This Architecture

I wanted to keep the application modular so that each part has a clear responsibility.

- React handles the user interface.
- Redux manages frontend state.
- FastAPI exposes REST APIs.
- LangGraph manages the AI workflow.
- Groq performs structured complaint extraction.
- PostgreSQL stores complaint records.

This separation makes the application easier to understand and extend.

---

## Future Improvements

Some features that could be added in future versions include:

- OCR support for scanned PDFs
- Duplicate complaint detection
- Complaint severity prediction
- Complaint summarization
- Root cause recommendations
- User authentication and role management

---

## Assignment Requirements Covered

- React + Redux
- FastAPI
- LangGraph
- PostgreSQL
- Groq LLM Integration
- AI Complaint Extraction
- REST API
- Responsive User Interface

---

## About Me

**Aditya Parmar**
B.Tech Computer Science Engineering (AI & ML)
Noida Institute of Engineering and Technology

GitHub:
https://github.com/Adithyaparmar

LinkedIn:
https://www.linkedin.com/in/adithyaparmar
----

## Note

This project was built for the AIVOA Full Stack Developer Assessment. The focus was on implementing the required workflow using the specified technology stack while keeping the code clean, modular, and easy to understand.
