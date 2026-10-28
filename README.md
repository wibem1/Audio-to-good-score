# Audio to Good Score

**Neue Bedienung:** [Vier Schritte zur Bearbeitung](BEDIENUNG.md). Eigene Aufnahme öffnen, Passage anhören, Vorschläge gemeinsam prüfen und Ergebnis speichern. Einzelnotenbearbeitung ist optional.

**Meilenstein 1 zur Nutzung freigegeben (technisch geprüfte Vorabversion).** [Freigabehinweise](RELEASE_M1.md). Umfang, aktuelle Tests und Benutzung: [MILESTONE_1.md](MILESTONE_1.md).

Lokale Web-App für **V0.1 – technischer Workflow aus Import, Transkription, selektiver Reparatur und Klaviernotation**. Standard: **Musikalisch ausgewogen**. Keine musikalische oder vollständige V0.1-Freigabe.

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

Originale sind separat herunterladbar. B/C vergleichen, rückgängig machen/wiederherstellen, MIDI und Diagnose exportieren. **Vor dem Schließen Projekt speichern**; keine automatische dauerhafte Speicherung. Projekte aus Meilenstein 1 (Schema 1) lassen sich weiterhin öffnen, neue Projekte benutzen Schema 5 (ältere Versionen sollen Ergänzungen/Notationsparameter nicht stillschweigend verlieren). Der Vergleichssynthesizer ist kein gesampeltes Klavier; Programme, Pitchbend und weitere Controller sind im Export erhalten, im Klang vereinfacht.

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

## Reparatur und Klaviernotation

Für fehlende Töne gewünschte Tonhöhe/Velocity und Start-/Endticks in der Einzelnotenmaske eingeben, die Passage passend wählen, begründen und „Als neue Note ergänzen“ benutzen. Auch Ergänzungen sind mit Undo/Redo reversibel und werden in Schema 4 gespeichert. Bei „Markierte Passage im Kontext analysieren“ entstehen unsichere Hypothesen. „Note prüfen“ wählt die betroffene Note; erst eine eigene Prüfbegründung und die einzelne Übernahme verändern die Bearbeitung. Keine vollwertige musikalische KI-Entscheidung – siehe `ACCEPTANCE.md`.

Unter „Klaviernotation / MusicXML“ Taktart und Handteilungsgrenze kontrollieren. Für Audio-only musikalisches BPM selbst wählen und Zeitbasis „Audiosekunden“ benutzen; die im MIDI hinterlegten 120 BPM sind kein erkannter Puls. Importierte metrische MIDI kann mit „MIDI-Metrik“ notiert werden. Das separate Score-Modell rundet auf Sechzehntel; expressive MIDI-Zeiten bleiben unverändert. Export ist eine **Prüffassung**, keine zugesicherte spielbare Endpartitur. Triolen, freie Rhythmik, Handteilung und Phrasierung müssen gegebenenfalls im Notationsprogramm nachgearbeitet werden.

Zusätzliche unabhängige Notationsprüfung:

```sh
node tests/generate-score.js
python3 -m pip install music21==9.9.1 verovio==5.7.0
python3 tests/independent_score.py
```

Diese Werkzeuge sind nur Testabhängigkeiten. Quellen: MusicXML-4.0-Referenz https://www.w3.org/2021/06/musicxml40/ und Verovio-Importreferenz https://book.verovio.org/toolkit-reference/input-formats.html. Reale Dorico-/MuseScore-Abnahme und menschlicher Hörvergleich bleiben erforderlich. Der verbindliche Gesamtstatus steht in `ACCEPTANCE.md`.

Die zusätzliche Schaltfläche „Markierte Passage lokal mit Audio gegenprüfen“ benötigt Audio und vorhandene MIDI. Sie verwendet das echte lokale Basic-Pitch-Modell und erzeugt nur eng begrenzte, unsichere Oktavvorschläge. Original und MIDI bleiben zunächst unverändert. Jeder Vorschlag braucht eine eigene Hör-/Prüfbegründung und einzelne Übernahme; keine Löschung aufgrund bloß vom Modell fehlender Noten. Zusatztest: `python3 tests/independent_countercheck.py` nach dem Browserlauf.

## MuseScore-Importprüfung

Mit tatsächlich installiertem MuseScore (hier geprüft: **3.2.3**, nicht MuseScore 4):

```sh
node tests/musescore-fixtures.js
MUSESCORE_EXECUTABLE=/pfad/zu/musescore3 python3 tests/musescore_import.py
```

Unter Windows die Umgebungsvariable entsprechend der Shell setzen. Der Test erzeugt sechs synthetische Notationsfälle und prüft echten Import, natives Speichern/Öffnen, Rückexport und PNG-Rendering. Er benötigt nur Python-Standardbibliothek plus Node für die vorhandenen Projektmodule. Ausgaben standardmäßig `/tmp/ags-musescore-results`, durch `TEST_OUTPUT_DIR` änderbar. Keine MuseScore-Installation für die Benutzung der Web-App nötig. Dorico-Abnahme und menschliche musikalische Freigabe fehlen weiterhin.

### MuseScore 4 prüfen

Derselbe Importtest unterstützt echte MuseScore-3- und MuseScore-4-Installationen. MuseScore 4.7.6 wurde mit sechs Fällen geprüft; Belege unter `test-results/musescore4/`. Bei einer laufenden X11-Anzeige beispielsweise:

```sh
TEST_OUTPUT_DIR=/tmp/ags-musescore4-results node tests/musescore-fixtures.js
QT_QPA_PLATFORM=xcb TEST_OUTPUT_DIR=/tmp/ags-musescore4-results MUSESCORE_EXECUTABLE=/path/to/MuseScore/AppRun python3 tests/musescore_import.py
```

`DISPLAY` muss auf die vorhandene Anzeige zeigen; in einer Headless-Umgebung wird ein separat bereitgestelltes Xvfb benötigt. Die getestete AppImage benötigt hier auch dann eine Anzeige, wenn Qt auf offscreen gesetzt wird. MuseScore ist ausschließlich ein externes Testwerkzeug.

## Notationspuls und lesbare Anschlagsfassung

Ein Speichertempo (z.B. 120 BPM eines Audio-Kandidaten) ist kein erkannter musikalischer Puls. Im optionalen Notationsbereich „Lesbare Notation vorbereiten“ wählen: Die App schlägt aus den MIDI-Einsätzen eine Unterteilung, Tempoalternativen und den Taktanfang vor. Taktart bleibt unverändert und muss musikalisch geprüft werden. Bei Zeitbasis Audiosekunden ist die ausdrückliche Bestätigung von Tempo/Taktart/Taktanfang vor dem Export erforderlich.

„Lesbare Anschlagsfassung“ gruppiert gleiche notierte Einsätze als Akkorde und verkürzt/verlängert deren Notationsdauern bis zum nächsten Anschlag derselben Hand. Das verhindert, dass bloßes Ausklingen zahlreiche Zusatzstimmen erzeugt. **Bewusste Vereinfachung, keine vollständige Stimmen- oder Tastendauerrekonstruktion.** „Erkannte Dauern beibehalten“ bleibt als Alternative erhalten. Punktierte Werte und explizite Tempoangaben werden als MusicXML exportiert. Die Performance-MIDI bleibt unverändert.

Realer Referenztest und Grenzen: `test-results/reference-score/`. Externe Referenzdateien werden nicht mit dem Repository veröffentlicht. Reproduktion mit eigenen Dateien:

```sh
node tests/generate-reference-score.js /path/to/source.mid /tmp/reference-score 3
python3 tests/check_reference_score.py /path/to/source.mid /tmp/reference-score/mapping.json /tmp/reference-score/reference.musicxml
python3 scripts/reference-diagnosis.py /path/to/audio.wav /path/to/source.mid /tmp/reference-diagnosis.json
```

Die `3` ist eine ausdrücklich gewählte Taktannahme, keine erkannte Taktart. Referenzdiagnose braucht nur als Testwerkzeuge mido, NumPy und SciPy, der Parservergleich music21. Keine neuen Produktabhängigkeiten. Audio-Onset-Abstände sind kein Beweis für Tonhöhenfehler.
