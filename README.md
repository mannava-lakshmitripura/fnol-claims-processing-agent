# Autonomous Insurance Claims Processing Agent (FNOL)

## Problem Understanding

Insurance companies receive FNOL (First Notice of Loss) documents in PDF or TXT formats that often contain unstructured, incomplete, or inconsistent information.  
Manual processing of these documents slows down claim handling and increases operational costs.

The goal of this project is to build a lightweight autonomous agent that can:
- Extract key fields from FNOL documents
- Identify missing mandatory information
- Classify claims based on business rules
- Route claims to the appropriate workflow
- Provide a clear explanation for each routing decision

---

## Approach

The solution is implemented as a **backend API with a frontend interface**.

- The **backend (Flask)** processes FNOL documents, extracts structured information using rule-based parsing, validates mandatory fields, and applies routing rules.
- The **frontend (React + Vite)** allows users to upload multiple FNOL documents and displays extracted fields, missing fields, and routing decisions in a clean UI.

The system is modular and can be extended with NLP or LLM-based approaches.

---

## Tech Stack

### Backend
- Python
- Flask
- pdfplumber
- Regular Expressions
- Flask-CORS

### Frontend
- React
- Vite
- JavaScript
- CSS

---

## How to Run

### Backend (Flask)

1. Create virtual environment:
```bash
python -m venv venv
```
2. Activate virtual environment:
```bash
venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the backend:
```bash
python app.py
```
Backend will run at:
```bash
http://localhost:5000
```
### Frontend (React + Vite)
1. Install dependencies:
```bash
npm install
```
2. Create .env file:
```bash
VITE_API_BASE_URL=http://localhost:5000
```
3. Run the frontend:
```bash
npm run dev

```
Frontend will run at:
```bash
http://localhost:5173

```

## Routing Logic Summary

- **Manual Review**
  - Triggered when any mandatory field is missing

- **Investigation Flag**
  - Triggered when the description contains keywords such as `fraud`, `staged`, or `inconsistent`

- **Specialist Queue**
  - Triggered when the claim type is `injury`

- **Fast-track**
  - Triggered when the estimated damage is less than 25,000

- **Standard Processing**
  - Default route when no conditions match
