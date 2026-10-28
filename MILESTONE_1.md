# Meilenstein 1 – technischer Abschluss, 28.10.2026

Der ursprünglich beauftragte erste Web-App-Prototyp ist implementiert und mit echten Browserkomponenten geprüft. Dies ist die technische Fertigstellung von **Meilenstein 1**, keine musikalische oder vollständige V0.1-Freigabe.

| Beauftragter Umfang | Nachweis |
|---|---|
| Audio- und MIDI-Import | WAV/MP3 und SMF 0/1 im echten Chromium-Browser |
| Synchronisierte Wiedergabe | Gemeinsamer Web-Audio-Zeitanker, Versatz, A/B/C und Mix; Audio-Rendering und Knotenanläufe geprüft |
| Pianorolle und Abschnitt | Echte Zeigeraktion und numerische Auswahl, mobilbreite Ansicht ohne Seitenüberlauf |
| Nicht-destruktive Einzelnoten | Originaldateien byteidentisch abrufbar, lokale Änderungen mit Begründung und Abschnittsschutz |
| Undo/Redo | Änderung, Ergänzung, Ausblendung und Projektwiederherstellung geprüft |
| A/B-Hörvergleich | Vergleichswiedergabe derselben Passage technisch geprüft; menschliches Qualitätsurteil ausstehend |
| MIDI-Export | Unabhängig mit mido 1.3.3 eingelesen; Zeiten, Tempokarte, Pedal und übrige Ereignisse erhalten |
| Diagnose | Quellenhashes, Gründe, Unsicherheiten und Kosten exportiert |
| Gleichrangiger Audio-only-Weg | Eigenständiger Import/Player; zusätzlich lokale echte Basic-Pitch-Inferenz bereits implementiert und regressiongeprüft |

33/33 Kerntests bestanden. Darunter 200 Editier-/Exportzyklen ohne neue Rhythmusabweichung sowie zwei Abschlussregressionen: Pause während ausstehender Audioaktivierung verhindert späteres Starten; bei überholenden Startbefehlen gewinnt ausschließlich der neueste. Beide neuen Tests schlugen vor der Korrektur fehl. Die Korrektur ändert keine MIDI-Daten.

Vollständiger Chromium-Bedienungs- und Modelltest nach der Korrektur bestanden, keine Seitenfehler. Vier unabhängige MIDI-Prüfungen erneut bestanden. Aktuelle maschinenlesbare Belege: `test-results/final/`. Reproduktion: `npm test`, `tests/browser.cjs`, `tests/transcription-browser.cjs` und die vier `tests/independent_*.py` für MIDI/Notenausblendung/Gegenprüfung/Transkription; Anleitung im README.

## Benutzen

Repository herunterladen/entpacken. Im Projektordner `python3 -m http.server 8000 --bind 127.0.0.1` starten (Windows gegebenenfalls `py` statt `python3`). `http://localhost:8000` öffnen, Audio und/oder MIDI laden. Kein npm-Build, kein API-Schlüssel, kein kostenpflichtiger Dienst erforderlich. Vor dem Schließen Projekt speichern.

## Grenze des Abschlusses

Die spätere Gesamt-V0.1 enthält zusätzliche Anforderungen. MuseScore 3 und 4 sind geprüft; Dorico fehlt. Echte Referenzaufnahme „Graziler Tanz“, menschlicher A/B/C-Hörentscheid und umfassende musikalische Modellvalidierung fehlen. Native Safari-/Tablet- und erfolgreiche Firefox-Prüfung liegen nicht vor; ein echter Firefox-Testlauf blieb in dieser Umgebung beim Audioladen hängen. Diese Grenzen sind keine als erledigt markierten Aufgaben. Gesamtstatus: `ACCEPTANCE.md`. Keine kostenpflichtigen KI-Aufrufe.
