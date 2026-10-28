# Abnahmestand V0.1 – 28.10.2026

Die Anwendung ist ein technisch geprüfter Entwicklungsstand. **V0.1 ist nicht vollständig fertig oder freigegeben.** Diese Liste trennt implementierte Funktionen von fehlender Fachabnahme.

| Pflichtenheft | Stand |
|---|---|
| F01/F02 Import | WAV/MP3/SMF 0/1 technisch geprüft, SMPTE/Typ 2 ausdrücklich nicht unterstützt |
| F03 Alignment | Gemeinsame Uhr und manueller konstanter Versatz; keine automatische Tempodriftkorrektur |
| F04/F05 Player/Pianorolle | Browsergeprüft, keine menschliche Hörfreigabe |
| F06 Diagnose | Heuristischer Kontext, Verdachtsfälle mit Unsicherheit, keine bestätigte Fehlerklassifikation |
| F07 KI-Musikanalyse | **Teilweise/offen:** neuronale Audio-Noteninferenz vorhanden; Kontextregeln für Tonklassen, Akkordmuster, Oberstimmen-Intervallmotive und Pulsabstände sind keine umfassende KI-Musikanalyse |
| F08 selektive KI-Reparatur | Lokale neuronale Audio-Gegenprüfung liefert begrenzte Oktavvorschläge für vorhandene MIDI; explizite Entscheidung, Gründe und Undo technisch geprüft. Keine allgemeine musikalische Reparaturfreigabe |
| F09/F10 Undo/Redo/MIDI | Ergänzung, Ausblendung, Notenänderungen und Ereigniserhalt technisch geprüft |
| F11 MusicXML | Zweihandsystem mit Stimmen/Pausen/Akkorden/Ties/Balken und unabhängiger Importprüfung implementiert; echter MuseScore-3.2.3-Test mit sechs Fällen bestanden; Dorico/MuseScore 4 fehlen |
| F12 Diagnoseexport | Quellen, Modellhashes, Parameter/Kosten, Änderungen/Gründe, Unsicherheit, Kontextdiagnose und technische Prüflücken; Notationsmapping separat exportierbar |
| F13 Projekt | Schema 4, Originalbytes/Änderungsjournal/Notationsparameter, ältere Formate lesbar |
| F14 Audio-only | Reale lokale Modellinferenz technisch geprüft; musikalische Abnahme offen |

## Tatsächliche Hindernisse für die Freigabe

- MuseScore 3.2.3 wurde tatsächlich ausgeführt: Import → natives MSCX → erneutes Öffnen → MusicXML; sechs Fälle mit identischen Tonhöhen, Notationszeiten und Systemen. Notenbild gerendert und visuell geprüft. Dorico ist weiterhin nicht verfügbar; MuseScore 4 ist nicht geprüft. A09 ist deshalb insgesamt offen.
- „Graziler Tanz“ bzw. eine rechtmäßig bereitgestellte echte Referenzpassage und die menschliche Hörentscheidung fehlen. Synthetische Tests ersetzen das nicht.
- Der lokale neuronale Gegenprüfungsweg ist implementiert und technisch getestet; seine allgemeine musikalische Zuverlässigkeit ist nicht validiert. Die begleitenden Kontextregeln sind keine umfassende semantische KI-Musikanalyse. Ein bloßer weiterer Modellaufruf würde die notwendige musikalische Validierung nicht ersetzen.

Keine kostenpflichtigen KI-Aufrufe. Keine neue Release-Versionsnummer. Standard bleibt Musikalisch ausgewogen, jede Reparatur explizit und reversibel.
