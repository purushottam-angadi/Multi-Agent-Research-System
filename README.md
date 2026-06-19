# 🔬 AI Research Pipeline

Multi-agent research system using **LangGraph + Mistral AI + Tavily**, served via **FastAPI**, and visualized with a **Streamlit** multi-page UI — all containerized with **Docker**.

---

## 📁 Project Structure

```
research_app/
├── backend/
│   ├── main.py          # FastAPI app (async job queue)
│   ├── pipeline.py      # LangGraph pipeline
│   ├── agents.py        # Agent builders
│   ├── tools.py         # LangChain tools
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── Home.py          # Streamlit entry point + topic input
│   ├── pages/
│   │   ├── 1_Report.py
│   │   ├── 2_Critique.py
│   │   └── 3_Citations.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── .gitignore
```

---

## 🚀 Quick Start

### 1. Clone and configure

```bash
git clone <your-repo>
cd research_app
cp .env.example .env
# Fill in your API keys in .env
```

### 2. Add your API keys to `.env`

```env
MISTRAL_API_KEY=your_mistral_key
TAVILY_API_KEY=your_tavily_key
```

### 3. Build and run with Docker Compose

```bash
docker-compose up --build
```

### 4. Open in browser

| Service   | URL                        |
|-----------|---------------------------|
| Streamlit | http://localhost:8501      |
| FastAPI   | http://localhost:8000      |
| API Docs  | http://localhost:8000/docs |

---

## 🔄 How It Works

```
User enters topic
      ↓
Streamlit → POST /research → FastAPI (async job)
      ↓
Streamlit polls GET /research/{job_id} every 4s
      ↓
Pipeline runs: Search → Scrape → Write → Critique → Citations
      ↓
Results stored, Streamlit shows 3 navigable pages
```

---

## 📄 Pages

| Page         | Shows                                    |
|-------------|------------------------------------------|
| 🏠 Home      | Topic input, pipeline trigger, status    |
| 📄 Report    | Full structured research report          |
| 🧐 Critique  | Score, strengths, areas to improve       |
| 📚 Citations | APA and IEEE formatted references        |

Every page has a **Download** button to save the output as `.txt`.

---

## 🛠 Run Locally (without Docker)

```bash
# Terminal 1 – backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Terminal 2 – frontend
cd frontend
pip install -r requirements.txt
streamlit run Home.py
```

> Make sure your `.env` file is in the `backend/` folder when running locally.
