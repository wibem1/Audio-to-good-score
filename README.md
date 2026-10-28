# Audio to Good Score

Lokale Web-App für **V0.1 – Meilenstein 1 und technischer Transkriptionsweg aus Meilenstein 2**. Standard: **Musikalisch ausgewogen**. Keine musikalische oder vollständige V0.1-Freigabe.

## Start

Repository herunterladen oder klonen, im Projektverzeichnis starten:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

http://localhost:8000 öffnen. Unter Windows ggf. `py -m http.server 8000 --bind 127.0.0.1`. Kein npm-/Python-Musikpaket für die Benutzung nötig: Modell, Worker, WebAssembly und Lizenztexte sind unter `vendor/` mitgeliefert. HTTP auf localhost oder HTTPS benutzen, kein `file://`. Es gibt keinen Audio-Upload, keinen Cloud-KI-Dienst und keine API-Schlüssel.

## Audio allein transkribieren

1. WAV oder MP3 laden, **keine MIDI erforderlich**. Unten eine Passage von 0,1 bis höchstens 60 Sekunden wählen.
2. „Markiertes Audio transkribieren“ starten. Basic Pitch arbeitet lokal im Hintergrund; Abbrechen beendet den Worker. Modelldateien werden vor Nutzung gegen festgelegte SHA-256-Werte geprüft.
3. Den Kandidaten ausdrücklich übernehmen oder verwerfen. Erst die Übernahme erzeugt die bearbeitbare MIDI-Vergleichsversion. Ein leerer Kandidat lässt sich nicht übernehmen. Bestehende MIDI wird nicht durch eine neue Transkription überschrieben.
4. A: Originalaudio, B: unbearbeiteter Kandidat, C: Bearbeitung. Dieselbe Passage vergleichen, einzelne Noten auswählen, Korrektur begründen und bei Bedarf rückgängig machen.
5. MIDI exportieren; zusätzlich das Projekt und die Diagnose sichern. Die Projektdatei enthält Originalaudio, unbearbeiteten Kandidaten, Modell-/Quellprüfsummen, Parameter, lokale Laufprotokolle und Undo/Redo.

**Wichtig:** Basic Pitch ist instrumentenübergreifend und kein abgenommenes Klaviermodell. Zusätzliche, fehlende und oktavversetzte Töne sind möglich; kurze Ornamente können fehlen. Pedal wird nicht rekonstruiert. Velocity beruht auf Modellaktivierung und ist kein gemessener Anschlagswert; Modellaktivierungen sind keine kalibrierten Vertrauenswahrscheinlichkeiten. Das Modell erkennt keine musikalische Tempokurve. 120 BPM im Kandidaten dient allein zur Speicherung der aus Audio abgeleiteten Sekundenzeiten mit 0,5-ms-Auflösung, nicht als erkannter Puls oder Score-Quantisierung. Das Originalaudio bleibt maßgeblich.

Der synthetische Test zeigt diese Grenzen ausdrücklich: 7 von 8 erwarteten Noten passend erkannt, 9 vorgeschlagen; Oktavfehler vorhanden. Das ist **kein Qualitätswert für reale Klaviermusik**. „Graziler Tanz“ und menschliche Hörfreigabe fehlen.

## Vorhandene MIDI bearbeiten

WAV/MP3 und/oder SMF 0/1 importieren, bei Audio+MIDI den konstanten Audio-Versatz einstellen. Positive Werte überspringen den entsprechenden Audioanfang; Tempodrift erfordert ein späteres Mehrpunkt-Alignment. Passage per Feldern oder Ziehen auf der Pianorolle markieren. Note anklicken oder in der Liste wählen, Tonhöhe/Velocity ändern und begründen. Start-/Endticks erfordern eine ausdrückliche Freigabe. Nur vollständig in der Passage liegende Noten werden bearbeitet; es gibt keine pauschale Quantisierung.

Originale sind separat herunterladbar. B/C vergleichen, rückgängig machen/wiederherstellen, MIDI und Diagnose exportieren. **Vor dem Schließen Projekt speichern**; keine automatische dauerhafte Speicherung. Projekte aus Meilenstein 1 (Schema 1) lassen sich weiterhin öffnen, neue Projekte benutzen Schema 3 (ältere Versionen sollen Ausblendungen nicht stillschweigend verlieren). Der Vergleichssynthesizer ist kein gesampeltes Klavier; Programme, Pitchbend und weitere Controller sind im Export erhalten, im Klang vereinfacht.

## Entwicklung und Prüfungen

Produkt benutzen: kein Build erforderlich. Mitgelieferte Transkriptionsdateien reproduzierbar neu erzeugen:

```sh
npm ci
npm run build
npm test
```

`package-lock.json` fixiert die Abhängigkeiten. Der Build verwendet die offiziellen npm-Modellbytes und verweigert abweichende Modellprüfsummen. Lizenztexte werden mitgeliefert. Audit: keine gemeldeten Schwachstellen zum dokumentierten Prüfzeitpunkt; keine allgemeine Sicherheitsgarantie.

Browsertests brauchen zusätzlich Playwright/Chromium und `ffmpeg` im PATH:

```sh
npm install --no-save --package-lock=false playwright@1.62.1
npx playwright install chromium
node tests/browser.cjs
node tests/transcription-browser.cjs
python3 -m pip install mido==1.3.3
python3 tests/independent_midi.py
python3 tests/independent_transcription.py
```

Testdaten sind synthetisch und werden automatisch erzeugt. Standardausgaben: `/tmp/ags-browser-results` und `/tmp/ags-transcription-results`. Mit `TEST_OUTPUT_DIR` änderbar; unter Windows einen beschreibbaren Pfad wählen und für die zusammengehörenden Browser-/Python-Tests denselben Pfad benutzen. Optional vorhandenen Browser mit `CHROMIUM_EXECUTABLE` und Playwright mit `PLAYWRIGHT_MODULE` wählen. Tatsächlich getestet wurde Chromium 138.0.7204.0; keine native Tablet-/Safari-Freigabe.

Siehe [PROJECT_STATE.md](PROJECT_STATE.md), [TEST_RESULTS.md](TEST_RESULTS.md), [ARCHITECTURE.md](ARCHITECTURE.md), [TRANSCRIPTION_DECISION.md](TRANSCRIPTION_DECISION.md) und [PFLICHTENHEFT_V0.1.md](PFLICHTENHEFT_V0.1.md).

Einzelnoten ausblenden: Note wählen, „Note aus Bearbeitung ausblenden“ ankreuzen, begründen und übernehmen. B und Originaldatei bleiben vollständig; C und MIDI-Export lassen nur diese Note weg. Ausgeblendete Noten bleiben blass sichtbar und lassen sich per Undo/Redo oder durch Aufheben des Häkchens wieder aufnehmen. Projekt Schema 3 speichert diesen Zustand, Schema 1/2 bleibt lesbar. Zusätzlicher Test: `python3 tests/independent_mute.py` nach dem M1-Browsertest.
