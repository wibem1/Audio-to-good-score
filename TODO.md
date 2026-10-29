# MusicCraft App – Aufgaben

## Verarbeitungskern 0.3

- [x] Inhalt/Gestaltung trennen, JSON-Schemas und semantische Validatoren für das begrenzte Klavierprofil
- [x] Kompakte verlustfreie Tabellen, Migration und Tonalternativen ohne automatische Übernahme
- [x] music21/mido-Export, unabhängige XML-Prüfung, MIDI-Roundtrip und Verovio-Rendering
- [x] 38 neue Tests, 12 Einheitenfälle und 39 bestehende JS-Kerntests bestanden
- [ ] **Nächster Schritt:** Browseranbindung an Analyse-/Kompositionsmodule; Player/Chat und tatsächliche KI-Aufträge offen
- [ ] Musikalisches Kandidatenranking, weitere Ausdrucksparameter, externer 0.3-Test und reale Dorico/MuseScore-Abnahme

## Historischer Übergabeprotokoll-Stand 0.2

- [x] Analysebefunde und spielbaren Composition Plan trennen; eindeutige Zeit-/Tempo-/Dauerregeln festhalten
- [x] 12 isolierte Einheiten-Regressionen ausführen; Gemini-Fehlerklassen abdecken
- [ ] Unabhängiger externer Test je Quelle mit aktuellem Protokoll 0.3
- [x] Begrenztes Kernprofil 0.3 mit Schemas/Validator/Exporter; reale Zielprogramm-Abnahmen separat offen

## Vereinbarte Neuausrichtung (29.10.2026)

- [x] Umbenanntes GitHub-Repository bestätigen und neue Ausrichtung in Pflichtenheft, PROJECT_STATE, AGENTS und README dokumentieren
- [ ] Nachgeordnet: versioniertes Analysebericht-Modell und einfache Modulansicht mit ausdrücklich gekennzeichneten Beispieldaten; Kriterien/Taktmatrix, Unsicherheiten, Nutzerhinweise und Änderungen zwischen Phrasen testen
- [ ] Echte musikalische Analyse von Audio-only, MIDI-only und Audio+MIDI integrieren und getrennt validieren; Modellwahl und Kosten kontrollieren, keine bezahlten Aufrufe ohne Zustimmung
- [ ] Sicherheit je Kriterium und Takt/Zeitabschnitt aus Befunden begründen; Taktart-/Grenzunsicherheit weiterreichen, keine erfundenen Prozentwerte
- [ ] Kurzurteil zu Eignung und erwartbarer Vorlagennähe; Details aufklappbar, Audiostelle/MIDI-Abschnitt direkt erreichbar
- [ ] Explizite Beauftragung vor Nachkomposition; versionierte Übergabe aus Quelle, Analyse, Unsicherheiten und Nutzerhinweisen; Änderungen machen abhängige Ergebnisse als veraltet sichtbar
- [ ] Kompositionsmodul: vorlagennahe Imitation und selektive Überarbeitung, Vergleich/Undo/Redo, MIDI und MusicXML
- [ ] Kompositionsmodul: eigenständige neue Komposition aus Motiv oder Vorgaben ohne Analysepflicht
- [ ] Neue Abnahmefälle MC01–MC10 aus dem Pflichtenheft ausführen; technische und musikalische Abnahme getrennt führen

Neue Modularchitektur ist geplant, nicht implementiert. Dokumentationsänderung ist keine Produktfreigabe.

## Offene Prüfungen und Nachweise des bisherigen Prototyps

# Meilenstein 1 technisch abgeschlossen; verbleibende V0.1-Aufgaben

Abschluss und Startanleitung: `MILESTONE_1.md`.

- [x] Audio/MIDI/Audio-only, Wiedergabe, Pianorolle und Abschnitt technisch prüfen
- [x] Nicht-destruktive Änderungen, Ausblenden, manuelles Ergänzen, Undo/Redo und MIDI-Export prüfen
- [x] Lokale Modellinferenz, Abbruch, Herkunft, Projekt und Diagnose prüfen
- [x] Kontextbeschreibung und explizite unsichere Reparaturvorschläge ohne automatische Übernahme
- [x] Getrenntes Score-Modell, zweisystemiger MusicXML-Export mit Stimmen/Pausen/Ties/Balken
- [x] MusicXML mit unabhängigem Parser vergleichen und echter Notensatz-Engine rendern
- [x] Echte lokale neuronale Audio-Gegenprüfung für explizite Oktavkorrekturen, Undo und unveränderte MIDI-Zeiten testen
- [ ] F07/F08 musikalisch validieren/bei Bedarf erweitern; Kontextregeln nicht als umfassende semantische KI-Analyse ausgeben
- [x] Reale MusicXML-Importe in MuseScore 3.2.3, natives Speichern/Öffnen, Rückexport und Rendering in sechs Fällen
- [x] MuseScore 4.7.6: sechs echte Import-/Native-Speicher-/Rückexportfälle und Rendering
- [ ] Reale MusicXML-Importe in Dorico
- [x] Reale Referenz „Etüde Piano“ mit Audio/MIDI/MusicXML analysieren; Notationsfehler reproduziert
- [x] Vereinfachte Anschlagsfassung separat erzeugen, MuseScore-4-Roundtrip, Parser- und Sichtprüfung
- [ ] MIDI-Stolperer der echten Referenz gezielt verifizieren und schonend korrigieren; musikalische A/B-Abnahme
- [ ] Vollständige Stimmen-/Takt-/Ausdrucksrekonstruktion; Anschlagsfassung ist kein fertiger Klaviersatz
- [ ] Native Tablet-/Safari-/Firefox-Abnahme

39 Kerntests bestanden. Vereinfachter Eingabe-/Abschnittsablauf sowie Schema-5-Sammelbearbeitung technisch geprüft; Nutzerbewertung der neuen Bedienung steht aus. Wiedergabe-Race behoben; vollständige Chromium-/Modellregression und unabhängige MIDI-Prüfungen wiederholt. Detaillierte Funktions-/Abnahmegrenzen: `ACCEPTANCE.md`. V0.1 nicht freigegeben. Keine kostenpflichtigen KI-Aufrufe.


