# Pflichtenheft – Audio to Good Score, Zielversion 0.1

**Status:** verbindliche Anforderungsbasis. Meilenstein 1 als technisch geprüfter Prototyp umgesetzt; Einzelstatus siehe `PROJECT_STATE.md`. V0.1 ist nicht freigegeben.  
**Plattform:** Web-App, nutzbar auf Windows/macOS/Tablets.  
**Zielgruppe:** Musiker, die aus Audio oder fehlerhaften Transkriptionen klanglich überzeugende MIDI und lesbare MusicXML erzeugen wollen.  
**Startumfang:** Soloklavier. **Referenz:** „Graziler Tanz“ (Audio + erste MIDI, nur wenn Testdateien verfügbar).  
**Standardmodus:** **Musikalisch ausgewogen**.

## 1. Produktziel
Nicht die maximale Zahl exakt übertragener Noten entscheidet, sondern eine musikalisch schlüssige Interpretation: tragende Melodie, motivische Wiedererkennbarkeit, harmonischer Sinn, rhythmischer Fluss, natürlicher Ausdruck, nachvollziehbare Form und spielbare, lesbare Klaviernotation. Änderungen dürfen maßvoll vom Original abweichen, wenn sie musikalisch helfen; intakte Abschnitte bleiben unverändert.

## 2. Gleichrangige Eingangspfade
- **A – Nur Audio** (MP3, WAV): polyphone Klaviertranskription, musikalische Analyse und Rekonstruktion; Vergleich zwischen Audio und renderbarer MIDI.
- **B – Audio + MIDI**: vorhandene Transkription durch zeitliche Ausrichtung und Audiovergleich gezielt verbessern; nicht grundlos neu transkribieren.
- **C – Nur MIDI**: musikalische Strukturanalyse, Reparatur, Klaviernotation; ohne Audio sind Tonhöhenfehler nicht sicher verifizierbar und müssen als unsicher gekennzeichnet werden.

Alle Pfade können über kontrollierte, versionierte Bearbeitungen zu MIDI- und MusicXML-Export führen. Audio-only ist ausdrücklich Kernumfang von 0.1, nicht eine spätere Option.

## 3. Qualitätsprioritäten (heuristisch, keine erfundenen Messwerte)
- Melodie und motivische Substanz: **25 %**
- Rhythmischer Fluss und charakteristischer Puls: **25 %**
- Harmonik/Bass/Stimmenführung: **20 %**
- Ausdruck/Charakter/Entwicklung: **15 %**
- Klaviersatz/Spielbarkeit: **10 %**
- Schonender Umgang mit intakten Stellen/Originalnähe: **5 %**

Diese Gewichtungen priorisieren Reviews; es gibt noch kein kalibriertes automatisches Prozent-Rating. Uneindeutige Stellen kennzeichnen statt ungeprüft zu verändern.

## 4. Funktionale Anforderungen
| ID | Verpflichtende Funktion | Abnahmehinweis |
|---|---|---|
| F01 | Audioimport MP3/WAV | Audio vollständig abspielbar |
| F02 | MIDI-Import (SMF) | Noten, Tempo, Pedal, Dynamik und Spuren möglichst erhalten |
| F03 | Audio-MIDI-Alignment, bei Bedarf manuell justierbar | Synchronisierte Abschnittsnavigation |
| F04 | A/B/C-Player: Audio, Ausgangs-MIDI, Bearbeitung | Hörvergleich gleicher Passage |
| F05 | Pianorolle mit Markierung | Noten und Reparaturbereiche sichtbar |
| F06 | Fehlerdiagnose | verdächtige Timing-/Tonhöhen-/Längen-/Stimmstellen nachvollziehbar |
| F07 | KI-gestützte musikalische Analyse | Melodie, Motivik, Harmonik, Rhythmus mit Unsicherheit |
| F08 | Selektive KI-Korrektur | Nur gewählter Abschnitt geändert, Begründung dokumentiert |
| F09 | Änderungsvergleich, Undo/Redo | Vollständige Reversibilität |
| F10 | MIDI-Export | Freigegebene Performance-Zeiten/Velocity/Pedal respektiert |
| F11 | MusicXML-Export | zweisystemige Klaviernotation mit Stimmen/Pausen/Bögen/Balken |
| F12 | Diagnoseexport | Quellen, Nutzeranweisungen, Modellparameter/Kosten, Änderungen, Validierungen |
| F13 | Projekt-/Versionenspeicherung | Ursprünge unverändert und abrufbar |
| F14 | Audio-only-Transkriptionspfad | Ohne vorhandene MIDI entsteht überprüfbarer MIDI-Kandidat |

## 5. Bearbeitungsregeln
- **Zwei Zeitdarstellungen:** expressive Spielzeiten im Performance-Modell; quantisierte, metrisch konsistente Zeitwerte nur im Score-Modell. Keine rückwirkende Zwangsquantisierung des Hör-MIDI.
- **Tempo:** eine dichte importierte Tempokurve nicht blind löschen; zuerst Ereignisse und absolute Zeit überprüfen. Notations-Tempozeichen separat sparsam ableiten.
- **Musikalische Reparatur:** Kontext über Nachbartakte, Bass/Harmonie, Motive, Stimmen und soweit vorhanden Audiosignal heranziehen. Für jede Änderung Hypothese, Vorher/Nachher und Unsicherheit speichern.
- **Sicherheit:** Original unverändert, atomare Änderungen, Undo/Redo; bei zweifelhaften Änderungen Nutzerentscheidung.
- **Unterschied MIDI vs. Notation:** Die Partitur darf lesbare Rhythmen verwenden, ohne die expressive Wiedergabe zu beeinträchtigen.
- **Keine stillen KI-Neukompositionen:** Umfang und Identität jeder Änderung müssen nachvollziehbar sein.

## 6. Qualitätskontrolle und Freigabe
1. **Technisch:** gültige Dateien, stabile Zeit-/Notenereignisse, unveränderte Originale; MusicXML wird erneut eingelesen; Takt-/Stimmkonsistenz.
2. **Musikalisch:** Motiv-/Melodieführung, Harmonik, lokaler Puls, Ausreißer, Spielbarkeit; Bearbeitung gegen Vorversion und ggf. Referenzaudio prüfen.
3. **Perzeptiv:** A/B-Hörvergleich synchronisierter Passagen, kein künstliches Holpern oder unerklärte Verluste; menschliche Hörfreigabe, solange automatisches Maß nicht validiert.
4. **Notation:** importierte Partitur in Dorico/MuseScore visuell prüfen, inklusive realem Zweihandsatz.
5. **Transparenz:** Status unterscheiden: geplant / implementiert / technisch geprüft / musikalisch geprüft / vom Nutzer bestätigt. Technischer Pass ist keine musikalische Abnahme.

## 7. Konkrete Abnahmetests
| ID | Test / Erfolgsbedingung |
|---|---|
| A01 | Audio und MIDI laden, korrekt zuordnen und ausrichten |
| A02 | Originale bleiben unverändert, sind wieder abrufbar |
| A03 | Verdachtsstellen im musikalischen Kontext darstellen |
| A04 | Markierte Passage bearbeitbar; Nachbarpassagen bleiben unverändert |
| A05 | Originalaudio, Ausgangs-MIDI und Bearbeitung abschnittsweise vergleichbar |
| A06 | Änderungen vollständig rückgängig und wiederherstellbar |
| A07 | Keine neu eingeführten Timing-Störungen durch Tempo-/Quantisierungsänderung |
| A08 | MIDI-Export spielt genehmigten Verlauf ab |
| A09 | MusicXML wird in Dorico und MuseScore geöffnet; lesbar und korrekt strukturiert |
| A10 | Diagnose enthält Eingaben, Anweisungen, Begründungen und Prüfergebnisse |
| A11 | Audio-only: aus einer MP3/WAV wird unabhängig von vorhandener MIDI ein Kandidat erstellt, angehört und überarbeitet |
| A12 | Ergebnis nur nach tatsächlicher Prüfung entsprechend gekennzeichnet; fehlende Prüfung klar benannt |

## 8. Technische Optionen, noch nicht entschieden
Web-Frontend React/TypeScript; Audio Web Audio API; MIDI z.B. mido/pretty_midi; Audioanalyse z.B. librosa; Transkriptionsmodelle (Klavier spezialisiert, Basic Pitch als Vergleich); Server FastAPI; Score-Modell/music21/Partitura; MusicXML-Rendering Verovio. Lizenz-/Performance-/Deployment-Eignung vor Implementierung überprüfen.

## 9. MVP-Reihenfolge
**Meilenstein 1:** Audio- und MIDI-Import, Zeitachsen-Vergleich, Abschnittsmarkierung, nicht-destruktive manuelle Reparatur, Undo, MIDI-Export.  
**Meilenstein 2:** Audio-only-Transkription integriert und anhand Hörvergleich überprüfbar.  
**Meilenstein 3:** KI-gestützte selektive Reparatur mit Diagnose und Versionsvergleich.  
**Meilenstein 4:** MusicXML-Export und reale Notationsprüfung.

Alle Meilensteine gehören zum Zielumfang V0.1; keine pauschale Freigabe vor den Abnahmen.

## 10. Ausgeschlossen in V0.1
Orchester-/Mehrinstrumenten-Arrangement, perfekter Notenrekonstruktionsanspruch, eigener Modell-Trainingsprozess, vollständiger Noteneditor, ungenehmigte umfassende Neukomposition.

## 11. Versions-/Kostenregeln
Keine als funktionsfähig veröffentlichte V0.1 ohne tatsächliche Kernprüfungen. Kostenpflichtige Modellaufrufe nur nachvollziehbar, mit Limits und Diagnose. Nach jedem nachgewiesenen Schritt PROJECT_STATE aktualisieren. Der aktuelle nachgewiesene Umsetzungsstand steht verbindlich in `PROJECT_STATE.md`; dies ist keine Freigabe der Gesamtversion V0.1.

