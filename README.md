# Local LangChain RAG

Eine vollständig lokal ausgeführte Retrieval-Augmented-Generation-Anwendung mit **LangChain**, **Ollama**, **ChromaDB** und **Gradio**.

Das Projekt verarbeitet PDF-, TXT- und Markdown-Dokumente, zerlegt sie strukturiert in Chunks, erzeugt lokale Embeddings, speichert diese persistent in ChromaDB und beantwortet Fragen mithilfe eines lokalen Sprachmodells. Die Antworten enthalten nachvollziehbare Quellenangaben. Zusätzlich bietet die Gradio-Oberfläche Funktionen zur Dokumentverwaltung, Index-Neuerstellung und Anzeige der Retrieval-Ergebnisse.


---

## Funktionsumfang

### Dokumentverarbeitung

- PDF-Loader über `PyMuPDFLoader`
- TXT- und Markdown-Loader
- PDF-Seitenmetadaten
- Metadaten für Dateiname, Dateityp und Quelle
- Upload von PDF-Dokumenten über die Gradio-Oberfläche
- technisches Beispieldokument für lokale Tests

### Intelligentes Chunking

- `MarkdownHeaderTextSplitter` für strukturierte Markdown-Inhalte
- `RecursiveCharacterTextSplitter` für feinere Textabschnitte
- konfigurierbare Chunk-Größe
- konfigurierbarer Chunk Overlap
- Übernahme der Dokument- und Abschnittsmetadaten

### Lokale Embeddings und Vektordatenbank

- lokale Embeddings über Ollama
- persistente ChromaDB-Vektordatenbank
- konfigurierbare Collection
- Aufbau und Wiederverwendung des Index
- Löschen und Neuaufbauen des Index

### Drei Retriever-Modi

1. **Similarity Search**  
   Liefert die semantisch ähnlichsten Chunks zur Benutzerfrage.

2. **Maximum Marginal Relevance, MMR**  
   Kombiniert Relevanz mit Vielfalt und reduziert redundante Ergebnisse.

3. **Similarity Score Threshold**  
   Liefert nur Ergebnisse, deren Relevanzwert den konfigurierten Mindestwert erreicht.

### Lokale Antwortgenerierung

- lokales LLM über `ChatOllama`
- `ChatPromptTemplate` für kontextgebundene Antworten
- Antworten ausschließlich auf Basis der gefundenen Dokumentabschnitte
- Quellenangaben mit Dateiname, Markdown-Überschrift und PDF-Seite
- verständliche Antwort, wenn kein ausreichend passender Kontext gefunden wurde

### Transparenz und Robustheit

- Anzeige der abgerufenen Chunks
- Anzeige von Similarity Scores
- Retry-Mechanismus bei vorübergehenden Ollama-Verbindungsfehlern
- verständliche Fehlerbehandlung
- detailliertes Logging
- Unit- und Integrationstests

### Benutzeroberfläche

- lokale Gradio-Weboberfläche
- Eingabefeld für Fragen
- Auswahl des Retriever-Modus
- Dokument-Upload
- Index-Neuerstellung
- Antwort- und Quellenanzeige
- Anzeige der gefundenen Chunks und Retrieval-Werte

---

## Architektur

```text
                         INGESTION

PDF / TXT / Markdown / Gradio Upload
                  │
                  ▼
          Document Loader
   PyMuPDFLoader / TextLoader
                  │
                  ▼
  MarkdownHeaderTextSplitter
                  │
                  ▼
RecursiveCharacterTextSplitter
        mit Chunk Overlap
                  │
                  ▼
        Chunks + Metadaten
                  │
                  ▼
       OllamaEmbeddings
                  │
                  ▼
     ChromaDB Vector Store
     persistent in chroma_db/

                         RETRIEVAL

          Benutzerfrage
                  │
                  ▼
       Embedding der Frage
                  │
                  ▼
             Retriever
 Similarity / MMR / Score Threshold
                  │
                  ▼
   Relevante Chunks + Scores

                         GENERATION

       Kontext + Benutzerfrage
                  │
                  ▼
       ChatPromptTemplate
                  │
                  ▼
          ChatOllama LLM
                  │
                  ▼
      Antwort + Quellenangaben
                  │
                  ▼
          Gradio Web UI
```

---

## Projektstruktur

```text
LangChain-RAG-Projekt/
├── app.py
├── ingest.py
├── requirements.txt
├── pytest.ini
├── .env.example
├── .gitignore
├── README.md
├── ROADMAP.md
│
├── data/
│   ├── beispiel_wissensbasis.md
│   ├── 01_doip_grundlagen.md
│   ├── 02_ethernet_grundlagen.md
│   ├── 03_datacapture_x2_handbuch.md
│   ├── 04_testablauf.pdf
│   └── README_TESTS.md
│
├── chroma_db/
│   └── .gitkeep
│
├── src/
│   └── local_rag/
│       ├── __init__.py
│       ├── config.py
│       ├── loaders.py
│       ├── splitter.py
│       ├── vectorstore.py
│       ├── retrievers.py
│       ├── retry.py
│       ├── prompts.py
│       ├── pipeline.py
│       └── ui.py
│
└── tests/
    ├── test_loaders.py
    ├── test_splitter.py
    ├── test_retry.py
    ├── test_vectorstore.py
    └── test_vectorstore_integration.py
```

Die genaue Liste der Test- und Beispieldateien kann sich während der Weiterentwicklung ändern.

---

## Voraussetzungen

- Python 3.11 oder 3.12
- Git
- lokal installiertes und gestartetes Ollama
- ausreichend RAM und Speicherplatz für die verwendeten Modelle


---

## Installation auf Windows

### 1. Repository klonen

```powershell
git clone <DEINE-REPOSITORY-URL>
cd LangChain-RAG-Projekt
```

### 2. Virtuelle Python-Umgebung erstellen

```powershell
python -m venv .venv
```

### 3. Virtuelle Umgebung aktivieren

```powershell
.\.venv\Scripts\Activate.ps1
```

Nach erfolgreicher Aktivierung erscheint `(.venv)` am Anfang der PowerShell-Zeile.

Falls PowerShell die Aktivierung blockiert:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### 4. pip aktualisieren

```powershell
python -m pip install --upgrade pip
```

### 5. Abhängigkeiten installieren

```powershell
pip install -r requirements.txt
```

### 6. Lokale Konfiguration erstellen

```powershell
Copy-Item .env.example .env
```

Die Datei `.env` darf nicht in Git eingecheckt werden.

---

## Installation auf Linux oder macOS

```bash
git clone <DEINE-REPOSITORY-URL>
cd LangChain-RAG-Projekt
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

---

## Ollama einrichten

Die Modellnamen werden über `.env` konfiguriert. Mit der Beispielkonfiguration werden folgende Modelle benötigt:

```bash
ollama pull nomic-embed-text
ollama pull llama3.2
```

Installierte Modelle prüfen:

```bash
ollama list
```

Ollama muss aktiv sein, bevor Dokumente indexiert oder Fragen beantwortet werden.

---

## Konfiguration

Beispiel für `.env`:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
OLLAMA_LLM_MODEL=llama3.2

DATA_DIR=./data
CHROMA_DIR=./chroma_db
CHROMA_COLLECTION=local_rag_documents

CHUNK_SIZE=800
CHUNK_OVERLAP=120

RETRIEVER_MODE=similarity
RETRIEVER_K=8
MMR_FETCH_K=12
SCORE_THRESHOLD=0.65

OLLAMA_RETRY_ATTEMPTS=3

GRADIO_HOST=127.0.0.1
GRADIO_PORT=7860
```

### Wichtige Parameter

- `CHUNK_SIZE`: maximale Größe eines Chunks
- `CHUNK_OVERLAP`: wiederholter Textbereich zwischen benachbarten Chunks
- `RETRIEVER_K`: Anzahl der zurückgegebenen Ergebnisse
- `MMR_FETCH_K`: Anzahl der zuerst betrachteten MMR-Kandidaten
- `SCORE_THRESHOLD`: Mindestwert für den Threshold-Retriever
- `OLLAMA_RETRY_ATTEMPTS`: maximale Zahl der Verbindungsversuche

---

## Anwendung starten

### 1. Dokumente vorbereiten

Lege unterstützte Dokumente in `data/` ab:

```text
.pdf
.txt
.md
```

Alternativ können PDF-Dokumente über die Gradio-Oberfläche hochgeladen werden.

### 2. Index aufbauen

```powershell
python ingest.py
```

Beim Indexieren passiert Folgendes:

```text
Dateien laden
→ Metadaten ergänzen
→ Text strukturieren
→ Chunks erzeugen
→ Embeddings berechnen
→ Chunks und Vektoren in ChromaDB speichern
```

### 3. Webanwendung starten

```powershell
python app.py
```

Die Anwendung ist anschließend standardmäßig unter folgender lokalen Adresse erreichbar:

```text
http://127.0.0.1:7860
```

### 4. Beispielanfragen

```text
Was ist DoIP?

Welche Aufgabe hat Tester Present?

Wie funktioniert eine Dateiübertragung über UDS?

Fasse die wichtigsten Inhalte des Testablaufs zusammen.
```

---

## Tests ausführen

Alle Tests starten:

```powershell
pytest -v
```

Nur einen bestimmten Test ausführen:

```powershell
pytest tests/test_splitter.py -v
```

Beispiele für geprüfte Bereiche:

- Loader und Metadaten
- Markdown- und rekursives Chunking
- Retry-Verhalten
- Vectorstore-Grundfunktionen
- ChromaDB-Integration

Bei Integrationstests muss Ollama verfügbar sein und das konfigurierte Embedding-Modell lokal vorliegen.

---

## Metadaten und Quellen

Je nach Dokumenttyp werden unter anderem folgende Metadaten gespeichert:

```text
source
file_name
file_type
page
header_1
header_2
header_3
start_index
```

Dadurch kann die Anwendung nicht nur eine Antwort generieren, sondern auch anzeigen, aus welcher Datei, PDF-Seite oder Markdown-Sektion die verwendete Information stammt.

---

## Bekannte Grenzen

- Die Antwortqualität hängt von Dokumentqualität, Chunking, Embedding-Modell, Retriever-Konfiguration und lokalem LLM ab.
- Eingescannte PDFs ohne extrahierbaren Text benötigen zusätzlich OCR.
- Der aktuelle Stand verwendet keinen Reranker und keine hybride Suche.
- ChromaDB und Ollama laufen lokal; es gibt aktuell keine Docker-Konfiguration.
- Die Anwendung ist als lokales Lern-, Demonstrations- und Portfolio-Projekt ausgelegt, nicht als produktiver Mehrbenutzerdienst.

---

## Verwendete Technologien

- Python
- LangChain
- LangChain Ollama Integration
- LangChain Chroma Integration
- Ollama
- ChromaDB
- Gradio
- PyMuPDF
- python-dotenv
- Tenacity
- Pytest

---

## Projektziel

Das Projekt zeigt praxisnah, wie eine lokale RAG-Anwendung modular aufgebaut, getestet und nachvollziehbar betrieben werden kann. Der Schwerpunkt liegt auf einer verständlichen Trennung der Verantwortlichkeiten:

```text
Loader → Splitter → Embeddings → Vectorstore → Retriever → Prompt → LLM → UI
```

Dadurch können einzelne Komponenten unabhängig untersucht, getestet und später ausgetauscht oder erweitert werden.

---

## Mögliche spätere Erweiterungen

Das aktuelle Projekt bleibt bewusst ohne Docker und kann in diesem Zustand abgeschlossen werden. Denkbare optionale Erweiterungen wären:

- Conversational Memory
- Streaming der Antworten
- Metadatenfilter
- Hybrid Search aus BM25 und Vektorsuche
- Reranking
- automatisierte RAG-Evaluation
- Unterstützung gescannter PDFs über OCR
- getrennte Collections für unterschiedliche Wissensbereiche

---

## Lizenz

Dieses Projekt wurde zu Lern-, Demonstrations- und Portfoliozwecken erstellt. Vor einer Weitergabe oder produktiven Nutzung müssen die Lizenzen der verwendeten Modelle, Bibliotheken und Dokumente geprüft werden.
