# Ergänzung: selektives Ausblenden, 28.10.2026

25 Kerntests bestanden. Echte Chromium-Browserprüfung ergänzt um Ausblenden, MIDI-Export, Schema-3-Projektwiederherstellung und Undo/Redo. `test-results/independent-mute-results.json`: unabhängiger mido-Parser bestätigt genau zwei entfernte Ereignisse; alle verbleibenden MIDI-Ereignisse und absoluten Ticks stimmen überein. Original/B bleibt unverändert, C rendert aktive Noten. Alle Noten können ausgeblendet werden, ohne Tempo/Pedal/Metadaten zu verlieren. Die zusätzliche Reparatur ist manuell begründet, keine automatische KI-Entscheidung und keine menschliche Hörfreigabe. Historische Schema-2-Angaben unten beziehen sich auf den vorigen M2-Stand; neue Projekte sind Schema 3, Schema 1/2 bleiben lesbar.

# Prüfbericht – aktueller Stand M1 + technischer M2-Weg

28.10.2026. **25/25 Kerntests bestanden**; beide echten Chromium-Browserregressionen und beide unabhängigen mido-Prüfungen bestanden. Nach Installation aus `package-lock.json` mit `npm ci` erfolgreich neu gebaut und geprüft. Keine Cloud-/kostenpflichtigen Modellaufrufe. Keine menschliche Hörfreigabe.

## Audio-only – echte Modellinferenz

`test-results/transcription-browser-results.json`: Chromium 138.0.7204.0, Basic Pitch 1.0.1, ICASSP-2022-Modell, TensorFlow.js 3.21.0, tatsächliches WASM-Backend. Keine simulierten Modellantworten. Stereo-WAV 44,1 kHz und MP3 ohne MIDI verarbeitet. Modell-/Quellprüfsummen dokumentiert. Testroute hätte jeden externen Request blockiert: **keine externen Requests und keine Nicht-GET-Requests** beobachtet.

Geprüft: zunächst separater Kandidat ohne aktive MIDI; Verwerfen ohne Quellenänderung; ausdrückliche Übernahme; A/B/C/Mix mit gestarteten realen Audioknoten; manuelle Velocitykorrektur ohne veränderte Start-/Endticks; Undo/Redo; Projekt Schema 2 einschließlich Herkunft und Originalen erneut geöffnet. Vorheriges Schema 1 separat im M1-Browserpfad geladen. Audio beim Download byteidentisch. Quelle/Modelldaten in der Diagnose, kein falscher musikalischer Freigabestatus.

Fehlerfälle im Browser: Abbruch vor Übernahme hinterlässt keine MIDI; korrupte Modellgewichte werden per SHA-256 abgelehnt; fehlende Modelldatei führt zu verständlicher Fehlermeldung; Stille erzeugt keine erfundenen Noten und kann nicht als leerer Notenkandidat übernommen werden. Nach diesen Fehlerfällen funktioniert ein erneuter MP3-Lauf. UI-Heartbeat während Inferenz nachgewiesen. Worker-Lifecycle und verspätete Antworten zusätzlich isoliert getestet.

## Konkrete Qualität des synthetischen Tests

Eigener Testgenerator in `tests/transcription-browser.cjs`, zwei vierstimmige Akkorde mit abklingenden Harmonischen, keine fremde Aufnahme. Referenz in `test-results/ground-truth.json`. 8 Referenznoten, 9 Kandidatennoten, 7 passend erkannte Referenznoten bei Tonhöhenübereinstimmung und Onsettoleranz 150 ms. Darunter falsche zusätzliche/ersetzte Oktavtöne: **C5 zusätzlich, D5 statt D4**. Keine verdeckte Nachkorrektur. Recall 0,875 und Präzision 0,7778 sind ausschließlich Werte für diese Testdatei, kein Qualitätsrating für reale Klavieraufnahmen. Maximale Onsetabweichung der korrekt zugeordneten 7 Noten: 13,5 ms. Nicht zugeordnete Noten sind ausdrücklich nicht in dieser Abweichungszahl enthalten.

4-s-Inferenz im zuletzt gesicherten Lauf: 721 ms; nach dem Modelllauf gezählte Tensorbytes 5.570.376. Grenztest mit 60 Sekunden Stille: 6.095 ms, 60.603.048 Tensorbytes, 40 Fortschrittsereignisse, null Noten. Dies ist kein Spitzen-RAM-Messwert und keine allgemeine Geschwindigkeitszusage. Nach jedem Lauf wird der Worker beendet.

## Unabhängiger Kandidatenexport

`tests/independent_transcription.py` mit mido 1.3.3: 9 Noten, nur eine freigegebene Note-on-Velocity geändert; sämtliche Ereigniszeiten, Tonhöhen und Transporttempo erhalten, Dauer 4 s. Quell-Audio- und unbearbeiteter Kandidatenhash mit der Diagnose abgeglichen. Bericht: `test-results/independent-transcription-results.json`. Die 0,5-ms-MIDI-Auflösung wird zusätzlich isoliert mit expressiven Sekundenwerten getestet (maximal 0,25 ms Rundung); keine musikalische Rasterquantisierung.

## Darstellung und Grenzen

Aktuelle Desktop-/Mobilansichten in `test-results/transcription-desktop.png` und `test-results/transcription-mobile.png` visuell geprüft. Kein horizontaler Seitenüberlauf; eigene horizontale Pianorollennavigation. Keine echte Tabletprüfung.

M2 ist als lokaler Kandidatenweg technisch nachgewiesen. **Musikalische Abnahme A11 bleibt offen**, weil weder eine echte Klavieraufnahme mit menschlicher Hörprüfung noch „Graziler Tanz“ vorliegt. Das Modell rekonstruiert kein Pedal, keinen musikalischen Puls, keine Tempokurve und keine kalibrierte Anschlagsdynamik. Kurze Ornamente können fehlen. M3/M4, echte musikalische Fehlerdiagnose und MusicXML sind nicht implementiert. Die Bedienung ermöglicht den Hörvergleich, dieser wurde nicht als menschlich durchgeführt behauptet.

## Reproduzieren

Siehe README. `npm test`, `node tests/browser.cjs`, `node tests/transcription-browser.cjs`, anschließend beide `independent_*.py`-Prüfungen. `test-results/source-sha256.json` erfasst die geprüften Quell-/Laufzeitdateien einschließlich lokaler Modell-/WASM-Assets. Der ursprüngliche M1-Commit bleibt in der Git-Historie erhalten. Nachfolgend der weiterhin gültige M1-Prüfumfang; seine damaligen Aussagen „Audio-only noch nicht implementiert“ sind durch diesen aktuellen Abschnitt ersetzt.

---

# Technischer M1-Nachweis (weiterhin gültiger Teilumfang)

28.10.2026. Geprüft mit synthetischen, im Testcode reproduzierbaren Dateien. Keine „Graziler Tanz“-Dateien vorhanden. Kein behaupteter menschlicher Hörtest. Keine kostenpflichtigen KI-Aufrufe. Geprüfter Quellfingerabdruck: `test-results/source-sha256.json`; Code, Testergebnisse und dieser Bericht werden gemeinsam in einem Commit gesichert.

## Ergebnis

- **15/15 ursprüngliche M1-Kerntests bestanden**, Node.js 24.22.1. Vollständiges TAP-Protokoll: `test-results/unit-tests.tap`.
- **Browserregression bestanden**, tatsächliches Chromium 138.0.7204.0, Playwright 1.62.1. Keine JavaScript-Seitenfehler. Maschinenbericht: `test-results/browser-results.json`.
- **Unabhängige MIDI-Exportprüfung bestanden**, mido 1.3.3. Maschinenbericht: `test-results/independent-midi-results.json`.
- Desktop (1280×900) und mobiles Viewport (390×844) im echten Browser gerendert, Screenshots visuell geprüft: `test-results/desktop.png`, `test-results/mobile.png`. Kein horizontaler Überlauf der Seite; Pianorolle hat bewusst eigene horizontale Navigation. Kein Test eines echten Tablets.

## Schutz des musikalischen Originals

| Prüfung | Tatsächlicher Nachweis |
|---|---|
| Unveränderte Quellen | Export ohne Änderung byteidentisch; Original-MIDI/-MP3 aus UI heruntergeladen und byteweise mit Eingaben verglichen |
| Kein neues Timing bei Tonhöhen-/Velocitykorrekturen | Alle Start-/Endticks gleich; 200 Korrektur-/Exportzyklen ohne neue Abweichung; Sekundenwerte bei Tempowechseln gleich |
| Tempokurve / Performance | Drei Tempoereignisse, mehrere Spuren, CC64, Release-Velocity, Metadaten und SysEx im Export erhalten; mido bestätigt gleiche Ereignisticks und unabhängig integrierte Sekunden |
| Abschnittsschutz | Änderungen außerhalb oder über Abschnittsgrenzen werden verworfen; Nachbarn bleiben unverändert |
| Explizite Rhythmusänderung | Start/Ende nur mit Timingfreigabe, gültigen Werten und Begründung; keine Quantisierungsfunktion |
| Notenüberlappung | Neue Überlappungen gleicher Tonhöhe auf demselben Kanal werden auch über Spurgrenzen abgelehnt |
| Exportkonsistenz | Vor jeder Änderung erneutes SMF-Lesen; vollständige Notensignaturen müssen dem erwarteten Zustand entsprechen |
| Undo/Redo | Rückkehr zu byteidentischem Original, Wiederherstellen und neue Bearbeitungszweige geprüft; Browser-Projektdatei inklusive Redo wieder geöffnet |
| Pedal-Reihenfolge | Pedal verlängert Vergleichsklang; Pedal-down nach Note-off am selben Tick darf die Note nicht nachträglich halten |

Unabhängiger Test mit konstanter Zeitbasis: 19 Ereignisse; ausschließlich Note-on und Note-off des freigegebenen Tons 60→62 geändert, alle Ereigniszeiten unverändert, Länge 4 s. Zweite Testdatei mit wechselndem Tempo: 1,05 s, Tempokarte/Pedal/SysEx/Spuren erhalten und von mido unabhängig in Sekunden integriert.

## Funktionale Browserprüfung

WAV ohne MIDI importiert und gespielt (Audio-only); MP3 importiert und vollständig dekodiert; MIDI-Datei importiert; Note geändert und Undo/Redo durchgeführt; unfreigegebene Zeitänderung abgelehnt; Passage auf der SVG per Maus gezogen und anschließend numerisch gesetzt; Ausgangs-MIDI/Bearbeitung/Mix gespielt, pausiert und fortgesetzt; Audio-Versatz eingestellt; MIDI, Originale und Diagnose heruntergeladen; Projekt einschließlich Originalen und Redo geöffnet. Diagnose enthält Quellhashes, Prüfstatus, Gründe und null KI-Aufrufe.

Die Web-Audio-Engine hat echte AudioBufferSource-/Oscillator-Starts ausgeführt. Zusätzlich wurde ein MIDI-Ton in `OfflineAudioContext` gerendert: Peak 0,041848, erstes messbares Sample nach 0,066032 s bei 0,06 s geplantem Start. Das weist ein erzeugtes Signal nach, **keine musikalische Klangqualität oder vom Menschen gehörte Synchronität**. Gemeinsamer Zeitanker und Audio-Offset werden zusätzlich isoliert mit einer kontrollierten Uhr getestet. Vollständige musikalische Synchronität verschiedener realer Aufnahmen ist nicht belegt.

## Prüfgrenzen und offene Abnahmen

- A01–A08 und A10 sind für den getesteten technischen Teilumfang belegt, nicht für alle realen Dateien oder musikalische Qualität. A03 ist eine einfache Verdachtsdiagnose, keine geprüfte musikalische Analyse. A07 ist eine gezielte technische Regression, keine allgemeine Garantie.
- Menschlicher A/B/C-Hörvergleich, Referenz „Graziler Tanz“ und musikalische Freigabe fehlen.
- A09/MusicXML und A11/Audio-only-Transkription sind M4 bzw. M2 und nicht implementiert. Der Audio-only-Eingang selbst funktioniert ohne MIDI.
- Kein realistischer Klaviersampler; Pitchbend, weitere Controller und Programme sind im Export erhalten, im Vergleichsklang vereinfacht.
- Kein automatisches/mehrpunktiges Alignment, kein Langaufnahme-/Stresstest, kein nativer Safari-/Firefox-/Tablet-Test.
- Keine Veröffentlichung einer als fertig abgenommenen V0.1. Dies ist ein technisch getesteter M1-Prototyp.

## Wiederholung

`npm test`; dann die im README beschriebenen Browser- und unabhängigen MIDI-Tests. Testdaten werden synthetisch erzeugt; FFmpeg erzeugt die MP3. Testergebnisse nicht als Hörfreigabe umdeuten. Standard-Playwright-Browserdownload war in der Arbeitsumgebung nicht verwendbar; der tatsächliche Browser wurde über das offizielle npm-Testbrowserpaket bereitgestellt. Dies ändert die Produktabhängigkeiten nicht.
