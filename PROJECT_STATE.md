# Projektstand – Audio to Good Score

Stand: 28.10.2026. **Meilenstein 1 als technisch geprüfte Vorabversion zur Nutzung freigegeben; V0.1 nicht vollständig abgenommen.** Freigabe am 28.10.2026 auf ausdrücklichen Auftrag, Zweig `release/v0.1-m1`, geprüfter Produktcode `d40b6058b5125fff89cdf6da3d16498a3e62c720`. Siehe `RELEASE_M1.md`. Siehe `MILESTONE_1.md`. GitHub `wibem1/Audio-to-Good-Score`, `main`, ist maßgeblich. Vorige gesicherte Stände bleiben in der Historie: M1 `6458b6d`, Audio-only `0b3bcf7`, Notenausblendung `b48547c`.

## Nachgewiesene Funktionen

- Audio-only, Audio+MIDI und MIDI-only; WAV/MP3, SMF 0/1, lokale Basic-Pitch-Transkription ohne Cloud und ohne bestehende MIDI.
- Gemeinsame Zeitachse, manuelles Alignment, Abschnittsauswahl/Pianorolle, A/B/C und Mix. Einfacher Vergleichssynthesizer, keine Klaviersample-Klangfreigabe.
- Nicht-destruktive Tonhöhen-/Velocity-/Zeitänderungen mit Begründung, separate Timingfreigabe, reversible Notenausblendung und **manuelles Ergänzen fehlender Noten**. Abschnitts-/Überlappungs-/Export-Roundtrip-Schutz, Undo/Redo. Originaldateien unverändert.
- **Kontextdiagnose und kontrollierte Vorschläge:** Tonklassen-/Bass-/Spitzenlage, einfache Akkordmuster, wiederkehrende Intervalle und Einsatzabstände; mögliche Oktavdoppelungen/-sprünge als unsichere Hypothesen. Zusätzlich echte lokale Basic-Pitch-Audio-Gegenprüfung bestehender MIDI mit begrenzten neuronalen Oktavvorschlägen und protokollierter Modellevidenz. Kein automatisches Übernehmen. Veraltete Vorschläge/Quellenwechsel werden abgefangen, Gründe stehen im Änderungsprotokoll und Kontext im Diagnoseexport.
- **Getrenntes Score-Modell und MusicXML:** zwei Klaviersysteme, mehrere unabhängige Stimmen, Akkorde, Pausen, Taktfüllung, Bindungen und Balken. Wählbare Taktart/Handteilung, MIDI-Metrik oder Audiosekunden mit gewähltem BPM. Sechzehntelraster ausschließlich im Score-Modell. Keine Rückquantisierung des Performance-MIDI.
- Projekt Schema 4 speichert Originale, Änderungen einschließlich Ergänzungen, Modellherkunft und Notationsparameter; ältere Schema 1/2/3 bleiben lesbar. Manuell speichern. Diagnose und Notationszuordnung exportierbar.

## Prüfgrundlage

33/33 Kerntests bestanden. Abschlusskorrektur verhindert verspätetes Starten nach Pause und doppelte Wiedergabe bei überholenden Audioaktivierungen. Vollständige Browser-/Modellregression und vier unabhängige MIDI-Prüfungen nach der Korrektur erneut bestanden (`test-results/final/`). Reale Chromium-Prüfung einschließlich Ergänzen, Projektwiederherstellung, Kontext-UI, MusicXML-/Mapping-Export; lokale Modellregression weiterhin bestanden. Unabhängige mido-Prüfungen bestätigen Ereignis-/Rhythmuserhalt. MusicXML durch music21 9.9.1 erneut gelesen: alle zehn Testnoten einschließlich quantisierter Start-/Dauerwerte nach Tie-Zusammenführung gleich. Jede Stimme füllt jeden Takt. Verovio 5.7.0 rendert zwei Systeme; SVG visuell geprüft. Kein XSD-Validierungsnachweis und noch keine Dorico-Abnahme. Einzelheiten: `TEST_RESULTS.md`, `ACCEPTANCE.md`, `test-results/`.

## Verbleibende Lücken für vollständige V0.1

1. **Musikalische KI-Abnahme offen:** Das neuronale Modell liefert Audio-Notenkandidaten und kann vorhandene MIDI selektiv mit Audio gegenprüfen. Ein echter Modell-Browsertest korrigiert nach ausdrücklicher Bestätigung einen synthetischen Oktavfehler und bestätigt Undo/Rhythmuserhalt. Die musikalische Kontextanalyse und Reparaturhypothesen sind transparente Regeln, kein abgenommenes KI-Modell für Melodie/Motivik/Harmonik. Keine erfundene KI-Freigabe.
2. **A09 offen:** MuseScore 3.2.3 ist jetzt in sechs Fällen mit echtem MusicXML-Import, nativem Speichern/Öffnen, Rückexport und PNG-Rendering geprüft. Alle Noten-Tonhöhen, Einsätze, Dauern und Systeme bleiben erhalten. MuseScore 4.7.6 besteht dieselben sechs Fälle ebenfalls; Dorico bleibt ungeprüft; A09 ist insgesamt noch offen.
3. **A11 musikalisch offen:** Keine bereitgestellte echte Referenzaufnahme „Graziler Tanz“ und keine menschliche A/B/C-Hörfreigabe. Im synthetischen Basic-Pitch-Test weiterhin Oktav-/Auslassungsfehler (7 passende von 8 Referenznoten, 9 Modellnoten).
4. Native Tablet-/Safari-/Firefox-Abnahme fehlt. Score-Handteilung ist heuristisch; kein Triole-/Rubato-/Phrasierungsautomatismus. Pedal wird nicht aus Audio rekonstruiert. Keine automatische Tempoausrichtung. Kein automatisches Spielbarkeitsurteil.

## Betrieb und Fortsetzung

`python3 -m http.server 8000 --bind 127.0.0.1`, dann `http://localhost:8000`. Kein zusätzlicher Modelldownload für die Benutzung. Globale Standards, AGENTS, Pflichtenheft, diesen Stand und `ACCEPTANCE.md` lesen. `npm test` ausführen. Neue Module `analysis.js` und `score.js`; Testwerkzeuge music21/Verovio sind keine Produktabhängigkeiten.

Nächste Abnahmeschritte: echte Klavierpassage mit menschlichem Hörvergleich, MusicXML in beiden Zielprogrammen prüfen und die begrenzte F07/F08-Musikqualität separat validieren und bei Bedarf erweitern. Keine umfassende automatische Korrektur ohne Einzelfreigabe und keine kostenpflichtigen KI-Aufrufe ohne Zustimmung. Kostenpflichtige/Cloud-Modellaufrufe bisher null.

## MuseScore-Nachweis

Echte MuseScore-Versionen 3.2.3 (Ubuntu) und 4.7.6 (offizielle AppImage), isoliert als Testwerkzeug bereitgestellt, keine Produktabhängigkeit. Sechs Import-/Native-Speicher-/Rückexportfälle bestanden; PNG visuell geprüft. Dies ist keine pauschale Satzqualitätsfreigabe oder Hörprüfung. Reproduzierbarer Test: `tests/musescore-fixtures.js`, `tests/musescore_import.py`; Berichte/native Beispieldatei/Notenbild: `test-results/musescore/` und `test-results/musescore4/`.
