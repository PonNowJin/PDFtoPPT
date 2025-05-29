# PDFtoPPT — KI-gestützter Generator für akademische Präsentationen

🌐 Sprache wählen: [繁體中文](./README.zh-tw.md) | [English](./README.md)

Automatische Umwandlung wissenschaftlicher PDF-Dokumente in klar strukturierte PowerPoint-Folien – mit extrahierten Abbildungen, zusammengefassten Inhalten und einem eleganten Layout.

---

## 🚀 Schnellstart

### 1. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 2. Gemini API-Schlüssel einrichten

* Erstelle eine `.env`-Datei im Verzeichnis `Gemini/` (oder benenne `.env.example` in `.env` um)
* Füge folgende Zeile hinzu (ohne Anführungszeichen):

```bash
GEMINI_API_KEY=your_api_key_here
```

### 3. Backend-Server starten

```bash
fastapi run app.py
```

### 4. Öffne das Frontend im Browser und beginne mit der Konvertierung!

---

## Benutzerdefiniertes Foliendesign (optional)

Du kannst dein eigenes PowerPoint-Design (`.pptx`) hochladen, um den Folienstil individuell anzupassen:

* **Empfohlenes Seitenverhältnis:** 4:3 für optimale Layout-Ergebnisse
* Speichere dein PowerPoint-Design und lade es über die Weboberfläche hoch
* Falls kein Design hochgeladen wird, verwendet das System eine Standardvorlage

---

## Bildextraktion aus PDFs (YOLO-Modell)

Ein integriertes YOLO-Modell erkennt und extrahiert automatisch Abbildungen, Diagramme und Tabellen aus PDF-Dokumenten:

* Skript: `FetchImage/extracted_yolo.py`
* Ausgabe:

  * `Crop_imgs/`: Gespeicherte Bildausschnitte
  * `output_metadata.json`: Metadaten zu Position und Seitenzahl der Bilder

### Manuelle Ausführung:

```bash
cd FetchImage
python3 extracted_yolo.py
```

---

## Integration von Gemini

Das System nutzt die Google Gemini API zur automatischen Inhaltszusammenfassung und zur Erzeugung strukturierter Foliensätze.

### Konfiguration:

1. Hole dir deinen API-Schlüssel von [Google AI Studio](https://aistudio.google.com/u/3/prompts/new_chat)
2. Speichere den Schlüssel in `Gemini/.env`
3. Passe `Gemini/prompt.txt` an, um den Generierungsstil zu verändern

---

## Projektstruktur

| Ordner / Datei         | Beschreibung                            |
| ---------------------- | --------------------------------------- |
| `app.py`               | Hauptskript des FastAPI-Backends        |
| `Gemini/`              | Gemini-API-Integration und Prompt-Setup |
| `FetchImage/`          | Logik für Bilderkennung und Zuschnitt   |
| `pptx_api/`            | Generierung von PowerPoint-Folien       |
| `Crop_imgs/`           | Gespeicherte Bildausschnitte            |
| `output_metadata.json` | Metadaten zur Bild- und Seitenzuordnung |

---

## Empfohlene Anwendungsfälle

* Vorbereitung akademischer Präsentationen (z. B. Verteidigung einer Abschlussarbeit)
* Automatische Folienerstellung für wissenschaftliche Artikel
* Schnelle visuelle Zusammenfassungen für Forschende

---

## Feedback & Zusammenarbeit

Wir freuen uns über Anregungen und Kooperationsvorschläge. Bitte kontaktiere unser Entwicklerteam für weitere Informationen.
