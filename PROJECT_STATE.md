# Projektstand – MusicCraft App

Stand: **29.10.2026**. Maßgebliches Repository: **`wibem1/MusicCraft-App`**, `main`; vom Nutzer umbenannt. Letzter technisch geprüfter Produktcode: `f1e5eccbb68c12abdd4b74b0a1c10aaac84aa98f`.

## Übergabeprotokoll 0.2 (29.10.2026)

Protokoll und isolierte Einheiten-Regression implementiert: `protocol/HANDOFF_PROTOCOL.md`, `tests/test_handoff_units.py`; 12/12 Tests bestanden (`test-results/handoff-0.2.txt`). Analyse bleibt lückenhafter Befundbericht; separater Composition Plan legt erst spielbare Ereignisse fest. Sekunden, Viertelnoten-Einheiten, Tempo-Bezugswert und exakte Brüche eindeutig definiert. Tests decken punktiertes Tempo, Taktfüllung, Triolen, Gate-Differenzen und unzureichende MusicXML-Divisionen ab. Kein Produktionsvalidator/Exporter, kein neues App-Release und keine bezahlten Aufrufe.

Explorative private Audio-/MIDI-Übergabe und frischer KI-Kontext waren laut Nutzer im Hören vielversprechend. Nutzer lieferte anschließend Gemini-Code mit inkonsistentem Tempo und MusicXML-Dauern sowie unbelegten Prüfbehauptungen. Diese Fehlerklassen werden lokal arithmetisch reproduziert; Geminis vollständiger Originalcode wurde nicht ausgeführt. Ein erneuter externer Gemini-Test mit 0.2 steht aus. Nutzer-Musikdateien bleiben privat und werden nicht in GitHub aufgenommen.

Nächster einzelner Schritt: 0.2 in frischen Kontexten je Quelle erneut prüfen; danach schema-validierten Composition Plan und gemeinsamen Exporter mit unabhängigem MIDI-/MusicXML-Roundtrip implementieren. Die folgenden früheren UI-Schritte sind nachgeordnet.

## Vorige Entscheidung und Entwicklungsplanung

**In diesem Schritt nur Dokumentation:** Produktname, Pflichtenheft, Agentenanweisungen, README und TODO auf die vereinbarte Ausrichtung gebracht. Kein Produktcode geändert, keine neue App-Version oder Freigabe, keine kostenpflichtigen Aufrufe. Die bisherigen Testnachweise sind historische Nachweise des unten beschriebenen Codes, keine Tests der neuen Zielarchitektur. Dokumentationsprüfung dieses Schritts: fünf Markdown-Dateien auf UTF-8, geschlossene Codeblöcke, vollständige MC01–MC10-Abnahmefälle, Kernkriterien, Statusabgrenzung und lokale Dateiverweise geprüft. Produkt-/Modelltests nicht erneut ausgeführt, da ausschließlich Dokumentation geändert wird.

**Verbindlich geplant:** zwei eigenständige Module **Analyse** und **Komposition**. Audio-only, Audio+MIDI und MIDI-only sind gleichberechtigt. Neue Komposition aus Motiven/Vorgaben ist auch ohne Vorlage möglich. Vorlagenbezogene Imitation erst nach verständlichem Analysebericht und ausdrücklichem Nutzerauftrag. Bericht enthält Kriterienkatalog, Sicherheit je Kriterium und Takt/Zeitabschnitt, offene Fragen, Machbarkeit und begründete Prognose der Vorlagennähe. Details optional aufklappbar; keine bürokratische Einzelnotenabnahme. Siehe `PFLICHTENHEFT_V0.1.md`, Abschnitt 12.

**Nachgeordneter UI-Schritt:** versionierten Analysebericht als Datenmodell und einfache Modulansicht prototypisch umsetzen: Kurzurteil, Kriterien und Takt-/Zeitabschnittsmatrix einschließlich begründeter Unsicherheiten und Nutzerhinweisen. Testfälle für unsichere Taktgrenzen, unterschiedliche Sicherheit innerhalb desselben Takts und eine veränderte Schlussfigur vorsehen. Beispieldaten eindeutig als solche kennzeichnen; kein fingierter KI-Nachweis. Modell-/Kostenentscheidung für echte Analyse separat treffen; bezahlte Aufrufe bleiben zustimmungspflichtig.

**Noch nicht implementiert:** vollständiger semantischer KI-Analysebericht, grafische Sicherheitsmatrix, Machbarkeitsprognose, darauf aufbauende Nachkomposition und freie generative Komposition. Die vorhandene Basic-Pitch-Inferenz und regelbasierte Kontextdiagnose ersetzen diese Funktionen nicht.

## Bisheriger technischer Stand (28.10.2026)

 **Realer Referenztest:** Nutzer meldet unbrauchbares Notenbild und hörbare Stolperer. Etüden-Audio/MIDI/MusicXML liegen vor; bisherige technische Abnahme war keine musikalische Qualitätsabnahme. Neue getrennte Anschlagsfassung mit Puls-/Taktanfangprüfung, punktierten Werten und explizitem Notationstempo implementiert und an dieser Referenz in MuseScore 4 geprüft. MIDI-Stolperer bleiben ungeklärt; Original-MIDI nicht quantisiert. Details: `test-results/reference-score/`.

 **Bedienüberarbeitung nach Nutzertest:** vier Schritte, zuverlässige sichtbare Dateinamen, Test-MIDI von eigenen Aufnahmen getrennt, Audio-only-Rückweg und gemeinsame Abschnittsänderung mit einmal Undo. Anleitung: `BEDIENUNG.md`. Vorige M1-Freigabe bleibt in `release/v0.1-m1` unverändert erhalten; diese Überarbeitung ist separat technisch geprüft.

 **Meilenstein 1 als technisch geprüfte Vorabversion zur Nutzung freigegeben; V0.1 nicht vollständig abgenommen.** Freigabe am 28.10.2026 auf ausdrücklichen Auftrag, Zweig `release/v0.1-m1`, geprüfter Produktcode `d40b6058b5125fff89cdf6da3d16498a3e62c720`. Siehe `RELEASE_M1.md`. Siehe `MILESTONE_1.md`. GitHub `wibem1/MusicCraft-App`, `main`, ist maßgeblich. Vorige gesicherte Stände bleiben in der Historie: M1 `6458b6d`, Audio-only `0b3bcf7`, Notenausblendung `b48547c`.

## Nachgewiesene Funktionen

- Audio-only, Audio+MIDI und MIDI-only; WAV/MP3, SMF 0/1, lokale Basic-Pitch-Transkription ohne Cloud und ohne bestehende MIDI.
- Gemeinsame Zeitachse, manuelles Alignment, Abschnittsauswahl/Pianorolle, A/B/C und Mix. Einfacher Vergleichssynthesizer, keine Klaviersample-Klangfreigabe.
- Nicht-destruktive Tonhöhen-/Velocity-/Zeitänderungen mit Begründung, separate Timingfreigabe, reversible Notenausblendung und **manuelles Ergänzen fehlender Noten**. Abschnitts-/Überlappungs-/Export-Roundtrip-Schutz, Undo/Redo. Originaldateien unverändert.
- **Kontextdiagnose und kontrollierte Vorschläge:** Tonklassen-/Bass-/Spitzenlage, einfache Akkordmuster, wiederkehrende Intervalle und Einsatzabstände; mögliche Oktavdoppelungen/-sprünge als unsichere Hypothesen. Zusätzlich echte lokale Basic-Pitch-Audio-Gegenprüfung bestehender MIDI mit begrenzten neuronalen Oktavvorschlägen und protokollierter Modellevidenz. Kein automatisches Übernehmen. Veraltete Vorschläge/Quellenwechsel werden abgefangen, Gründe stehen im Änderungsprotokoll und Kontext im Diagnoseexport.
- **Getrenntes Score-Modell und MusicXML:** zwei Klaviersysteme, mehrere unabhängige Stimmen, Akkorde, Pausen, Taktfüllung, Bindungen und Balken. Wählbare Taktart/Handteilung, MIDI-Metrik oder Audiosekunden mit gewähltem BPM. Sechzehntelraster ausschließlich im Score-Modell. Keine Rückquantisierung des Performance-MIDI.
- Projekt Schema 5 speichert Originale, Änderungen einschließlich Ergänzungen, Modellherkunft und Notationsparameter; ältere Schema 1/2/3/4 bleiben lesbar. Manuell speichern. Diagnose und Notationszuordnung exportierbar.

## Prüfgrundlage

39/39 Kerntests bestanden. Neue Prüfbelege: `test-results/usability/`. Sammelbearbeitung atomar; Ablehnung hinterlässt auch Redo unverändert. Projektrückladen und einmal Undo für gemeinsame Abschnittsänderungen im echten Browser geprüft. Abschlusskorrektur verhindert verspätetes Starten nach Pause und doppelte Wiedergabe bei überholenden Audioaktivierungen. Vollständige Browser-/Modellregression und vier unabhängige MIDI-Prüfungen nach der Korrektur erneut bestanden (`test-results/final/`). Reale Chromium-Prüfung einschließlich Ergänzen, Projektwiederherstellung, Kontext-UI, MusicXML-/Mapping-Export; lokale Modellregression weiterhin bestanden. Unabhängige mido-Prüfungen bestätigen Ereignis-/Rhythmuserhalt. MusicXML durch music21 9.9.1 erneut gelesen: alle zehn Testnoten einschließlich quantisierter Start-/Dauerwerte nach Tie-Zusammenführung gleich. Jede Stimme füllt jeden Takt. Verovio 5.7.0 rendert zwei Systeme; SVG visuell geprüft. Kein XSD-Validierungsnachweis und noch keine Dorico-Abnahme. Einzelheiten: `TEST_RESULTS.md`, `ACCEPTANCE.md`, `test-results/`.

## Verbleibende Lücken für vollständige V0.1

1. **Musikalische KI-Abnahme offen:** Das neuronale Modell liefert Audio-Notenkandidaten und kann vorhandene MIDI selektiv mit Audio gegenprüfen. Ein echter Modell-Browsertest korrigiert nach ausdrücklicher Bestätigung einen synthetischen Oktavfehler und bestätigt Undo/Rhythmuserhalt. Die musikalische Kontextanalyse und Reparaturhypothesen sind transparente Regeln, kein abgenommenes KI-Modell für Melodie/Motivik/Harmonik. Keine erfundene KI-Freigabe.
2. **A09 offen:** MuseScore 3.2.3 ist jetzt in sechs Fällen mit echtem MusicXML-Import, nativem Speichern/Öffnen, Rückexport und PNG-Rendering geprüft. Alle Noten-Tonhöhen, Einsätze, Dauern und Systeme bleiben erhalten. MuseScore 4.7.6 besteht dieselben sechs Fälle ebenfalls; Dorico bleibt ungeprüft; A09 ist insgesamt noch offen.
3. **A11 musikalisch offen:** Reale Referenz „Etüde Piano“ liegt vor (164,4 s Audio, MIDI nur erste 60 s). Nutzertest benennt Notations- und Hörmängel; keine positive menschliche A/B/C-Freigabe. „Graziler Tanz“ wurde nicht bereitgestellt. Im synthetischen Basic-Pitch-Test weiterhin Oktav-/Auslassungsfehler (7 passende von 8 Referenznoten, 9 Modellnoten).
4. Native Tablet-/Safari-/Firefox-Abnahme fehlt. Score-Handteilung ist heuristisch; kein Triole-/Rubato-/Phrasierungsautomatismus. Pedal wird nicht aus Audio rekonstruiert. Keine automatische Tempoausrichtung. Kein automatisches Spielbarkeitsurteil.

## Betrieb und Fortsetzung

`python3 -m http.server 8000 --bind 127.0.0.1`, dann `http://localhost:8000`. Kein zusätzlicher Modelldownload für die Benutzung. Globale Standards, AGENTS, Pflichtenheft, diesen Stand und `ACCEPTANCE.md` lesen. `npm test` ausführen. Neue Module `analysis.js` und `score.js`; Testwerkzeuge music21/Verovio sind keine Produktabhängigkeiten.

Offene Abnahmen des bisherigen Prototyps (neben dem oben priorisierten nächsten Entwicklungsschritt): echte Klavierpassage mit menschlichem Hörvergleich, MusicXML in beiden Zielprogrammen prüfen und die begrenzte F07/F08-Musikqualität separat validieren und bei Bedarf erweitern. Keine umfassende automatische Korrektur ohne Einzelfreigabe und keine kostenpflichtigen KI-Aufrufe ohne Zustimmung. Kostenpflichtige/Cloud-Modellaufrufe bisher null.

## MuseScore-Nachweis

Echte MuseScore-Versionen 3.2.3 (Ubuntu) und 4.7.6 (offizielle AppImage), isoliert als Testwerkzeug bereitgestellt, keine Produktabhängigkeit. Sechs Import-/Native-Speicher-/Rückexportfälle bestanden; PNG visuell geprüft. Dies ist keine pauschale Satzqualitätsfreigabe oder Hörprüfung. Reproduzierbarer Test: `tests/musescore-fixtures.js`, `tests/musescore_import.py`; Berichte/native Beispieldatei/Notenbild: `test-results/musescore/` und `test-results/musescore4/`.

