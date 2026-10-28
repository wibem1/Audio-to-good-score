# Transkriptionsentscheidung – technischer Meilenstein 2

28.10.2026. Geltungsbereich: lokaler Audio-only-Kandidat; keine musikalische Klavierfreigabe.

## Auswahl und Alternativen

| Option | Lizenz / technische Grundlage | Ergebnis der Prüfung |
|---|---|---|
| Spotify Basic Pitch TypeScript 1.0.1, ICASSP-2022-Modell | Apache-2.0, offizielle npm-Verteilung einschließlich Modell | Integriert und im echten Browser mit WebAssembly ausgeführt. Polyphon, instrumentenübergreifend, keine Pedalerkennung. Kleiner lokaler Browserweg ohne Backend/API. |
| Basic Pitch Python 0.4.0 / ONNX | Apache-2.0; offizielle Python-Inferenz bietet mehrere Runtimes | Quellprüfung und Paketinspektion, keine Installation als Produktbackend. Würde Python-Musikpakete und einen lokalen Dienst benötigen. Kein Vorteil für den ersten statischen Browserweg. |
| Piano Transcription / piano_transcription_inference | Apache-2.0 im Trainingsrepository; separates PyTorch-Modell/Checkpoint | Primärdokumentation geprüft, nicht integriert oder als Modell getestet. Klavierspezifisch mit Pedalen; ältere dokumentierte Python/PyTorch-Umgebung, separate Checkpoint-/Plattformprüfung erforderlich. Kein behaupteter Qualitätsvergleich. |

Der Browserweg ist eine bewusst austauschbare **Baseline**. Er ersetzt die spätere Prüfung eines klavierspezifischen Modells nicht. Es wurde kein kostenpflichtiger Dienst aufgerufen, kein Training gestartet und keine Nutzerdatei an Dritte gesendet.

## Festgelegte Komponenten

`@spotify/basic-pitch` 1.0.1, `@tensorflow/tfjs` 3.21.0 und `@tensorflow/tfjs-backend-wasm` 3.21.0: Apache-2.0. `esbuild` 0.25.11: MIT, nur Buildwerkzeug. Transitive Pakete im mitgelieferten Lizenzindex: Apache-2.0, MIT, BSD-2-Clause, BSD-3-Clause und ISC. Vollständige Lizenztexte und Copyright-Hinweise unter `vendor/licenses/`, Bundlerhinweise in `vendor/transcription-worker.js.LEGAL.txt`. Keine neue Lizenz für das Gesamtprojekt festgelegt. Originaldateien der Pakete und Modellgewichte nicht verändert; der eigene Adapter steht in `transcription-worker.js`.

| Modelldatei | Bytes | SHA-256 |
|---|---:|---|
| `model.json` | 174537 | `1ed1aaee3409ec1dc098c8b01f430c0911f6fe9412e7af8086750f9e8f302f68` |
| `group1-shard1of1.bin` | 742392 | `b142a95737a52e1e412d5f92e73d8bb80dfe8d04941acc0702f11f4524fb377c` |

Build und Worker prüfen diese Werte gegen `model-spec.js`; der Worker lädt nur lokale, geprüfte Modellbytes über einen In-Memory-GraphModel-Loader. Gesamte ausgelieferte `vendor/`-Dateien beim Test rund 2,93 MB. `npm ci` plus Build erfolgreich reproduziert, npm Audit ohne gemeldete Schwachstellen. Audit ist eine Momentaufnahme.

## Laufzeit und Nachvollziehbarkeit

- Nur Audio wird benötigt. Ausgewählte Passage: 0,1–60 s, als Mono auf 22050 Hz per OfflineAudioContext resampelt. Mitteln der Kanäle; die Quelldatei wird nie geändert.
- Ein dedizierter Worker pro Versuch. Kein GPU-/Cloud-Backend, kein automatischer kostenpflichtiger Fallback. WebAssembly ohne Thread-/COOP-Pflicht, SIMD falls unterstützt. Abbruch und Fünf-Minuten-Zeitlimit terminieren den Worker; so werden auch Modell-/Tensorressourcen nach jedem Versuch freigegeben.
- TFJS 3.21 `signal.frame` ruft beim Auffüllen `Fill` ohne dtype auf; der WASM-Kernel scheitert dann mit „Unknown dtype undefined“. Nach Ursachenprüfung ergänzt der Adapter für diesen Kernel ausschließlich den fehlenden float32-Standard. Bibliotheksquellen bleiben unverändert. Echte Modelltests einschließlich 60-s-Eingabe prüfen diesen Pfad.
- Decoderparameter: Onset 0,5, Frame 0,3, Mindestlänge 11 Modellframes (etwa 128 ms); keine Pitchbends für den Klavierkandidaten. Kurze Ornamente sind damit gefährdet. Kein Nutzerprompt und keine musikalische Neukomposition.
- Kandidatenzeiten bleiben in Sekunden auf der Originalaudioachse; MIDI nutzt PPQ 1000 bei nominell 120 BPM = 0,5 ms/Tick. Keine Beat-/Rasterquantisierung und kein behauptet erkanntes Tempo. Beim Randbeschnitt werden Clipping-Zahlen protokolliert. Überlappende gleiche Tonhöhen werden bei der Kandidatenerzeugung auf verschiedene MIDI-Kanäle verteilt, damit Note-offs keine neuen Notenpaarungsfehler verursachen. Die zugehörigen Zeiten bleiben erhalten.
- Der Kandidat wird erst durch ausdrückliche Übernahme ins Bearbeitungsmodell gebracht. B bleibt der unbearbeitete Kandidat, C die manuelle Bearbeitung. Bestehende MIDI blockiert Neu-Transkription. Quellenwechsel invalidiert laufende/pending Ergebnisse.
- Projekt Schema 2 und Diagnose speichern Modellversion/-hashes, Audiohash, Kandidatenhash, Parameter, Abschnitt, Laufdauer, Laufstatus, Hinweise und null externe/zahlbare Aufrufe. Referenzaudiowechsel wird markiert. Prüfsummen der Herkunft werden beim Projektöffnen berücksichtigt. Schema 1 bleibt lesbar.

## Tatsächliche Ressourcenprüfung und Qualität

Chromium-138-Browser auf der Arbeitsumgebung, CPU/WASM: 4-s-Stereotest und tatsächlicher 60-s-Lauf erfolgreich. Laufzeit und Tensorbytes stehen in `test-results/transcription-browser-results.json`. Tensorbytes sind die nach dem Modelllauf gezählten Tensoren, **kein gemessener Spitzen-RAM-Verbrauch**. Keine zugesicherte Tabletgeschwindigkeit.

Im synthetischen polyphonen 8-Noten-Test: 7 passend erkannte Referenznoten, insgesamt 9 Modellnoten, darunter zusätzliche/ersetzte Oktavtöne. Präzision/Recall gelten nur für diese konkrete Datei und den dokumentierten Matchingtest. Sie sind keine kalibrierten Musikqualitätswerte. Keine Schwellenanpassung an diese Testdatei, kein stilles Entfernen vermeintlicher Obertöne. Der Fehler bleibt sichtbar und muss musikalisch beurteilt werden. „Graziler Tanz“, echte Klavierhörprüfung und nativer Tablet-/Safari-/Firefox-Test fehlen.

## Primärquellen

- https://github.com/spotify/basic-pitch-ts – README, Inferenz-/Decoderquellen, npm-Paket und Apache-Lizenz geprüft.
- https://github.com/spotify/basic-pitch – Python-Inferenz, Runtimes und Modellumfang geprüft.
- https://github.com/bytedance/piano_transcription – Klavierspezialisierung und Apache-Lizenz, derzeit archiviertes Repository laut GitHub.
- https://github.com/qiuqiangkong/piano_transcription_inference – Umgebungs-/Checkpoint-/Plattformhinweise geprüft.
- https://www.npmjs.com/package/@spotify/basic-pitch – eingesetzte offizielle Paketversion 1.0.1, durch Lockfile-Integrität fixiert.
