# Freigabe – Audio to Good Score V0.1, Meilenstein 1

Freigabe zur Nutzung als technisch geprüfte **M1-Vorabversion**, vom Projektinhaber am 28.10.2026 ausdrücklich beauftragt. Geprüfter Produktquellstand: `d40b6058b5125fff89cdf6da3d16498a3e62c720`. Freigabezweig: `release/v0.1-m1`. Diese Freigabe ändert ausschließlich die Dokumentation; der geprüfte Produktcode bleibt unverändert.

## Enthalten

Audio-/MIDI-Import, gemeinsame Wiedergabe mit manuellem Versatz, Pianorolle und Abschnittsauswahl, nicht-destruktive Einzelnotenbearbeitung mit Begründung und Schutz der Performance-Zeiten, Undo/Redo, A/B/C-Vergleich, MIDI-Export und Diagnose. Zusätzlich bereits enthalten: lokale Audio-only-Transkription, kontrollierte lokale Audio-Gegenprüfung, Projektwiederherstellung und getrennte MusicXML-Prüffassung.

## Prüfgrundlage

33 Kerntests, vollständige echte Chromium-Bedienungs-/Modellregression und vier unabhängige mido-Prüfungen bestanden. Keine neu eingeführten Rhythmusabweichungen in den geprüften Fällen. MuseScore 3.2.3 und 4.7.6 jeweils mit sechs realen Import-/Speicher-/Rückexportfällen geprüft. Belege: `test-results/final/`, `test-results/musescore/`, `test-results/musescore4/`.

## Start

Archiv entpacken, im Projektordner starten:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Dann `http://localhost:8000` öffnen. Unter Windows gegebenenfalls `py` statt `python3`. Kein npm-Build und kein API-Schlüssel nötig. Dateien werden lokal verarbeitet; Projekte vor dem Schließen speichern. Arbeitsmodus: Musikalisch ausgewogen. Keine kostenpflichtigen KI-Aufrufe.

## Bekannte Grenzen

Die technische M1-Freigabe ist keine vollständige fachliche V0.1-Abnahme oder behauptete Hörfreigabe. Echte Referenzaufnahme und menschliche musikalische Beurteilung, umfassende F07/F08-Validierung, Dorico sowie weitere Plattformprüfungen bleiben offen. Synthesizer vereinfacht; Basic Pitch kann Töne auslassen, hinzufügen oder oktavversetzen. Jeder Kandidat muss geprüft werden. Alle weiteren Grenzen stehen in `ACCEPTANCE.md`.

Kein separater GitHub-Releases-Eintrag: Die verfügbare Anbindung unterstützt dessen Erstellung nicht. Der freigegebene Stand wird im benannten Freigabezweig bereitgestellt.
