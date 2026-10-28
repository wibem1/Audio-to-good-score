# Projektstand – Audio to Good Score

**Stand:** 28.10.2026  
**Phase:** M1 technisch geprüft; M2 als lokaler polyphoner Audio-only-Kandidatenweg implementiert und mit echtem Modell technisch geprüft. **Musikalische Abnahme offen.**  
**Zielversion:** V0.1 insgesamt nicht freigegeben.  
**Repository:** `wibem1/Audio-to-Good-Score`, `main`. Code, Modellassets, Testnachweise und Übergabe liegen gemeinsam im Commit dieses Dokuments. Letzter M1-Stand bleibt als Commit `6458b6db070652821d2ead96a947b64ebbffe0be` erhalten.

## Verbindliche Leitplanken

Audio allein, Audio+MIDI und MIDI allein sind gleichrangige Eingänge. Standard **Musikalisch ausgewogen**. Originale nicht überschreiben; Korrekturen einzeln begründen, sichtbar machen, vergleichen und rückgängig machen. Performance und spätere Score-Zeiten getrennt. Keine pauschale Quantisierung. Keine kostenpflichtigen KI-Aufrufe ohne Zustimmung. Technische Tests ersetzen keine musikalische Hörfreigabe.

## Aktuell nachgewiesen

| Bereich | Nachweis / Grenzen |
|---|---|
| M1 Import, Pianorolle, Passage, manuelles Alignment | Echte Chromium-Regression für WAV/MP3/SMF 0/1, Mausmarkierung, gemeinsame Web-Audio-Uhr; keine automatische Tempoausrichtung |
| Einzelnoten, Undo/Redo, MIDI-Export | Abschnitts-/Timingfreigabe-/Überlappungsschutz und Export-Roundtrip; ursprüngliche Tempokarte/Ereignisse erhalten; unabhängige mido-Prüfung |
| Audio-only → MIDI-Kandidat | Basic Pitch 1.0.1 / ICASSP 2022 mit TensorFlow-WASM direkt im Browser. Kein vorheriges MIDI, kein Backend, keine Cloud. WAV/MP3 einschließlich Stereo-Resampling mit echtem Modell geprüft |
| Kandidatensicherheit | Separates Ergebnis, Übernehmen/Verwerfen; vorhandene MIDI blockiert Neu-Transkription; Abbruch terminiert Worker, Quellenwechsel invalidiert Ergebnisse, Modellhashes vor Ausführung geprüft |
| Vergleich und Korrektur | A Originalaudio, B unbearbeiteter Kandidat, C manuell bearbeiteter Kandidat; reale Audioknoten gestartet, Zeiten nach Korrektur unverändert; kein behaupteter menschlicher Hörtest |
| Projekt/Diagnose | Schema 2 mit Audio, unbearbeitetem Kandidaten, Modell-/Quellhashes, Parametern, Laufprotokollen und Undo/Redo; Schema 1 weiterhin im Browser lesbar. Manuell speichern |
| Fehlerfälle/Ressourcen | Fehlende/korrupte Modelle, Abbruch und Stille getestet; tatsächlich 60-s-Eingabe verarbeitet; keine erfundenen Noten aus Stille; kein externer Request im Modellbrowsertest |

**Prüfstand:** 23/23 Kerntests bestanden, M1- und M2-Browserregression in Chromium 138.0.7204.0 bestanden, unabhängige mido-Exportprüfungen bestanden. `npm ci`/Build reproduziert. `TEST_RESULTS.md`, Maschinenberichte/Screenshots unter `test-results/` und Quellfingerabdrücke dokumentieren den Stand.

## Modellqualität – ausdrücklich begrenzt

Der synthetische Test mit 8 Referenznoten ergibt 9 Modellnoten, davon 7 zu passenden Referenznoten zugeordnet. Oktavfehler sind vorhanden. Das ist ein technischer Funktionsnachweis und **keine Freigabe für reale Klaviermusik**. Keine Schwellenanpassung oder stille musikalische Nachkorrektur. Basic Pitch erkennt kein Pedal; 120 BPM im Kandidaten ist nur Transport für Sekundenzeiten, kein erkanntes musikalisches Tempo. Velocity ist Modellaktivierung, keine gemessene Anschlagsdynamik. Weitere Grenzen und Lizenz-/Modellvergleich: `TRANSCRIPTION_DECISION.md`.

## Start / Code

`python3 -m http.server 8000 --bind 127.0.0.1`, dann `http://localhost:8000`. Modell und Worker sind mitgeliefert; zum Benutzen kein npm-/KI-Dienst erforderlich. Entwicklung: `npm ci`, `npm run build`, `npm test`. Einstieg `index.html`, MIDI `midi.js`, Änderungen `model.js`, Wiedergabe `player.js`, Transkription `transcription.js`/`transcription-worker.js`/`model-spec.js`, reproduzierbare Assets `scripts/build-transcription.js` → `vendor/`.

## Offen

- Menschliche A/B/C-Hörprüfung einer echten Klavieraufnahme sowie Referenz „Graziler Tanz“ fehlen mangels bereitgestellter Testdaten. A11 ist technisch vorbereitet, musikalisch nicht abgenommen.
- Native Tablet-/Safari-/Firefox-Tests, Hintergrundtab-/Langaufnahme-/Spitzen-RAM-Prüfung fehlen. Transkriptionspassage auf 0,1–60 s begrenzt; fünf Minuten Laufzeitlimit.
- M3: musikalische Fehlerdiagnose und selektive KI-Reparatur fehlen. Aktuelle Diagnose ist heuristisch, keine Harmonie-/Stimmenanalyse.
- M4: Score-Modell, MusicXML und reale Dorico-/MuseScore-Prüfung fehlen.
- Vergleichssynthesizer bleibt vereinfacht; zusätzliche Controller/Programme bleiben im MIDI erhalten, werden nicht vollständig gerendert. Kein automatisches oder Mehrpunkt-Audioalignment.

## Nächster einzelner Schritt

Den neuen Audio-only-Kandidaten mit einer rechtmäßig verfügbaren echten Klavierpassage im menschlichen A/B/C-Hörvergleich prüfen und Fehler dokumentieren. Die nachgewiesenen Oktav-/Auslassungsfehler als Ausgangspunkt für M3 verwenden; keine pauschale Korrektur oder musikalische Freigabe aus den synthetischen Kennzahlen ableiten. „Graziler Tanz“ nur nach tatsächlicher Bereitstellung verwenden.

## Übergabe

Globale Standards, `AGENTS.md`, diese Datei, `TODO.md`, Pflichtenheft, Architektur-/Transkriptionsentscheidung, Testergebnisse und Code lesen. GitHub ist maßgeblich. Mit `npm test` beginnen. Lokale Modellversuche sind protokolliert, externe/zahlbare KI-Aufrufe: null.
