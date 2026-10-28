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

# Aktuelle Ergänzung – Reparatur und MusicXML

31 Kerntests bestanden. Hinzugekommen: reversible Ergänzung fehlender Noten mit unveränderten Nachbarn; Kontext-Hypothesen ohne automatische Änderung; Zurückweisung veralteter Vorschläge; Score-/Performance-Trennung; unabhängige Stimmen und gleichzeitige identische Tonhöhen; Taktwechsel/Balkengruppierung (einschließlich 6/8). Im Balkentest wurde ein Fehler der zusammengesetzten Metrik gefunden und vor Sicherung korrigiert.

Browserprüfung: manuelle Ergänzung, Undo/Redo, Schema-4-Wiederherstellung, MusicXML und Mapping herunterladen, Kontextanalyse darstellen; keine JavaScript-Seitenfehler. Lokale Modellregression weiter bestanden. MusicXML-Prüfung mit music21 9.9.1 und Verovio 5.7.0: zehn Noten nach Zusammenführung von Bindungen mit identischen Score-Tonhöhen/Startwerten/Dauern; alle Stimmen/Takte exakt gefüllt; zwei Systeme, echte SVG-Renderausgabe visuell geprüft. Ergebnisse und Beispieldatei unter `test-results/score-*`.

Keine XSD-Validierung behauptet: der versuchte Zugriff auf das verschobene W3C-GitHub-Schema lieferte keinen verwendbaren Schema-Download. Der belegte Nachweis ist unabhängiger Parserimport mit Notenvergleich und Verovio-Rendering. Keine reale Dorico-/MuseScore-Prüfung oder menschliche Hörfreigabe. Vollständige Grenzen einschließlich F07/F08: `ACCEPTANCE.md`.

## Neuronale selektive Gegenprüfung

Echtes lokales Basic-Pitch-WASM-Modell gegen synthetischen C4-Audioton und MIDI-C5 geprüft: Vorschlag erscheint ohne Änderung; fehlende Prüfbegründung verhindert Übernahme; explizite Übernahme korrigiert nur 72→60; Undo stellt 72 wieder her. Unabhängiger mido-Test bestätigt nur zwei geänderte Pitch-Ereignisse, keine veränderten Ereigniszeiten. Modellevidenz und Aktivierungsunsicherheit sind im Kontextbericht, Modell-/Audiohash und Parameter im lokalen Laufprotokoll. Kein Cloud-/kostenpflichtiger Aufruf.

## Echter MuseScore-Import – 28.10.2026

MuseScore3 3.2.3 aus den offiziellen Ubuntu-Noble-Snapshotpaketen (Paket 3.2.3+dfsg2-16build5), isoliert mit Qt bereitgestellt. Keine MuseScore-Binärdateien als Produktbestandteil. CLI-Aufrufe mit `-s` und `QT_QPA_PLATFORM=offscreen`: MusicXML importieren und als MSCX speichern, MSCX erneut öffnen und als MusicXML exportieren, PNG mit der MuseScore-Engine erzeugen. Alle Aufrufe erfolgreich.

Sechs synthetische Fälle: zweisystemiger Satz mit unabhängigen Stimmen und Taktbindungen (10 Noten), 6/8-Balkengruppen (8), 3/4 mit langer Bassnote (9), gleichzeitig gleiche Tonhöhen in verschiedenen Stimmen (9), Sekunden-/BPM-Zeitbasis bei Tempowechseln (2), leere Partitur (0). Unabhängiger XML-Ereignisvergleich mit exakten rationalen Viertelzeiten und zusammengeführten Ties bestätigt jeweils dieselben Tonhöhen, Einsätze, Dauern und Systemzuordnungen nach dem MuseScore-Durchlauf. Native Datei enthält zwei Systeme. Das Notenbild wurde weiß hinterlegt visuell geprüft; keine umfassende Spielbarkeits-/Layoutfreigabe.

`test-results/musescore/` enthält JSON-Bericht, vollständige CLI-Protokolle, native MSCX, Rückexport und Notenbild. Protokollierte AF_NETLINK-Meldungen stammen aus der eingeschränkten Arbeitsumgebung; alle eigentlichen Konvertierungen erfolgreich. Test verwendete isolierte offizielle Pakete, nachdem normale Paketinstallation an Umgebungseinschränkungen scheiterte.

Der Nachweis gilt nur für MuseScore 3.2.3 und diese Fälle. MuseScore 4, Dorico, reale Referenz „Graziler Tanz“ und menschliche Hörfreigabe bleiben offen. Bestehende ältere Aussagen über fehlenden MuseScore-Test oben sind historisch durch diesen Abschnitt ergänzt. Keine App-Quellcodeänderung und keine kostenpflichtigen KI-Aufrufe.

## Echter MuseScore-4-Import – 28.10.2026

Offizielle MuseScore Studio 4.7.6 AppImage (Build 261022093, x86_64), Release `https://github.com/musescore/MuseScore/releases/tag/v4.7.6`. SHA-256 `5fcbd1f292270eca5c3867d56b767c31a173a155216a415f5caee22553f8e7a6` stimmt mit der offiziellen Release-Metadatenangabe überein. Keine zusätzliche Produktabhängigkeit.

Alle sechs zuvor beschriebenen Fälle bestehen den tatsächlichen MusicXML→MSCX→MusicXML-Durchlauf mit identischen Tonhöhen, rationalen Einsätzen, Dauern und Systemzuordnungen nach Bindungszusammenführung. Je zwei native Systeme. Engine-PNG visuell geprüft: zwei Klaviersysteme, Stimmen/Pausen und Bindungen sichtbar. Für den abgelegten Sichtbeleg wurde nur weißer Hintergrund ergänzt und verkleinert; keine Noteninhalte verändert. Keine umfassende Layout- oder Hörfreigabe.

Die AppImage erzwingt hier einen Anzeigeweg; bloßes Offscreen-Environment genügte nicht. Test erfolgreich unter isoliertem Xvfb 21.1.12 via TCP-Loopback/xcb im selben Prozessraum; systemweites Installieren nicht erforderlich. MuseScore 4 unterstützt das alte `-s` nicht; der gemeinsame Test verwendet daher nur `-o`. Qt/DBus-/Pipewire-/Audiomeldungen sind in den vollständigen Protokollen erhalten. Alle 13 Konvertierungen/Renderaufrufe erfolgreich. Version wird tatsächlich aus `--version` gelesen; das MuseScore-4-Prüffeld ist nicht mehr pauschal falsch.

Belege: `test-results/musescore4/` mit Versions-/Quellnachweis, JSON-Bericht, CLI-Protokollen, nativer Datei, MusicXML-Rückexport und Notenbild. 31/31 Kerntests erneut bestanden. Produktcode unverändert, keine kostenpflichtigen KI-Aufrufe. Dorico und menschliche musikalische Hörabnahme bleiben offen. Die frühere MuseScore-4-Lücke ist mit diesem Abschnitt geschlossen.

## Abschluss Meilenstein 1 – 28.10.2026

33/33 Kerntests bestanden. Zwei neue Tests reproduzierten vor der Korrektur verspätetes Wiederstarten nach Pause bzw. überholende `AudioContext.resume()`-Zusagen. Ein Generationenzähler verwirft überholte Starts nach `stop()`/weiterem `play()`; abgebrochene Starts melden keinen laufenden Playerstatus mehr. Keine Performance-/Exportdatenänderung. Beide Regressionen nach Korrektur bestanden.

Vollständiger echter Chromium-138.0.7204.0-Bedienungstest und echte lokale Modellregression erneut bestanden. A/B/C/Mix, echte MP3/WAV-Dekodierung, Einzelnotenänderung/Ausblendung/Ergänzung, Projektwiederherstellung, MusicXML und neuronale Audio-Gegenprüfung erfolgreich. Vier unabhängige mido-1.3.3-Prüfungen bestätigen Ereignis-/Tick-/Tempoerhalt, selektive Entfernung, neuronale Pitchkorrektur und Audio-only-Kandidatenexport. Modell weiterhin 7 passende Referenznoten von 8, insgesamt 9 Kandidaten im synthetischen Test; kein neuer allgemeiner Qualitätswert. 60 Sekunden Stille erfolgreich, null Noten. Aktuelle vollständige Berichte: `test-results/final/`.

Zusätzlicher realer Firefox-153.0-Versuch: Browser/Seite starten, aber der WAV-Ladevorgang beendet sich nicht innerhalb 30 Sekunden. Auch isolierter Medienprozess-/Sandboxversuch behebt das nicht. Kein Firefox-Erfolgsnachweis; experimentelle Runneränderungen verworfen. Standard-Chromiumdownload war unbrauchbar; der erfolgreiche Test nutzte wieder das isolierte npm-Testbrowserpaket @sparticuz/chromium 138.0.2. Keine neuen Produktabhängigkeiten.

`MILESTONE_1.md` trennt jetzt den abgeschlossenen technischen Prototypauftrag von der noch offenen vollständigen V0.1-Abnahme. Keine behauptete menschliche Hörprüfung, keine kostenpflichtigen KI-Aufrufe.

## Bedienung nach Nutzertest – 28.10.2026

Nutzertest kritisierte verwirrende Eingabe, unverbundene Test-MIDI und erzwungene Einzelnotenarbeit. Neue Oberfläche mit vier Schritten; Dateinamen aus tatsächlich geladenem Zustand statt leerer nativer Dateifeldanzeige. Demo nur im optionalen Testbereich, bei vorhandener Aufnahme gesperrt; eigene Aufnahme entfernt aktive Demo nach gegebenenfalls erforderlicher Bearbeitungsbestätigung. Explizites Entfernen vorhandener MIDI erhält Audio und öffnet die Audio-only-Umwandlung. Audio ist nach Import die vorausgewählte Wiedergabequelle. Standardpassage für lange Audio-only-Aufnahmen auf erste 60 Sekunden begrenzt. Wellenform markierbar, Pianorolle und Einzelnoten optional; Diagnose/Notation ebenfalls eingeklappt.

Passagenvorschläge sind standardmäßig nicht ausgewählt. Gesammelte Auswahl und gemeinsame Übernahme erst mit Prüfbegründung; Snapshot-/Quell-/Abschnittsschutz. Session.editBatch prüft auf einer Kopie; wenn eine Teiländerung scheitert, bleiben Noten, History und Redo unverändert. Einmal Undo/Redo betrifft die komplette Gruppe. Schema 5 speichert Gruppen einschließlich Redo; Projekte 1–4 weiterhin lesbar. Alte App-Stände dürfen Schema 5 nicht öffnen. Keine Zeitänderungen über die neue Gruppenfunktion. Modelle unverändert und weiterhin musikalisch ungeprüft.

35 Kerntests bestanden. Echter Chromium-138-Bedienungstest prüft zusätzlich Demo→eigene WAV (Audio-only), sichtbare Namen, defekte WAV ohne Verlust der geladenen Aufnahme, erneutes Öffnen derselben MP3, Entfernen von MIDI ohne Audioverlust, Wellenformmarkierung, zwei Vorschläge als Gruppe, fehlende Begründung, einmal Undo, Schema-5-Redo nach Projektöffnung, byteidentische Wiederherstellung. Vollständige lokale Modellregression bestanden einschließlich MP3-only, Abbruch, fehlendem/beschädigtem Modell und 60 Sekunden Stille. Kein Seitenfehler/Upload/Cloudaufruf. Fünf unabhängige mido-Prüfungen einschließlich neuem Gruppentest bestätigen unveränderte verbleibende Notenzeiten/Velocity und originalgetreues Undo. Reproduzierbarer Gruppentest: `tests/independent_batch.py` nach Browserlauf.

`test-results/usability/` enthält aktuelle Berichte und visuell geprüftes Standardlayout. Ein Testlauf scheiterte zunächst am geschlossenen Browserkontext der speziellen Single-Process-Testumgebung; Kontexte werden nun bis Testende offengehalten. Ein zweiter Testschritt scrollte auf die inzwischen absichtlich versteckte Transkriptionsschaltfläche nach Kandidatübernahme; Screenshotanker auf sichtbaren Export umgestellt. Danach beide vollständigen Browserregressionen erfolgreich. Kein behaupteter Nutzertest der neuen Bedienung und keine allgemeine Musikqualitätsfreigabe. Keine kostenpflichtigen KI-Aufrufe.

## Reale Etüdenreferenz und Notationsursache – 28.10.2026

Quelle: tatsächlich bereitgestellte WAV (164,4 s), MIDI (60 s einschließlich Endereignis, 578 Tonansätze) und alte MusicXML. Das alte Dokument hat 1.770 Notenelemente einschließlich 572 Pausen, 1.240 Tie-Elemente und zehn Voice-IDs; keine Sound-Tempoangabe. Kandidaten-MIDI enthält nur technisches 120-BPM-Speichertempo. Sekunden darauf als feste 4/4-Metrik zu interpretieren und nach exakten Start-/Endpaaren Stimmen zu verteilen erzeugt den reproduzierten überladenen Satz.

Unabhängige spektrale Audio-Onset-Analyse (16 kHz, 1.024 Samples, Hop 128, erste 61 s, vier 15-s-Fenster) bestätigt Unterteilungen ca. 0,1780/0,1789/0,1780/0,1780 s. MIDI hat zum nächsten globalen Audiopeak median 7 ms Abstand, rund 60 Einsätze liegen über 50 ms entfernt. Keine pitchspezifische Wahrheit; dies sind mögliche Prüfstellen, keine bewiesenen falschen Noten. Nicht blind geglättet/gelöscht. NumPy/SciPy/mido nur Testwerkzeuge.

Neue Score-Option: ausdrücklich vereinfachte Anschlagsfassung bis zum nächsten Handanschlag, getrennter Taktanfang, punktierte Werte, explizites MusicXML-Tempo. Pulsvorschlag zeigt Halb-/Doppeltempoambiguität; Taktart wird nicht automatisch verändert. Audiosekunden-Export verlangt Parameterbestätigung; Herkunft und Notationsparameter werden gespeichert, bei Wiederöffnung neu bestätigt. Die bisherige Performance-Notation bleibt verfügbar. Die neue Funktion verändert kein MIDI.

Konkrete Arbeitsfassung: Unterteilung 0,1782 s; Annahme Viertel = 4 Unterteilungen → 84,175 BPM, Alternative 168,35 BPM. Notierter Beginn 0,0913 s, bewusst angenommener 3/4-Takt. Das ist keine bestätigte Taktart. Alle 578 Pitch-Attacken erhalten; 661 Notenelemente, zwei Pausen, 162 Tie-Elemente, zwei Stimmen. Notationsdauern sind ausdrücklich vereinfacht; weder vollständiger Klaviersatz noch unveränderte Aufführung. Originaldateien nicht überschrieben und nicht in GitHub hochgeladen.

39 Kerntests bestanden. Reale Chromium-Bedienungs-/Modellregression und fünf unabhängige MIDI-Prüfungen bestanden. Neuer UI-Test: Pulsvorschlag, keine automatische Taktartänderung, Export verweigert ungeprüfte Audiosekunden-Parameter, explizit gewählte Fassung enthält Tempo, Projektparameter wiederhergestellt. Music21 bestätigt für echte Arbeitsfassung UND echten MuseScore-4.7.6-Rückexport alle 578 geplanten Score-Tonhöhen, Einsätze, Dauern und Systeme; jede Stimme füllt die Takte. MuseScore-Import, natives Wiederöffnen, Rückexport und PDF erfolgreich, beide PDF-Seiten visuell geprüft. Sechs ältere synthetische MuseScore-Fälle nach Exportänderung ebenfalls erneut bestanden.

Belege unter `test-results/reference-score/`; Reproduktionsskripte verlangen externe Nutzerdaten, keine musikalischen Originaldateien im Repository. Die zwei Vergleichsdateien werden separat bereitgestellt. MIDI-Stolperer und vollständige musikalische Rekonstruktion bleiben offen. Keine behauptete Hörfreigabe, keine kostenpflichtigen KI-Aufrufe.
