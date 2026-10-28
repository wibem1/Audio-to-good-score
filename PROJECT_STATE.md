# Projektstand – Audio to Good Score

**Stand:** 28.10.2026  
**Phase:** Meilenstein 1 als technisch geprüfter Web-App-Prototyp implementiert.  
**Zielversion:** V0.1 bleibt geplant und ist **nicht als Gesamtversion freigegeben**.  
**Repository:** `wibem1/Audio-to-Good-Score`, Branch `main`. Der Commit, der diesen Stand enthält, ist der reproduzierbare M1-Stand; Tests und Quellfingerabdrücke liegen gemeinsam im Repository.

## Ziel und verbindliche Entscheidungen

Drei gleichrangige Eingänge: Audio allein, Audio+MIDI, MIDI allein. Soloklavier, Standard **Musikalisch ausgewogen**. Originale erhalten, einzelne Änderungen begründen, sichtbar machen und rückgängig machen. Performance-Ticks und Tempokurve bleiben von späterer Score-/MusicXML-Zeitdarstellung getrennt. Technische Validität ersetzt keine musikalische Prüfung. Keine kostenpflichtigen KI-Aufrufe ohne Zustimmung.

## Nachgewiesener Stand

| Funktion | Status / Prüfgrundlage |
|---|---|
| WAV/MP3 und SMF 0/1 importieren | Im Chromium-Browser mit synthetischen Dateien getestet; SMF-0/1-Kerntests |
| Audio-only als eigener Eingang | Im Browser ohne MIDI importiert und abgespielt; Transkription noch nicht implementiert (M2) |
| Manuelles Alignment, gemeinsame Zeitachse | Audio-Versatz, Navigation und Mix mit gemeinsamer Web-Audio-Uhr technisch getestet; kein automatisches oder elastisches Alignment |
| Abschnitt/Pianorolle | SVG, Notenauswahl und Abschnittsmarkierung per Maus sowie Zahlenfelder im Browser getestet |
| Nicht-destruktive Einzelnotenbearbeitung | Tonhöhe/Velocity, ausdrücklich freizugebende Start-/Endticks, Begründung, Abschnittsschutz, Überlappungsschutz und Export-Roundtrip getestet |
| Undo/Redo und Projektsicherung | Browser-Roundtrip inklusive eingebetteten Originalen und wiederherstellbarer Änderung getestet; manuelle Projektdatei speichern, keine automatische dauerhafte Speicherung |
| A/B/C und synchroner Mix | Echter Browser, gestartete Audio-/Synthesizerknoten und erzeugtes Audiosignal nachgewiesen; **kein menschlicher Hörtest** |
| MIDI-Export | Eigener Reimport plus unabhängiger mido-1.3.3-Parser; ursprüngliche Zeiten, Tempowechsel, CC64, Spuren und SysEx bei Testkorrekturen erhalten |
| Diagnose und JSON-Export | Unsichere Längen-/Klavierumfang-/Überlappungshinweise, Quell-SHA-256, Änderungen, Begründungen, Prüflücken und null KI-Aufrufe getestet |

**Tests:** 15/15 automatisierte Kerntests bestanden; Browserregression in Chromium 138.0.7204.0 ohne JavaScript-Seitenfehler; unabhängige MIDI-Prüfung bestanden. Details und Grenzen: `TEST_RESULTS.md`. Desktop- und mobile Viewport-Screenshots visuell geprüft. Dies belegt keine native Tablet-/Safari-Kompatibilität oder musikalische Qualität.

## Start und Architektur

`python3 -m http.server 8000 --bind 127.0.0.1`, dann `http://localhost:8000`. Kein Produkt-Build, keine Laufzeitpakete, kein KI-/Backenddienst. Einstieg `index.html`, Performance/Import `midi.js`, Änderungen `model.js`, Audio `player.js`, UI `app.js`. Begründung, Lizenzprüfung und Transkriptionsvertrag: `ARCHITECTURE.md`. Prüfkommandos: `README.md`.

## Grenzen / offene Prüfungen

- „Graziler Tanz“ wurde nicht bereitgestellt: kein Referenz-Abnahmetest und keine behauptete Hörfreigabe.
- Der Synthesizer ist ein technischer Vergleichsklang, kein realistisches Klavier. CC64 wird gerendert; weitere Controller, Programme und Pitchbend bleiben im Export, sind im Klang nicht vollständig umgesetzt.
- Audio-only-Transkription, KI-Analyse/-Reparatur und MusicXML fehlen planmäßig bis M2–M4. Kein Modell und keine Modellgewichte geprüft oder installiert.
- Kein automatisches Alignment; konstante Audio-Verschiebung kann Tempodrift nicht lösen.
- SMPTE und SMF Typ 2 werden abgelehnt. Dateigrößen-/Ereignisgrenzen siehe Architektur. Keine Langaufnahme-/Lastprüfung.
- Menschlicher musikalischer B/C-Hörtest, native Safari-/Firefox-/Tabletprüfung und später echte Dorico-/MuseScore-Importtests stehen aus.

## Nächster einzelner Schritt

M1 anhand einer rechtmäßig verfügbaren echten Klavierpassage musikalisch im A/B/C-Vergleich prüfen und Befunde dokumentieren. Danach M2: Modell-/Lizenz-/Hardwareprüfung für den unabhängigen Audio-only-Transkriptionsprovider, bevor ein Kandidat integriert wird. Ohne Zustimmung keine kostenpflichtigen Modellaufrufe.

## Übergabe

Globale Standards und `AGENTS.md` lesen, dann diese Datei, `TODO.md`, `PFLICHTENHEFT_V0.1.md`, `ARCHITECTURE.md`, `TEST_RESULTS.md` und Code. Mit `npm test` beginnen. Keine Arbeitsstände aus Chat-Erinnerungen ableiten und keine musikalische Freigabe aus technischen Testerfolgen behaupten.
