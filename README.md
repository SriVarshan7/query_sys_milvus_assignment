# AI-Powered Query System

This is an AI-powered query system that allows users to upload URLs, images, and PDFs, extract text, store embeddings in a Milvus vector database, and query the content using a generative AI model (powered by Google Gemini). It features a Streamlit frontend and a FastAPI backend, deployed with Docker for Milvus.

---

## Features
- **Multi-Source Input**: Supports text extraction from URLs, images (via OCR), and PDFs.
- **Vector Storage**: Uses Milvus (via Docker) to store and search text embeddings.
- **AI Querying**: Answers questions based on stored content using the Gemini model.
- **Clear Memory**: Option to reset the Milvus collection via the frontend.
- **Real-Time Updates**: Backend reloads automatically with Uvicorn for development.

---

## Prerequisites
- **Python 3.8+**
- **Docker** (for Milvus)
- **Git**
- **Tesseract OCR** (for image text extraction)
- **Internet Connection** (for Gemini API and dependencies)

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/SriVarshan7/query_sys_milvus_assignment.git
cd query_sys_milvus_assignment
```

### 2. Set Up a Virtual Environment
Create and activate a virtual environment:

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root with your Gemini API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Install Tesseract OCR
**Windows:** Download and install Tesseract from GitHub. Add installation path to system PATH.

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

### 6. Start Milvus with Docker

Go to **PowerShell** (Run as Administrator)

1. Download the Milvus standalone Docker Compose file:
   ```bash
   Invoke-WebRequest https://github.com/milvus-io/milvus/releases/download/v2.4.15/milvus-standalone-docker-compose.yml -OutFile docker-compose.yml
   ```

2. Start Milvus with Docker Compose:
   ```bash
   docker compose up -d
---

## Running the Application

### 1. Start the Backend
```bash
uvicorn src.api.main:app --reload
```
Access at [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 2. Start the Frontend
```bash
streamlit run src/frontend/app.py
```
Access at [http://localhost:8501](http://localhost:8501)

### 3. Test the Application
- **Insert Sources:** Upload URLs, images, or PDFs.
- **Query:** Ask questions based on uploaded content.
- **Clear Memory:** Reset Milvus collection.

---

## Usage Flow
1. Upload a URL, image, or PDF.
2. Backend extracts text, generates embeddings, and stores in Milvus.
3. Query content through frontend.
4. Clear memory when needed.

---

## Code Structure

### Backend (`src/api/main.py`)
- **Endpoints:** `/insert`, `/query`, `/clear`
- **Modules:**
  - `data_extraction.py`: Text extraction.
  - `embeddings.py`: Embedding generation.
  - `milvus_ops.py`: Milvus management.
  - `generative_ai.py`: Gemini AI querying.

### Frontend (`src/frontend/app.py`)
- **Functions:**
  - Upload and insert sources.
  - Query system.
  - Clear memory.

---

## Troubleshooting
- **File errors:** Ensure temp directory is writable.
- **Milvus issues:** Check Docker container status.
- **OCR errors:** Ensure Tesseract is installed and properly configured.

---

## Contributing
Fork, create a branch, commit changes, and submit a pull request.

---

## License
Free to modify and distribute.

---

## Acknowledgments
- Milvus for vector database.
- Streamlit for frontend framework.
- Google Gemini for generative AI capabilities.
