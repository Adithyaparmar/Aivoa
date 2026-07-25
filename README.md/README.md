# AIVOA – AI Assisted Pharmaceutical Complaint Management System

This project was developed as part of the **AIVOA Full Stack Developer Assessment**.

The goal was to build an AI-assisted complaint management system for pharmaceutical companies that can extract important information from customer complaints and automatically populate a complaint form. Instead of manually reading emails or documents, the application uses an AI workflow built with **LangGraph** and **Groq LLMs** to identify the relevant details and return structured data.

---

## Features

- Extracts complaint details using AI
- Automatically fills the complaint form
- Built using a LangGraph-based AI workflow
- FastAPI backend with REST APIs
- React + Redux frontend
- PostgreSQL database integration
- Clean and responsive interface
- Structured JSON output from the LLM

---

## Tech Stack

### Frontend

- React
- Redux Toolkit
- Vite
- Axios
- CSS

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic

### AI

- LangGraph
- Groq API
- Llama-3.3-70B-Versatile

---

## How it Works

1. The user uploads a complaint document or pastes complaint text.
2. The frontend sends the data to the FastAPI backend.
3. LangGraph starts the extraction workflow.
4. Groq processes the complaint and returns structured JSON.
5. The backend validates the extracted data.
6. The complaint form is automatically populated.
7. The complaint can then be reviewed and stored in PostgreSQL.

---

## Information Extracted

The AI extracts fields such as:

- Complaint Source
- Customer Name
- Product Name
- Product Strength
- Batch/Lot Number
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
├── aivoa-backend
│   ├── app
│   ├── alembic
│   └── ...
│
├── aivoa-frontend
│   ├── src
│   └── ...
│
└── README.md
```

---

## API

### Process Complaint

```
POST /api/complaints/process
```

Accepts complaint text and returns structured complaint data extracted by the AI workflow.

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

## Design Choices

A few decisions made while building the project:

- **FastAPI** was chosen for its simplicity and performance.
- **React + Redux** keeps the frontend organized and makes state management easier.
- **LangGraph** provides a clear workflow for AI processing instead of placing all logic in a single function.
- **PostgreSQL** stores complaint data in a structured and reliable way.
- The AI returns **JSON-only responses**, making the extracted data easier to validate and display.

---

## Future Improvements

If this project were expanded further, possible additions include:

- OCR support for scanned PDFs
- Duplicate complaint detection
- Root cause suggestions
- CAPA recommendations
- Authentication and role-based access
- Complaint dashboard and analytics

---

## Assignment Requirements Covered

- ✔ React with Redux
- ✔ FastAPI
- ✔ LangGraph
- ✔ PostgreSQL
- ✔ Groq LLM Integration
- ✔ AI-Based Complaint Extraction
- ✔ REST APIs
- ✔ Responsive User Interface

---

## About

Developed by **Aditya Parmar**

B.Tech Computer Science Engineering (AI & ML)

Noida Institute of Engineering and Technology

**GitHub:** https://github.com/Adithyaparmar

**LinkedIn:** www.linkedin.com/in/adithyaparmar

---

## License

This project was created for the **AIVOA Full Stack Developer Assessment** and is intended for educational and evaluation purposes.