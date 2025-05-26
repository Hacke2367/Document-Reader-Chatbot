# Due to some unexpected errors with the Git push process, the files in this repository have been uploaded manually. However, all the code and resources are fully updated and ready to use.
# I am aware of the repository structure issues and promise to fix and improve it as soon as possible. Thanks for your understanding and patience!



# Document-Reader-Chatbot
A production-ready Retrieval-Augmented Generation (RAG) chatbot built using FastAPI and LangChain, capable of answering questions based on multiple uploaded documents by leveraging transformer-based language models and vector search.

---

## Features

- Upload and process multiple documents for conversational queries  
- Semantic search using Chroma DB vector store for fast and accurate retrieval  
- Document metadata management using SQLite3  
- Modular and scalable FastAPI backend with asynchronous request handling  
- Robust error handling for smooth user experience  
- Integration with Hugging Face transformer models via LangChain for high-quality response generation

---

## Tech Stack

- **Language:** Python  
- **Backend Framework:** FastAPI  
- **NLP & ML:** Hugging Face Transformers, LangChain  
- **Vector Database:** Chroma DB  
- **Database:** SQLite3  
- **Others:** Asyncio, Uvicorn (for ASGI server)

---


├── app/
│   ├── main.py              # FastAPI app and endpoints
│   ├── chatbot.py           # RAG chatbot logic with LangChain
│   ├── vectorstore.py       # Chroma DB integration
│   ├── database.py          # SQLite3 management
│   └── utils.py             # Helper functions and error handling
├── requirements.txt
├── README.md
└── ...


