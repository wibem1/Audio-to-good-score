# Musik prüfen – der kurze Weg

1. **Musik öffnen:** „Audio öffnen“ wählen. Der Dateiname bleibt sichtbar. Eine eigene MIDI nur hinzufügen, wenn sie zu dieser Aufnahme gehört. Ein Testbeispiel ist dafür nicht erforderlich.
2. **Anhören:** Originalaudio wählen und starten. Für die Prüfung einen Abschnitt über Von/Bis oder durch Ziehen auf der Wellenform wählen. Ohne MIDI: „Gewählte Passage umwandeln“, danach die vorgeschlagene MIDI-Fassung zum Vergleichen verwenden. Je Durchlauf höchstens 60 Sekunden; bei langen Audioaufnahmen sind zunächst die ersten 60 Sekunden gewählt.
3. **Passage prüfen:** Mit Audio und MIDI „Passage mit Originalaudio prüfen“ wählen. Anschließend Original und Bearbeitung vergleichen. Vorschläge sind unsicher und ändern noch nichts. Gewünschte Vorschläge oder „Alle angezeigten Vorschläge auswählen“ wählen, den Hörvergleich kurz begründen und gemeinsam übernehmen. **Einmal Rückgängig nimmt die gesamte Sammeländerung zurück.** Keine Vorschläge bedeutet nicht, dass die Passage fehlerfrei ist.
4. **Speichern:** MIDI herunterladen. Zusätzlich „Projekt speichern“, um später mit Originalen und Änderungsverlauf weiterzuarbeiten.

Einzelnoten, Pianorolle und technische Angaben sind optional aufklappbar. Du musst keine Noten einzeln eintippen, um den Abschnittsablauf zu benutzen.

Eine MIDI versehentlich geladen? „MIDI entfernen · nur Audio verwenden“ erhält deine Audioaufnahme. Bei bereits bearbeiteter MIDI fragt die App vor dem Entfernen nach. Das synthetische Beispiel ist von eigenen Aufnahmen getrennt; beim Laden einer Aufnahme wird eine aktive Test-MIDI entfernt.

Die Anwendung bleibt ein Prototyp: lokale Modelle können Noten verwechseln, vergessen oder ergänzen. Die Audio-Gegenprüfung macht derzeit nur begrenzte Oktavvorschläge; Kontextanalyse liefert einfache Hypothesen. Dies ist keine umfassende automatische musikalische Reparatur. Originale bleiben erhalten; keine kostenpflichtigen KI-Aufrufe.

Neue Projekte verwenden Schema 5 für gemeinsam rückgängig machbare Änderungen. Ältere Projekte (Schema 1–4) lassen sich weiter öffnen; Schema-5-Projekte benötigen diesen neuen Programmstand. Start wie im README über einen lokalen Webserver.

## Wenn das Notenbild zerfällt

Klaviernotation aufklappen und „Lesbare Notation vorbereiten“ wählen. Tempoalternativen, Taktart und Anfang des ersten Taktes kontrollieren. Dann die Prüfung bestätigen und MusicXML exportieren. „Lesbare Anschlagsfassung“ vereinfacht nur die notierten Dauern; sie repariert keine unklaren Tonhöhen oder hörbaren MIDI-Stolperer. Eine ausführliche Einzelnotenreparatur ist dafür nicht erforderlich.
