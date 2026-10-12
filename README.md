# Solid Local LangChain RAG – Lernprojekt

Dieses Repository ist ein **gemeinsam erweiterbares Lern-Template** für eine vollständig lokale RAG-Anwendung. Wir bauen es schrittweise aus, damit jede Stufe verständlich bleibt: Dokumente laden → strukturieren → in Chunks teilen → einbetten → in Chroma speichern → passende Chunks abrufen → Antwort mit Quellen erzeugen → über Gradio bedienen.

> Status: **Grundgerüst / Lern-Template**. Die Architektur, Schnittstellen, Konfiguration, Beispielinhalte und Tests sind vorbereitet. Einige Stellen sind bewusst mit `TODO` markiert, damit wir sie gemeinsam implementieren und verstehen können.

## Geplante Funktionen

- LangChain-basierte RAG-Pipeline
- PDF-, TXT- und Markdown-Loader
- `PyMuPDFLoader` mit Seitenmetadaten
- `MarkdownHeaderTextSplitter`
- `RecursiveCharacterTextSplitter` mit Chunk Overlap
- lokale Embeddings über Ollama
- persistente Chroma-Vektordatenbank
- drei Retriever-Modi:
  1. Similarity Search
  2. MMR für Relevanz und Vielfalt
  3. Similarity Score Threshold
- lokales LLM über Ollama
- Quellenangaben in Antworten
- Retry-Mechanismus für Verbindungsfehler
- Gradio-Weboberfläche
- Beispieldokument und Tests
- `.env.example`, `.gitignore` und `requirements.txt`

## Architektur

```text
Dokumente (.pdf/.txt/.md)
        │
        ▼
Document Loader
(PyMuPDFLoader / TextLoader)
        │
        ▼
Dokumentspezifisches Splitting
(MarkdownHeaderTextSplitter)
        │
        ▼
Feineres Chunking
(RecursiveCharacterTextSplitter + Overlap)
        │
        ▼
OllamaEmbeddings ──► Chroma (persistent)
                         │
Frage ──────────────────┤
                         ▼
Retriever (Similarity / MMR / Threshold)
                         │
                         ▼
Prompt + Kontext + Quellen
                         │
                         ▼
ChatOllama ──► Antwort mit Quellen
                         │
                         ▼
                    Gradio UI
```

## Projektstruktur

```text
solid-langchain-rag-template/
├── app.py
├── ingest.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── data/
│   └── beispiel_wissensbasis.md
├── chroma_db/
│   └── .gitkeep
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
└── tests/
    ├── test_loaders.py
    └── test_splitter.py
```

## Voraussetzungen

- Python 3.11 oder 3.12 empfohlen
- Git
- Ollama lokal installiert und gestartet
- ausreichend Speicher für die gewählten Modelle

**Hinweis für Firmengeräte:** Vor Installation oder Nutzung von Ollama bitte interne Freigaben, Toolmanagement und Datenschutzvorgaben prüfen.

## Installation

### 1. Projekt entpacken und öffnen

```bash
cd solid-langchain-rag-template
```

### 2. Virtuelle Umgebung erstellen

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Abhängigkeiten installieren

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Umgebungsdatei erstellen

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Linux/macOS:

```bash
cp .env.example .env
```

### 5. Ollama-Modelle laden

Die Modellnamen stehen in `.env`. Beispiel:

```bash
ollama pull nomic-embed-text
ollama pull llama3.2
```

Prüfen, ob Ollama erreichbar ist:

```bash
ollama list
```

## Geplanter Ablauf

### Index aufbauen

```bash
python ingest.py
```

### Weboberfläche starten

```bash
python app.py
```

Danach wird die lokale Gradio-Adresse im Terminal angezeigt.

### Tests starten

```bash
pytest -q
```

## Retriever-Modi

### `similarity`
Liefert die Chunks mit der höchsten semantischen Ähnlichkeit zur Frage. Das ist der einfachste Ausgangspunkt.

### `mmr`
MMR bedeutet Maximum Marginal Relevance. Der Modus versucht, gleichzeitig relevante und untereinander weniger redundante Chunks zu liefern.

### `threshold`
Liefert nur Chunks, deren Ähnlichkeitswert den konfigurierten Mindestwert erreicht. Dadurch kann die Pipeline bei unpassenden Fragen bewusst ohne Kontext antworten.

## Metadaten und Quellen

Jeder geladene Datensatz soll mindestens diese Metadaten tragen:

- `source`: Pfad der Quelldatei
- `file_name`: Dateiname
- `file_type`: `pdf`, `txt` oder `md`
- `page`: PDF-Seite, sofern vorhanden
- `header_1`, `header_2`, `header_3`: Markdown-Überschriften, sofern vorhanden

Die Antwort zeigt anschließend deduplizierte Quellen. Seitenwerte werden menschenfreundlich als Seite 1, 2, 3 usw. ausgegeben.

## Lernplan für unsere gemeinsame Umsetzung

1. **Loader vollständig verstehen und testen**
2. **Markdown- und rekursives Chunking vergleichen**
3. **Ollama Embeddings anbinden**
4. **Chroma persistent aufbauen und erneut laden**
5. **drei Retriever-Modi praktisch vergleichen**
6. **RAG-Prompt und lokale Generierung implementieren**
7. **Quellen sauber formatieren**
8. **Retry und verständliche Fehlermeldungen ergänzen**
9. **Gradio-Oberfläche fertigstellen**
10. **Tests und GitHub-Dokumentation vervollständigen**

## Sicherheit und Datenschutz

- Keine vertraulichen Unternehmensdaten in ein öffentliches GitHub-Repository hochladen.
- `data/`, `.env` und `chroma_db/` sind standardmäßig ignoriert; nur das öffentliche Beispieldokument wird gezielt aufgenommen.
- Vor dem Einsatz auf Firmenhardware interne Vorgaben für Ollama, Modelle und Python-Pakete prüfen.
- Auch bei lokaler Verarbeitung können Dokumente sensible Inhalte enthalten. Zugriffsrechte und Löschkonzept gehören später zur produktiven Lösung.

## Nächster gemeinsamer Schritt

Wir beginnen mit `loaders.py`: Wir schauen uns die Ausgabe jedes Loaders und die erzeugten Metadaten an. Danach implementieren wir das Chunking nachvollziehbar und testen es am Beispieldokument.
