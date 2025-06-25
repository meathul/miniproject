# SmartReco

A full-stack AI-powered product recommendation system.

## Project Structure

```
smartreco/
│
├── backend/
│   ├── agents/
│   │   └── smartreco_agent.py
│   ├── tools/
│   │   ├── filter_tool.py
│   │   ├── compare_tool.py
│   │   ├── summarize_tool.py
│   │   └── scrape_tool.py
│   ├── vector_store/
│   │   └── setup_vector_store.py
│   ├── api/
│   │   └── routes.py
│   ├── data/
│   │   └── product_catalog.csv
│   ├── .env
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── ProductCard.jsx
│   │   │   └── PreferencesForm.jsx
│   │   ├── pages/
│   │   │   └── Home.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── index.js
│   │   └── styles/
│   │       ├── global.css
│   │       └── product.css
│   └── package.json
│
└── README.md
```

## Backend
- Python (FastAPI or Flask)
- LangChain agent-based logic
- Tools: semantic search (FAISS/ChromaDB), filtering, comparison, summarization, web scraping
- Embeddings: OpenAI or SentenceTransformers
- Vector DB: FAISS or ChromaDB
- Data: CSV/JSON product catalog

## Frontend
- React
- CSS styling
- Components: Chat UI, Product Cards, Preferences Form
- API service for backend communication

---

See subfolders for more details and placeholder files to get started. 