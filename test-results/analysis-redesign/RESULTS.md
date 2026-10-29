# Analyseüberarbeitung – technische Prüfung am 29.10.2026

- 60 Python-Tests bestanden: 45 vorhandene Fälle plus 15 Austausch-/Zusammenführungsfälle. Darunter eigenständige Dekodierung homogener und heterogener Kandidaten, Originalsekunden, null/fehlend, vollständiger Beobachtungserhalt, Nutzerhinweise, stale Referenz, Pflichtkriterien, doppelte Updates, abgewiesene Zeitänderung, Abschnittsdeckung und Tempo-Gleichung.
- 61 Node-Tests bestanden: 50 vorhandene Fälle plus Ablauf-/Providerfälle für abgeschnittene Antworten, fehlende Zähler, abgebrochene und HTTP-fehlerhafte Aufträge, begrenzte Eingabe, ungültiges JSON und asynchrone Verbrauchssicherung vor Fehlerweitergabe. Alle Providerantworten simuliert; keine API-Anfrage.
- 12 ältere Einheitenfälle erneut bestanden. Code für MIDI-Zeiten und gemeinsame MIDI-/MusicXML-Exporte wird nicht verändert; die vorhandenen rhythmischen Exportregressionen bleiben bestanden.
- Vergleich mit privater Zehn-Sekunden-Datei: 56.652 Zeichen für bisherigen Daten-/Schemateil gegenüber 13.232 Zeichen für gesamten neuen Prompt; 76,6 % weniger Text, alle 144 Beobachtungen behalten. Keine Tokenmessung oder gemessene Kostenersparnis.

## Browser mit echten Komponenten

Chromium/Sites-Vorschau, Pyodide mit echtem JSON-Schema-Kern: Beta-2-Oberfläche geladen; synthetische Voranalyse importiert und ausdrücklich als Voranalyse angezeigt. Kleine synthetische Interpretation importiert, zwölf Kriterien lokal zusammengeführt, als Interpretation mit klarer Testkennzeichnung angezeigt. Veraltete Ergänzung abgewiesen; vorhandene Interpretation blieb sichtbar.

Vollständige Analyse und separater kompakter Analyseauftrag tatsächlich heruntergeladen. Die heruntergeladene Analyse anschließend unabhängig mit dem Python-Kern ausgepackt und validiert: alle 14 synthetischen Beobachtungen einschließlich ursprünglicher Zeitwerte exakt erhalten, Revision von 1 auf 2, alle zwölf Kriterien vorhanden. Neuer Diagnose-Download ohne fertige Komposition erfolgreich; Datei als JSON geprüft, Version Beta 2, keine Schlüssel oder Musikdaten. Nachweise `browser-roundtrip.json` und `browser-diagnosis.json`.

Provider-MAX_TOKENS und zugehörige Tokenzähler sind technisch simuliert, nicht durch einen echten Gemini-Aufruf erzeugt. Produktionsabläufe hinter privater Anmeldung und Modellqualität bleiben offen. Frühere Download-Prüfgrenze aus Beta 1 gilt nicht für diese jetzt tatsächlich heruntergeladenen Analyse-/Diagnose-/Auftragsdateien; MIDI-/MusicXML-Downloads wurden in diesem Schritt nicht erneut im Browser geprüft.

## Veröffentlichung

Beta 2 wurde auf derselben owner-privaten Site erfolgreich veröffentlicht. Projektkennung und Ziel bleiben unverändert; siehe `deployment.json`. Kein neuer öffentlicher Zugang eingerichtet. Keine musikalische Freigabe und keine erfolgreich absolvierte Live-Gemini-Anfrage behauptet.
