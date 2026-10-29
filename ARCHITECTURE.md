# Architekturentscheidung – Meilenstein 1

Stand: 28.10.2026. Die folgenden Abschnitte dokumentieren die ursprüngliche M1-Entscheidung. **Aktueller M2-Zusatz:** Lokale Browsertranskription mit mitgeliefertem Basic Pitch/TensorFlow-WASM; siehe `TRANSCRIPTION_DECISION.md`. M1 bleibt nutzbar, Gesamtversion 0.1 ist nicht freigegeben.

## Entscheidung

Eine statisch auslieferbare Anwendung mit nativen JavaScript-ES-Modulen, SVG und Web Audio API. Kein Buildschritt, kein Serverdienst außer statischer Auslieferung, keine Laufzeitbibliotheken, CDN-Abhängigkeiten, Telemetrie oder KI-Aufrufe. Das hält den ersten Meilenstein reproduzierbar und erlaubt lokale Verarbeitung privater Musikdateien. React/TypeScript und FastAPI sind Optionen, keine Pflicht aus dem Pflichtenheft; sie werden erst bei tatsächlichem Bedarf eingeführt. Keine als fertig dargestellte Transkriptionsattrappe.

- `midi.js`: begrenzter SMF-0/1-Reader und Writer, unveränderte Ereignisdaten und PPQ-Tempokarte. Running Status wird gelesen, bei Bearbeitungen expliziter Status geschrieben. Ohne Änderungen wird die Originaldatei byteidentisch zurückgegeben. SMPTE, Typ 2 und defekte Dateien werden ausdrücklich abgelehnt.
- `model.js`: Performance-Noten in Originalticks, atomare Änderungsoperationen und Undo/Redo. Kein Score-Modell und keine Quantisierung. Bearbeitung verlangt Begründung; Timing separat freigeben. Vollständige Note muss innerhalb des Abschnitts liegen. Neue überlappende gleiche Töne werden abgelehnt. Vor Übernahme wird der Export erneut eingelesen und gegen alle erwarteten Noten geprüft.
- `player.js`: Audio und MIDI verwenden denselben `AudioContext`-Zeitanker. Lookahead-Scheduling verhindert Timer-Jitter als Notenzeitgeber. Audio-Versatz ist manuell und konstant; kein automatisches oder elastisches Alignment. CC64 wird beim Rendern berücksichtigt, einschließlich Reihenfolge von Pedal und Note-off am selben Tick. Einfacher Dreiecksynthesizer zum technischen Vergleichen; kein realistisches Klavier. Weitere Controller/Programme bleiben im SMF erhalten, werden nicht klanggetreu interpretiert.
- `app.js`: Originalquellen, Passage in Sekunden, SVG-Pianorolle, lokale Downloads und Projektdatei mit eingebetteten Originalbytes und Änderungsverlauf. Keine implizite dauerhafte Speicherung: vor dem Schließen Projekt speichern. SHA-256 der Quellen im Diagnoseexport. Diagnose markiert nur heuristische Verdachtsfälle; sie komponiert und korrigiert nichts automatisch.

Audio-Versatz: `Audiozeit = MIDI-/Projektzeit + Versatz`. Beide Player beginnen mit demselben Vorlauf von 60 ms; negative Audiozeiten erzeugen Stille bis zum Audioanfang. Wechsel A/B/C während der Wiedergabe startet die neue Quelle an der aktuellen Passageposition; die Starttaste beginnt stets am Abschnittsanfang. Beim Suchen in eine gehaltene MIDI-Note wird deren Restdauer neu angeschlagen; klanglicher Verlauf ist daher nicht identisch mit kontinuierlicher Wiedergabe. Browser-Hintergrundtabs können Scheduler ausbremsen; Hörvergleiche im Vordergrund durchführen.

## Audio-only als gleichrangiger Eingang

`inputPath` unterscheidet Audio allein, Audio+MIDI und MIDI allein. Audio allein kann schon importiert, abgespielt, markiert und mit Original im Projekt gespeichert werden. Im ursprünglichen M1-Stand war noch kein Provider installiert. Der aktuelle Stand verwendet `LocalTranscriber` und einen abbrechbaren Basic-Pitch-Worker, siehe `TRANSCRIPTION_DECISION.md`. Für M2 liefert ein Provider einen SMF-Kandidaten samt Modellversion, Konfiguration, Unsicherheit und Kostenprotokoll; dieser wird durch denselben Import, dieselbe Änderungsverwaltung und denselben Hörvergleich geführt. MIDI ist keine Voraussetzung für den Audioeingang.

Ein späterer Transkriptionsprozess gehört in einen Worker oder lokalen Backendprozess; Audio-Dekodierung/Modelle dürfen die UI nicht blockieren. Kein kostenpflichtiger Provider ohne ausdrückliche Genehmigung. Auswahl und Gewichte müssen vor Integration neu auf Lizenz, Hardwarebedarf und polyphone Klaviereignung geprüft werden. Im historischen M1-Stand waren Basic Pitch, spezialisierte Klaviermodelle und ein möglicher Python-Stack weder installiert noch bestätigt. Der aktuelle M2-Stand bestätigt nur den technisch geprüften Basic-Pitch-Browserweg; kein musikalischer Eignungsnachweis. Score-Modell und MusicXML bleiben von der Performance getrennt.

## Abhängigkeiten und Lizenzen

| Bestandteil | Verwendung | Entscheidung / Lizenz |
|---|---|---|
| Web Audio, SVG, File API, Web Crypto | Browserlaufzeit | Native APIs, kein zusätzlich gebündelter Bibliothekscode |
| Node.js 24.22.1 | Tests | Nur Entwicklungswerkzeug; Node-Lizenz/MIT und Drittkomponenten, nicht mitgeliefert |
| Python 3 | Lokaler statischer Server | Standardbibliothek; PSF, nicht mitgeliefert |
| Playwright 1.62.1 | Browserautomation | Apache-2.0, nur Testwerkzeug |
| Chromium 138.0.7204.0 | Tatsächlicher Browsertest | Chromium BSD und Drittkomponenten; nicht Teil der Anwendung |
| @sparticuz/chromium 138.0.2 | Bereitstellung des Testbrowsers in dieser Umgebung | MIT für Paket, Chromium-Lizenzen für Binärdateien; nicht Teil der Anwendung |
| mido 1.3.3 | Unabhängiges Lesen des Exports | MIT, nur Testwerkzeug |
| FFmpeg | Synthetische MP3-Testdatei aus WAV | Buildabhängig LGPL/GPL; nur vorhandenes Testwerkzeug, nicht weitergegeben |

Projektcode enthält keinen kopierten Parser-/Synthesizer-Bibliothekscode. Keine neue Lizenz für das Gesamtprojekt festgelegt. Für M1 ist keine Python-Musikbibliothek im Produkt erforderlich. Der eigene SMF-Kern braucht wegen des kleineren, expliziten Formatumfangs gezielte Regressionstests statt einer behaupteten universellen MIDI-Unterstützung.

Primärquellen (28.10.2026 geprüft):
- https://midi.org/standard-midi-files – SMF-Ereignisse/Spuren/Tempo.
- https://developer.mozilla.org/de/docs/Web/API/AudioBufferSourceNode/start – Scheduling mit AudioContext-Zeit und Audio-Offset.
- https://github.com/microsoft/playwright/blob/main/LICENSE – Testwerkzeug-Lizenz.
- https://github.com/mido/mido/blob/1.3.3/LICENSE – unabhängiger Testparser.
- https://github.com/Sparticuz/chromium/blob/v138.0.2/LICENSE – Testbrowserpaket.

## Grenzen

Maximal 50 MiB komprimiertes Audio, 10 MiB MIDI, 100.000 MIDI-Ereignisse und 10.000 vollständige Noten. Dekodiertes Audio benötigt wesentlich mehr RAM; kein Langaufnahme-/Stresstest. Keine Mehrinstrumenten-Klangtreue, kein automatisches Timing-Repair, kein automatisches Audioalignment. Wiederholte gleichzeitige Noten derselben Höhe werden beim Import als FIFO-Unsicherheit gekennzeichnet; unsichere Änderungen können am Roundtrip-Schutz scheitern. Diagnose ist keine Stimmen-/Harmonieanalyse. Native Tablet-/Safari-/Firefox-Tests und menschliche Hörfreigabe fehlen. Keine Serverbereitstellung oder als V0.1 freigegebene Veröffentlichung.

## Optionaler MusicCraft-Kern 0.3 (29.10.2026)

Isolierter Python-Kern `musiccraft/`, noch ohne Browser-/Provideranbindung. jsonschema 4.26.0 prüft Verträge, music21 9.9.1 übernimmt Notation und mido 1.3.3 SMF. Gemeinsamer Plan, kontrollierte Performance-Abweichungen, unabhängige ElementTree-Zeitachsenprüfung und Bibliotheks-Roundtrips. Optionale Abhängigkeiten: `requirements-composition.txt`. Kein kopierter Forschungsmodell-/Tokenizer-Code oder Gewichte. Umfang, Lizenzen und Grenzen: `protocol/IMPLEMENTATION_0.3.md`.

