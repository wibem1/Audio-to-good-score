# Prüfbericht – Meilenstein 1

28.10.2026. Geprüft mit synthetischen, im Testcode reproduzierbaren Dateien. Keine „Graziler Tanz“-Dateien vorhanden. Kein behaupteter menschlicher Hörtest. Keine kostenpflichtigen KI-Aufrufe. Geprüfter Quellfingerabdruck: `test-results/source-sha256.json`; Code, Testergebnisse und dieser Bericht werden gemeinsam in einem Commit gesichert.

## Ergebnis

- **15/15 Kerntests bestanden**, Node.js 24.22.1. Vollständiges TAP-Protokoll: `test-results/unit-tests.tap`.
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
