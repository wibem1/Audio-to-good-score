# Audio to Good Score

Lokaler Web-App-Prototyp für **V0.1 – Meilenstein 1**. Standardmodus: **Musikalisch ausgewogen**. Technisch getestet; keine musikalische oder vollständige V0.1-Freigabe.

## Start

Repository herunterladen oder klonen, im Projektverzeichnis ausführen:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Dann http://localhost:8000 öffnen. Unter Windows ggf. `py -m http.server 8000 --bind 127.0.0.1`. Module benötigen HTTP; `index.html` nicht per Doppelklick als `file://` öffnen. Keine Installation von Produktabhängigkeiten und kein Build erforderlich.

## Benutzung

1. WAV/MP3 und/oder MIDI importieren. Ohne eigene Datei funktioniert das ausdrücklich synthetische MIDI-Beispiel. Originale bleiben erhalten.
2. Bei Audio+MIDI Audio-Versatz manuell einstellen. Positive Werte überspringen den entsprechenden Anfang des Audios. Tempodrift erfordert später ein anderes Alignmentverfahren.
3. Passage per Sekundenfeldern oder Ziehen auf der Pianorolle markieren. A (Audio), B (Ausgangs-MIDI), C (Bearbeitung) starten dieselbe Passage; Mix spielt Audio und Bearbeitung mit gemeinsamer Uhr.
4. Note wählen, Tonhöhe/Velocity ändern und begründen. Zeiten bleiben ohne ausdrückliche Timingfreigabe unverändert. Änderungen sind nur an vollständig im Abschnitt liegenden Noten möglich. Rückgängig/Wiederherstellen ist jederzeit möglich.
5. B/C anhören und musikalisch beurteilen. Der eingebaute Synthesizer ist kein Klaviersample; weitere Controller und Instrumentenprogramme sind im Export erhalten, im Vergleichsklang vereinfacht.
6. MIDI und Diagnose exportieren. **Projekt vor dem Schließen speichern**: die JSON-Projektdatei enthält Quellen, Audio-Versatz, Abschnitt, Änderungen und Undo/Redo-Verlauf. Sie kann über „Projekt öffnen“ wieder geladen werden. Originaldateien sind separat herunterladbar.

Audio-only ist ein eigenständiger Eingang mit Wiedergabe und Abschnittsauswahl. Die polyphone Transkription gehört zu Meilenstein 2 und ist hier ausdrücklich noch nicht verfügbar. Es gibt keine KI-Aufrufe und keine automatischen musikalischen Reparaturen.

## Prüfungen

```sh
npm test
```

Browserregression (zusätzliche Testwerkzeuge, keine Produktabhängigkeiten):

```sh
npm install --no-save --package-lock=false playwright@1.62.1
npx playwright install chromium
node tests/browser.cjs
python3 -m pip install mido==1.3.3
python3 tests/independent_midi.py
```

Der Browsertest benötigt außerdem `ffmpeg` im PATH, erzeugt nur synthetische Testdaten und schreibt Ergebnisse standardmäßig nach `/tmp/ags-browser-results` (mit `TEST_OUTPUT_DIR` änderbar). Unter Windows `TEST_OUTPUT_DIR` auf ein beschreibbares Verzeichnis setzen. Optional eigenen Browser mit `CHROMIUM_EXECUTABLE` und installiertes Playwright mit `PLAYWRIGHT_MODULE` angeben. In dieser Sitzung wurde Chromium 138 benutzt; Testergebnisse nennen die tatsächlich geprüfte Version.

Siehe [TEST_RESULTS.md](TEST_RESULTS.md), [ARCHITECTURE.md](ARCHITECTURE.md), [PROJECT_STATE.md](PROJECT_STATE.md) und [PFLICHTENHEFT_V0.1.md](PFLICHTENHEFT_V0.1.md). Referenzfall „Graziler Tanz“, menschlicher Hörtest und native Tabletprüfung stehen aus.
