# 📈 Mutual Fund FAQ Assistant (Facts-Only RAG System)

A compliance-first **Retrieval-Augmented Generation (RAG)** application that answers factual questions about mutual fund schemes using official public sources. The assistant strictly avoids investment advice and provides concise, source-backed responses with transparent citations.

> **Facts-only. No investment advice.**

---

## 🚀 Project Overview

The Mutual Fund FAQ Assistant is designed to help retail investors quickly access verified information about mutual fund schemes without relying on opinions or recommendations.

Unlike generic AI chatbots, this system:

- Retrieves information only from trusted official sources
- Refuses advisory or comparison questions
- Grounds every answer in retrieved content
- Provides exactly one citation link with every response
- Maintains transparency using a "Last Updated" timestamp

---

## 🎯 Problem Statement

Investors frequently search for objective information such as:

- Expense Ratio
- Exit Load
- Minimum SIP
- Benchmark Index
- Riskometer
- Fund Manager Details
- Investment Objective
- Statement Download Process

Most AI assistants either hallucinate information or provide financial advice.

This project solves that problem by building a **facts-only retrieval system** that prioritizes compliance, transparency, and accuracy over conversational intelligence.

---

# ✨ Features

- ✅ Facts-only mutual fund Q&A
- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Semantic Search using Vector Embeddings
- ✅ Official source citations
- ✅ Query classification
- ✅ Automatic refusal for advisory questions
- ✅ Daily data refresh scheduler
- ✅ Clean chat interface
- ✅ Source-backed responses
- ✅ Privacy-first architecture

---

# 📚 Supported Queries

Examples:

- What is the expense ratio of HDFC Mid Cap Fund?
- Who manages HDFC Defence Fund?
- What is the minimum SIP amount?
- What is the benchmark index?
- What is the exit load?
- What is the investment objective?
- What is the fund house?

---

# ❌ Unsupported Queries

The assistant politely refuses questions such as:

- Should I invest?
- Which mutual fund is better?
- Will this fund give good returns?
- Compare HDFC and SBI funds
- Which fund should I buy?

Instead, it redirects users to educational resources from AMFI/SEBI.

---

# 🏗️ System Architecture

```
                    User Question
                          │
                          ▼
                Query Classification
             (Facts vs Advisory)
                    │        │
          Advisory  │        │ Facts
                    │        ▼
          Refusal Handler   Retriever
                    │        │
                    │        ▼
                    │   Vector Database
                    │        │
                    ▼        ▼
              Response Generator (LLM)
                       │
                       ▼
               Output Validation
                       │
                       ▼
                Final Response
```

---

# ⚙️ Tech Stack

| Layer | Technology |
|---------|------------|
| Frontend | React / HTML / CSS |
| Backend | FastAPI |
| Language | Python |
| Embeddings | BGE Small / BGE Large |
| Vector Database | ChromaDB |
| LLM | Groq |
| Parsing | BeautifulSoup |
| Scheduler | GitHub Actions / APScheduler |
| Deployment | Vercel + Render |

---

# 📂 Project Structure

```
MutualFundFAQAssistant/
│
├── app/
│   ├── classifier.py
│   ├── retriever.py
│   ├── generator.py
│   ├── validator.py
│   └── formatter.py
│
├── ingestion/
│   ├── fetch.py
│   ├── parse.py
│   ├── chunk.py
│   ├── embed.py
│   └── run.py
│
├── scheduler/
│   └── daily.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── index/
│
├── docs/
│   ├── architecture.md
│   ├── implementation-plan.md
│   ├── edge-case.md
│   └── problemStatement.md
│
├── ui/
│
├── tests/
│
├── requirements.txt
│
└── README.md
```

---

# 🔄 Data Pipeline

```
Official Sources
       │
       ▼
 Fetch HTML Pages
       │
       ▼
 Clean & Parse Content
       │
       ▼
 Section Extraction
       │
       ▼
 Chunking
       │
       ▼
 Generate Embeddings
       │
       ▼
 Store in ChromaDB
       │
       ▼
 Ready for Retrieval
```

---

# 🤖 RAG Workflow

```
User Query
      │
      ▼
Query Classification
      │
      ▼
Metadata Filtering
      │
      ▼
Semantic Retrieval
      │
      ▼
Top Relevant Chunks
      │
      ▼
Groq LLM
      │
      ▼
Grounded Response
      │
      ▼
Citation + Last Updated
```

---

# 📖 Corpus

Currently indexed:

- HDFC Mid Cap Fund Direct Growth
- HDFC Large Cap Fund Direct Growth
- HDFC Small Cap Fund Direct Growth
- HDFC Gold ETF Fund of Fund Direct Growth
- HDFC Defence Fund Direct Growth

---

# 🛡️ Compliance

The assistant strictly follows:

- Facts-only responses
- No financial advice
- No recommendations
- No return predictions
- No comparisons
- No personal data collection
- One official citation per answer
- Maximum three sentences

---

# 🔍 Example

### User

```
Who manages HDFC Defence Fund?
```

### Assistant

```
HDFC Defence Fund Direct Growth is managed by Priya Ranjan, Dhruv Muchhal, and Rahul Baijal. Their tenure and experience are available on the official scheme page.

Source:
https://groww.in/mutual-funds/hdfc-defence-fund-direct-growth

Last Updated:
2026-05-29
```

---

# 📊 Future Improvements

- Support multiple AMCs
- Ingest AMFI & SEBI documents
- Multilingual support
- OCR for PDFs
- Admin dashboard
- Hybrid search
- Clarification questions
- Conversation memory
- Analytics dashboard

---

# 📌 Key Highlights

- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Compliance-first Design
- Source-backed Answers
- Query Classification
- Hallucination Reduction
- Automated Daily Data Refresh
- Lightweight Architecture
- Production-ready Project Structure

---

# ⚠️ Disclaimer

This assistant is intended **only for educational and informational purposes**.

It does **not** provide:

- Investment advice
- Financial recommendations
- Portfolio suggestions
- Return predictions

Always consult official AMC, AMFI, or SEBI resources before making investment decisions.

---

# 👨‍💻 Author

**Yashwanth (YS)**

If you found this project helpful, feel free to ⭐ the repository.
