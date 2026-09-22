# AI-Powered Visual Data Analytics & Business Intelligence

## Milestone 3 — Practice Package

---

## 📁 Project Structure

```
AI-POWERED-VISUAL-DATA-ANALYTICS-AND-BUSINESS-INTELLIGENCE/
│
├── data/
│   └── safety_manual.pdf          ← Place your PDF here
│
├── src/
│   ├── documents/
│   │   ├── __init__.py
│   │   ├── chunker.py             ← Splits text into chunks for RAG
│   │   ├── document_loader.py     ← Loads PDF / DOCX / TXT files
│   │   ├── metadata.py            ← Extracts file & chunk metadata
│   │   └── text_cleaner.py        ← Cleans & normalises raw text
│   │
│   └── knowledge_base/
│       ├── __init__.py
│       └── database.py            ← ChromaDB vector knowledge base
│
├── best.pt                        ← Fine-tuned PPE YOLO model (you provide)
├── yolov8n.pt                     ← YOLOv8 nano (auto-downloaded)
│
├── ppe_model.py                   ← PPE detection wrapper
├── vision.py                      ← Real-time vision pipeline
├── yolo_model.py                  ← General YOLO detection wrapper
│
├── milestone3_practice.py         ← ✅ Main entry point — run this!
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add required files
| File | Where to get it |
|---|---|
| `data/safety_manual.pdf` | Provided by your instructor |
| `best.pt` | Your trained PPE model weights |
| `yolov8n.pt` | Auto-downloaded on first run |

---

## 🚀 Running the Code

### Full pipeline (Milestone 3 practice)
```bash
python milestone3_practice.py
```

### Live webcam (PPE monitoring)
```bash
python vision.py
```

### Single image
```bash
python vision.py --image path/to/photo.jpg
```

### Video file
```bash
python vision.py --video path/to/clip.mp4
```

### Individual module tests
```bash
python src/documents/document_loader.py
python src/documents/text_cleaner.py
python src/documents/chunker.py
python src/knowledge_base/database.py
python yolo_model.py path/to/image.jpg
```

---

## 🧠 Pipeline Overview

```
safety_manual.pdf
      │
      ▼
DocumentLoader  →  raw text
      │
      ▼
TextCleaner     →  cleaned text
      │
      ▼
Chunker         →  list[TextChunk]
      │
      ▼
KnowledgeBase   →  embeddings stored in ChromaDB
      │
      ▼
kb.search(query) →  relevant chunks  →  LLM answer
```

---

## 📦 Module Reference

| Module | Class | Key Method |
|---|---|---|
| `document_loader.py` | `DocumentLoader` | `.load(path)` |
| `text_cleaner.py` | `TextCleaner` | `.clean(text)` |
| `chunker.py` | `Chunker` | `.split(text)` |
| `metadata.py` | `MetadataExtractor` | `.extract(path, text)` |
| `database.py` | `KnowledgeBase` | `.add_chunks()` / `.search()` |
| `yolo_model.py` | `YOLODetector` | `.detect(source)` |
| `ppe_model.py` | `PPEDetector` | `.detect(source)` |
| `vision.py` | `VisionPipeline` | `.run_webcam()` / `.run_image()` |

---

## ❓ Troubleshooting

| Error | Fix |
|---|---|
| `ModuleNotFoundError: ultralytics` | `pip install ultralytics` |
| `ModuleNotFoundError: chromadb` | `pip install chromadb` |
| `ModuleNotFoundError: sentence_transformers` | `pip install sentence-transformers` |
| `FileNotFoundError: best.pt` | Place your trained model in the project root |
| Camera not opening | Check `camera_id=0` in `vision.py`; try `camera_id=1` |
